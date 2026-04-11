import random
import Dados
import Raça

class Personagem:
    def __init__(self, nome, raca, classe):
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.atributos = {
            "FOR": 0,
            "DES": 0,
            "CON": 0,
            "INT": 0,
            "SAB": 0,
            "CAR": 0
        }
    def distribuir_classico(self):
        ordem = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]
        for chave in ordem:
            self.atributos[chave] = Dados.rolar_dado(6, 3)

    def distribuir_aventureiro(self):
        valores = [Dados.rolar_dado(6, 3) for _ in range(6)]
        print("Seus 6 valores (3d6):", valores)
        restantes = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]
        for v in valores:
            while True:
                print("Atributos restantes:", restantes)
                escolha = input(f"Em qual atributo deseja colocar o valor {v}? ").strip().upper()
                if escolha in restantes:
                    self.atributos[escolha] = v
                    restantes.remove(escolha)
                    break
                else:
                    print("Atributo inválido. Tente de novo.")

    def distribuir_heroico(self):
        def rolar_4d6_drop_menor():
            rolagens = [random.randint(1, 6) for _ in range(4)]
            rolagens.sort()
            return sum(rolagens[1:])

        valores = [rolar_4d6_drop_menor() for _ in range(6)]
        print("Seus 6 valores (4d6 descartando o menor):", valores)
        restantes = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]
        for v in valores:
            while True:
                print("Atributos restantes:", restantes)
                escolha = input(f"Em qual atributo deseja colocar o valor {v}? ").strip().upper()
                if escolha in restantes:
                    self.atributos[escolha] = v
                    restantes.remove(escolha)
                    break
                else:
                    print("Atributo inválido. Tente de novo.")
    def teste_atributo(self, nome_atributo, ajuste=0):
        valor = self.atributos.get(nome_atributo.upper(), 0) + ajuste
        d20 = random.randint(1, 20)

        print(f"Teste de {nome_atributo.upper()} (valor {valor}, ajuste {ajuste:+d}) -> d20: {d20}")

        if d20 == 1:
            print("Sucesso automático (1).")
            return True
        if d20 == 20:
            print("Falha automática (20).")
            return False

        if d20 <= valor:
            print("Sucesso!")
            return True
        else:
            print("Falhou.")
            return False
    def ficha(self):
        print("\n=== FICHA DO PERSONAGEM ===")
        print(f"Nome:   {self.nome}")
        print(f"Raça:   {self.raca.nome}")
        print(f"Classe: {self.classe.nome}")
        print("Atributos:")
        for k in ["FOR", "DES", "CON", "INT", "SAB", "CAR"]:
            print(f"  {k}: {self.atributos[k]}")
        print("============================\n")