import unicodedata

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

frase = input("Digite uma frase: ")

frase_limpa = remover_acentos(frase).lower().replace(" ", "")

if(frase_limpa == frase_limpa[::-1]):
    print("É um palindromo")
else:
    print("Não é um palindromo")