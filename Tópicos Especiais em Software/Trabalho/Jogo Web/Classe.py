from abc import ABC, abstractmethod

CLASSES = ["guerreiro", "mago", "ladrão"]

class Classe(ABC):
    def __init__(self, nome, vida, nivel):
        self.nome = nome
        self.vida = vida
        self.nivel = nivel

    @abstractmethod
    def habilidades(self):
        pass

class Guerreiro(Classe):
    def __init__(self, nome = "Guerreiro", vida = 10, nivel = 1):
        super().__init__(nome, vida, nivel)

    def habilidades(self):
        return super().habilidades()

class Ladrão(Classe):
    def __init__(self, nome = "Ladrão", vida = 6, nivel = 1):
        super().__init__(nome, vida, nivel)

    def habilidades(self):
        return super().habilidades()

class Mago(Classe):
    def __init__(self, nome = "Mago", vida = 4, nivel = 1):
        super().__init__(nome, vida, nivel)

    def habilidades(self):
        return super().habilidades()