#Classificador - versão 1
#Arquivo de dados: fertility_diagnosys.txt
#Versão sem balanceamento de classes

from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import RandomizedSearchCV
import matplotlib.pyplot as plt
from pickle import load, dump
from imblearn.over_sampling import SMOTE #Para balancear os dados
import numpy as np
#Abrir o arquivo de dados
dados = pd.read_csv('fertility_Diagnosis.txt', sep = ',')
#Separar atributos e classe
dados_atributos = dados.drop(columns=['Diagnostico'])
dados_classe = dados['Diagnostico']



#==========================
# Balancear os dados
resampler = SMOTE() # Constroi o balanceador#Executar o balanceamento
atributos_b, classes_b = resampler.fit_resample(dados_atributos, dados_classe)
print('#### FREQUENCIA DAS CLASSES APÓS O BALANCEAMENTO ###')
from collections import Counter
class_count = Counter(classes_b)
class_count
dados.columns #utilizar os rótulos das colunas

#=======================
#segmentar os dados em dados para treinamento e dados para teste
atributos_train, atributos_teste, classe_train,classe_test = train_test_split(atributos_b,classes_b, test_size=0.3)


#TREINAR O MODELO
tree = DecisionTreeClassifier(random_state=42)

#HIPERPARAMETRIZAÇÃO DA RANDOM FOREST
#Definir os domínios para os hiperparâmetros
n_estimators = [int(x) for x in np.linspace(start=10, stop=100, num=10)]
criterion = ['gini', 'entropy']
min_samples_split = [int(x) for x in np.linspace(start=2, stop=10, num=2)]
max_depth = [int(x) for x in np.linspace(start=10, stop=100, num=20)]
max_features = ['sqrt', 'log2']

#criar a grade de valores
rf_grid={
    'n_estimators': n_estimators,
    'criterion': criterion,
    'min_samples_split':min_samples_split,
    'max_depth': max_depth,
    'max_features': max_features
}

rf = RandomForestClassifier()
rf_hyperparameters = RandomizedSearchCV(
    estimator=rf,
    param_distributions= rf_grid,
    n_iter=10,
    cv = 3,
    verbose=2,
    n_jobs=-1
)
rf_hyperparameters.fit(dados_atributos, dados_classe)
#Mostrar o resultado da hiperparametrização
from pprint import pprint
print('Melhores parametros:')
pprint(rf_hyperparameters.best_params_)
#instanciar o estimador
rf = RandomForestClassifier(**rf_hyperparameters.best_params_)


# fertility_tree = tree.fit(atributos_train, classe_train)
fertility_rf = rf.fit(atributos_train, classe_train)
# #Salvar o modelo
# dump(fertility_tree, 
#      open('fertilty_tree.pkl', 'wb'))

dump(fertility_rf, 
     open('fertilty_rf.pkl', 'wb'))

# #Testando o modelo
# diagnostico_predito = \
#     fertility_tree.predict(atributos_teste)

diagnostico_predito_rf = \
    fertility_rf.predict(atributos_teste)

# #Acurácia geral
# acuracia = accuracy_score(classe_test, diagnostico_predito)
# print('acurácia (tree):', acuracia)
acuracia = accuracy_score(classe_test, diagnostico_predito_rf)
print('acurácia (rf):', acuracia)
#Calcular especificidade e sensibilidade
tn, fp, fn, tp = confusion_matrix(classe_test, diagnostico_predito_rf).ravel()
#especificidade = vn/(vn+fp)
especificidade = tn/(tn+fp)

#sensibilidade = vp/(vp+fn)
sensibilidade = tp/(tp+fn)

print('especificidade (rf): ', especificidade)
print('sensibiliade: (rf)', sensibilidade)
# #Matriz de contingência
# # ConfusionMatrixDisplay.from_estimator(fertility_tree,atributos_teste, classe_test)
# # plt.show()

# #Calcular especificidade e sensibilidade
# tn, fp, fn, tp = confusion_matrix(classe_test, diagnostico_predito).ravel()
# #especificidade = vn/(vn+fp)
# especificidade = tn/(tn+fp)

# #sensibilidade = vp/(vp+fn)
# sensibilidade = tp/(tp+fn)

# print('especificidade (tree): ', especificidade)
# print('sensibiliade: (tree)', sensibilidade)


