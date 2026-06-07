import os
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, abort, g, jsonify, request, send_file
from werkzeug.utils import secure_filename


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("NODE_DATA_DIR", BASE_DIR / "data"))
FILES_DIR = DATA_DIR / "files"
DB_PATH = DATA_DIR / "node.db"

NODE_API_KEY = os.getenv("NODE_API_KEY", "node-secret")
NODE_PORT = int(os.getenv("NODE_PORT", "7001"))

app = Flask(__name__)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def db():
    if "db" not in g:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        FILES_DIR.mkdir(parents=True, exist_ok=True)
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
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            name TEXT NOT NULL DEFAULT 'Node',
            role TEXT NOT NULL DEFAULT 'primary',
            capacity_gb REAL NOT NULL DEFAULT 1,
            backup_of_id INTEGER,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS files (
            stored_name TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )
    exists = conn.execute("SELECT id FROM config WHERE id = 1").fetchone()
    if not exists:
        conn.execute(
            """
            INSERT INTO config (id, name, role, capacity_gb, backup_of_id, updated_at)
            VALUES (1, 'Node', 'primary', 1, NULL, ?)
            """,
            (now(),),
        )
        conn.commit()


def require_token(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if request.headers.get("X-Node-Token") != NODE_API_KEY:
            abort(401)
        return view(*args, **kwargs)

    return wrapped


def used_bytes():
    row = db().execute("SELECT COALESCE(SUM(size_bytes), 0) AS total FROM files").fetchone()
    return int(row["total"])


def config_row():
    return db().execute("SELECT * FROM config WHERE id = 1").fetchone()


def capacity_bytes(config):
    return int(float(config["capacity_gb"]) * 1024 * 1024 * 1024)


@app.route("/api/health")
@require_token
def health():
    config = config_row()
    used = used_bytes()
    return jsonify(
        {
            "status": "online",
            "name": config["name"],
            "role": config["role"],
            "capacity_gb": config["capacity_gb"],
            "used_bytes": used,
            "free_bytes": max(capacity_bytes(config) - used, 0),
        }
    )


@app.route("/api/configure", methods=["POST"])
@require_token
def configure():
    payload = request.get_json(force=True)
    role = payload.get("role", "primary")
    if role not in {"primary", "backup"}:
        return jsonify({"error": "role inválido"}), 400
    capacity_gb = float(payload.get("capacity_gb", 1))
    if capacity_gb <= 0:
        return jsonify({"error": "capacity_gb precisa ser maior que zero"}), 400
    db().execute(
        """
        UPDATE config
        SET name = ?, role = ?, capacity_gb = ?, backup_of_id = ?, updated_at = ?
        WHERE id = 1
        """,
        (
            payload.get("name", "Node"),
            role,
            capacity_gb,
            payload.get("backup_of_id"),
            now(),
        ),
    )
    db().commit()
    return jsonify({"ok": True})


@app.route("/api/files/<stored_name>", methods=["POST"])
@require_token
def upload(stored_name):
    stored_name = secure_filename(stored_name)
    upload_file = request.files.get("file")
    if not upload_file:
        return jsonify({"error": "arquivo ausente"}), 400
    display_name = secure_filename(request.form.get("display_name", stored_name)) or stored_name

    temp_path = FILES_DIR / f".tmp_{stored_name}"
    final_path = FILES_DIR / stored_name
    upload_file.save(temp_path)
    size = temp_path.stat().st_size

    existing = db().execute("SELECT size_bytes FROM files WHERE stored_name = ?", (stored_name,)).fetchone()
    projected = used_bytes() - (existing["size_bytes"] if existing else 0) + size
    if projected > capacity_bytes(config_row()):
        temp_path.unlink(missing_ok=True)
        return jsonify({"error": "capacidade do node excedida"}), 507

    temp_path.replace(final_path)
    if existing:
        db().execute(
            """
            UPDATE files
            SET display_name = ?, size_bytes = ?, updated_at = ?
            WHERE stored_name = ?
            """,
            (display_name, size, now(), stored_name),
        )
    else:
        db().execute(
            """
            INSERT INTO files (stored_name, display_name, size_bytes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (stored_name, display_name, size, now(), now()),
        )
    db().commit()
    return jsonify({"ok": True, "stored_name": stored_name, "size_bytes": size})


@app.route("/api/files/<stored_name>")
@require_token
def download(stored_name):
    stored_name = secure_filename(stored_name)
    record = db().execute("SELECT * FROM files WHERE stored_name = ?", (stored_name,)).fetchone()
    path = FILES_DIR / stored_name
    if not record or not path.exists():
        abort(404)
    return send_file(path, as_attachment=True, download_name=record["display_name"])


@app.route("/api/files/<stored_name>", methods=["PATCH"])
@require_token
def rename(stored_name):
    stored_name = secure_filename(stored_name)
    payload = request.get_json(force=True)
    display_name = secure_filename(payload.get("display_name", ""))
    if not display_name:
        return jsonify({"error": "novo nome inválido"}), 400
    db().execute(
        "UPDATE files SET display_name = ?, updated_at = ? WHERE stored_name = ?",
        (display_name, now(), stored_name),
    )
    db().commit()
    return jsonify({"ok": True})


@app.route("/api/files/<stored_name>", methods=["DELETE"])
@require_token
def delete(stored_name):
    stored_name = secure_filename(stored_name)
    (FILES_DIR / stored_name).unlink(missing_ok=True)
    db().execute("DELETE FROM files WHERE stored_name = ?", (stored_name,))
    db().commit()
    return jsonify({"ok": True})


with app.app_context():
    init_db()


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host="127.0.0.1", port=NODE_PORT, debug=debug, use_reloader=False)
