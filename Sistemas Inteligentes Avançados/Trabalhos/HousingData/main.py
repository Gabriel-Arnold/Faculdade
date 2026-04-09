import pickle
import pandas as pd

def descrever_segmentos(dados, modelo):
    dados_desc = dados.copy()
    dados_desc['cluster'] = modelo.labels_

    print("\nMédia de cada atributo por cluster:")
    print(dados_desc.groupby('cluster').mean())

def inferir_cluster(nova_casa):
    normalizador = pickle.load(open('normalizador.pkl', 'rb'))
    modelo = pickle.load(open('cluster.pkl', 'rb'))

    nova_casa_df = pd.DataFrame([nova_casa])
    nova_casa_norm = normalizador.transform(nova_casa_df)
    cluster_previsto = modelo.predict(nova_casa_norm)

    return cluster_previsto[0]

if __name__ == "__main__":
    # Ler os dados
    dados = pd.read_csv("HousingData.csv")

    # Tratar valores nulos
    dados.fillna(dados.mean(), inplace=True)

    # Carregar modelo treinado
    modelo = pickle.load(open('cluster.pkl', 'rb'))

    # Descrever os segmentos
    descrever_segmentos(dados, modelo)

    # Exemplo de inferência
    nova_casa = {
        'CRIM': 0.1,
        'ZN': 20.0,
        'INDUS': 5.0,
        'CHAS': 0.0,
        'NOX': 0.5,
        'RM': 6.0,
        'AGE': 60.0,
        'DIS': 4.0,
        'RAD': 4,
        'TAX': 300,
        'PTRATIO': 15.0,
        'B': 390.0,
        'LSTAT': 10.0
    }

    cluster = inferir_cluster(nova_casa)
    print("\nCluster previsto para a nova casa:", cluster)