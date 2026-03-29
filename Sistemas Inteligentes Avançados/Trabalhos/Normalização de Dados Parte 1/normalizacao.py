from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import pandas as pd
import pickle

class Normalizdor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    
    def ajustar(self, df): 
        self.scaler.fit(df[["idade", "altura", "Peso"]])

        self.encoder.fit(df[["sexo"]])

    def transformar(self, df):
        dados_numericos = self.scaler.transform(df[["idade", "altura", "Peso"]])

        df_numerico = pd.DataFrame(
            dados_numericos,
            columns=["idade", "altura", "Peso"]
        )

        dados_sexo = self.encoder.transform(df[["sexo"]])

        colunas_sexo = self.encoder.get_feature_names_out(["sexo"])
        df_sexo = pd.DataFrame(dados_sexo, columns=colunas_sexo)

        df_final = pd.concat([df_numerico, df_sexo], axis=1)
        return df_final
    
    def reverter(self, df_transformado):
        dados_numericos_originais = self.scaler.inverse_transform(
            df_transformado[["idade", "altura", "Peso"]]
        )

        df_numerico = pd.DataFrame(
            dados_numericos_originais,
            columns=["idade", "altura", "Peso"]
        )

        colunas_sexo = self.encoder.get_feature_names_out(["sexo"])
        dados_sexo = df_transformado[colunas_sexo]

        sexo_original = self.encoder.inverse_transform(dados_sexo)
        df_sexo = pd.DataFrame(sexo_original, columns=["sexo"])

        df_original = pd.concat([df_numerico, df_sexo], axis=1)
        return df_original
    
    def salvar_modelos(self):
        pickle.dump(self.scaler, open("scaler_model.pkl", "wb"))
        pickle.dump(self.encoder, open("encoder_model.pkl", "wb"))

    def carregar_modelos(self):
        self.scaler = pickle.load(open("scaler_model.pkl", "rb"))
        self.encoder = pickle.load(open("encoder_model.pkl", "rb"))
        