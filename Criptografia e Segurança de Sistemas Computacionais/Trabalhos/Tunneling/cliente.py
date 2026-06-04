import socket
import threading
import random
import math

# ---------------- RSA SIMPLES ----------------
def eh_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def gerar_primo():
    while True:
        n = random.randint(100, 300)
        if eh_primo(n):
            return n

def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def inverso_modular(e, phi):
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None

def gerar_chaves():
    p = gerar_primo()
    q = gerar_primo()
    while q == p:
        q = gerar_primo()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if mdc(e, phi) != 1:
        e = 3
        while mdc(e, phi) != 1:
            e += 2

    d = inverso_modular(e, phi)
    return (e, n), (d, n)

def criptografar(texto, chave_publica):
    e, n = chave_publica
    return [pow(ord(char), e, n) for char in texto]

def descriptografar(lista, chave_privada):
    d, n = chave_privada
    return ''.join(chr(pow(num, d, n)) for num in lista)

# ---------------- CHAT CLIENTE ----------------
HOST = "127.0.0.1"
PORTA = 5000

minha_publica, minha_privada = gerar_chaves()
chave_publica_servidor = None
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receber_mensagens():
    while True:
        try:
            dados = cliente.recv(4096).decode()

            if not dados:
                print("\nServidor desconectou.")
                break

            numeros = list(map(int, dados.split(",")))
            mensagem = descriptografar(numeros, minha_privada)
            print("\nServidor:", mensagem)
            print("Você: ", end="", flush=True)

        except:
            print("\nErro ao receber mensagem.")
            break

def enviar_mensagens():
    while True:
        mensagem = input("Você: ")

        if mensagem.lower() == "sair":
            cliente.close()
            break

        criptografada = criptografar(mensagem, chave_publica_servidor)
        texto_envio = ",".join(map(str, criptografada))
        cliente.send(texto_envio.encode())

def iniciar_cliente():
    global chave_publica_servidor

    cliente.connect((HOST, PORTA))
    print("Conectado ao servidor.")

    # Recebe chave pública do servidor
    dados = cliente.recv(1024).decode()
    e_servidor, n_servidor = map(int, dados.split(","))
    chave_publica_servidor = (e_servidor, n_servidor)

    # Envia chave pública do cliente
    e, n = minha_publica
    cliente.send(f"{e},{n}".encode())

    print("Chaves assimétricas trocadas com sucesso.")
    print("Digite suas mensagens. Para sair, digite: sair\n")

    thread_receber = threading.Thread(target=receber_mensagens)
    thread_receber.daemon = True
    thread_receber.start()

    enviar_mensagens()

iniciar_cliente()