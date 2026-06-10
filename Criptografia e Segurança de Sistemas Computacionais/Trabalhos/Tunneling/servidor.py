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

# ---------------- CHAT SERVIDOR ----------------
HOST = "127.0.0.1"
PORTA = 5050

minha_publica, minha_privada = gerar_chaves()
chave_publica_cliente = None
cliente = None

def receber_mensagens():
    global cliente

    while True:
        try:
            dados = cliente.recv(4096).decode()

            if not dados:
                print("\nCliente desconectou.")
                break

            numeros = list(map(int, dados.split(",")))
            mensagem = descriptografar(numeros, minha_privada)
            print("\nCliente:", mensagem)
            print("Você: ", end="", flush=True)

        except:
            print("\nErro ao receber mensagem.")
            break

def enviar_mensagens():
    global cliente, chave_publica_cliente

    while True:
        mensagem = input("Você: ")

        if mensagem.lower() == "sair":
            cliente.close()
            break

        criptografada = criptografar(mensagem, chave_publica_cliente)
        texto_envio = ",".join(map(str, criptografada))
        cliente.send(texto_envio.encode())

def iniciar_servidor():
    global cliente, chave_publica_cliente

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORTA))
    servidor.listen(1)

    print("Servidor iniciado.")
    print("Aguardando cliente conectar...")

    cliente, endereco = servidor.accept()
    print("Cliente conectado:", endereco)

    # Envia chave pública do servidor
    e, n = minha_publica
    cliente.send(f"{e},{n}".encode())

    # Recebe chave pública do cliente
    dados = cliente.recv(1024).decode()
    e_cliente, n_cliente = map(int, dados.split(","))
    chave_publica_cliente = (e_cliente, n_cliente)

    print("Chaves assimétricas trocadas com sucesso.")
    print("Digite suas mensagens. Para sair, digite: sair\n")

    thread_receber = threading.Thread(target=receber_mensagens)
    thread_receber.daemon = True
    thread_receber.start()

    enviar_mensagens()

iniciar_servidor()
