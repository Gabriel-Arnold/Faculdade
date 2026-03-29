from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import pickle

class NovaInstancia:
    def __init__(self, caminho_encoder="encoder_model.pkl"):
        self.encoder = pickle.load(open(caminho_encoder, "rb"))
    def transformar(self, nova_instancia):
        df_novo = pd.DataFrame([nova_instancia])
        dados_transformados = self.encoder.transform(df_novo[["cor"]])
        colunas = self.encoder.get_feature_names_out(["cor"])
        df_resultado = pd.DataFrame(dados_transformados, columns=colunas)
        return df_resultado

df = pd.DataFrame({
    "cor": ["Azul", "Verde", "Vermelho", "Azul", "Verde"]
})

encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")

encoder.fit(df[["cor"]])

pickle.dump(encoder, open("encoder_model.pkl", "wb"))

nova_instancia = {"cor": "Azul"}

instancia = NovaInstancia( "encoder_model.pkl")
resultado = instancia.transformar(nova_instancia)

print("Nova instancia original: ", nova_instancia)
print("\nNova instancia transformada: \n", resultado)

