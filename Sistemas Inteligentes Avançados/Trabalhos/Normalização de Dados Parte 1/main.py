import pandas as pd
import os
from normalizacao import Normalizdor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(BASE_DIR, "dados_normalizar.csv")

df = pd.read_csv(caminho_csv, sep=";")

df["altura"] = df["altura"].str.replace(",", ".", regex=False).astype(float)

print("Dados Originais: ")
print(df)
print("\n-------------------\n")

normalizador = Normalizdor()

normalizador.ajustar(df)

df_transformado = normalizador.transformar(df)

print("Dados Transformados: ")
print(df_transformado)
print("\n-------------------\n")

normalizador.salvar_modelos()

novo_normalizador = Normalizdor()
novo_normalizador.carregar_modelos()

df_revertido = novo_normalizador.reverter(df_transformado)

print("Dados Revertidos: ")
print(df_revertido)
print("\n-------------------\n")