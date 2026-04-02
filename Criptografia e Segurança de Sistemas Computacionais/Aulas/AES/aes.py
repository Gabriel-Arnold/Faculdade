import base64
from ctypes.wintypes import tagSIZE
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

KEY_SIZE = 32
SALT_SIZE = 16
NONCE_SIZE = 12
TAG_SIZE = 16
PBKDF2_INTERATIONS = 100_000

def gerar_chave(senha: str, salt: bytes) -> bytes:
    return PBKDF2(senha, salt, dkLen=KEY_SIZE, count=PBKDF2_INTERATIONS)

def criptografar_texto(texto: str, senha: str) -> str:
    salt = get_random_bytes(SALT_SIZE)
    chave = gerar_chave(senha, salt)

    cipher = AES.new(chave, AES.MODE_GCM, nonce=get_random_bytes(NONCE_SIZE))
    texto_bytes = texto.encode("utf-8")

    ciphertext, tag = cipher.encrypt_and_digest(texto_bytes)

    resultado = salt + cipher.nonce + tag + ciphertext
    return base64.b64encode(resultado).decode("utf-8")

def descriptografar_texto(conteudo_criptografado: str, senha: str) -> str:
        dados = base64.b64decode(conteudo_criptografado)

        salt = dados[:SALT_SIZE]
        nonce = dados[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
        tag = dados[SALT_SIZE + NONCE_SIZE:SALT_SIZE + NONCE_SIZE + TAG_SIZE]
        ciphertext = dados[SALT_SIZE + NONCE_SIZE + TAG_SIZE:]


        chave = gerar_chave(senha, salt)
        cipher = AES.new(chave, AES.MODE_GCM, nonce=nonce)

        try:
             texto_bytes = cipher.decrypt_and_verify(ciphertext, tag)
             return texto_bytes.decode("utf-8")
        except ValueError:
             raise ValueError("Senha incorreta ou conteúdo corrompido.")
        
if __name__ == "__main__":
    texto_original = "Ola, este é um texto secreto."
    senha = "senha123"

    criptografado = criptografar_texto(texto_original, senha)
    print("Texto Original: ", texto_original)
    print("Texto Criptografado: ", criptografado)

    try:
        descriptografado = descriptografar_texto(criptografado, senha)
        print("Texto Descriptografado: ", descriptografado)
    except ValueError as e:
          print("Erro: ", e)
