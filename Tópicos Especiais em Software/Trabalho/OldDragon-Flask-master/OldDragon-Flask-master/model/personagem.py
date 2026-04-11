class Personagem:
    def __init__(self, nome, atributos):
        self.nome = nome
        self.atributos = atributos

    def modificador(self, atributo):
        """Calcula modificador no estilo Old Dragon:
        (atributo - 10) // 2, arredondado para baixo"""
        valor = self.atributos.get(atributo, 10)
        return (valor - 10) // 2

    def resumo(self):
        return {
            "nome": self.nome,
            "atributos": self.atributos,
            "modificadores": {a: self.modificador(a) for a in self.atributos}
        }
