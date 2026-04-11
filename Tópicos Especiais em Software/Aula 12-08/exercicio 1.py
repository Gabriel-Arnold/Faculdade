numeros = []
cont = True

while cont == True:
    n = int(input("Digite um numero ou 0 para continuar"))
    if(n > 0):
        numeros.append(n)
    else:
        cont = False

total = len(numeros)
maior = 0
menor = 0
media = 0
pares = 0
impares = 0
for i, valor in enumerate(numeros):
    media = media + numeros[i]
    if(numeros[i]%2 == 0): 
        pares = pares + 1
    else:
        impares = impares + 1
    if(i == 0):
        maior = numeros[i]
        menor = numeros[i]
    else:
        if(numeros[i] >= maior): maior = numeros[i]
        if(numeros[i] <= menor): menor = numeros[i]
media = media / len(numeros)
print("Maior numero:", maior)
print("Menor numero:", menor)
print("Média:", media)
print("Quantidade de pares:", pares)
print("Quantidade de impares:", impares)
