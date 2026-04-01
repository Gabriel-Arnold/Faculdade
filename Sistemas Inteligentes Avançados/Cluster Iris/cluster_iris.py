#SISTEMAS INTELITGENTES
#Modelos não supervisionados
#Base iris

#Imports
from turtle import distance

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

#1. Abrir os dados
dados = pd.read_csv('iris.csv', sep= ';')

#2. Normalizar os dados
#2.1 Separar atributos numéricos e atributos categóricos
dados_num = dados.drop(columns=['class'])
dados_cat = dados['class']

#2.2 Normalizar os dados numéricos
# -- Instanciar o normalizador
scaler = MinMaxScaler()
# -- Treinar o normalizador
normalizador = scaler.fit(dados_num)
# -- Salvar o normalizador para uso posterior
pickle.dump(
            normalizador,
            open(
                'normalizador_iris.pkl', 'wb'
                ))
# -- normalizar os dados
dados_num_norm = normalizador.fit_transform(dados_num)

#2.3 Normalizar os dados categóricos
dados_cat_norm = pd.get_dummies(
                    dados_cat, prefix_sep='_',
                    dtype=int)

#2.4 Reagrupas os objetos normalizados em um data frame
#---- Converter a matriz numérica (dados_num_norm) em dataframe
dados_num_norm = pd.DataFrame(dados_num_norm,
                              columns = dados_num.columns)

# --  juntar o dados_num_norm com o dados_cat_norm
dados_norm = dados_num_norm.join(dados_cat_norm)

#3. HIPERPARAMETRIZAR  
#Vamos determinar o número ótimo de clusters antes do treinamento
from sklearn.cluster import KMeans #Kmeans é um clusterizador
import math
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist #método para cálculo de distâncias cartesianas
import numpy as np
distortions=[] #Matriz para armazenar as distorçoes
K = range(1, dados.shape[0])
for i in K:
    cluster_model = KMeans(n_clusters=i, 
                           random_state=42).fit(dados_norm)
    
    #calcular e armarzenar a distorção de cada treinamento.
    distortions.append(
        sum(np.min(cdist(dados_norm, cluster_model.cluster_centers_, "euclidean"), axis=1)/dados_norm.shape[0])
    )

x0 = K[0]
y0 = distortions[0]
xn = K[-1]
yn = distortions[-1]
distance = []
for i in range(len(distortions)):
    x = K[i]
    y = distortions[i]
    numerador = abs(
        (yn-y0)*x - (xn-x0)*y + xn*y0 - yn*x0
    )
    denominador = math.sqrt(
        (yn - y0)**2 + (xn-x0)**2
    )
    distance.append(numerador/denominador)

numero_clusters_otimo = K[distance.index(np.max(distance))]

#print(K[distance.index(np.max(distance))])

cluster_model = KMeans(
    n_clusters= numero_clusters_otimo,
    random_state= 42).fit(dados_norm)

pickle.dump(cluster_model, open())


#Paramos aqui. Falta calcular a distorcao para cada iteração
#continuaremos na aula do dia 31/03    
