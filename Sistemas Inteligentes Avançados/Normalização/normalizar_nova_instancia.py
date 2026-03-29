#recebe um novo valor numerico e normaliza usando o modelo original
import pickle

#abrir o modelo normalizador original
scaler_model = pickle.load(open('scaler_model.pkl', 'rb')) #metodo load carrega o modelo do arquivo binário rb.

novo_dado = [[2000]] #novo valor numerico a ser normalizado
novo_dado_norm = scaler_model.transform(novo_dado) #metodo transform normaliza o novo valor usando o modelo original.

print(novo_dado)
print(novo_dado_norm)

dado_revertido = scaler_model.inverse_transform(novo_dado_norm) #metodo inverse_transform reverte a normalização para o valor original.
print(dado_revertido)