import os
import sys
from pickle import load

if os.path.isdir('.python_libs'):
    sys.path.insert(0, '.python_libs')

import pandas as pd


PASTA_MODELOS = 'modelos_treinados'
PASTA_DATA = 'data'
ALVOS = [
    'product_category',
    'payment_method',
    'age_group',
]


def preparar_nova_venda(venda):
    venda = venda.copy()
    venda['purchase_date'] = pd.to_datetime(venda['purchase_date'])
    venda['purchase_day'] = venda['purchase_date'].dt.day
    venda['purchase_dayofweek'] = venda['purchase_date'].dt.dayofweek
    return venda


nova_venda = pd.DataFrame([{
    'transaction_id': 'T_EXEMPLO',
    'customer_id': 'C_EXEMPLO',
    'age_group': '26-35',
    'gender': 'Female',
    'city': 'New York',
    'customer_segment': 'Returning',
    'product_id': 'P_EXEMPLO',
    'product_category': 'Electronics',
    'original_price': 499.90,
    'discount_pct': 35,
    'final_price': 324.94,
    'quantity': 1,
    'purchase_amount': 324.94,
    'payment_method': 'Credit Card',
    'purchase_date': '2025-11-28',
    'purchase_hour': 18,
    'is_weekend': 0,
    'is_black_friday': 1,
}])

nova_venda = preparar_nova_venda(nova_venda)

relatorio = [
    '# Relatorio de inferencia - Black Friday',
    '',
    '## Nova venda usada na demonstracao',
    '',
    '```text',
    nova_venda.to_string(index=False),
    '```',
    '',
]

for alvo in ALVOS:
    caminho_modelo = os.path.join(PASTA_MODELOS, alvo + '_modelo.pkl')
    pacote = load(open(caminho_modelo, 'rb'))
    modelo = pacote['modelo']
    colunas_atributos = pacote['colunas_atributos']

    venda_atributos = nova_venda[colunas_atributos]
    classe_predita = modelo.predict(venda_atributos)[0]
    probabilidades = modelo.predict_proba(venda_atributos)[0]
    classes = modelo.named_steps['classificador'].classes_
    certeza = probabilidades.max() * 100

    print('\nIndicação para', alvo)
    print('Classe mais provável:', classe_predita)
    print('Grau de certeza:', round(certeza, 2), '%')
    print('Scores por classe:')

    relatorio.extend([
        '## Indicacao para ' + alvo,
        '',
        '- Classe mais provavel: `' + str(classe_predita) + '`',
        '- Grau de certeza: `' + str(round(certeza, 2)) + '%`',
        '',
        '### Scores por classe',
        '| Classe | Score |',
        '|---|---:|',
    ])

    for nome_classe, score in zip(classes, probabilidades):
        print(nome_classe, ':', round(score * 100, 2), '%')
        relatorio.append('| ' + str(nome_classe) + ' | ' + str(round(score * 100, 2)) + '% |')

    relatorio.append('')

os.makedirs(PASTA_DATA, exist_ok=True)
caminho_relatorio = os.path.join(PASTA_DATA, 'relatorio_inferencia.md')
with open(caminho_relatorio, 'w', encoding='utf-8') as arquivo:
    arquivo.write('\n'.join(relatorio))

print('\nRelatorio de inferencia salvo em:', caminho_relatorio)
