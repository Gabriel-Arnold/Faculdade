#!/usr/bin/env python3
"""
cofre.py

Programa para cifrar e decifrar arquivos usando:
- AES-256
- modo CBC
- derivação de chave PBKDF2-HMAC-SHA256

====================================================
O QUE ESTE ARQUIVO FAZ
====================================================

Este programa implementa 3 comandos principais:

1) cifrar
   Exemplo:
       python cofre.py cifrar mensagem.txt

   O programa:
   - pede uma senha ao usuário
   - gera um salt aleatório
   - deriva uma chave AES-256 a partir da senha com PBKDF2
   - gera um IV aleatório
   - cifra o arquivo usando AES-256 em modo CBC
   - salva tudo em:
         [salt][IV][ciphertext]

2) decifrar
   Exemplo:
       python cofre.py decifrar mensagem.txt.cifrado

   O programa:
   - lê o salt e o IV do início do arquivo
   - pede a senha
   - deriva novamente a mesma chave via PBKDF2
   - decifra o conteúdo
   - exibe o conteúdo original

3) testar
   Exemplo:
       python cofre.py testar

   O programa:
   - roda testes automáticos
   - testa o AES-256 com vetor conhecido
   - testa decifração
   - testa CBC ida e volta
   - mostra SUCESSO ou FALHA
"""

import os
import sys
import getpass
import hashlib
from typing import List

# Importa a implementação do AES-256 feita no outro arquivo
from aes_aluno import AES256


# ====================================================
# CONSTANTES DO SISTEMA
# ====================================================

# O AES trabalha com blocos fixos de 16 bytes
BLOCK_SIZE = 16

# AES-256 usa chave de 32 bytes
KEY_SIZE = 32

# Salt de 16 bytes, conforme especificação
SALT_SIZE = 16

# IV de 16 bytes, conforme especificação do CBC
IV_SIZE = 16

# Número de iterações do PBKDF2
PBKDF2_ITERATIONS = 100_000


# ====================================================
# XOR DE BYTES
# ====================================================
def xor_bytes(a: bytes, b: bytes) -> bytes:
    """
    Faz XOR byte a byte entre duas sequências.

    Exemplo:
        b'\\x01\\x02' XOR b'\\x03\\x04'
    resultado:
        b'\\x02\\x06'

    Essa função é essencial no modo CBC.
    """
    return bytes(x ^ y for x, y in zip(a, b))


# ====================================================
# QUEBRAR EM BLOCOS
# ====================================================
def split_blocks(data: bytes, block_size: int = BLOCK_SIZE) -> List[bytes]:
    """
    Divide um conteúdo em blocos de tamanho fixo.

    Exemplo:
        48 bytes -> 3 blocos de 16 bytes
    """
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]


# ====================================================
# PKCS#7 PADDING
# ====================================================
def pkcs7_pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    """
    Adiciona padding PKCS#7.

    COMO FUNCIONA:
    ------------------------------------------------
    O AES só cifra blocos de 16 bytes.
    Então, se o arquivo não tiver tamanho múltiplo de 16,
    precisamos completar o final.

    Exemplo:
    - se faltam 5 bytes para completar o bloco,
      adicionamos 0x05 0x05 0x05 0x05 0x05

    Se o tamanho já for múltiplo de 16,
    ainda assim adicionamos um bloco inteiro de padding.
    """
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    """
    Remove o padding PKCS#7.

    Verifica:
    - se os dados têm tamanho válido
    - se o último byte indica um padding válido
    - se todos os bytes finais realmente têm aquele valor
    """
    if not data or len(data) % block_size != 0:
        raise ValueError("Dados inválidos para remoção de padding.")

    pad_len = data[-1]

    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Padding inválido.")

    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Padding inválido.")

    return data[:-pad_len]


# ====================================================
# DERIVAÇÃO DE CHAVE COM PBKDF2
# ====================================================
def derive_key(password: str, salt: bytes) -> bytes:
    """
    Deriva uma chave de 32 bytes a partir da senha do usuário.

    ESSE PASSO É MUITO IMPORTANTE.
    ------------------------------------------------
    O usuário digita uma senha em texto.
    Mas o AES-256 precisa de uma chave binária de 32 bytes.

    Então usamos:
        PBKDF2-HMAC-SHA256

    com:
    - senha
    - salt
    - 100.000 iterações
    - saída de 32 bytes

    O salt garante que a mesma senha não gere sempre a mesma chave
    entre arquivos diferentes.
    """
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=KEY_SIZE
    )


# ====================================================
# CBC ENCRYPT
# ====================================================
def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    """
    Cifra dados usando AES-256 em modo CBC.

    COMO O CBC FUNCIONA:
    ------------------------------------------------
    Para o primeiro bloco:
        bloco_1_entrada = plaintext_1 XOR IV
        ciphertext_1 = AES(bloco_1_entrada)

    Para os próximos:
        bloco_i_entrada = plaintext_i XOR ciphertext_(i-1)
        ciphertext_i = AES(bloco_i_entrada)

    Isso faz com que blocos iguais produzam resultados diferentes,
    desde que o IV ou o bloco anterior sejam diferentes.
    """

    aes = AES256(key)

    # Primeiro aplicamos padding
    plaintext = pkcs7_pad(plaintext, BLOCK_SIZE)

    previous = iv
    ciphertext = b""

    for block in split_blocks(plaintext, BLOCK_SIZE):
        # XOR do bloco atual com o IV ou com o bloco cifrado anterior
        xored = xor_bytes(block, previous)

        # Cifra esse bloco
        encrypted = aes.encrypt_block(xored)

        # Acumula no resultado final
        ciphertext += encrypted

        # O bloco cifrado atual vira o "previous" do próximo
        previous = encrypted

    return ciphertext


# ====================================================
# CBC DECRYPT
# ====================================================
def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    """
    Decifra dados usando AES-256 em modo CBC.

    COMO A DECIFRAÇÃO CBC FUNCIONA:
    ------------------------------------------------
    Para o primeiro bloco:
        temp = AES^-1(ciphertext_1)
        plaintext_1 = temp XOR IV

    Para os próximos:
        temp = AES^-1(ciphertext_i)
        plaintext_i = temp XOR ciphertext_(i-1)
    """

    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext inválido: tamanho não múltiplo de 16.")

    aes = AES256(key)

    previous = iv
    plaintext_padded = b""

    for block in split_blocks(ciphertext, BLOCK_SIZE):
        # Primeiro desfaz o AES do bloco atual
        decrypted = aes.decrypt_block(block)

        # Depois faz XOR com o IV ou bloco cifrado anterior
        plain_block = xor_bytes(decrypted, previous)

        plaintext_padded += plain_block

        # O bloco atual passa a ser o previous do próximo
        previous = block

    # Remove o padding do final
    return pkcs7_unpad(plaintext_padded, BLOCK_SIZE)


# ====================================================
# CIFRAR ARQUIVO
# ====================================================
def cifrar_arquivo(caminho: str) -> None:
    """
    Cifra um arquivo no disco.

    PASSO A PASSO:
    ------------------------------------------------
    1. verifica se o arquivo existe
    2. pede senha e confirmação
    3. lê conteúdo do arquivo
    4. gera salt aleatório
    5. gera IV aleatório
    6. deriva chave com PBKDF2
    7. cifra com AES-CBC
    8. salva em:
         arquivo_original + ".cifrado"

    FORMATO DO ARQUIVO CIFRADO:
    ------------------------------------------------
    [salt 16 bytes] [IV 16 bytes] [ciphertext ...]
    """

    if not os.path.isfile(caminho):
        print(f"Erro: arquivo '{caminho}' não encontrado.")
        sys.exit(1)

    senha = getpass.getpass("Digite a senha: ")
    confirmar = getpass.getpass("Confirme a senha: ")

    if senha != confirmar:
        print("Erro: as senhas não conferem.")
        sys.exit(1)

    # Lê o arquivo original em modo binário
    with open(caminho, "rb") as f:
        conteudo = f.read()

    # Gera salt aleatório de 16 bytes
    salt = os.urandom(SALT_SIZE)

    # Gera IV aleatório de 16 bytes
    iv = os.urandom(IV_SIZE)

    # Deriva a chave AES-256 a partir da senha e do salt
    key = derive_key(senha, salt)

    # Cifra o conteúdo
    ciphertext = aes_cbc_encrypt(key, iv, conteudo)

    # Nome de saída
    saida = caminho + ".cifrado"

    # Salva no formato exigido:
    # [salt][IV][ciphertext]
    with open(saida, "wb") as f:
        f.write(salt + iv + ciphertext)

    print(f"Arquivo cifrado com sucesso: {saida}")


# ====================================================
# DECIFRAR ARQUIVO
# ====================================================
def decifrar_arquivo(caminho: str) -> None:
    """
    Decifra um arquivo cifrado.

    PASSO A PASSO:
    ------------------------------------------------
    1. verifica se o arquivo existe
    2. lê os bytes do arquivo
    3. extrai:
         - salt = primeiros 16 bytes
         - IV = próximos 16 bytes
         - ciphertext = resto
    4. pede a senha
    5. deriva a chave novamente com PBKDF2
    6. decifra o conteúdo
    7. exibe o conteúdo original
    """

    if not os.path.isfile(caminho):
        print(f"Erro: arquivo '{caminho}' não encontrado.")
        sys.exit(1)

    with open(caminho, "rb") as f:
        data = f.read()

    # Precisamos ter pelo menos 32 bytes para salt + IV
    if len(data) < SALT_SIZE + IV_SIZE:
        print("Erro: arquivo cifrado inválido ou corrompido.")
        sys.exit(1)

    # Extrai os componentes
    salt = data[:SALT_SIZE]
    iv = data[SALT_SIZE:SALT_SIZE + IV_SIZE]
    ciphertext = data[SALT_SIZE + IV_SIZE:]

    senha = getpass.getpass("Digite a senha: ")

    # Deriva novamente a mesma chave
    key = derive_key(senha, salt)

    try:
        plaintext = aes_cbc_decrypt(key, iv, ciphertext)
    except Exception as e:
        print(f"Erro ao decifrar: senha incorreta ou arquivo corrompido. ({e})")
        sys.exit(1)

    print("\n=== CONTEÚDO ORIGINAL ===\n")

    # Tenta exibir como texto UTF-8
    try:
        print(plaintext.decode("utf-8"))
    except UnicodeDecodeError:
        # Se não for texto, mostra em hexadecimal
        print("O conteúdo não é texto UTF-8. Exibindo em hexadecimal:\n")
        print(plaintext.hex())


# ====================================================
# AUXILIAR PARA TESTES
# ====================================================
def hex_to_bytes(s: str) -> bytes:
    """
    Converte string hexadecimal em bytes.

    Exemplo:
        "00112233" -> b'\\x00\\x11\\x22\\x33'
    """
    return bytes.fromhex(s.replace(" ", ""))


# ====================================================
# TESTES
# ====================================================
def testar() -> None:
    """
    Executa testes automáticos do sistema.

    TESTE 1
    ------------------------------------------------
    Testa AES-256 com vetor conhecido:
    - chave conhecida
    - plaintext conhecido
    - ciphertext esperado conhecido

    TESTE 2
    ------------------------------------------------
    Testa a decifração do mesmo vetor

    TESTE 3
    ------------------------------------------------
    Testa CBC ida e volta:
    cifra -> decifra -> compara com original

    TESTE 4
    ------------------------------------------------
    Verifica se PBKDF2 gera uma chave de 32 bytes
    """

    print("Executando testes...\n")

    sucesso_total = True

    # ============================================
    # TESTE 1: AES-256 BLOCO ÚNICO
    # ============================================
    key = hex_to_bytes(
        "000102030405060708090A0B0C0D0E0F"
        "101112131415161718191A1B1C1D1E1F"
    )

    plaintext = hex_to_bytes("00112233445566778899AABBCCDDEEFF")
    ciphertext_esperado = hex_to_bytes("8EA2B7CA516745BFEAFC49904B496089")

    aes = AES256(key)
    ciphertext_obtido = aes.encrypt_block(plaintext)

    if ciphertext_obtido == ciphertext_esperado:
        print("Teste AES-256 bloco único: SUCESSO")
    else:
        print("Teste AES-256 bloco único: FALHA")
        print("Esperado :", ciphertext_esperado.hex())
        print("Obtido   :", ciphertext_obtido.hex())
        sucesso_total = False

    # ============================================
    # TESTE 2: DECIFRAÇÃO DO BLOCO ÚNICO
    # ============================================
    decrypted = aes.decrypt_block(ciphertext_esperado)

    if decrypted == plaintext:
        print("Teste AES-256 decifração bloco único: SUCESSO")
    else:
        print("Teste AES-256 decifração bloco único: FALHA")
        print("Esperado :", plaintext.hex())
        print("Obtido   :", decrypted.hex())
        sucesso_total = False

    # ============================================
    # TESTE 3: CBC IDA E VOLTA
    # ============================================
    iv = hex_to_bytes("000102030405060708090A0B0C0D0E0F")
    mensagem = b"Teste AES CBC com padding PKCS7."

    try:
        cifrado = aes_cbc_encrypt(key, iv, mensagem)
        decifrado = aes_cbc_decrypt(key, iv, cifrado)

        if decifrado == mensagem:
            print("Teste CBC ida e volta: SUCESSO")
        else:
            print("Teste CBC ida e volta: FALHA")
            sucesso_total = False
    except Exception as e:
        print("Teste CBC ida e volta: FALHA")
        print(f"Erro: {e}")
        sucesso_total = False

    # ============================================
    # TESTE 4: TAMANHO DA CHAVE PBKDF2
    # ============================================
    salt = b"0123456789abcdef"
    senha = "senha-teste"
    chave = derive_key(senha, salt)

    if len(chave) == 32:
        print("Teste PBKDF2 chave 32 bytes: SUCESSO")
    else:
        print("Teste PBKDF2 chave 32 bytes: FALHA")
        sucesso_total = False

    print("\nResultado final:")
    print("TODOS OS TESTES PASSARAM" if sucesso_total else "HOUVE FALHAS")


# ====================================================
# AJUDA / USO DO PROGRAMA
# ====================================================
def mostrar_uso() -> None:
    """
    Mostra como usar o programa pela linha de comando.
    """
    print("Uso:")
    print("  python cofre.py cifrar <arquivo>")
    print("  python cofre.py decifrar <arquivo.cifrado>")
    print("  python cofre.py testar")


# ====================================================
# MAIN
# ====================================================
def main() -> None:
    """
    Função principal.

    Aqui lemos os argumentos da linha de comando e decidimos
    qual operação o programa vai executar.
    """

    if len(sys.argv) < 2:
        mostrar_uso()
        sys.exit(1)

    comando = sys.argv[1].lower()

    if comando == "cifrar":
        if len(sys.argv) != 3:
            mostrar_uso()
            sys.exit(1)
        cifrar_arquivo(sys.argv[2])

    elif comando == "decifrar":
        if len(sys.argv) != 3:
            mostrar_uso()
            sys.exit(1)
        decifrar_arquivo(sys.argv[2])

    elif comando == "testar":
        testar()

    else:
        mostrar_uso()
        sys.exit(1)


if __name__ == "__main__":
    main()