import pandas as pd
from sklearn.preprocessing import OneHotEncoder

#criar dados para entrada
df = pd.DataFrame({'cor': ['vermelho', 'azul', 'verde', 'azul']})

print(df)

df_normalizado = pd.get_dummies(df, columns=['cor'])

print(df_normalizado.iloc[1])

#isolar uma linha do dataframe normalizado
nova_instancia = df_normalizado.iloc[1]

#converte a panda.series em data fram

df_nova_instancia = nova_instancia.to_frame().T
print(df_nova_instancia)

dc_nova_instancia_desnormalizada = pd.from_dummies(df_nova_instancia, sep='_')

