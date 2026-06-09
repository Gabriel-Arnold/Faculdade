# Relatorio de inferencia - Black Friday

## Nova venda usada na demonstracao

```text
transaction_id customer_id age_group gender     city customer_segment product_id product_category  original_price  discount_pct  final_price  quantity  purchase_amount payment_method purchase_date  purchase_hour  is_weekend  is_black_friday  purchase_day  purchase_dayofweek
     T_EXEMPLO   C_EXEMPLO     26-35 Female New York        Returning  P_EXEMPLO      Electronics           499.9            35       324.94         1           324.94    Credit Card    2025-11-28             18           0                1            28                   4
```

## Indicacao para product_category

- Classe mais provavel: `Sports`
- Grau de certeza: `38.9%`

### Scores por classe
| Classe | Score |
|---|---:|
| Accessories | 30.35% |
| Beauty | 0.19% |
| Books | 0.0% |
| Clothing | 0.19% |
| Electronics | 8.46% |
| Footwear | 0.96% |
| Groceries | 0.2% |
| Home & Kitchen | 20.54% |
| Sports | 38.9% |
| Toys | 0.21% |

## Indicacao para payment_method

- Classe mais provavel: `Mobile Wallet`
- Grau de certeza: `17.42%`

### Scores por classe
| Classe | Score |
|---|---:|
| Cash | 17.41% |
| Credit Card | 16.1% |
| Debit Card | 16.61% |
| Gift Card | 15.53% |
| Mobile Wallet | 17.42% |
| PayPal | 16.92% |

## Indicacao para age_group

- Classe mais provavel: `56+`
- Grau de certeza: `21.45%`

### Scores por classe
| Classe | Score |
|---|---:|
| 18-25 | 20.81% |
| 26-35 | 20.78% |
| 36-45 | 19.92% |
| 46-55 | 17.04% |
| 56+ | 21.45% |
