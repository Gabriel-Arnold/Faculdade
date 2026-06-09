# Relatorio de inferencia - Black Friday

## Nova venda usada na demonstracao

```text
transaction_id customer_id age_group gender     city customer_segment product_id product_category  original_price  discount_pct  final_price  quantity  purchase_amount payment_method purchase_date  purchase_hour  is_weekend  is_black_friday  purchase_day  purchase_dayofweek
     T_EXEMPLO   C_EXEMPLO     26-35 Female New York        Returning  P_EXEMPLO      Electronics           499.9            35       324.94         1           324.94    Credit Card    2025-11-28             18           0                1            28                   4
```

## Indicacao para product_category

- Classe mais provavel: `Sports`
- Grau de certeza: `50.78%`

### Scores por classe
| Classe | Score |
|---|---:|
| Accessories | 25.86% |
| Beauty | 0.0% |
| Books | 0.0% |
| Clothing | 0.0% |
| Electronics | 5.26% |
| Footwear | 0.27% |
| Groceries | 0.0% |
| Home & Kitchen | 17.83% |
| Sports | 50.78% |
| Toys | 0.0% |

## Indicacao para payment_method

- Classe mais provavel: `PayPal`
- Grau de certeza: `19.67%`

### Scores por classe
| Classe | Score |
|---|---:|
| Cash | 15.45% |
| Credit Card | 17.16% |
| Debit Card | 17.9% |
| Gift Card | 14.6% |
| Mobile Wallet | 15.22% |
| PayPal | 19.67% |

## Indicacao para age_group

- Classe mais provavel: `56+`
- Grau de certeza: `27.05%`

### Scores por classe
| Classe | Score |
|---|---:|
| 18-25 | 19.36% |
| 26-35 | 16.74% |
| 36-45 | 19.67% |
| 46-55 | 17.19% |
| 56+ | 27.05% |
