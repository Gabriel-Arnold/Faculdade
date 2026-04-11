import random

def rolar_dado(lados, vezes=1):
    soma = 0
    for _ in range(vezes):
        soma += random.randint(1, lados)
    return soma

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
            self.atributos[chave] = rolar_dado(6, 3)

    def distribuir_aventureiro(self):
        valores = [rolar_dado(6, 3) for _ in range(6)]
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
        print(f"Nome:  {self.nome}")
        print(f"Raça:  {self.raca}")
        print(f"Classe:{self.classe}")
        print("Atributos:")
        for k in ["FOR", "DES", "CON", "INT", "SAB", "CAR"]:
            print(f"  {k}: {self.atributos[k]}")
        print("============================\n")


class Jogo:
    def __init__(self):
        self.personagem = None

    def escolher_estilo(self):
        print("Escolha o estilo de distribuição de atributos:")
        print("1) Clássico (3d6 na ordem)")
        print("2) Aventureiro (3d6 e você escolhe onde colocar)")
        print("3) Heroico (4d6 descartando o menor e você escolhe)")
        while True:
            op = input("Opção (1/2/3): ").strip()
            if op in ("1", "2", "3"):
                return op
            print("Opção inválida.")

    def criar_personagem(self):
        nome = input("Nome do personagem: ").strip()
        raca = input("Raça (Humano, Elfo, Anão, Halfling...): ").strip()
        classe = input("Classe (Guerreiro, Clérigo, Mago, Ladrão...): ").strip()

        self.personagem = Personagem(nome, raca, classe)

        estilo = self.escolher_estilo()
        if estilo == "1":
            self.personagem.distribuir_classico()
        elif estilo == "2":
            self.personagem.distribuir_aventureiro()
        else:
            self.personagem.distribuir_heroico()

        self.personagem.ficha()

    def rodar_teste(self):
        if not self.personagem:
            print("Crie um personagem primeiro.")
            return
        print("Fazer um teste de atributo (ex.: FOR, DES, CON, INT, SAB, CAR)")
        nome_attr = input("Qual atributo? ").strip().upper() 
        ajuste = 0
        if(nome_attr == "FOR" or nome_attr == "DES" or nome_attr == "CON" or nome_attr == "INT" or nome_attr == "SAB" or nome_attr == "CAR"):
            if (self.personagem.atributos[nome_attr] <= 3):
                ajuste = -3
            elif (self.personagem.atributos[nome_attr] >= 4 and self.personagem.atributos[nome_attr] <= 5):
                ajuste = -2
            elif (self.personagem.atributos[nome_attr] >= 6 and self.personagem.atributos[nome_attr] <= 8):
                ajuste = -1
            elif (self.personagem.atributos[nome_attr] >= 13 and self.personagem.atributos[nome_attr] <= 14):
                ajuste = 1
            elif (self.personagem.atributos[nome_attr] >= 15 and self.personagem.atributos[nome_attr] <= 16):
                ajuste = 2
            elif (self.personagem.atributos[nome_attr] >= 17 and self.personagem.atributos[nome_attr] <= 18):
                ajuste = 3
            elif (self.personagem.atributos[nome_attr] >= 19 and self.personagem.atributos[nome_attr] <= 20):
                ajuste = 4
        self.personagem.teste_atributo(nome_attr, ajuste)

    def menu(self):
        while True:
            print("=== MENU ===")
            print("1) Criar personagem")
            print("2) Mostrar ficha")
            print("3) Teste de atributo")
            print("4) Sair")
            opc = input("Escolha: ").strip()
            if opc == "1":
                self.criar_personagem()
            elif opc == "2":
                if self.personagem:
                    self.personagem.ficha()
                else:
                    print("Nenhum personagem criado ainda.")
            elif opc == "3":
                self.rodar_teste()
            elif opc == "4":
                print("Até mais!")
                break
            else:
                print("Opção inválida.")


def main():
    random.seed()
    jogo = Jogo()
    jogo.menu()

if __name__ == "__main__":
    main()
