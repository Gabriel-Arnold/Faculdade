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
5. Codificar variaveis categoricas com `OneHotEncoder`
6. Treinar `RandomForestClassifier`

### Metricas gerais
- Acuracia global: `0.339`
- F1-score ponderado: `0.3252`

### Matriz de confusao
```text
                Accessories  Beauty  Books  Clothing  Electronics  Footwear  Groceries  Home & Kitchen  Sports  Toys
Accessories             673     165    621       323            0       421        313               0     339   192
Beauty                    2     328   1330       382            0       114        653               0       0   186
Books                     0       6   2952         0            0         0         50               0       0     1
Clothing                  7     234   1068       519            0       294        568               0       2   281
Electronics             130      14      0        55         1676        75         31             759     227    25
Footwear                154     215    850       493            0       533        487               1      32   266
Groceries                 1     239   1744       106            0        15        802               0       0    71
Home & Kitchen          285      54    241       112           24       123        130            1572     361    64
Sports                  563     123    486       276            0       277        279              16     847   126
Toys                      7     292   1144       526            0       288        488               0       4   267
```

### Metricas por classe
| Classe | Acuracia | Especificidade | Sensibilidade |
|---|---:|---:|---:|
| Accessories | 0.2209 | 0.9574 | 0.2209 |
| Beauty | 0.1095 | 0.9503 | 0.1095 |
| Books | 0.9811 | 0.7227 | 0.9811 |
| Clothing | 0.1746 | 0.9159 | 0.1746 |
| Electronics | 0.5602 | 0.9991 | 0.5602 |
| Footwear | 0.1758 | 0.9404 | 0.1758 |
| Groceries | 0.2693 | 0.889 | 0.2693 |
| Home & Kitchen | 0.53 | 0.9713 | 0.53 |
| Sports | 0.283 | 0.9643 | 0.283 |
| Toys | 0.0885 | 0.9551 | 0.0885 |

Modelo salvo em: `modelos_treinados/product_category_modelo.pkl`

## payment_method

### Pipeline
1. Abrir o CSV
2. Criar `purchase_day` e `purchase_dayofweek` a partir de `purchase_date`
3. Descartar: `transaction_id`, `customer_id`, `product_id`, `purchase_date`
4. Remover os alvos das colunas de entrada: `product_category`, `payment_method`, `age_group`
5. Codificar variaveis categoricas com `OneHotEncoder`
6. Treinar `RandomForestClassifier`

### Metricas gerais
- Acuracia global: `0.172`
- F1-score ponderado: `0.1718`

### Matriz de confusao
```text
               Cash  Credit Card  Debit Card  Gift Card  Mobile Wallet  PayPal
Cash            857          858         750        875            750     914
Credit Card     839          866         764        881            772     877
Debit Card      827          825         787        948            730     915
Gift Card       832          811         754        941            743     903
Mobile Wallet   794          884         781        877            789     888
PayPal          792          872         757        880            746     921
```

### Metricas por classe
| Classe | Acuracia | Especificidade | Sensibilidade |
|---|---:|---:|---:|
| Cash | 0.1713 | 0.8366 | 0.1713 |
| Credit Card | 0.1732 | 0.83 | 0.1732 |
| Debit Card | 0.1564 | 0.8476 | 0.1564 |
| Gift Card | 0.1888 | 0.8217 | 0.1888 |
| Mobile Wallet | 0.1574 | 0.8503 | 0.1574 |
| PayPal | 0.1854 | 0.8203 | 0.1854 |

Modelo salvo em: `modelos_treinados/payment_method_modelo.pkl`

## age_group

### Pipeline
1. Abrir o CSV
2. Criar `purchase_day` e `purchase_dayofweek` a partir de `purchase_date`
3. Descartar: `transaction_id`, `customer_id`, `product_id`, `purchase_date`
4. Remover os alvos das colunas de entrada: `product_category`, `payment_method`, `age_group`
5. Codificar variaveis categoricas com `OneHotEncoder`
6. Treinar `RandomForestClassifier`

### Metricas gerais
- Acuracia global: `0.202`
- F1-score ponderado: `0.2018`

### Matriz de confusao
```text
       18-25  26-35  36-45  46-55   56+
18-25   1237   1215   1157   1082  1301
26-35   1173   1273   1145   1151  1246
36-45   1215   1285   1124   1129  1291
46-55   1221   1236   1110   1133  1304
56+     1160   1283   1139   1097  1293
```

### Metricas por classe
| Classe | Acuracia | Especificidade | Sensibilidade |
|---|---:|---:|---:|
| 18-25 | 0.2064 | 0.8014 | 0.2064 |
| 26-35 | 0.2126 | 0.791 | 0.2126 |
| 36-45 | 0.186 | 0.81 | 0.186 |
| 46-55 | 0.1887 | 0.8142 | 0.1887 |
| 56+ | 0.2165 | 0.786 | 0.2165 |

Modelo salvo em: `modelos_treinados/age_group_modelo.pkl`
