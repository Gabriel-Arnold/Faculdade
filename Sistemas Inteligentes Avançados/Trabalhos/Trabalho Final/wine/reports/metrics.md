# Wine Quality - Relatorio

## Pipeline

1. Ler `winequality-red.csv` e `winequality-white.csv`.
2. Unir os dois arquivos em `data/winequality-combined.csv`.
3. Separar atributos e classe, usando `quality` como alvo.
4. Dividir os dados em treino e teste.
5. Treinar tres classificadores.
6. Avaliar acuracia global, acuracia por classe, matriz de confusao e F1-score.
7. Salvar o melhor modelo para inferencia.

## Melhor Modelo

- Modelo: `extra_trees`
- Arquivo salvo: `/Users/gabrielarnold/Downloads/wine/models/melhor_modelo_wine.pkl`
- Acuracia global: `0.6872`
- F1 macro: `0.4162`
- F1 ponderado: `0.6777`

## Comparacao dos Classificadores

| Modelo | Acuracia | F1 macro | F1 ponderado |
|---|---:|---:|---:|
| `random_forest` | 0.6754 | 0.4003 | 0.6646 |
| `extra_trees` | 0.6872 | 0.4162 | 0.6777 |
| `gradient_boosting` | 0.5938 | 0.3323 | 0.5798 |

## Acuracia por Classe

| Classe quality | Acuracia |
|---:|---:|
| 3 | 0.0000 |
| 4 | 0.2000 |
| 5 | 0.6869 |
| 6 | 0.7920 |
| 7 | 0.5864 |
| 8 | 0.3793 |
| 9 | 0.0000 |

## Matriz de Confusao

Linhas representam a classe real; colunas representam a classe prevista.

| Real \ Previsto | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0 | 0 | 6 | 3 | 0 | 0 | 0 |
| 4 | 0 | 13 | 30 | 20 | 2 | 0 | 0 |
| 5 | 0 | 1 | 441 | 196 | 4 | 0 | 0 |
| 6 | 0 | 3 | 121 | 674 | 53 | 0 | 0 |
| 7 | 0 | 0 | 10 | 122 | 190 | 2 | 0 |
| 8 | 0 | 0 | 1 | 13 | 22 | 22 | 0 |
| 9 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
