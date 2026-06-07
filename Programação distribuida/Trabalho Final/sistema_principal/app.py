import os
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from uuid import uuid4

import requests
from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TEMP_DIR = DATA_DIR / "tmp"
DB_PATH = DATA_DIR / "main.db"

APP_SECRET = os.getenv("MAIN_SECRET_KEY", "troque-esta-chave-em-producao")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@local")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
REQUEST_TIMEOUT = 8

app = Flask(__name__)
app.secret_key = APP_SECRET


def db():
    if "db" not in g:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    conn = g.pop("db", None)
    if conn:
        conn.close()


def init_db():
    conn = db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            base_url TEXT NOT NULL,
            api_key TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('primary', 'backup')),
            capacity_gb REAL NOT NULL,
            backup_of_id INTEGER,
            status TEXT NOT NULL DEFAULT 'unknown',
            last_checked TEXT,
            used_bytes INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (backup_of_id) REFERENCES nodes(id)
        );

        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_name TEXT NOT NULL,
            stored_name TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            primary_node_id INTEGER NOT NULL,
            backup_node_id INTEGER,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (primary_node_id) REFERENCES nodes(id),
            FOREIGN KEY (backup_node_id) REFERENCES nodes(id)
        );
        """
    )
    exists = conn.execute("SELECT id FROM users WHERE email = ?", (ADMIN_EMAIL,)).fetchone()
    if not exists:
        conn.execute(
            """
            INSERT INTO users (name, email, password_hash, is_admin, created_at)
            VALUES (?, ?, ?, 1, ?)
            """,
            ("Administrador", ADMIN_EMAIL, generate_password_hash(ADMIN_PASSWORD), now()),
        )
        conn.commit()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


@app.context_processor
def inject_user():
    return {"current_user": current_user()}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = current_user()
        if not user or not user["is_admin"]:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def node_headers(node):
    return {"X-Node-Token": node["api_key"]}


def refresh_node_status(node):
    status = "offline"
    used_bytes = node["used_bytes"]
    try:
        response = requests.get(
            f"{node['base_url'].rstrip('/')}/api/health",
            headers=node_headers(node),
            timeout=REQUEST_TIMEOUT,
        )
        if response.ok:
            payload = response.json()
            status = "online"
            used_bytes = int(payload.get("used_bytes", used_bytes))
    except requests.RequestException:
        pass

    db().execute(
        "UPDATE nodes SET status = ?, last_checked = ?, used_bytes = ? WHERE id = ?",
        (status, now(), used_bytes, node["id"]),
    )
    db().commit()
    return status


def capacity_bytes(node):
    return int(float(node["capacity_gb"]) * 1024 * 1024 * 1024)


def available_nodes(role, required_size):
    rows = db().execute(
        "SELECT * FROM nodes WHERE role = ? ORDER BY id ASC",
        (role,),
    ).fetchall()
    ready = []
    for node in rows:
        if refresh_node_status(node) != "online":
            continue
        fresh = db().execute("SELECT * FROM nodes WHERE id = ?", (node["id"],)).fetchone()
        if capacity_bytes(fresh) - fresh["used_bytes"] >= required_size:
            ready.append(fresh)
    return ready


def backup_for(primary_node, size_bytes):
    rows = db().execute(
        """
        SELECT * FROM nodes
        WHERE role = 'backup' AND (backup_of_id = ? OR backup_of_id IS NULL)
        ORDER BY backup_of_id IS NULL ASC, id ASC
        """,
        (primary_node["id"],),
    ).fetchall()
    for node in rows:
        if refresh_node_status(node) == "online":
            fresh = db().execute("SELECT * FROM nodes WHERE id = ?", (node["id"],)).fetchone()
            if capacity_bytes(fresh) - fresh["used_bytes"] >= size_bytes:
                return fresh
    return None


def upload_to_node(node, stored_name, source_path, display_name):
    with open(source_path, "rb") as handle:
        response = requests.post(
            f"{node['base_url'].rstrip('/')}/api/files/{stored_name}",
            headers=node_headers(node),
            data={"display_name": display_name},
            files={"file": handle},
            timeout=REQUEST_TIMEOUT,
        )
    response.raise_for_status()
    refresh_node_status(node)


def rename_on_node(node, stored_name, new_name):
    response = requests.patch(
        f"{node['base_url'].rstrip('/')}/api/files/{stored_name}",
        headers=node_headers(node),
        json={"display_name": new_name},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()


def delete_on_node(node, stored_name):
    response = requests.delete(
        f"{node['base_url'].rstrip('/')}/api/files/{stored_name}",
        headers=node_headers(node),
        timeout=REQUEST_TIMEOUT,
    )
    if response.status_code not in (200, 404):
        response.raise_for_status()
    refresh_node_status(node)


@app.route("/")
def index():
    if current_user():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 6:
            flash("Preencha nome, e-mail e uma senha com pelo menos 6 caracteres.", "error")
            return render_template("register.html")
        try:
            db().execute(
                """
                INSERT INTO users (name, email, password_hash, is_admin, created_at)
                VALUES (?, ?, ?, 0, ?)
                """,
                (name, email, generate_password_hash(password), now()),
            )
            db().commit()
            flash("Conta criada. Entre com seu e-mail e senha.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Este e-mail já está cadastrado.", "error")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        flash("E-mail ou senha inválidos.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    files = db().execute(
        """
        SELECT f.*, pn.name AS primary_node, bn.name AS backup_node
        FROM files f
        JOIN nodes pn ON pn.id = f.primary_node_id
        LEFT JOIN nodes bn ON bn.id = f.backup_node_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC
        """,
        (current_user()["id"],),
    ).fetchall()
    return render_template("dashboard.html", files=files)


@app.route("/files/upload", methods=["POST"])
@login_required
def upload_file():
    file = request.files.get("file")
    if not file or not file.filename:
        flash("Selecione um arquivo para enviar.", "error")
        return redirect(url_for("dashboard"))

    original_name = secure_filename(file.filename) or "arquivo"
    stored_name = f"{uuid4().hex}_{original_name}"
    temp_path = TEMP_DIR / stored_name
    file.save(temp_path)
    size_bytes = temp_path.stat().st_size

    primaries = available_nodes("primary", size_bytes)
    if not primaries:
        temp_path.unlink(missing_ok=True)
        flash("Nenhum node principal online com espaço suficiente.", "error")
        return redirect(url_for("dashboard"))

    primary = primaries[0]
    backup = backup_for(primary, size_bytes)
    try:
        upload_to_node(primary, stored_name, temp_path, original_name)
        if backup:
            upload_to_node(backup, stored_name, temp_path, original_name)
        db().execute(
            """
            INSERT INTO files
            (user_id, original_name, stored_name, size_bytes, primary_node_id, backup_node_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                current_user()["id"],
                original_name,
                stored_name,
                size_bytes,
                primary["id"],
                backup["id"] if backup else None,
                now(),
            ),
        )
        db().commit()
        flash("Arquivo enviado com sucesso.", "success")
    except requests.RequestException as exc:
        flash(f"Falha ao enviar para o node: {exc}", "error")
    finally:
        temp_path.unlink(missing_ok=True)
    return redirect(url_for("dashboard"))


@app.route("/files/<int:file_id>/download")
@login_required
def download_file(file_id):
    record = db().execute(
        "SELECT * FROM files WHERE id = ? AND user_id = ?",
        (file_id, current_user()["id"]),
    ).fetchone()
    if not record:
        abort(404)

    for node_id in (record["primary_node_id"], record["backup_node_id"]):
        if not node_id:
            continue
        node = db().execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()
        try:
            response = requests.get(
                f"{node['base_url'].rstrip('/')}/api/files/{record['stored_name']}",
                headers=node_headers(node),
                timeout=REQUEST_TIMEOUT,
                stream=True,
            )
            if response.ok:
                temp_path = TEMP_DIR / f"download_{record['stored_name']}"
                with open(temp_path, "wb") as handle:
                    for chunk in response.iter_content(chunk_size=1024 * 256):
                        if chunk:
                            handle.write(chunk)
                return send_file(temp_path, as_attachment=True, download_name=record["original_name"])
        except requests.RequestException:
            continue
    flash("Arquivo indisponível nos nodes configurados.", "error")
    return redirect(url_for("dashboard"))


@app.route("/files/<int:file_id>/rename", methods=["POST"])
@login_required
def rename_file(file_id):
    new_name = secure_filename(request.form.get("new_name", "").strip())
    if not new_name:
        flash("Informe um novo nome válido.", "error")
        return redirect(url_for("dashboard"))
    record = db().execute(
        "SELECT * FROM files WHERE id = ? AND user_id = ?",
        (file_id, current_user()["id"]),
    ).fetchone()
    if not record:
        abort(404)

    for node_id in (record["primary_node_id"], record["backup_node_id"]):
        if node_id:
            node = db().execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()
            try:
                rename_on_node(node, record["stored_name"], new_name)
            except requests.RequestException:
                pass
    db().execute("UPDATE files SET original_name = ? WHERE id = ?", (new_name, file_id))
    db().commit()
    flash("Arquivo renomeado.", "success")
    return redirect(url_for("dashboard"))


@app.route("/files/<int:file_id>/delete", methods=["POST"])
@login_required
def delete_file(file_id):
    record = db().execute(
        "SELECT * FROM files WHERE id = ? AND user_id = ?",
        (file_id, current_user()["id"]),
    ).fetchone()
    if not record:
        abort(404)
    for node_id in (record["primary_node_id"], record["backup_node_id"]):
        if node_id:
            node = db().execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()
            try:
                delete_on_node(node, record["stored_name"])
            except requests.RequestException:
                pass
    db().execute("DELETE FROM files WHERE id = ?", (file_id,))
    db().commit()
    flash("Arquivo removido.", "success")
    return redirect(url_for("dashboard"))


@app.route("/admin")
@admin_required
def admin_home():
    users = db().execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    nodes = db().execute(
        """
        SELECT n.*, parent.name AS backup_of_name
        FROM nodes n
        LEFT JOIN nodes parent ON parent.id = n.backup_of_id
        ORDER BY n.id DESC
        """
    ).fetchall()
    return render_template("admin.html", users=users, nodes=nodes)


@app.route("/admin/users/<int:user_id>/password", methods=["POST"])
@admin_required
def admin_change_password(user_id):
    password = request.form.get("password", "")
    if len(password) < 6:
        flash("A nova senha precisa ter pelo menos 6 caracteres.", "error")
        return redirect(url_for("admin_home"))
    db().execute(
        "UPDATE users SET password_hash = ? WHERE id = ?",
        (generate_password_hash(password), user_id),
    )
    db().commit()
    flash("Senha alterada.", "success")
    return redirect(url_for("admin_home"))


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    if user_id == current_user()["id"]:
        flash("Você não pode deletar o próprio usuário admin logado.", "error")
        return redirect(url_for("admin_home"))
    db().execute("DELETE FROM files WHERE user_id = ?", (user_id,))
    db().execute("DELETE FROM users WHERE id = ?", (user_id,))
    db().commit()
    flash("Usuário deletado.", "success")
    return redirect(url_for("admin_home"))


@app.route("/admin/nodes", methods=["POST"])
@admin_required
def admin_create_node():
    role = request.form.get("role")
    backup_of_id = request.form.get("backup_of_id") or None
    if role not in {"primary", "backup"}:
        flash("Tipo de node inválido.", "error")
        return redirect(url_for("admin_home"))
    db().execute(
        """
        INSERT INTO nodes
        (name, base_url, api_key, role, capacity_gb, backup_of_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            request.form.get("name", "").strip(),
            request.form.get("base_url", "").strip().rstrip("/"),
            request.form.get("api_key", "").strip(),
            role,
            float(request.form.get("capacity_gb", "0")),
            int(backup_of_id) if backup_of_id else None,
            now(),
        ),
    )
    db().commit()
    flash("Node cadastrado.", "success")
    return redirect(url_for("admin_home"))


@app.route("/admin/nodes/<int:node_id>/configure", methods=["POST"])
@admin_required
def admin_configure_node(node_id):
    node = db().execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()
    if not node:
        abort(404)
    payload = {
        "name": node["name"],
        "role": node["role"],
        "capacity_gb": node["capacity_gb"],
        "backup_of_id": node["backup_of_id"],
    }
    try:
        response = requests.post(
            f"{node['base_url'].rstrip('/')}/api/configure",
            headers=node_headers(node),
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        refresh_node_status(node)
        flash("Configuração enviada ao node.", "success")
    except requests.RequestException as exc:
        flash(f"Não foi possível configurar o node: {exc}", "error")
    return redirect(url_for("admin_home"))


@app.route("/admin/nodes/<int:node_id>/check", methods=["POST"])
@admin_required
def admin_check_node(node_id):
    node = db().execute("SELECT * FROM nodes WHERE id = ?", (node_id,)).fetchone()
    if not node:
        abort(404)
    status = refresh_node_status(node)
    flash(f"Node marcado como {status}.", "success" if status == "online" else "error")
    return redirect(url_for("admin_home"))


@app.route("/admin/nodes/<int:node_id>/delete", methods=["POST"])
@admin_required
def admin_delete_node(node_id):
    in_use = db().execute(
        "SELECT id FROM files WHERE primary_node_id = ? OR backup_node_id = ? LIMIT 1",
        (node_id, node_id),
    ).fetchone()
    if in_use:
        flash("Este node possui arquivos vinculados e não pode ser removido.", "error")
        return redirect(url_for("admin_home"))
    db().execute("DELETE FROM nodes WHERE id = ?", (node_id,))
    db().commit()
    flash("Node removido.", "success")
    return redirect(url_for("admin_home"))


@app.template_filter("filesize")
def filesize(value):
    value = int(value or 0)
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}" if unit != "B" else f"{value} B"
        size /= 1024


@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Banco inicializado.")


with app.app_context():
    init_db()


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host="127.0.0.1", port=int(os.getenv("MAIN_PORT", "5000")), debug=debug, use_reloader=False)
