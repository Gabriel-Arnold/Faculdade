import pandas as pd
import pickle
import numpy as np
import math

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist


ARQUIVO_DADOS = "HousingData.csv"
ARQUIVO_IMPUTER = "imputer.pkl"
ARQUIVO_NORMALIZADOR = "normalizador.pkl"
ARQUIVO_CLUSTER = "cluster.pkl"

# Colunas usadas no treino do cluster
# MEDV será usada apenas para descrição dos grupos
FEATURES_NUMERICAS = [
    "CRIM", "ZN", "INDUS", "NOX", "RM", "AGE",
    "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"
]

FEATURES_CATEGORICAS = ["CHAS"]

FEATURES = FEATURES_NUMERICAS + FEATURES_CATEGORICAS

def preencher_vazios(df):
    medias = df[FEATURES_NUMERICAS].mean()
    
    # numéricas → média
    df[FEATURES_NUMERICAS] = df[FEATURES_NUMERICAS].fillna(medias)
    
    # categórica → moda
    moda = df["CHAS"].mode()[0]
    df["CHAS"] = df["CHAS"].fillna(moda)

    return df, medias, moda

def determinar_numero_clusters(dados_normalizados, k_min=2,):
    distortions = []
    n = dados_normalizados.shape[0]
    k_max = int(np.sqrt(n))  # máximo baseado nos dados
    K = list(range(k_min, k_max + 1))

    for k in K:
        modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
        modelo.fit(dados_normalizados)

        distorcao = sum(
            np.min(
                cdist(dados_normalizados, modelo.cluster_centers_, "euclidean"),
                axis=1
            )
        ) / dados_normalizados.shape[0]

        distortions.append(distorcao)

    # Método do "cotovelo" via maior distância até a reta entre extremos
    x0, y0 = K[0], distortions[0]
    xn, yn = K[-1], distortions[-1]

    distances = []
    for i in range(len(K)):
        x = K[i]
        y = distortions[i]

        numerador = abs((yn - y0) * x - (xn - x0) * y + xn * y0 - yn * x0)
        denominador = math.sqrt((yn - y0) ** 2 + (xn - x0) ** 2)
        distances.append(numerador / denominador)

    melhor_k = K[distances.index(max(distances))]
    return melhor_k, K, distortions


def classificar_nivel(valor_cluster, valor_geral, tolerancia=0.10):
    if valor_cluster > valor_geral * (1 + tolerancia):
        return "alto"
    elif valor_cluster < valor_geral * (1 - tolerancia):
        return "baixo"
    return "médio"


def descrever_clusters_humanamente(df):
    medias_gerais = df[FEATURES + ["MEDV"]].mean()
    medias_clusters = df.groupby("cluster")[FEATURES + ["MEDV"]].mean()

    print("\n" + "=" * 70)
    print("DESCRIÇÃO HUMANA DOS CLUSTERS")
    print("=" * 70)

    for cluster_id, linha in medias_clusters.iterrows():
        crim = classificar_nivel(linha["CRIM"], medias_gerais["CRIM"])
        rm = classificar_nivel(linha["RM"], medias_gerais["RM"])
        lstat = classificar_nivel(linha["LSTAT"], medias_gerais["LSTAT"])
        dis = classificar_nivel(linha["DIS"], medias_gerais["DIS"])
        tax = classificar_nivel(linha["TAX"], medias_gerais["TAX"])
        medv = classificar_nivel(linha["MEDV"], medias_gerais["MEDV"])

        print(f"\nCluster {cluster_id}:")
        print(f"- Criminalidade: {crim}")
        print(f"- Número médio de cômodos: {rm}")
        print(f"- Distância dos centros de emprego: {dis}")
        print(f"- Impostos: {tax}")
        print(f"- Percentual de população de menor status: {lstat}")
        print(f"- Valor mediano das casas (MEDV): {medv}")

        resumo = []

        if rm == "alto" and medv == "alto":
            resumo.append("regiões com casas maiores e de maior valor")
        elif rm == "baixo" and medv == "baixo":
            resumo.append("regiões com casas menores e de menor valor")

        if crim == "alto":
            resumo.append("maior criminalidade")
        elif crim == "baixo":
            resumo.append("menor criminalidade")

        if lstat == "alto":
            resumo.append("maior vulnerabilidade socioeconômica")
        elif lstat == "baixo":
            resumo.append("menor vulnerabilidade socioeconômica")

        if dis == "alto":
            resumo.append("mais distantes dos centros de emprego")
        elif dis == "baixo":
            resumo.append("mais próximas dos centros de emprego")

        if not resumo:
            resumo.append("perfil intermediário em relação à média geral")

        print("- Resumo:", "; ".join(resumo) + ".")


def main():
    # 1. Ler dados
    dados = pd.read_csv(ARQUIVO_DADOS)

    print("Primeiras linhas do dataset:")
    print(dados.head())

    print("\nInformações do dataset:")
    print(dados.info())

    print("\nQuantidade de valores nulos por coluna:")
    print(dados.isnull().sum())

    # 2. Preencher vazios
    dados, medias_preenchimento, moda_chas = preencher_vazios(dados)

    # Salvar as médias usadas no preenchimento
    pickle.dump(medias_preenchimento, open(ARQUIVO_IMPUTER, "wb"))
    pickle.dump(moda_chas, open("chas_mode.pkl", "wb"))

    # 3. Normalizar
    scaler = MinMaxScaler()
    # Normaliza apenas numéricas
    dados_num_norm = scaler.fit_transform(dados[FEATURES_NUMERICAS])

    # Mantém CHAS como está
    dados_cat = dados[FEATURES_CATEGORICAS].values

    # Junta tudo
    dados_normalizados = np.hstack((dados_num_norm, dados_cat))

    # Salvar normalizador
    pickle.dump(scaler, open(ARQUIVO_NORMALIZADOR, "wb"))

    # 4. Determinar número de clusters
    numero_clusters_otimo, ks, distortions = determinar_numero_clusters(dados_normalizados)
    print(f"\nNúmero ótimo de clusters: {numero_clusters_otimo}")

    # 5. Treinar modelo final
    modelo_cluster = KMeans(
        n_clusters=numero_clusters_otimo,
        random_state=42,
        n_init=10
    )
    modelo_cluster.fit(dados_normalizados)

    # 6. Salvar modelo
    pickle.dump(modelo_cluster, open(ARQUIVO_CLUSTER, "wb"))

    # 7. Analisar clusters
    dados["cluster"] = modelo_cluster.labels_

    print("\nMédia dos atributos por cluster:")
    print(dados.groupby("cluster")[FEATURES + ["MEDV"]].mean())

    # 8. Descrever clusters humanamente
    descrever_clusters_humanamente(dados)

if __name__ == "__main__":
    main()