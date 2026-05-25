#Classificador v1
#Versao sem balanceamento de classes.
#dados = fertility_Diagnosis.txt

from sklearn.model_selection import train_test_split
import pandas as pd

dados = pd.read_csv('fertility_Diagnosis.txt', sep=',')

#segmentar dados para treinamentos e dados para teste
#separar atributos chave

dados_atributos = dados.drop(columns=['Diagnostico'])
dados_classe = dados['Diagnostico']

atributos_train, class_train, atributos_test, class_test = train_test_split(dados_atributos, dados_classe, test_size=0.3)