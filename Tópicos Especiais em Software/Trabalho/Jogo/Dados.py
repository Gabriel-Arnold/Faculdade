import random

def rolar_dado(lados, vezes=1):
    soma = 0
    for _ in range(vezes):
        soma += random.randint(1, lados)
    return soma