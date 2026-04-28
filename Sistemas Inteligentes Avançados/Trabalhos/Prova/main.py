import pandas as pd
import pickle
import numpy as np
import math

from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

ARQUIVO_DADOS = "ObesityDataSet.csv"

NUMERICAS = ["Age", "Height", "Weight", "FCVC", "NCP", "CH2O", "FAF", "TUE"]

CATEGORICAS = [
    "Gender", "family_history_with_overweight", "FAVC", "CAEC",
    "SMOKE", "SCC", "CALC", "MTRANS"
]

TARGET = "NObeyesdad"


def treinar_modelo():
    dados = pd.read_csv(ARQUIVO_DADOS)

    scaler = MinMaxScaler()
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")

    dados_num = scaler.fit_transform(dados[NUMERICAS])
    dados_cat = encoder.fit_transform(dados[CATEGORICAS])

    dados_normalizados = np.hstack([dados_num, dados_cat])

    pickle.dump(scaler, open("normalizador.pkl", "wb"))
    pickle.dump(encoder, open("encoder.pkl", "wb"))

    distortions=[] #Matriz para armazenar as distorçoes
    K = range(1, dados.shape[0])
    for i in K:
        cluster_model = KMeans(n_clusters=i, 
                            random_state=42).fit(dados_normalizados)

        #calcular e armazenar a distorção de cada treinamento
        distortions.append(
            sum(
                np.min(
                    cdist(dados_normalizados,
                        cluster_model.cluster_centers_,
                        'euclidean'), axis=1)/dados_normalizados.shape[0] 
                )
            )
        
    #Determinar o número ótimo de cluster para o modelo
    x0 = K[0]
    y0 = distortions[0]
    xn = K[-1]    
    yn = distortions[-1]
    distances = []
    for i in range(len(distortions)):
        x = K[i]
        y = distortions[i]
        numerador = abs(
            (yn-y0)*x - (xn-x0)*y + xn*y0 - yn*x0
        )
        denominador = math.sqrt(
            (yn-y0)**2 + (xn-x0)**2
        )
        distances.append(numerador/denominador)

    numero_clusters_otimo = K[distances.index(np.max(distances))]

    print(f"Número ideal de clusters encontrado: {numero_clusters_otimo}")

    modelo_final = KMeans(
        n_clusters=numero_clusters_otimo,
        random_state=42
    ).fit(dados_normalizados)

    dados["cluster"] = modelo_final.predict(dados_normalizados)

    pickle.dump(modelo_final, open("cluster.pkl", "wb"))

    descrever_clusters(dados)

    print("Modelo treinado e salvo.")


def descrever_clusters(dados):
    print("\n===== DESCRIÇÃO DOS CLUSTERS =====")

    for cluster in sorted(dados["cluster"].unique()):
        grupo = dados[dados["cluster"] == cluster]

        print(f"\n--- Cluster {cluster} ---")
        print(f"Quantidade de pacientes: {len(grupo)}")

        print("\nMédias numéricas:")
        print(grupo[NUMERICAS].mean())

        print("\nCategorias predominantes:")

        for coluna in CATEGORICAS + [TARGET]:
            mais_comum = grupo[coluna].mode()[0]

            print(f"{coluna}: {mais_comum}")


def inferir_paciente(paciente):
    scaler = pickle.load(open("normalizador.pkl", "rb"))
    encoder = pickle.load(open("encoder.pkl", "rb"))
    modelo = pickle.load(open("cluster.pkl", "rb"))

    paciente_df = pd.DataFrame([paciente])

    paciente_num = scaler.transform(paciente_df[NUMERICAS])
    paciente_cat = encoder.transform(paciente_df[CATEGORICAS])

    paciente_normalizado = np.hstack([paciente_num, paciente_cat])

    cluster = modelo.predict(paciente_normalizado)[0]

    return cluster


if __name__ == "__main__":
    treinar_modelo()

    paciente_teste = {
        "Gender": "Male",
        "Age": 21,
        "Height": 1.75,
        "Weight": 85,
        "family_history_with_overweight": "yes",
        "FAVC": "yes",
        "FCVC": 2,
        "NCP": 3,
        "CAEC": "Sometimes",
        "SMOKE": "no",
        "CH2O": 2,
        "SCC": "no",
        "FAF": 1,
        "TUE": 1,
        "CALC": "Sometimes",
        "MTRANS": "Public_Transportation"
    }

    cluster = inferir_paciente(paciente_teste)

    print(f"\nPaciente desconhecido pertence ao cluster: {cluster}")