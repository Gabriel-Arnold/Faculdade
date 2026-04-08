from matplotlib.pyplot import sca
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

scaler = MinMaxScaler()

dados = pd.read_csv('HousingData.csv', sep= ',')
df = dados.fillna(dados.mean())

normalizador = scaler.fit(df)

dados_normalizados = normalizador.fit_transform(df)




