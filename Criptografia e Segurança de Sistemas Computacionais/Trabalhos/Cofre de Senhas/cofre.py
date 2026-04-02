import os
import sys
import hashlib
import getpass
from aes import AES256

BLOCK_SIZE = 16
KEY_SIZE = 32
SALT_SIZE = 16
IV_SIZE = 16
PBKDF2_ITERATIONS = 100_000


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def pad(data):
    n = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([n] * n)


def unpad(data):
    if not data or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Padding inválido")
    n = data[-1]
    if n < 1 or n > BLOCK_SIZE or data[-n:] != bytes([n] * n):
        raise ValueError("Padding inválido")
    return data[:-n]


def derive_key(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=KEY_SIZE
    )


def cbc_encrypt(key, iv, plaintext):
    aes = AES256(key)
    plaintext = pad(plaintext)

    ciphertext = b""
    previous = iv

    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i + BLOCK_SIZE]
        block = xor_bytes(block, previous)
        encrypted = aes.encrypt_block(block)
        ciphertext += encrypted
        previous = encrypted

    return ciphertext


def cbc_decrypt(key, iv, ciphertext):
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Tamanho do texto cifrado inválido")

    aes = AES256(key)
    plaintext = b""
    previous = iv

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        decrypted = aes.decrypt_block(block)
        plaintext += xor_bytes(decrypted, previous)
        previous = block

    return unpad(plaintext)


def cbc_encrypt_raw(key, iv, plaintext):
    aes = AES256(key)
    ciphertext = b""
    previous = iv

    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i + BLOCK_SIZE]
        block = xor_bytes(block, previous)
        encrypted = aes.encrypt_block(block)
        ciphertext += encrypted
        previous = encrypted

    return ciphertext


def cbc_decrypt_raw(key, iv, ciphertext):
    aes = AES256(key)
    plaintext = b""
    previous = iv

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        decrypted = aes.decrypt_block(block)
        plaintext += xor_bytes(decrypted, previous)
        previous = block

    return plaintext


def encrypt_file(filename):
    if not os.path.exists(filename):
        print("Arquivo não encontrado")
        return

    password = getpass.getpass("Digite a senha: ")

    with open(filename, "rb") as f:
        data = f.read()

    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    key = derive_key(password, salt)

    ciphertext = cbc_encrypt(key, iv, data)

    with open(filename + ".cifrado", "wb") as f:
        f.write(salt + iv + ciphertext)

    print("Arquivo cifrado com sucesso:", filename + ".cifrado")


def decrypt_file(filename):
    if not os.path.exists(filename):
        print("Arquivo não encontrado")
        return

    password = getpass.getpass("Digite a senha: ")

    with open(filename, "rb") as f:
        data = f.read()

    if len(data) < SALT_SIZE + IV_SIZE:
        print("Arquivo cifrado inválido")
        return

    salt = data[:SALT_SIZE]
    iv = data[SALT_SIZE:SALT_SIZE + IV_SIZE]
    ciphertext = data[SALT_SIZE + IV_SIZE:]

    key = derive_key(password, salt)

    try:
        plaintext = cbc_decrypt(key, iv, ciphertext)
        print("\nConteúdo original:\n")
        try:
            print(plaintext.decode("utf-8"))
        except UnicodeDecodeError:
            print(plaintext)
    except Exception as e:
        print("Erro ao decifrar:", e)


def test():
    print("Executando teste NIST...\n")

    key = bytes.fromhex(
        "603deb1015ca71be2b73aef0857d7781"
        "1f352c073b6108d72d9810a30914dff4"
    )

    iv = bytes.fromhex("000102030405060708090a0b0c0d0e0f")

    plaintext = bytes.fromhex(
        "6bc1bee22e409f96e93d7e117393172a"
        "ae2d8a571e03ac9c9eb76fac45af8e51"
        "30c81c46a35ce411e5fbc1191a0a52ef"
        "f69f2445df4f9b17ad2b417be66c3710"
    )

    expected = bytes.fromhex(
        "f58c4c04d6e5f1ba779eabfb5f7bfbd6"
        "9cfc4e967edb808d679f777bc6702c7d"
        "39f23369a9d9bacfa530e26304231461"
        "b2eb05e2c39be9fcda6c19078c6a9d1b"
    )

    result_enc = cbc_encrypt_raw(key, iv, plaintext)
    if result_enc == expected:
        print("Teste de cifragem CBC: SUCESSO")
    else:
        print("Teste de cifragem CBC: FALHA")

    result_dec = cbc_decrypt_raw(key, iv, expected)
    if result_dec == plaintext:
        print("Teste de decifragem CBC: SUCESSO")
    else:
        print("Teste de decifragem CBC: FALHA")


def usage():
    print("Uso:")
    print("  python3 cofre.py cifrar <arquivo>")
    print("  python3 cofre.py decifrar <arquivo.cifrado>")
    print("  python3 cofre.py testar")


def main():
    if len(sys.argv) < 2:
        usage()
        return

    command = sys.argv[1].lower()

    if command == "cifrar":
        if len(sys.argv) != 3:
            usage()
            return
        encrypt_file(sys.argv[2])

    elif command == "decifrar":
        if len(sys.argv) != 3:
            usage()
            return
        decrypt_file(sys.argv[2])

    elif command == "testar":
        test()

    else:
        usage()


if __name__ == "__main__":
    main()