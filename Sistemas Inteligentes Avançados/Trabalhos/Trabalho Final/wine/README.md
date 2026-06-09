# Wine Quality

Sistema em Python para treinar classificadores no dataset Wine Quality da UCI.

## Arquivos de entrada

- `winequality-red.csv`: dados dos vinhos tintos.
- `winequality-white.csv`: dados dos vinhos brancos.
- `winequality.names`: descricao e nomes das colunas.

## Treinamento

```bash
.venv/bin/python train.py
```

O treinamento:

1. une tintos e brancos em `data/winequality-combined.csv`;
2. usa `quality` como classe;
3. avalia os modelos com validacao cruzada estratificada;
4. normaliza os atributos com `StandardScaler`;
5. balanceia as classes com `SMOTE`;
6. hiperparametriza com `RandomizedSearchCV`;
7. treina `random_forest`, `extra_trees` e `gradient_boosting`;
8. compara acuracia global e F1-score;
9. salva o melhor modelo em `models/melhor_modelo_wine.pkl`;
10. gera `reports/metrics.md` com pipeline, acuracia por classe e matriz de confusao.

## Inferencia

```bash
.venv/bin/python predict.py --json '{"fixed acidity":7.4,"volatile acidity":0.7,"citric acid":0,"residual sugar":1.9,"chlorides":0.076,"free sulfur dioxide":11,"total sulfur dioxide":34,"density":0.9978,"pH":3.51,"sulphates":0.56,"alcohol":9.4}'
```
