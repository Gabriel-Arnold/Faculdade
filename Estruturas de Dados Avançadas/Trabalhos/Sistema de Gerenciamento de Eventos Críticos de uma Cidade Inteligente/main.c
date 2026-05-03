#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef enum {
    ACIDENTE_TRANSITO = 1,
    FALHA_SEMAFORO,
    INTERRUPCAO_ENERGIA,
    ALAGAMENTO,
    INCENDIO
} TipoEvento;

typedef enum {
    ATIVO = 1,
    RESOLVIDO = 2
} StatusEvento;

typedef struct {
    int dia;
    int mes;
    int ano;
    int hora;
    int minuto;
} DataHora;

typedef struct Evento {
    int id;
    TipoEvento tipo;
    int severidade;
    DataHora registro;
    char regiao[80];
    StatusEvento status;
    int altura;
    struct Evento *esq;
    struct Evento *dir;
} Evento;

typedef struct {
    int totalRotacoes;
} MetricasGlobais;

MetricasGlobais metricas = {0};

int maximo(int a, int b) {
    return (a > b) ? a : b;
}

int altura(Evento *no) {
    return no ? no->altura : 0;
}

int fatorBalanceamento(Evento *no) {
    return no ? altura(no->esq) - altura(no->dir) : 0;
}

void atualizarAltura(Evento *no) {
    if (no) {
        no->altura = 1 + maximo(altura(no->esq), altura(no->dir));
    }
}

const char *tipoParaTexto(TipoEvento tipo) {
    switch (tipo) {
        case ACIDENTE_TRANSITO: return "Acidente de transito";
        case FALHA_SEMAFORO: return "Falha em semaforo";
        case INTERRUPCAO_ENERGIA: return "Interrupcao de energia";
        case ALAGAMENTO: return "Alagamento";
        case INCENDIO: return "Incendio";
        default: return "Desconhecido";
    }
}

const char *statusParaTexto(StatusEvento status) {
    return status == ATIVO ? "Ativo" : "Resolvido";
}

Evento *rotacaoDireita(Evento *y) {
    Evento *x = y->esq;
    Evento *t2 = x->dir;

    x->dir = y;
    y->esq = t2;

    atualizarAltura(y);
    atualizarAltura(x);

    metricas.totalRotacoes++;
    return x;
}

Evento *rotacaoEsquerda(Evento *x) {
    Evento *y = x->dir;
    Evento *t2 = y->esq;

    y->esq = x;
    x->dir = t2;

    atualizarAltura(x);
    atualizarAltura(y);

    metricas.totalRotacoes++;
    return y;
}

Evento *balancear(Evento *no) {
    if (!no) return no;

    atualizarAltura(no);
    int fb = fatorBalanceamento(no);

    if (fb > 1 && fatorBalanceamento(no->esq) >= 0) {
        return rotacaoDireita(no);
    }

    if (fb > 1 && fatorBalanceamento(no->esq) < 0) {
        no->esq = rotacaoEsquerda(no->esq);
        return rotacaoDireita(no);
    }

    if (fb < -1 && fatorBalanceamento(no->dir) <= 0) {
        return rotacaoEsquerda(no);
    }

    if (fb < -1 && fatorBalanceamento(no->dir) > 0) {
        no->dir = rotacaoDireita(no->dir);
        return rotacaoEsquerda(no);
    }

    return no;
}

Evento *criarEvento(int id, TipoEvento tipo, int severidade, DataHora registro, const char *regiao) {
    Evento *novo = (Evento *)malloc(sizeof(Evento));
    if (!novo) {
        printf("Erro: falha ao alocar memoria.\n");
        exit(1);
    }

    novo->id = id;
    novo->tipo = tipo;
    novo->severidade = severidade;
    novo->registro = registro;
    strncpy(novo->regiao, regiao, sizeof(novo->regiao) - 1);
    novo->regiao[sizeof(novo->regiao) - 1] = '\0';
    novo->status = ATIVO;
    novo->altura = 1;
    novo->esq = NULL;
    novo->dir = NULL;
    return novo;
}

Evento *buscarEvento(Evento *raiz, int id) {
    if (!raiz || raiz->id == id) return raiz;
    if (id < raiz->id) return buscarEvento(raiz->esq, id);
    return buscarEvento(raiz->dir, id);
}

Evento *inserirEvento(Evento *raiz, Evento *novo, int *sucesso) {
    if (!raiz) {
        *sucesso = 1;
        return novo;
    }

    if (novo->id < raiz->id) {
        raiz->esq = inserirEvento(raiz->esq, novo, sucesso);
    } else if (novo->id > raiz->id) {
        raiz->dir = inserirEvento(raiz->dir, novo, sucesso);
    } else {
        printf("Erro: ja existe um evento com o ID %d.\n", novo->id);
        free(novo);
        *sucesso = 0;
        return raiz;
    }

    return balancear(raiz);
}

Evento *menorNo(Evento *no) {
    Evento *atual = no;
    while (atual && atual->esq) atual = atual->esq;
    return atual;
}

void copiarDadosEvento(Evento *destino, Evento *origem) {
    destino->id = origem->id;
    destino->tipo = origem->tipo;
    destino->severidade = origem->severidade;
    destino->registro = origem->registro;
    strcpy(destino->regiao, origem->regiao);
    destino->status = origem->status;
}

Evento *removerEvento(Evento *raiz, int id, int *sucesso) {
    if (!raiz) {
        printf("Evento nao encontrado.\n");
        *sucesso = 0;
        return NULL;
    }

    if (id < raiz->id) {
        raiz->esq = removerEvento(raiz->esq, id, sucesso);
    } else if (id > raiz->id) {
        raiz->dir = removerEvento(raiz->dir, id, sucesso);
    } else {
        if (raiz->status != RESOLVIDO) {
            printf("Erro: apenas eventos com status Resolvido podem ser removidos.\n");
            *sucesso = 0;
            return raiz;
        }

        if (!raiz->esq || !raiz->dir) {
            Evento *temp = raiz->esq ? raiz->esq : raiz->dir;
            free(raiz);
            *sucesso = 1;
            return temp;
        } else {
            Evento *temp = menorNo(raiz->dir);
            copiarDadosEvento(raiz, temp);
            raiz->dir = removerEvento(raiz->dir, temp->id, sucesso);
        }
    }

    return balancear(raiz);
}

void exibirEvento(Evento *e) {
    if (!e) return;
    printf("ID: %d | Tipo: %s | Severidade: %d | Registro: %02d/%02d/%04d %02d:%02d | Regiao: %s | Status: %s\n",
           e->id,
           tipoParaTexto(e->tipo),
           e->severidade,
           e->registro.dia,
           e->registro.mes,
           e->registro.ano,
           e->registro.hora,
           e->registro.minuto,
           e->regiao,
           statusParaTexto(e->status));
}

void listarEmOrdem(Evento *raiz) {
    if (!raiz) return;
    listarEmOrdem(raiz->esq);
    exibirEvento(raiz);
    listarEmOrdem(raiz->dir);
}

void listarAtivosPorSeveridade(Evento *raiz, int min, int max, int *encontrou) {
    if (!raiz) return;

    listarAtivosPorSeveridade(raiz->esq, min, max, encontrou);

    if (raiz->status == ATIVO && raiz->severidade >= min && raiz->severidade <= max) {
        exibirEvento(raiz);
        *encontrou = 1;
    }

    listarAtivosPorSeveridade(raiz->dir, min, max, encontrou);
}

int compararTextoIgnorandoCaixa(const char *a, const char *b) {
    while (*a && *b) {
        if (tolower((unsigned char)*a) != tolower((unsigned char)*b)) return 0;
        a++;
        b++;
    }
    return *a == *b;
}

void relatorioPorRegiao(Evento *raiz, const char *regiao, int *encontrou) {
    if (!raiz) return;

    relatorioPorRegiao(raiz->esq, regiao, encontrou);

    if (raiz->status == ATIVO && compararTextoIgnorandoCaixa(raiz->regiao, regiao)) {
        exibirEvento(raiz);
        *encontrou = 1;
    }

    relatorioPorRegiao(raiz->dir, regiao, encontrou);
}

void buscarIntervaloID(Evento *raiz, int min, int max, int *encontrou) {
    if (!raiz) return;

    if (raiz->id > min) buscarIntervaloID(raiz->esq, min, max, encontrou);

    if (raiz->id >= min && raiz->id <= max) {
        exibirEvento(raiz);
        *encontrou = 1;
    }

    if (raiz->id < max) buscarIntervaloID(raiz->dir, min, max, encontrou);
}

int contarNos(Evento *raiz) {
    if (!raiz) return 0;
    return 1 + contarNos(raiz->esq) + contarNos(raiz->dir);
}

int contarAtivos(Evento *raiz) {
    if (!raiz) return 0;
    return (raiz->status == ATIVO ? 1 : 0) + contarAtivos(raiz->esq) + contarAtivos(raiz->dir);
}

int somaFatoresAbsolutos(Evento *raiz) {
    if (!raiz) return 0;
    int fb = fatorBalanceamento(raiz);
    if (fb < 0) fb = -fb;
    return fb + somaFatoresAbsolutos(raiz->esq) + somaFatoresAbsolutos(raiz->dir);
}

double fatorBalanceamentoMedio(Evento *raiz) {
    int total = contarNos(raiz);
    if (total == 0) return 0.0;
    return (double)somaFatoresAbsolutos(raiz) / total;
}

void alterarStatus(Evento *raiz, int id) {
    Evento *e = buscarEvento(raiz, id);
    if (!e) {
        printf("Evento nao encontrado.\n");
        return;
    }

    if (e->status == RESOLVIDO) {
        printf("Evento ja esta resolvido.\n");
        return;
    }

    e->status = RESOLVIDO;
    printf("Status alterado para Resolvido.\n");
}

void atualizarSeveridade(Evento *raiz, int id, int novaSeveridade) {
    Evento *e = buscarEvento(raiz, id);
    if (!e) {
        printf("Evento nao encontrado.\n");
        return;
    }

    if (e->status != ATIVO) {
        printf("Erro: apenas eventos ativos podem ter a severidade atualizada.\n");
        return;
    }

    e->severidade = novaSeveridade;
    printf("Severidade atualizada com sucesso.\n");
}

void liberarArvore(Evento *raiz) {
    if (!raiz) return;
    liberarArvore(raiz->esq);
    liberarArvore(raiz->dir);
    free(raiz);
}

int lerInteiro(const char *mensagem, int min, int max) {
    int valor;
    char linha[100];

    while (1) {
        printf("%s", mensagem);
        if (!fgets(linha, sizeof(linha), stdin)) continue;
        if (sscanf(linha, "%d", &valor) == 1 && valor >= min && valor <= max) {
            return valor;
        }
        printf("Entrada invalida. Digite um numero entre %d e %d.\n", min, max);
    }
}

void lerTexto(const char *mensagem, char *destino, int tamanho) {
    printf("%s", mensagem);
    if (fgets(destino, tamanho, stdin)) {
        destino[strcspn(destino, "\n")] = '\0';
    }
}

DataHora lerDataHora() {
    DataHora dh;
    dh.dia = lerInteiro("Dia: ", 1, 31);
    dh.mes = lerInteiro("Mes: ", 1, 12);
    dh.ano = lerInteiro("Ano: ", 2000, 2100);
    dh.hora = lerInteiro("Hora: ", 0, 23);
    dh.minuto = lerInteiro("Minuto: ", 0, 59);
    return dh;
}

TipoEvento lerTipoEvento() {
    printf("\nTipos de evento:\n");
    printf("1 - Acidente de transito\n");
    printf("2 - Falha em semaforo\n");
    printf("3 - Interrupcao de energia\n");
    printf("4 - Alagamento\n");
    printf("5 - Incendio\n");
    return (TipoEvento)lerInteiro("Escolha o tipo: ", 1, 5);
}

void menuCadastros(Evento **raiz) {
    int opcao;
    do {
        printf("\n=== CADASTROS E ATUALIZACOES ===\n");
        printf("1 - Inserir evento\n");
        printf("2 - Alterar status para Resolvido\n");
        printf("3 - Atualizar severidade de evento ativo\n");
        printf("4 - Remover evento resolvido\n");
        printf("0 - Voltar\n");
        opcao = lerInteiro("Opcao: ", 0, 4);

        if (opcao == 1) {
            int id = lerInteiro("ID do evento: ", 1, 999999);
            TipoEvento tipo = lerTipoEvento();
            int severidade = lerInteiro("Severidade (1 a 5): ", 1, 5);
            printf("Data e hora do registro:\n");
            DataHora dh = lerDataHora();
            char regiao[80];
            lerTexto("Regiao da cidade: ", regiao, sizeof(regiao));

            int sucesso = 0;
            Evento *novo = criarEvento(id, tipo, severidade, dh, regiao);
            *raiz = inserirEvento(*raiz, novo, &sucesso);
            if (sucesso) printf("Evento inserido com sucesso.\n");
        } else if (opcao == 2) {
            int id = lerInteiro("ID do evento: ", 1, 999999);
            alterarStatus(*raiz, id);
        } else if (opcao == 3) {
            int id = lerInteiro("ID do evento: ", 1, 999999);
            int sev = lerInteiro("Nova severidade (1 a 5): ", 1, 5);
            atualizarSeveridade(*raiz, id, sev);
        } else if (opcao == 4) {
            int id = lerInteiro("ID do evento: ", 1, 999999);
            int sucesso = 0;
            *raiz = removerEvento(*raiz, id, &sucesso);
            if (sucesso) printf("Evento removido com sucesso.\n");
        }
    } while (opcao != 0);
}

void menuConsultas(Evento *raiz) {
    int opcao;
    do {
        printf("\n=== CONSULTAS ===\n");
        printf("1 - Buscar evento por ID\n");
        printf("2 - Listar eventos ativos por intervalo de severidade\n");
        printf("3 - Relatorio de eventos ativos por regiao\n");
        printf("4 - Buscar eventos por intervalo de ID\n");
        printf("5 - Listar todos em ordem de ID\n");
        printf("0 - Voltar\n");
        opcao = lerInteiro("Opcao: ", 0, 5);

        if (opcao == 1) {
            int id = lerInteiro("ID do evento: ", 1, 999999);
            Evento *e = buscarEvento(raiz, id);
            if (e) exibirEvento(e);
            else printf("Evento nao encontrado.\n");
        } else if (opcao == 2) {
            int min = lerInteiro("Severidade minima: ", 1, 5);
            int max = lerInteiro("Severidade maxima: ", min, 5);
            int encontrou = 0;
            listarAtivosPorSeveridade(raiz, min, max, &encontrou);
            if (!encontrou) printf("Nenhum evento ativo encontrado nesse intervalo.\n");
        } else if (opcao == 3) {
            char regiao[80];
            int encontrou = 0;
            lerTexto("Regiao: ", regiao, sizeof(regiao));
            relatorioPorRegiao(raiz, regiao, &encontrou);
            if (!encontrou) printf("Nenhum evento ativo encontrado para essa regiao.\n");
        } else if (opcao == 4) {
            int min = lerInteiro("ID inicial: ", 1, 999999);
            int max = lerInteiro("ID final: ", min, 999999);
            int encontrou = 0;
            buscarIntervaloID(raiz, min, max, &encontrou);
            if (!encontrou) printf("Nenhum evento encontrado nesse intervalo.\n");
        } else if (opcao == 5) {
            if (!raiz) printf("Arvore vazia.\n");
            else listarEmOrdem(raiz);
        }
    } while (opcao != 0);
}

void exibirMetricas(Evento *raiz) {
    printf("\n=== METRICAS DA ARVORE ===\n");
    printf("Altura total da arvore: %d\n", altura(raiz));
    printf("Numero total de nos: %d\n", contarNos(raiz));
    printf("Numero de eventos ativos: %d\n", contarAtivos(raiz));
    printf("Fator de balanceamento medio absoluto: %.2f\n", fatorBalanceamentoMedio(raiz));
    printf("Quantidade total de rotacoes realizadas: %d\n", metricas.totalRotacoes);
}

void carregarExemplos(Evento **raiz) {
    int ids[] = {50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55};
    TipoEvento tipos[] = {ACIDENTE_TRANSITO, INCENDIO, ALAGAMENTO, FALHA_SEMAFORO, INTERRUPCAO_ENERGIA, INCENDIO, ALAGAMENTO, ACIDENTE_TRANSITO, FALHA_SEMAFORO, INTERRUPCAO_ENERGIA, ALAGAMENTO, INCENDIO};
    int severidades[] = {4, 5, 3, 2, 4, 5, 3, 1, 2, 4, 5, 3};
    const char *regioes[] = {"Centro", "Norte", "Sul", "Centro", "Leste", "Oeste", "Sul", "Norte", "Centro", "Leste", "Oeste", "Centro"};
    int total = 12;

    for (int i = 0; i < total; i++) {
        DataHora dh = {1 + i, 5, 2026, 8 + (i % 10), 15};
        int sucesso = 0;
        Evento *novo = criarEvento(ids[i], tipos[i], severidades[i], dh, regioes[i]);
        *raiz = inserirEvento(*raiz, novo, &sucesso);
    }
    printf("Eventos de exemplo carregados.\n");
}

int main() {
    Evento *raiz = NULL;
    int opcao;

    do {
        printf("\n===============================================\n");
        printf(" SISTEMA DE EVENTOS CRITICOS - CIDADE INTELIGENTE\n");
        printf("===============================================\n");
        printf("1 - Cadastros e atualizacoes\n");
        printf("2 - Consultas e relatorios\n");
        printf("3 - Metricas da arvore AVL\n");
        printf("4 - Carregar eventos de exemplo\n");
        printf("0 - Sair\n");
        opcao = lerInteiro("Opcao: ", 0, 4);

        switch (opcao) {
            case 1:
                menuCadastros(&raiz);
                break;
            case 2:
                menuConsultas(raiz);
                break;
            case 3:
                exibirMetricas(raiz);
                break;
            case 4:
                carregarExemplos(&raiz);
                break;
            case 0:
                printf("Encerrando sistema...\n");
                break;
        }
    } while (opcao != 0);

    liberarArvore(raiz);
    return 0;
}
