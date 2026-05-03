#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TAM_NOME 100
#define TAM_CARGO 100

// Estrutura do nó da árvore binária de pesquisa
typedef struct Funcionario {
    int matricula;                    // Identificador único do funcionário
    char nome[TAM_NOME];              // Nome do funcionário
    char cargo[TAM_CARGO];            // Cargo do funcionário
    float salario;                    // Salário do funcionário
    struct Funcionario *left;         // Ponteiro para o filho esquerdo
    struct Funcionario *right;        // Ponteiro para o filho direito
} Funcionario;

// Função para criar um novo nó com os dados do funcionário
Funcionario* criarFuncionario(int matricula, char nome[], char cargo[], float salario) {
    Funcionario *novo = (Funcionario*) malloc(sizeof(Funcionario));

    if (novo == NULL) {
        printf("Erro ao alocar memoria.\n");
        exit(1);
    }

    novo->matricula = matricula;
    strcpy(novo->nome, nome);
    strcpy(novo->cargo, cargo);
    novo->salario = salario;
    novo->left = NULL;
    novo->right = NULL;

    return novo;
}

// Função para inserir um funcionário na árvore
Funcionario* inserirFuncionario(Funcionario *raiz, int matricula, char nome[], char cargo[], float salario) {
    // Se a árvore estiver vazia, cria o nó e retorna como raiz
    if (raiz == NULL) {
        return criarFuncionario(matricula, nome, cargo, salario);
    }

    // Se a matrícula for menor, insere na subárvore esquerda
    if (matricula < raiz->matricula) {
        raiz->left = inserirFuncionario(raiz->left, matricula, nome, cargo, salario);
    }
    // Se a matrícula for maior, insere na subárvore direita
    else if (matricula > raiz->matricula) {
        raiz->right = inserirFuncionario(raiz->right, matricula, nome, cargo, salario);
    }
    // Se a matrícula já existir, não insere duplicado
    else {
        printf("Erro: ja existe um funcionario com a matricula %d.\n", matricula);
    }

    return raiz;
}

// Função para buscar um funcionário pela matrícula
Funcionario* buscarFuncionario(Funcionario *raiz, int matricula) {
    // Se a árvore estiver vazia ou encontrou a matrícula
    if (raiz == NULL || raiz->matricula == matricula) {
        return raiz;
    }

    // Se a matrícula procurada for menor, busca na esquerda
    if (matricula < raiz->matricula) {
        return buscarFuncionario(raiz->left, matricula);
    }

    // Caso contrário, busca na direita
    return buscarFuncionario(raiz->right, matricula);
}

// Função para atualizar os dados de um funcionário existente
void atualizarFuncionario(Funcionario *raiz, int matricula) {
    Funcionario *encontrado = buscarFuncionario(raiz, matricula);

    if (encontrado == NULL) {
        printf("Funcionario com matricula %d nao encontrado.\n", matricula);
        return;
    }

    printf("\nFuncionario encontrado!\n");
    printf("Matricula: %d\n", encontrado->matricula);
    printf("Nome atual: %s\n", encontrado->nome);
    printf("Cargo atual: %s\n", encontrado->cargo);
    printf("Salario atual: %.2f\n", encontrado->salario);

    printf("\nDigite o novo nome: ");
    getchar(); // limpa o buffer do teclado
    fgets(encontrado->nome, TAM_NOME, stdin);
    encontrado->nome[strcspn(encontrado->nome, "\n")] = '\0';

    printf("Digite o novo cargo: ");
    fgets(encontrado->cargo, TAM_CARGO, stdin);
    encontrado->cargo[strcspn(encontrado->cargo, "\n")] = '\0';

    printf("Digite o novo salario: ");
    scanf("%f", &encontrado->salario);

    printf("Dados atualizados com sucesso!\n");
}

// Função para exibir um funcionário
void exibirFuncionario(Funcionario *f) {
    if (f != NULL) {
        printf("Matricula: %d\n", f->matricula);
        printf("Nome: %s\n", f->nome);
        printf("Cargo: %s\n", f->cargo);
        printf("Salario: %.2f\n", f->salario);
        printf("-----------------------------\n");
    }
}

// Função para listar todos os funcionários em ordem crescente de matrícula
void listarFuncionarios(Funcionario *raiz) {
    // Percurso em ordem: esquerda -> raiz -> direita
    if (raiz != NULL) {
        listarFuncionarios(raiz->left);
        exibirFuncionario(raiz);
        listarFuncionarios(raiz->right);
    }
}

// Função para liberar toda a memória da árvore
void liberarArvore(Funcionario *raiz) {
    if (raiz != NULL) {
        liberarArvore(raiz->left);
        liberarArvore(raiz->right);
        free(raiz);
    }
}

// Função principal com menu
int main() {
    Funcionario *raiz = NULL;
    int opcao;
    int matricula;
    char nome[TAM_NOME];
    char cargo[TAM_CARGO];
    float salario;

    do {
        printf("\n===== SISTEMA DE CADASTRO DE FUNCIONARIOS =====\n");
        printf("1. Inserir funcionario\n");
        printf("2. Atualizar funcionario\n");
        printf("3. Buscar funcionario\n");
        printf("4. Listar funcionarios\n");
        printf("0. Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("\nDigite a matricula: ");
                scanf("%d", &matricula);
                getchar(); // limpa o buffer

                printf("Digite o nome: ");
                fgets(nome, TAM_NOME, stdin);
                nome[strcspn(nome, "\n")] = '\0';

                printf("Digite o cargo: ");
                fgets(cargo, TAM_CARGO, stdin);
                cargo[strcspn(cargo, "\n")] = '\0';

                printf("Digite o salario: ");
                scanf("%f", &salario);

                raiz = inserirFuncionario(raiz, matricula, nome, cargo, salario);
                break;

            case 2:
                printf("\nDigite a matricula do funcionario a ser atualizado: ");
                scanf("%d", &matricula);
                atualizarFuncionario(raiz, matricula);
                break;

            case 3: {
                Funcionario *resultado;
                printf("\nDigite a matricula a ser buscada: ");
                scanf("%d", &matricula);

                resultado = buscarFuncionario(raiz, matricula);

                if (resultado != NULL) {
                    printf("\nFuncionario encontrado:\n");
                    exibirFuncionario(resultado);
                } else {
                    printf("Funcionario com matricula %d nao encontrado.\n", matricula);
                }
                break;
            }

            case 4:
                if (raiz == NULL) {
                    printf("\nNenhum funcionario cadastrado.\n");
                } else {
                    printf("\n===== LISTA DE FUNCIONARIOS =====\n");
                    listarFuncionarios(raiz);
                }
                break;

            case 0:
                printf("\nEncerrando o programa...\n");
                break;

            default:
                printf("\nOpcao invalida!\n");
        }

    } while (opcao != 0);

    liberarArvore(raiz);
    return 0;
}