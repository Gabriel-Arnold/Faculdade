#Imports
import pickle
import pandas as pd

#Abrir o modelo de clusters
cluster_model = pickle.load(open('cluster_iris.pkl','rb'))

#Abrir o normalizador numérico salvo anteriormente
normalizador = pickle.load(open('normalizador_iris.pkl', 'rb'))

#Desnormalizar os centroides
columns_names = ['sepal_length', 
                 'sepal_width', 
                 'petal_length', 
                 'petal_width',
                 'Iris-setosa', 
                 'Iris-versicolor', 
                 'Iris-virginica']

#Converter os centroides em dataframe
dataframe = pd.DataFrame(cluster_model.cluster_centers_,
                          columns = columns_names 
    )



atributos_num_desnorm = pd.DataFrame(
    normalizador
      .inverse_transform(
          dataframe[
              ['sepal_length', 
                 'sepal_width', 
                 'petal_length', 
                 'petal_width']]),
                 columns  = ['sepal_length', 
                 'sepal_width', 
                 'petal_length', 
                 'petal_width']
                 )

#Desnormalizar as colunas codificadas com one_hot_encoder
class_dataframe = dataframe[['Iris-setosa', 
                 'Iris-versicolor', 
                 'Iris-virginica']].round(0).astype(int)

class_dataframe = pd.from_dummies(class_dataframe)
class_dataframe.columns=['class']

#Juntar os dataframes: colunas numéricas desnormalizadas e a categoria desnormalizada
cluster = atributos_num_desnorm.join(class_dataframe)
print(cluster)


