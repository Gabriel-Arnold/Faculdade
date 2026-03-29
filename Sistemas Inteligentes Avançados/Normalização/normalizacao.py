from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pickle

# dados numericos
dados = np.array([[1500], [3000], [5500], [10000]])

#instaciar o nomalizador
scaler = MinMaxScaler()

#treinar modelor normalizador para uso posterior
scaler_model = scaler.fit(dados) #metodo fit trinar o modelo normalizador.

#salvar o modelo normalizador treinado para uso posterior
pickle.dump(scaler_model, open('scaler_model.pkl', 'wb')) #metodo dump salva o modelo em um arquivo binário wb.

dados_norm = scaler_model.fit_transform(dados) #metodo fit_transform normaliza os dados usando o modelo treinado.

print(dados)
print(dados_norm)