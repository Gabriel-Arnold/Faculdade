import random
import Personagem
import Raça
import Classe

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
    raca = ""
    def criar_personagem(self):
        nome = input("Nome do personagem: ").strip()
        raca = ""
        while True:
            raca = input("Raça (Humano, Elfo, Anão, Halfling, Gnomo, Meioelfo): ").strip()
            if raca.lower() in Raça.RAÇAS:
                if(raca.lower() == "humano"):
                    raca = Raça.humano()
                    break
                elif(raca.lower() == "elfo"):
                    raca = Raça.elfo()
                    break
                elif(raca.lower() == "anão"):
                    raca = Raça.anão()
                    break
                elif(raca.lower() == "halfling"):
                    raca = Raça.halfling()
                    break
                elif(raca.lower() == "gnomo"):
                    raca = Raça.gnomo()
                    break
                elif(raca.lower() == "meioelfo"):
                    raca = Raça.meioelfo()
                    break
            else:
                print("Raça inválida. Tente de novo.")
        classe = ""
        while True:
            classe = input("Classe (Guerreiro, Mago, Ladrão): ").strip()
            if classe.lower() in Classe.CLASSES:
                if(classe.lower() == "guerreiro"):
                    classe = Classe.Guerreiro()
                elif(classe.lower() == "ladrão"):
                    classe = Classe.Ladrão()
                elif(classe.lower() == "mago"):
                    classe = Classe.Mago()
                break
            else:
                print("Classe inválida. Tente de novo.")

        self.personagem = Personagem.Personagem(nome, raca, classe)

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
