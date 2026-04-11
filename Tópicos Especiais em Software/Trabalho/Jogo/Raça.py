from abc import ABC, abstractmethod

RAÇAS = ["humano", "elfo", "anão", "halfling", "gnomo", "meioelfo"]

class Raça(ABC):
    def __init__(self, nome, movimento, infravisao, alinhamento):
        self.nome = nome
        self.movimento = movimento
        self.infravisao = infravisao
        self.alinhamento = alinhamento

    @abstractmethod
    def habilidades(self):
        pass

class humano(Raça):
    def __init__(self):
        super().__init__(nome = "Humano", movimento = 9, infravisao = 0, alinhamento = "Qualquer")

    def habilidades(self):
        Habilidades = ["APRENDIZADO", "ADAPTIBILIDADE"]

class elfo(Raça):
    def __init__(self):
        super().__init__(nome = "Elfo", movimento = 9, infravisao = 18, alinhamento = "Neutro")

    def habilidades(self):
        Habilidades = ["PERCEPÇÃO NATURAL", "GRACIOSOS", "TREINAMENTO RACIAL", "IMUNIDADES"]
    
class anão(Raça):
    def __init__(self):
        super().__init__(nome = "Anão", movimento = 9, infravisao = 18, alinhamento = "Ordem")

    def habilidades(self):
        Habilidades = ["MINERADORES", "VIGOROSO", "ARMAS GRANDES", "INIMIGOS"]

class halfling(Raça):
    def __init__(self):
        super().__init__(nome = "Halfling", movimento = 9, infravisao = 0, alinhamento = "Neutro")

    def habilidades(self):
        Habilidades = ["FURTIVO", "DESTEMIDO", "BONS DE MIRA", "PEQUENOS", "RESTRIÇÕES"]

class gnomo(Raça):
    def __init__(self):
        super().__init__(nome = "Gnomo", movimento = 9, infravisao = 18, alinhamento = "Neutro")

    def habilidades(self):
        Habilidades = ["AVALIADORES", "SAGAZES E VIGOROSOS", "RESTRIÇÕES"]

class meioelfo(Raça):
    def __init__(self):
        super().__init__(nome = "Meio-elfo", movimento = 9, infravisao = 9, alinhamento = "Caos")

    def habilidades(self):
        Habilidades = ["APRENDIZADO", "GRACIOSO E VIGOROSO", "IDIOMA EXTRA", "IMUNIDADES"]