# Wine Quality - Relatorio

## Melhor Modelo

- Modelo: `extra_trees`
- Arquivo salvo: `/Users/gabrielarnold/GitHub/Faculdade/Sistemas Inteligentes Avançados/Trabalhos/Trabalho Final/wine/models/melhor_modelo_wine.pkl`
- Acuracia global: `0.6869`
- F1 macro: `0.4103`
- F1 ponderado: `0.6803`
- Melhores parametros: `{'classificador__n_estimators': 100, 'classificador__min_samples_split': 5, 'classificador__max_features': 'sqrt', 'classificador__max_depth': 30}`

## Comparacao dos Classificadores

| Modelo | Acuracia | F1 macro | F1 ponderado |
|---|---:|---:|---:|
| `random_forest` | 0.6745 | 0.4090 | 0.6702 |
| `extra_trees` | 0.6869 | 0.4103 | 0.6803 |
| `gradient_boosting` | 0.4096 | 0.2584 | 0.4330 |

## Acuracia por Classe

| Classe quality | Acuracia |
|---:|---:|
| 3 | 0.0000 |
| 4 | 0.2269 |
| 5 | 0.7413 |
| 6 | 0.7398 |
| 7 | 0.6070 |
| 8 | 0.3938 |
| 9 | 0.0000 |

## Matriz de Confusao

Linhas representam a classe real; colunas representam a classe prevista.

| Real \ Previsto | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0 | 5 | 13 | 12 | 0 | 0 | 0 |
| 4 | 6 | 49 | 103 | 55 | 3 | 0 | 0 |
| 5 | 1 | 34 | 1585 | 491 | 26 | 1 | 0 |
| 6 | 1 | 19 | 453 | 2098 | 258 | 7 | 0 |
| 7 | 0 | 1 | 20 | 376 | 655 | 27 | 0 |
| 8 | 0 | 0 | 2 | 47 | 68 | 76 | 0 |
| 9 | 0 | 0 | 1 | 0 | 4 | 0 | 0 |
