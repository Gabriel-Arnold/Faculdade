import pandas as pd
import pickle
import numpy as np
import math

from matplotlib.pyplot import sca
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

scaler = MinMaxScaler()

dados = pd.read_csv('HousingData.csv', sep= ',')

print(dados.head())
print(dados.info())
print(dados.isnull().sum())

dados.fillna(dados.mean(), inplace=True)

dados_cluster = dados.drop(columns=['MEDV'])

normalizador = scaler.fit(dados_cluster)
# -- Salvar o normalizador para uso posterior
pickle.dump(
            normalizador,
            open(
                'normalizador.pkl', 'wb'
                ))
dados_normalizados = normalizador.fit_transform(dados_cluster)

# Calcular número ótimo de clusters
distortions = []
K = range(1, 11)

for i in K:
    cluster_model = KMeans(n_clusters=i, random_state=42, n_init=10)
    cluster_model.fit(dados_normalizados)

    distortions.append(
        sum(
            np.min(
                cdist(
                    dados_normalizados,
                    cluster_model.cluster_centers_,
                    'euclidean'
                ),
                axis=1
            )
        ) / dados_normalizados.shape[0]
    )

x0 = K[0]
y0 = distortions[0]
xn = K[-1]
yn = distortions[-1]

distances = []
for i in range(len(distortions)):
    x = K[i]
    y = distortions[i]

    numerador = abs((yn - y0) * x - (xn - x0) * y + xn * y0 - yn * x0)
    denominador = math.sqrt((yn - y0) ** 2 + (xn - x0) ** 2)
    distances.append(numerador / denominador)

numero_clusters_otimo = K[distances.index(np.max(distances))]
print("Número ótimo de clusters:", numero_clusters_otimo)

# Treinar modelo final
cluster_model = KMeans(
    n_clusters=numero_clusters_otimo,
    random_state=42,
    n_init=10
)
cluster_model.fit(dados_normalizados)

# Salvar o modelo
pickle.dump(cluster_model, open('cluster.pkl', 'wb'))

# Adicionar cluster ao dataframe para análise
dados['cluster'] = cluster_model.labels_
print(dados.groupby('cluster').mean())