from sha256_impl import sha256

def gerar_hash():
    caminho = input("Arquivo para gerar hash: ").strip()

    with open(caminho, "rb") as f:
        conteudo = f.read()

    resultado = sha256(conteudo)
    print("\nSHA256:")
    print(resultado)

def validar_hash():
    caminho = input("Arquivo para validar: ").strip()
    hash_informado = input("Hash SHA256: ").strip().lower()

    with open(caminho, "rb") as f:
        conteudo = f.read()

    hash_calculado = sha256(conteudo)

    print("\nHash calculado:", hash_calculado)

    if hash_calculado == hash_informado:
        print("ARQUIVO AUTÊNTICO - HASH VÁLIDO")
    else:
        print("ARQUIVO NÃO AUTÊNTICO - HASH INVÁLIDO")

while True:
    print("\n=== SISTEMA SHA256 ===")
    print("1 - Gerar hash")
    print("2 - Validar arquivo")
    print("0 - Sair")

    op = input("Escolha: ")

    if op == "1":
        gerar_hash()
    elif op == "2":
        validar_hash()
    elif op == "0":
        break
    else:
        print("Opção inválida.")
