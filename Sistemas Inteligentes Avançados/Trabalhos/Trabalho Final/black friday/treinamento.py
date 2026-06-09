import os
import sys
from pickle import dump

if os.path.isdir('.python_libs'):
    sys.path.insert(0, '.python_libs')

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

ARQUIVO_DADOS = 'retail_black_friday_sales_100k.csv'
PASTA_MODELOS = 'modelos_treinados'
PASTA_DATA = 'data'

ALVOS = [
    'product_category',
    'payment_method',
    'age_group',
]

COLUNAS_DESCARTADAS = [
    'transaction_id',  # identificador unico da transacao
    'customer_id',     # identificador de cliente com muitos valores distintos
    'product_id',      # identificador de produto com muitos valores distintos
    'purchase_date',   # substituida por informacoes numericas da data
]


def preparar_dados(dados):
    dados = dados.copy()
    dados['purchase_date'] = pd.to_datetime(dados['purchase_date'])
    dados['purchase_day'] = dados['purchase_date'].dt.day
    dados['purchase_dayofweek'] = dados['purchase_date'].dt.dayofweek
    return dados


def calcular_metricas(classe_real, classe_predita, classes):
    matriz = confusion_matrix(classe_real, classe_predita, labels=classes)
    total = matriz.sum()

    metricas_por_classe = []
    for indice, nome_classe in enumerate(classes):
        vp = matriz[indice, indice]
        fp = matriz[:, indice].sum() - vp
        fn = matriz[indice, :].sum() - vp
        vn = total - vp - fp - fn

        acuracia_classe = vp / matriz[indice, :].sum() if matriz[indice, :].sum() else 0
        especificidade = vn / (vn + fp) if (vn + fp) else 0
        sensibilidade = vp / (vp + fn) if (vp + fn) else 0

        metricas_por_classe.append({
            'classe': nome_classe,
            'acuracia_classe': acuracia_classe,
            'especificidade': especificidade,
            'sensibilidade': sensibilidade,
        })

    return matriz, metricas_por_classe


def criar_relatorio_markdown(alvo, acuracia_global, f1, matriz, classes, metricas_por_classe, caminho_modelo):
    matriz_df = pd.DataFrame(matriz, index=classes, columns=classes)
    linhas = [
        '## ' + alvo,
        '',
        '### Pipeline',
        '1. Abrir o CSV',
        '2. Criar `purchase_day` e `purchase_dayofweek` a partir de `purchase_date`',
        '3. Descartar: `' + '`, `'.join(COLUNAS_DESCARTADAS) + '`',
        '4. Remover os alvos das colunas de entrada: `' + '`, `'.join(ALVOS) + '`',
        '5. Codificar variaveis categoricas com `OneHotEncoder`',
        '6. Treinar `RandomForestClassifier`',
        '',
        '### Metricas gerais',
        '- Acuracia global: `' + str(round(acuracia_global, 4)) + '`',
        '- F1-score ponderado: `' + str(round(f1, 4)) + '`',
        '',
        '### Matriz de confusao',
        '```text',
        matriz_df.to_string(),
        '```',
        '',
        '### Metricas por classe',
        '| Classe | Acuracia | Especificidade | Sensibilidade |',
        '|---|---:|---:|---:|',
    ]

    for metrica in metricas_por_classe:
        linhas.append(
            '| ' + str(metrica['classe']) +
            ' | ' + str(round(metrica['acuracia_classe'], 4)) +
            ' | ' + str(round(metrica['especificidade'], 4)) +
            ' | ' + str(round(metrica['sensibilidade'], 4)) +
            ' |'
        )

    linhas.extend([
        '',
        'Modelo salvo em: `' + caminho_modelo + '`',
        '',
    ])
    return linhas


def treinar_modelo(dados, alvo):
    atributos = dados.drop(columns=ALVOS + COLUNAS_DESCARTADAS)
    classe = dados[alvo]

    atributos_treino, atributos_teste, classe_treino, classe_teste = train_test_split(
        atributos,
        classe,
        test_size=0.3,
        random_state=42,
        stratify=classe,
    )

    colunas_categoricas = atributos.select_dtypes(include=['object', 'string']).columns.tolist()
    colunas_numericas = atributos.select_dtypes(exclude=['object', 'string']).columns.tolist()

    pre_processamento = ColumnTransformer(
        transformers=[
            ('categoricas', OneHotEncoder(handle_unknown='ignore'), colunas_categoricas),
            ('numericas', 'passthrough', colunas_numericas),
        ]
    )

    modelo = RandomForestClassifier(
        n_estimators=40,
        max_depth=12,
        min_samples_leaf=5,
        random_state=42,
        class_weight='balanced',
        n_jobs=-1,
    )

    pipeline = Pipeline([
        ('pre_processamento', pre_processamento),
        ('classificador', modelo),
    ])

    print('\n====================================================')
    print('ALVO:', alvo)
    print('Pipeline:')
    print('1) Abrir o CSV')
    print('2) Criar purchase_day e purchase_dayofweek a partir de purchase_date')
    print('3) Descartar:', COLUNAS_DESCARTADAS)
    print('4) Remover os alvos das colunas de entrada:', ALVOS)
    print('5) Codificar variaveis categoricas com OneHotEncoder')
    print('6) Treinar RandomForestClassifier')

    pipeline.fit(atributos_treino, classe_treino)
    classe_predita = pipeline.predict(atributos_teste)
    classes = pipeline.named_steps['classificador'].classes_

    acuracia_global = accuracy_score(classe_teste, classe_predita)
    f1 = f1_score(classe_teste, classe_predita, average='weighted')
    matriz, metricas_por_classe = calcular_metricas(classe_teste, classe_predita, classes)

    print('\nAcuracia global:', round(acuracia_global, 4))
    print('F1-score ponderado:', round(f1, 4))
    print('\nMatriz de confusao:')
    print(pd.DataFrame(matriz, index=classes, columns=classes))

    print('\nMetricas por classe:')
    for metrica in metricas_por_classe:
        print(
            metrica['classe'],
            '| acuracia:',
            round(metrica['acuracia_classe'], 4),
            '| especificidade:',
            round(metrica['especificidade'], 4),
            '| sensibilidade:',
            round(metrica['sensibilidade'], 4),
        )

    os.makedirs(PASTA_MODELOS, exist_ok=True)
    caminho_modelo = os.path.join(PASTA_MODELOS, alvo + '_modelo.pkl')
    dump({
        'alvo': alvo,
        'modelo': pipeline,
        'colunas_atributos': atributos.columns.tolist(),
        'colunas_descartadas': COLUNAS_DESCARTADAS,
        'alvos': ALVOS,
    }, open(caminho_modelo, 'wb'))
    print('\nModelo salvo em:', caminho_modelo)
    return criar_relatorio_markdown(
        alvo,
        acuracia_global,
        f1,
        matriz,
        classes,
        metricas_por_classe,
        caminho_modelo,
    )


dados_vendas = pd.read_csv(ARQUIVO_DADOS)
dados_vendas = preparar_dados(dados_vendas)

print('Arquivo de dados:', ARQUIVO_DADOS)
print('Quantidade de registros:', len(dados_vendas))
print('Colunas do arquivo:', list(dados_vendas.columns))

relatorio = [
    '# Relatorio de treinamento - Black Friday',
    '',
    'Arquivo de dados: `' + ARQUIVO_DADOS + '`',
    '',
    'Quantidade de registros: `' + str(len(dados_vendas)) + '`',
    '',
    'Colunas do arquivo: `' + '`, `'.join(dados_vendas.columns) + '`',
    '',
]

for alvo in ALVOS:
    relatorio.extend(treinar_modelo(dados_vendas, alvo))

os.makedirs(PASTA_DATA, exist_ok=True)
caminho_relatorio = os.path.join(PASTA_DATA, 'relatorio_treinamento.md')
with open(caminho_relatorio, 'w', encoding='utf-8') as arquivo:
    arquivo.write('\n'.join(relatorio))

print('\nRelatorio de treinamento salvo em:', caminho_relatorio)
