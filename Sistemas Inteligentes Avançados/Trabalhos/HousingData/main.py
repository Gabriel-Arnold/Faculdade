import pickle
import pandas as pd
import numpy as np

ARQUIVO_IMPUTER = "imputer.pkl"
ARQUIVO_NORMALIZADOR = "normalizador.pkl"
ARQUIVO_CLUSTER = "cluster.pkl"

FEATURES_NUMERICAS = [
    "CRIM", "ZN", "INDUS", "NOX", "RM", "AGE",
    "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"
]

FEATURES_CATEGORICAS = ["CHAS"]

FEATURES = FEATURES_NUMERICAS + FEATURES_CATEGORICAS

def descrever_segmentos(dados, modelo):
    dados_desc = dados.copy()
    dados_desc["cluster"] = modelo.labels_

    print("\nMédia de cada atributo por cluster:")
    print(dados_desc.groupby("cluster").mean())


def inferir_cluster(nova_casa):
    medias_preenchimento = pickle.load(open(ARQUIVO_IMPUTER, "rb"))
    normalizador = pickle.load(open(ARQUIVO_NORMALIZADOR, "rb"))
    modelo = pickle.load(open(ARQUIVO_CLUSTER, "rb"))
    moda_chas = pickle.load(open("chas_mode.pkl", "rb"))

    nova_casa_df = pd.DataFrame([nova_casa])

    # Garantir que todas as colunas existam
    for coluna in FEATURES:
        if coluna not in nova_casa_df.columns:
            nova_casa_df[coluna] = None

    # numéricas
    nova_casa_df[FEATURES_NUMERICAS] = nova_casa_df[FEATURES_NUMERICAS].fillna(medias_preenchimento)

    # categórica
    nova_casa_df["CHAS"] = nova_casa_df["CHAS"].fillna(moda_chas)

    # Normalizar

    num_norm = normalizador.transform(nova_casa_df[FEATURES_NUMERICAS])
    cat = nova_casa_df[FEATURES_CATEGORICAS].values

    nova_casa_norm = np.hstack((num_norm, cat))

    # Prever cluster
    cluster_previsto = modelo.predict(nova_casa_norm)

    return cluster_previsto[0]


if __name__ == "__main__":
    # Ler os dados
    dados = pd.read_csv("HousingData.csv")

    # Mesmo tratamento usado no treino apenas para visualização
    dados[FEATURES] = dados[FEATURES].fillna(dados[FEATURES].mean())

    # Carregar modelo treinado
    modelo = pickle.load(open(ARQUIVO_CLUSTER, "rb"))

    # Descrever segmentos
    dados["cluster"] = modelo.labels_
    descrever_segmentos(dados, modelo)

    # Exemplo de inferência
    nova_casa = {
        "CRIM": 0.1,
        "ZN": 20.0,
        "INDUS": 5.0,
        "CHAS": 0.0,
        "NOX": 0.5,
        "RM": 6.0,
        "AGE": 60.0,
        "DIS": 4.0,
        "RAD": 4,
        "TAX": 300,
        "PTRATIO": 15.0,
        "B": 390.0,
        "LSTAT": 10.0
    }

    cluster = inferir_cluster(nova_casa)
    print("\nCluster previsto para a nova casa:", cluster)