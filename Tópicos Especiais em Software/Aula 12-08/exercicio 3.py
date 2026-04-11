class produto:
    def __init__(self, nome, estoque):
        self.nome = nome
        self.estoque = estoque

p1 = produto("Cadeira", 5)
p2 = produto("Mesa", 15)
p3 = produto("Penteadeira", 7)
p4 = produto("Armario", 3)

produtos = [p1, p2, p3, p4]

aaaaaaaaaaaaaaaaaaaaaaaaaaaaa = True
while aaaaaaaaaaaaaaaaaaaaaaaaaaaaa == True:
    print("1 - Cadastrar produto")
    print("2 - Remover produto")
    print("3 - Editar estoque produto")
    print("4 - Listar produtos")
    print("0 - Sair")
    selecionar = int(input("Digite um numero: "))

    if(selecionar == 1):
        nome = input("Digite o nome do produto: ")
        estoque = int(input("Digite o estoque do produto: "))
        p = produto(nome, estoque)
        produtos.append(p)
        print("Produto criado")
    elif(selecionar == 2):
        for i, p in enumerate(produtos):
            print(i, p.nome)
        indice = int(input("Digite o indice do produto para remover"))
        p = produtos[indice]
        produtos.remove(p)
        print("Produto removido.")
    elif(selecionar == 3):
        for i, p in enumerate(produtos):
            print(i, p.nome)
        indice = int(input("Digite o indice do produto para editar"))
        es = int(input("Digite o estoque do produto"))
        p = produtos[indice]
        p.estoque = es
        print("Estoque alterado.")
    elif(selecionar == 4):
        for i, p in enumerate(produtos):
            print(i, p.nome)
    elif(selecionar == 0): aaaaaaaaaaaaaaaaaaaaaaaaaaaaa = False

    