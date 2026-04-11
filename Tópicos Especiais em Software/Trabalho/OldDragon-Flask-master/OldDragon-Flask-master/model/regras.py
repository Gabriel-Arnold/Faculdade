import random

def rolar_dado(lados=6, qtd=3):
    return [random.randint(1, lados) for _ in range(qtd)]

def gerar_atributos():
    atributos = {}
    nomes = ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"]
    for nome in nomes:
        rolagem = rolar_dado()
        atributos[nome] = sum(rolagem)
    return atributos
