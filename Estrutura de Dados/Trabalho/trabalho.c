#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_CIDADES 100

int **matriz;
char *cidades[MAX_CIDADES];
int totalCidades = 20;

// Cidades e distâncias iniciais
char *cidadesIniciais[] = {
    "Curitiba", "Londrina", "Maringa", "Foz do Iguacu", "Ponta Grossa", "Cascavel", "Colombo", "Guarapuava", "Paranagua", "S.J. Pinhais",
    "Toledo", "Pinhais", "Araucaria", "Umuarama", "Apucarana", "Campo Largo", "Arapongas", "Pato Branco", "Alm. Tamandare", "Sarandi"
};

int dadosIniciais[20][20] = {
    {0,0,0,0,0,0,16,0,90,13,0,8,22,0,0,29,0,0,21,0},
    {0,0,0,0,277,0,0,315,0,0,0,0,0,0,53,0,38,0,0,0},
    {0,0,0,0,400,273,0,329,0,0,278,0,0,145,51,0,61,0,0,14},
    {0,0,0,0,0,131,0,0,0,0,156,0,0,0,0,0,0,337,0,0},
    {0,277,400,0,0,516,0,163,0,0,0,0,0,0,250,90,0,0,0,0},
    {0,0,273,131,516,0,0,252,0,0,39,0,0,168,348,0,0,232,0,0},
    {16,0,0,0,0,0,0,0,105,0,0,17,0,0,0,0,0,0,10,0},
    {0,315,329,0,163,252,0,0,0,0,0,0,0,0,264,226,0,200,0,287},
    {90,0,0,0,0,0,105,0,0,82,0,75,0,0,0,0,0,0,0,0},
    {13,0,0,0,0,0,0,0,82,0,0,10,21,0,0,0,0,0,0,0},
    {0,0,278,156,0,39,0,0,0,0,0,0,0,132,334,0,0,285,0,0},
    {8,0,0,0,0,0,17,0,75,10,0,0,0,0,0,0,0,0,13,0},
    {22,0,0,0,0,0,0,0,0,21,0,0,0,0,0,30,0,0,0,0},
    {0,0,145,0,0,168,0,0,0,0,132,0,0,0,0,0,0,0,0,0},
    {0,53,51,0,250,348,0,264,0,0,334,0,0,0,0,0,18,0,0,63},
    {29,0,0,0,90,0,25,226,0,0,0,0,30,0,0,0,0,0,42,0},
    {0,38,61,0,0,0,0,0,0,0,0,0,0,0,18,0,0,0,0,70},
    {0,0,0,337,0,232,0,200,0,0,285,0,0,0,0,0,0,0,0,0},
    {21,0,0,0,0,0,10,0,0,0,0,13,0,0,0,42,0,0,0,0},
    {0,0,14,0,0,0,0,287,0,0,0,0,0,0,63,0,70,0,0,0}
};

void inicializarGrafo() {
    matriz = (int **)malloc(MAX_CIDADES * sizeof(int *));
    int i, j;
    for (i = 0; i < MAX_CIDADES; i++) {
        matriz[i] = (int *)calloc(MAX_CIDADES, sizeof(int));
    }

    for (i = 0; i < 20; i++) {
        cidades[i] = strdup(cidadesIniciais[i]);
        for (j = 0; j < 20; j++) {
            matriz[i][j] = dadosIniciais[i][j];
        }
    }
}

void liberarGrafo() {
    int i;
    for (i = 0; i < MAX_CIDADES; i++) {
        free(matriz[i]);
    }
    free(matriz);
    for (i = 0; i < totalCidades; i++) {
        free(cidades[i]);
    }
}

void inserirCidade(char *nome) {
    if (totalCidades >= MAX_CIDADES) {
        printf("Limite de cidades atingido.\n");
        return;
    }
    cidades[totalCidades] = strdup(nome);
    int i;
    for (i = 0; i <= totalCidades; i++) {
        int distancia;
        printf("Distancia de %s ate %s: ", nome, cidades[i]);
        scanf("%d", &distancia);
        matriz[totalCidades][i] = distancia;
        matriz[i][totalCidades] = distancia;
    }
    totalCidades++;
}

void removerCidade(int indice) {
    if (indice < 0 || indice >= totalCidades) {
        printf("Indice invalido.\n");
        return;
    }

    free(cidades[indice]);
    int i, j;
    for (i = indice; i < totalCidades - 1; i++) {
        cidades[i] = cidades[i + 1];
        for (j = 0; j < totalCidades; j++) {
            matriz[i][j] = matriz[i + 1][j];
        }
    }
    for (j = indice; j < totalCidades - 1; j++) {
        for (i = 0; i < totalCidades; i++) {
            matriz[i][j] = matriz[i][j + 1];
        }
    }
    totalCidades--;
}

void imprimirMatriz() {
    printf("\nMatriz de Adjacencia:\n     ");
    int i, j;
    for (i = 0; i < totalCidades; i++)
        printf("%2d ", i);
    printf("\n");
    for (i = 0; i < totalCidades; i++) {
        printf("%2d |", i);
        for (j = 0; j < totalCidades; j++)
            printf("%2d ", matriz[i][j]);
        printf("\n");
    }
}

void listarCidades() {
    int i;
    for (i = 0; i < totalCidades; i++) {
        printf("%2d - %s\n", i, cidades[i]);
    }
}

void menorRota(int origem, int destino) {
    int dist[MAX_CIDADES], visitado[MAX_CIDADES], anterior[MAX_CIDADES];
    int i, j, v, count;
    for (i = 0; i < totalCidades; i++) {
        dist[i] = INT_MAX;
        visitado[i] = 0;
        anterior[i] = -1;
    }
    dist[origem] = 0;

    for (count = 0; count < totalCidades - 1; count++) {
        int min = INT_MAX, u = -1;
        for (v = 0; v < totalCidades; v++)
            if (!visitado[v] && dist[v] <= min)
                min = dist[v], u = v;

        if (u == -1) break;
        visitado[u] = 1;

        for (v = 0; v < totalCidades; v++)
            if (!visitado[v] && matriz[u][v] && dist[u] + matriz[u][v] < dist[v]) {
                dist[v] = dist[u] + matriz[u][v];
                anterior[v] = u;
            }
    }

    printf("\nMenor rota de %s para %s: ", cidades[origem], cidades[destino]);
    int caminho[MAX_CIDADES], atual = destino;
    i = 0;
    while (atual != -1)
        caminho[i++] = atual, atual = anterior[atual];
    for (j = i - 1; j >= 0; j--) {
        printf("%s", cidades[caminho[j]]);
        if (j > 0) printf(" -> ");
    }
    printf("\nDistancia total: %d km\n", dist[destino]);
}

void DFSUtil(int v, int visitado[]) {
    visitado[v] = 1;
    printf("%s ", cidades[v]);
    int i;
    for (i = 0; i < totalCidades; i++)
        if (matriz[v][i] && !visitado[i])
            DFSUtil(i, visitado);
}

void buscaEmProfundidade(int origem) {
    int visitado[MAX_CIDADES] = {0};
    printf("Busca a partir de %s: ", cidades[origem]);
    DFSUtil(origem, visitado);
    printf("\n");
}

void menu() {
    int opcao, origem, destino, indice;
    char nome[100];
    do {
        printf("\n--- Menu ---\n");
        printf("1. Inserir cidade\n");
        printf("2. Remover cidade\n");
        printf("3. Mostrar matriz\n");
        printf("4. Menor rota\n");
        printf("5. Busca em profundidade\n");
        printf("6. Listar cidades\n");
        printf("0. Sair\n");
        printf("Escolha: ");
        scanf("%d", &opcao);
        getchar();

        switch (opcao) {
            case 1:
                printf("Nome da nova cidade: ");
                fgets(nome, sizeof(nome), stdin);
                nome[strcspn(nome, "\n")] = '\0';
                inserirCidade(nome);
                break;
            case 2:
                listarCidades();
                printf("Indice da cidade a remover: ");
                scanf("%d", &indice);
                removerCidade(indice);
                break;
            case 3:
                imprimirMatriz();
                break;
            case 4:
                listarCidades();
                printf("Origem: "); scanf("%d", &origem);
                printf("Destino: "); scanf("%d", &destino);
                menorRota(origem, destino);
                break;
            case 5:
                listarCidades();
                printf("Origem: "); scanf("%d", &origem);
                buscaEmProfundidade(origem);
                break;
            case 6:
                listarCidades();
                break;
            case 0:
                liberarGrafo();
                printf("Encerrando...\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 0);
}

int main() {
    inicializarGrafo();
    menu();
    return 0;
}
