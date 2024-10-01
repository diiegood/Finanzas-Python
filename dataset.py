# Practica basica de como importar data set # introduccion a  machine learning

#librerias 
"la funcion para leer cuadros en python es "
#creo_mifuncion = pd.read_"tipo_de_archivo" ("nombre/archivo"."tipo/archivo").

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#se crea funcion / funcion especifica ('nombre_del_archivo.csv') #la terminacion puede ser jason /csv
dataframe = pd.read_csv('data.csv') #se carga los datos de data.csv
#para que sea mas eficiente los datos y el archivo de este script deben estar en
#la misma direccion para que se guarden.

#al ser validada aparece en variable explorer en un cuadro#, se le da click
#nos indica que el archivo "data.csv", es un data frame de 4 columnas y 169 filas
#nos indica el contenido de las columnas : duracion, pulso, maxpulso, calorias

"se va realizar la funcion de machine learning"
#se crea una funcion para poder realizar un nuevo cuadro filtrado valores del cuadro anterior
# nuevafuncion / nombre_archivo.iloc[]-> se busca determinar los rangos de busqueda dentro del corchete
#funcion iloc -> es para localizacion
X = dataframe.iloc[1:3, 0:2] 
#se pone las [filas donde_empiezan : donde_terminan , columnas donde_empiezan : donde_terminan ]
#si no se pone nada te muestra toda la tabla o valores, de esa seccion.

"nueva funcion de las variables dependientes" #se muestra como matriz X1 va en mayuscula
X1 = dataframe.iloc [:,:-1].values #para que me muestre los primeros 3 valores
#se puede teclear en la consola X1 y nos muestra los datos de las variables.
#en este caso ignora las variable dependiente que  es la que se muestran predecir

"para crear la variable independiente" #va en minuscula porque es un vector
y = dataframe.iloc [:, 3].values

"para corregir los datos faltantes" 
#se importa libreria 
from sklearn.impute import SimpleImputer

"se crea la variable para la sustitucion"
imputer = SimpleImputer(missing_values= np.nan, strategy="mean")
#se usa la funcion de valores perdidos con la libreria de numpy 
#nan es el nombre de los valores que estan extraviados o van a ser filtrados
#usamos como estrategia la media / mean , para sustituir (se puede usar la mediana u otra estrategia)

"que columnas se van a sustituir" #se usa la variable imputer imputer.fit(dentro la variable que se va hacer)
imputer = imputer.fit(X1[:, 1:3]) #se especifica el rango de las columnas / como son todas las filas se deja vacio

#Se transforma especificando todas las filas de la columna 1:3 se iguala a imputer

X1 [:,1:3] = imputer.transform(X1[:,1:3]) #lo que hace es sacar la media .