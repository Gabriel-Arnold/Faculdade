import sqlite3, hashlib, hmac, base64, json, time, os

DB_NAME = "usuarios.db"
JWT_SECRET = "221DEF08-DF5E-4A0C-9FD9-F8063FD44C1B"

def base64_encoder(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

def base64_decoder(data: str) -> bytes:
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data)
def conectar_banco():
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,4
            senha_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def gerar_hash_senha(senha: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(16)

    senha_hash = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        100000
    )

    return senha_hash.hex(), salt.hex()

def verificar_senha(senha_digitada: str, senha_hash_salva: str, salt_salvo: str) -> bool:
    salt_bytes = bytes.fromhex(salt_salvo)

    novo_hash, _ = gerar_hash_senha(senha_digitada, salt_bytes)

    return hmac.compare_digest(novo_hash, senha_hash_salva)

def gerar_jwt(payload: dict, secret: str) -> str:
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    header_json = json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

    header_b64 = base64_encoder(header_json)
    payload_b64 = base64_encoder(payload_json)

    assinatura_base = f"{header_b64}.{payload_b64}".encode("utf-8")

    assinatura = hmac.new(
        secret.encode("utf-8"),
        assinatura_base,
        hashlib.sha256
    ).digest()

    assinatura_b64 = base64_encoder(assinatura)

    token = f"{header_b64}.{payload_b64}.{assinatura_b64}"
    return token


def validar_jwt(token: str, secret: str):
    try:
        partes = token.split(".")
        if len(partes) != 3:
            return None

        header_b64, payload_b64, assinatura_recebida_b64 = partes

        assinatura_base = f"{header_b64}.{payload_b64}".encode("utf-8")

        assinatura_esperada = hmac.new(
            secret.encode("utf-8"),
            assinatura_base,
            hashlib.sha256
        ).digest()

        assinatura_esperada_b64 = base64_encoder(assinatura_esperada)

        if not hmac.compare_digest(assinatura_recebida_b64, assinatura_esperada_b64):
            return None

        payload_json = base64_decoder(payload_b64)
        payload = json.loads(payload_json.decode("utf-8"))

        if "exp" in payload:
            if time.time() > payload["exp"]:
                return None

        return payload

    except Exception:
        return None

def criar_usuario():
    print("\n=== CRIAR USUÁRIO ===")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()

    if not nome or not email or not senha:
        print("Erro: todos os campos são obrigatórios.")
        return

    senha_hash, salt = gerar_hash_senha(senha)

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha_hash, salt)
            VALUES (?, ?, ?, ?)
        """, (nome, email, senha_hash, salt))

        conn.commit()
        conn.close()

        print("Usuário criado com sucesso!")

    except sqlite3.IntegrityError:
        print("Erro: já existe um usuário com esse email.")


def login_usuario():
    print("\n=== LOGIN ===")
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, senha_hash, salt
        FROM usuarios
        WHERE email = ?
    """, (email,))

    usuario = cursor.fetchone()
    conn.close()

    if usuario is None:
        print("Erro: email ou senha inválidos.")
        return None

    user_id, nome, email, senha_hash_salva, salt_salvo = usuario

    if not verificar_senha(senha, senha_hash_salva, salt_salvo):
        print("Erro: email ou senha inválidos.")
        return None

    payload = {
        "sub": user_id,
        "nome": nome,
        "email": email,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }

    token = gerar_jwt(payload, JWT_SECRET)

    print("\nLogin realizado com sucesso!")
    print("Seu JWT:")
    print(token)

    return token


def metodo_sensivel():
    print("\n=== MÉTODO SENSÍVEL ===")
    token = input("Informe o JWT: ").strip()

    payload = validar_jwt(token, JWT_SECRET)

    if payload is None:
        print("Acesso negado: token inválido ou expirado.")
        return

    print("Acesso permitido!")
    print("Usuário autenticado:")
    print(f"ID: {payload['sub']}")
    print(f"Nome: {payload['nome']}")
    print(f"Email: {payload['email']}")
    print("Você acessou um método sensível com sucesso.")


def listar_usuarios():
    print("\n=== USUÁRIOS CADASTRADOS ===")
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, email FROM usuarios")
    usuarios = cursor.fetchall()

    conn.close()

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for usuario in usuarios:
        print(f"ID: {usuario[0]} | Nome: {usuario[1]} | Email: {usuario[2]}")

def menu():
    criar_tabela()

    while True:
        print("\n==============================")
        print("   SISTEMA DE AUTENTICAÇÃO")
        print("==============================")
        print("1. Criar conta")
        print("2. Fazer login")
        print("3. Acessar método sensível com JWT")
        print("4. Listar usuários")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            login_usuario()
        elif opcao == "3":
            metodo_sensivel()
        elif opcao == "4":
            listar_usuarios()
        elif opcao == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()