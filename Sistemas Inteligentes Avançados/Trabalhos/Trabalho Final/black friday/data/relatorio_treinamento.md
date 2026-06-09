# Relatorio de treinamento - Black Friday

Arquivo de dados: `retail_black_friday_sales_100k.csv`

Quantidade de registros: `100000`

Colunas do arquivo: `transaction_id`, `customer_id`, `age_group`, `gender`, `city`, `customer_segment`, `product_id`, `product_category`, `original_price`, `discount_pct`, `final_price`, `quantity`, `purchase_amount`, `payment_method`, `purchase_date`, `purchase_hour`, `is_weekend`, `is_black_friday`, `purchase_day`, `purchase_dayofweek`

## product_category

### Pipeline
1. Abrir o CSV
2. Criar `purchase_day` e `purchase_dayofweek` a partir de `purchase_date`
3. Descartar: `transaction_id`, `customer_id`, `product_id`, `purchase_date`
4. Remover os alvos das colunas de entrada: `product_category`, `payment_method`, `age_group`
5. Usar validacao cruzada estratificada
6. Balancear os dados de treino de cada fold por oversampling
7. Codificar variaveis categoricas com `OneHotEncoder`
8. Normalizar variaveis numericas com `StandardScaler`
9. Hiperparametrizar com `RandomizedSearchCV`
10. Treinar `RandomForestClassifier` com os melhores parametros
11. Avaliar a acuracia e demais metricas com cross validation

### Balanceamento
Frequencia das classes antes do balanceamento:
```text
product_category
Accessories       10156
Beauty             9984
Books             10031
Clothing           9911
Electronics        9974
Footwear          10104
Groceries          9925
Home & Kitchen     9886
Sports             9975
Toys              10054
```

Frequencia das classes depois do balanceamento:
```text
classe_alvo
Accessories       10156
Beauty            10156
Books             10156
Clothing          10156
Electronics       10156
Footwear          10156
Groceries         10156
Home & Kitchen    10156
Sports            10156
Toys              10156
```

### Melhores hiperparametros
```text
{'classificador__n_estimators': 40, 'classificador__min_samples_leaf': 3, 'classificador__max_depth': 16, 'classificador__criterion': 'gini'}
```

### Metricas gerais
- Acuracia global: `0.3261`
- Especificidade media: `0.9251`
- Sensibilidade media: `0.3264`
- F1-score ponderado: `0.3166`

### Matriz de confusao
```text
                Accessories  Beauty  Books  Clothing  Electronics  Footwear  Groceries  Home & Kitchen  Sports  Toys
Accessories            2159     725   2003       886            2      1126        899              41    1517   798
Beauty                   71    1431   4139       988            0       584       1863               3      26   879
Books                     4     176   9043        66            0        28        649               0       1    64
Clothing                118    1231   3148      1500            0      1026       1530               1      78  1279
Electronics             417      98      0       141         5690       227         94            2484     686   137
Footwear                612    1057   2525      1355            2      1694       1367              10     244  1238
Groceries                40    1106   5293       521            0       254       2245               4       9   453
Home & Kitchen          900     298    764       338          311       429        379            4820    1358   289
Sports                 1803     595   1565       693           11       914        707             249    2772   666
Toys                    135    1259   3394      1486            0       936       1511               3      71  1259
```

### Metricas por classe
| Classe | Acuracia | Especificidade | Sensibilidade |
|---|---:|---:|---:|
| Accessories | 0.2126 | 0.9544 | 0.2126 |
| Beauty | 0.1433 | 0.9273 | 0.1433 |
| Books | 0.9015 | 0.7462 | 0.9015 |
| Clothing | 0.1513 | 0.9281 | 0.1513 |
| Electronics | 0.5705 | 0.9964 | 0.5705 |
| Footwear | 0.1677 | 0.9386 | 0.1677 |
| Groceries | 0.2262 | 0.9001 | 0.2262 |
| Home & Kitchen | 0.4876 | 0.969 | 0.4876 |
| Sports | 0.2779 | 0.9557 | 0.2779 |
| Toys | 0.1252 | 0.9355 | 0.1252 |

Modelo salvo em: `modelos_treinados/product_category_modelo.pkl`

## payment_method

### Pipeline
1. Abrir o CSV
2. Criar `purchase_day` e `purchase_dayofweek` a partir de `purchase_date`
3. Descartar: `transaction_id`, `customer_id`, `product_id`, `purchase_date`
4. Remover os alvos das colunas de entrada: `product_category`, `payment_method`, `age_group`
5. Usar validacao cruzada estratificada
6. Balancear os dados de treino de cada fold por oversampling
7. Codificar variaveis categoricas com `OneHotEncoder`
8. Normalizar variaveis numericas com `StandardScaler`
9. Hiperparametrizar com `RandomizedSearchCV`
10. Treinar `RandomForestClassifier` com os melhores parametros
11. Avaliar a acuracia e demais metricas com cross validation

### Balanceamento
Frequencia das classes antes do balanceamento:
```text
payment_method
Cash             16680
Credit Card      16663
Debit Card       16772
Gift Card        16614
Mobile Wallet    16711
PayPal           16560
```

Frequencia das classes depois do balanceamento:
```text
classe_alvo
Cash             16772
Credit Card      16772
Debit Card       16772
Gift Card        16772
Mobile Wallet    16772
PayPal           16772
```

### Melhores hiperparametros
```text
{'classificador__n_estimators': 40, 'classificador__min_samples_leaf': 3, 'classificador__max_depth': 16, 'classificador__criterion': 'gini'}
```

### Metricas gerais
- Acuracia global: `0.1662`
- Especificidade media: `0.8332`
- Sensibilidade media: `0.1662`
- F1-score ponderado: `0.1662`

### Matriz de confusao
```text
               Cash  Credit Card  Debit Card  Gift Card  Mobile Wallet  PayPal
Cash           2932         2756        2810       2775           2656    2751
Credit Card    2847         2702        2883       2682           2767    2782
Debit Card     2850         2760        2893       2643           2816    2810
Gift Card      2827         2687        2936       2675           2767    2722
Mobile Wallet  2906         2769        2857       2706           2681    2792
PayPal         2869         2730        2818       2643           2760    2740
```

### Metricas por classe
| Classe | Acuracia | Especificidade | Sensibilidade |
|---|---:|---:|---:|
| Cash | 0.1758 | 0.8284 | 0.1758 |
| Credit Card | 0.1622 | 0.8356 | 0.1622 |
| Debit Card | 0.1725 | 0.8281 | 0.1725 |
| Gift Card | 0.161 | 0.8387 | 0.161 |
| Mobile Wallet | 0.1604 | 0.8347 | 0.1604 |
| PayPal | 0.1655 | 0.8339 | 0.1655 |

Modelo salvo em: `modelos_treinados/payment_method_modelo.pkl`

## age_group

### Pipeline
1. Abrir o CSV
2. Criar `purchase_day` e `purchase_dayofweek` a partir de `purchase_date`
3. Descartar: `transaction_id`, `customer_id`, `product_id`, `purchase_date`
4. Remover os alvos das colunas de entrada: `product_category`, `payment_method`, `age_group`
5. Usar validacao cruzada estratificada
6. Balancear os dados de treino de cada fold por oversampling
7. Codificar variaveis categoricas com `OneHotEncoder`
8. Normalizar variaveis numericas com `StandardScaler`
9. Hiperparametrizar com `RandomizedSearchCV`
10. Treinar `RandomForestClassifier` com os melhores parametros
11. Avaliar a acuracia e demais metricas com cross validation

### Balanceamento
Frequencia das classes antes do balanceamento:
```text
age_group
18-25    19974
26-35    19960
36-45    20145
46-55    20014
56+      19907
```

Frequencia das classes depois do balanceamento:
```text
classe_alvo
18-25    20145
26-35    20145
36-45    20145
46-55    20145
56+      20145
```

### Melhores hiperparametros
```text
{'classificador__n_estimators': 40, 'classificador__min_samples_leaf': 3, 'classificador__max_depth': 16, 'classificador__criterion': 'gini'}
```

### Metricas gerais
- Acuracia global: `0.2002`
- Especificidade media: `0.8001`
- Sensibilidade media: `0.2002`
- F1-score ponderado: `0.2002`

### Matriz de confusao
```text
       18-25  26-35  36-45  46-55   56+
18-25   3891   4122   4019   3936  4006
26-35   3991   4174   3900   3921  3974
36-45   3950   4217   4033   3972  3973
46-55   3975   4146   3983   3893  4017
56+     3989   4063   3882   3943  4030
```

### Metricas por classe
| Classe | Acuracia | Especificidade | Sensibilidade |
|---|---:|---:|---:|
| 18-25 | 0.1948 | 0.8013 | 0.1948 |
| 26-35 | 0.2091 | 0.7933 | 0.2091 |
| 36-45 | 0.2002 | 0.8023 | 0.2002 |
| 46-55 | 0.1945 | 0.8028 | 0.1945 |
| 56+ | 0.2024 | 0.8006 | 0.2024 |

Modelo salvo em: `modelos_treinados/age_group_modelo.pkl`
