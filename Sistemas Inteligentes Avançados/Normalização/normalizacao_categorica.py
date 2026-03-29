from sklearn.preprocessing import LabelEncoder

#Dados categoricos para normalizar
cores = ['vermelho', 'azul', 'verde', 'azul']

#Instanciar o codificador
encoder = LabelEncoder()

#Treinar o modelo normalizador para uso posterior
cores_normalizadas = encoder.fit_transform(cores) #metodo fit treina o modelo normal

print(cores)
print(cores_normalizadas)

#inverter uma cor modificada
print("cor natural:", encoder.classes_[0]) #mostra a cor natural associada ao numero 0