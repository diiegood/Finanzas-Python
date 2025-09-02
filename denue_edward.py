"Filtrado de datos de INEGI" ##################################################
###############################################################################
"Nociones principales"
#Comercio_al_por_Mayor es la matriz del sector limpia sobre la cual se va trabajar
#Comercio_al_por_Mayor_informal es un data frame de todas las empresas informales (matriz de residuos)
#Comercio_al_por_Mayor_original es la matriz orignal sin modificar
#estadisticas_daframe son las estadisticas de la matriz limpia (Comercio_al_por_Mayor)

#empresas formales se consideran aquellas que poseen razon social
#empresas informales se consideran las que no poseen razon social por lo que muchas veces son pequeños (tiendas, )

"Para cargar multiples librerias y generar una sola matriz" 

import pandas as pd
import os
import numpy as np
import re

direccion = "J:\Diego-files\Base de datos muestreo -INEGI\DENUE-0525\Bases-sucias"
librerias = ["denue_Otros_Servicios_81_1.csv",
             "denue_Otros_Servicios_81_2.csv",
             ]

Comercio_al_por_Menor_lista = []

for archivo in librerias:
    lectura_Datos = os.path.join(direccion, archivo) 
    Comercio_al_por_menor1 = pd.read_csv(lectura_Datos, encoding='latin1')
    Comercio_al_por_Menor_lista.append(Comercio_al_por_menor1) #funcion para agregar a la lista vacia los datos
    

#se combinan los data frames en uno
Comercio_al_por_Mayor = pd.concat(Comercio_al_por_Menor_lista, ignore_index=True)
Comercio_al_por_Mayor_original = pd.concat(Comercio_al_por_Menor_lista, ignore_index=True)

###############################################################################
###############################################################################
"Para cargar una sola lectura de datos"

import pandas as pd
import os
import numpy as np
import re

#para cargar una sola libreria
direccion = "S:\Diego-files\INEGI\Base de datos muestreo -INEGI\DENUE-0525\Bases-sucias"
libreria =  "denue_Comercio_al_por_Mayor_43.csv" #cambiar la libreria para ver cada sector

lectura_Datos = os.path.join(direccion, libreria)
Comercio_al_por_Mayor = pd.read_csv(lectura_Datos, encoding='latin1')  #matriz que sera modificada 
Comercio_al_por_Mayor_original = pd.read_csv(lectura_Datos, encoding='latin1') #matriz original 


#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
"Aqui empieza el codigo"#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

#data frame con todas las empresas informales(bruto, falta filtrar)
Comercio_al_por_Mayor_informal = Comercio_al_por_Mayor_original[
    Comercio_al_por_Mayor_original['raz_social'].isna()
][['clee', 'nom_estab', 'raz_social', 'per_ocu', 'codigo_act',
    'nombre_act', 'entidad', 'municipio', 'id']]


"Analisis de la matriz original"

Comercio_al_por_Mayor.head(45)#primeros 45 valores
Comercio_al_por_Mayor.tail(45) #ultimos 45 valores
Comercio_al_por_Mayor.dtypes #ver tipo de datos de cada variable del data frame
Comercio_al_por_Mayor.isnull().values.any() #ver si hay alguna columna con un valor nulo
Comercio_al_por_Mayor.columns #muestra las columnas 
Comercio_al_por_Mayor.duplicated().sum() #para ver si hay filas duplicadas


#se filtran las columnas que solamente son de importancia para la matriz
Comercio_al_por_Mayor = Comercio_al_por_Mayor[['clee', 'nom_estab', 'raz_social', 'per_ocu','codigo_act', 
                                               'nombre_act', 'entidad', 'municipio', 'id']].fillna(0) 

"Para poder conocer el total de las empresas que hay"
#el primero cuenta los individuos que no se repiten por variable de nombre de establecimiento, pero pueden tener la misma razon social

#incluyendo las empresas no tan establecidas o formalizadas (en su mayoria micro o negocio propio)
Empresas_formales_e_informales = Comercio_al_por_Mayor_original['nom_estab'].drop_duplicates() 
Empresas_formales_e_informales = len(Empresas_formales_e_informales) #calcular las empresas unicas

#empresas que realmente no se repiten porque tienen diferente razon social
empresas_formales = Comercio_al_por_Mayor_original['raz_social'].nunique() 


###############################################################################
"Modificacion del data frame"

#Transformaciones de las variables ############################################

# primera Transformacion de los datos de la variable per_ocu.
Comercio_al_por_Mayor['per_ocu'].unique() #para conocer que valores estan contenidos dentro de la columna ("per_ocu")
Comercio_al_por_Mayor['per_ocu'] = Comercio_al_por_Mayor['per_ocu'].replace({'251 y más personas': '251 a 500 personas'}) 


# segunda Transformacion de los datos de la variable codigo_act. (este puede incurrir en sesgo de variable por lo que)
#tomar solo los 4 primeros digitos del codigo SCIAN de actividad ya que son los que estan bien.
Comercio_al_por_Mayor["codigo_act"] = Comercio_al_por_Mayor["codigo_act"].astype(str)
Comercio_al_por_Mayor["codigo_act"].unique()


#Creacion de columnas ######################################################### 

#Con los valores numericos de la columna per_ocu se crean dos columnas: 

#se crea poblacion minima con los primeros valores numericos de la columna per_ocu
#se crea poblacion maxima con los segundos valores numericos de la columna per_ocu
#se crea la columna de rango entre poblacion minima y poblacion maxima
#se crea la columna de promedio entre poblacion minima y poblacion maxima 

# Extracción de valores numéricos desde 'per_ocu' donde se crean dos nuevas columnas , poblacion_minima y poblacion_maxima
Comercio_al_por_Mayor[['poblacion_minima', 'poblacion_maxima']] = Comercio_al_por_Mayor['per_ocu'].astype(str).str.extract(r'(\d+\.?\d*)\D*(\d+\.?\d*)')

# Convierte las columnas extraidas a valores numericos reales int o float, si no se queda como NaN
Comercio_al_por_Mayor['poblacion_minima'] = pd.to_numeric(Comercio_al_por_Mayor['poblacion_minima'], errors='coerce')
Comercio_al_por_Mayor['poblacion_maxima'] = pd.to_numeric(Comercio_al_por_Mayor['poblacion_maxima'], errors='coerce')

#se borra la columna de (per_ocu)
#Comercio_al_por_Menor.drop(columns='per_ocu', inplace=True) 

#se crea una columna que promedie los valores de poblacion minima y poblacion maxima
Comercio_al_por_Mayor["promedio"] = (Comercio_al_por_Mayor["poblacion_maxima"] + Comercio_al_por_Mayor["poblacion_minima"])/2
Comercio_al_por_Mayor["pesimista"] = (Comercio_al_por_Mayor["poblacion_minima"] + ((Comercio_al_por_Mayor["poblacion_maxima"] - Comercio_al_por_Mayor["poblacion_minima"])*0.25))
Comercio_al_por_Mayor["optimista"] = (Comercio_al_por_Mayor["poblacion_maxima"] - ((Comercio_al_por_Mayor["poblacion_maxima"] - Comercio_al_por_Mayor["poblacion_minima"])*0.25))

###############################################################################
"Filtros y las agrupaciones del Data Frame principal"

#1er filtro empresas que no cuenten con razon social
Comercio_al_por_Mayor = Comercio_al_por_Mayor[Comercio_al_por_Mayor["raz_social"] != 0]


"Agrupamientos por nombre de establecimiento, sumando población mínima y máxima"
#despues aplicar otro agrupamiento por nombre de la razon social
#Columnas de Municipio, Entidad, id, no se suman proque son valores que difieren del la localidad de cada sucursal de la empresa general 

# Agrupamiento de empresas por razón social (esto sobrescribe el anterior DataFrame) / SOLO EMPRESAS FORMALES ESTABLECIDAS
Comercio_al_por_Mayor = Comercio_al_por_Mayor.groupby('raz_social')[['poblacion_minima', 'poblacion_maxima', 'promedio', 'pesimista', 'optimista']].sum()
# Columnas con valores que no quiero que se sumen para posteriormente agruparlas
columnas_agregadas = Comercio_al_por_Mayor_original.groupby('raz_social')[['codigo_act', 'nom_estab', 'nombre_act']].first()
Comercio_al_por_Mayor = Comercio_al_por_Mayor.join(columnas_agregadas) # Unir ambos DataFrames


#muestra las estadisticas del data frame anterior
estadisticas_dataframe = Comercio_al_por_Mayor.describe()

###############################################################################

"Filtros para delimitar la clasificacion de las empresas"
#segun la clasificacion del INEGI.

# condiciones para micro-empresas, de 0 a 10 trabajadores #############################################
micro_empresas_pesimista = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["pesimista"] >= 0) & (Comercio_al_por_Mayor["pesimista"] <= 10)]
micro_empresas_pesimista = micro_empresas_pesimista.drop(columns = ['promedio', 'optimista'])

micro_empresas_promedio = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["promedio"] >= 0) & (Comercio_al_por_Mayor["promedio"] <= 10)]
micro_empresas_promedio = micro_empresas_promedio.drop(columns = ['pesimista', 'optimista'])

micro_empresas_optimista = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["optimista"] >= 0) & (Comercio_al_por_Mayor["optimista"] <= 10)]
micro_empresas_optimista = micro_empresas_optimista.drop(columns = ['pesimista', 'promedio'])

print(len(micro_empresas_pesimista))

print(len(micro_empresas_promedio))

print(len(micro_empresas_optimista))

# condiciones para empresas pequeñas, de 11 a 50 trabajadores ##########################################
pequeñas_empresas_pesimista = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["pesimista"] > 10) & (Comercio_al_por_Mayor["pesimista"] <= 50)]
pequeñas_empresas_pesimista = pequeñas_empresas_pesimista.drop(columns = ['promedio', 'optimista'])

pequeñas_empresas_promedio = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["promedio"] > 10) & (Comercio_al_por_Mayor["promedio"] <= 50)]
pequeñas_empresas_promedio = pequeñas_empresas_promedio.drop(columns = ['pesimista', 'optimista'])

pequeñas_empresas_optimista = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["optimista"] > 10) & (Comercio_al_por_Mayor["optimista"] <= 50)]
pequeñas_empresas_optimista = pequeñas_empresas_optimista.drop(columns = ['pesimista', 'promedio'])

print(len(pequeñas_empresas_pesimista))

print(len(pequeñas_empresas_promedio))

print(len(pequeñas_empresas_optimista))

# condiciones para empresas medianas, de 51 a 250 trabajadores ##########################################
medianas_empresas_pesimista = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["pesimista"] > 50) & (Comercio_al_por_Mayor["pesimista"] <= 250)]
medianas_empresas_pesimista = medianas_empresas_pesimista.drop(columns = ['promedio', 'optimista'])

medianas_empresas_promedio = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["promedio"] > 50) & (Comercio_al_por_Mayor["promedio"] <= 250)]
medianas_empresas_promedio = medianas_empresas_promedio.drop(columns = ['pesimista', 'optimista'])

medianas_empresas_optimista = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["optimista"] > 50) & (Comercio_al_por_Mayor["optimista"] <= 250)]
medianas_empresas_optimista = medianas_empresas_optimista.drop(columns = ['pesimista', 'promedio'])

print(len(medianas_empresas_pesimista))

print(len(medianas_empresas_promedio))

print(len(medianas_empresas_optimista))

#condiciones para empresas grandes, de 250 a más trabajadores ############################################
grandes_empresas_pesimista = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["pesimista"] > 250)]
grandes_empresas_pesimista = grandes_empresas_pesimista.drop(columns = ['promedio', 'optimista'])

grandes_empresas_promedio = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["promedio"] > 250)]
grandes_empresas_promedio = grandes_empresas_promedio.drop(columns = ['pesimista', 'optimista'])

grandes_empresas_optimista = Comercio_al_por_Mayor[(Comercio_al_por_Mayor["optimista"] > 250)]
grandes_empresas_optimista = grandes_empresas_optimista.drop(columns = ['pesimista', 'promedio'])

print(len(grandes_empresas_pesimista))

print(len(grandes_empresas_promedio))

print(len(grandes_empresas_optimista))
###############################################################################
###############################################################################
###############################################################################
"Comprobacion de agrupacion"
# Conjunto de valores que no estan dentro de ninguno de los anteriores debe ser 0
valores_residuales_pesimista = pd.concat([micro_empresas_pesimista, pequeñas_empresas_pesimista, medianas_empresas_pesimista, grandes_empresas_pesimista]).index
print(len(Comercio_al_por_Mayor.drop(valores_residuales_pesimista)))

valores_residuales_promedio = pd.concat([micro_empresas_promedio, pequeñas_empresas_promedio, medianas_empresas_promedio, grandes_empresas_promedio]).index
print(len(Comercio_al_por_Mayor.drop(valores_residuales_promedio)))

valores_residuales_optimista = pd.concat([micro_empresas_optimista, pequeñas_empresas_optimista, medianas_empresas_optimista, grandes_empresas_optimista]).index
print(len(Comercio_al_por_Mayor.drop(valores_residuales_optimista)))

###############################################################################
###############################################################################
###############################################################################

"Transformacion de los datos de variable a dummys"  
#Agrupa en el dataframe ya filtrado posteriormente

# Dummys según la columna "promedio" actualizada

#dummy generada con base a los valores de las micro-empresas
Comercio_al_por_Mayor["empresa_micro_pesimista"] = (
    (Comercio_al_por_Mayor["pesimista"] >= 0) &
    (Comercio_al_por_Mayor["pesimista"] <= 10)
).astype(int)

Comercio_al_por_Mayor["empresa_micro_promedio"] = (
    (Comercio_al_por_Mayor["promedio"] >= 0) &
    (Comercio_al_por_Mayor["promedio"] <= 10)
).astype(int)

Comercio_al_por_Mayor["empresa_micro_optimista"] = (
    (Comercio_al_por_Mayor["optimista"] >= 0) &
    (Comercio_al_por_Mayor["optimista"] <= 10)
).astype(int)

#dummy generada con base a los valores de las empresas pequeñas
Comercio_al_por_Mayor["empresa_pequeña_pesimista"] = (
    (Comercio_al_por_Mayor["pesimista"] > 10) &
    (Comercio_al_por_Mayor["pesimista"] <= 50)
).astype(int)

Comercio_al_por_Mayor["empresa_pequeña_promedio"] = (
    (Comercio_al_por_Mayor["promedio"] > 10) &
    (Comercio_al_por_Mayor["promedio"] <= 50)
).astype(int)

Comercio_al_por_Mayor["empresa_pequeña_optimista"] = (
    (Comercio_al_por_Mayor["optimista"] > 10) &
    (Comercio_al_por_Mayor["optimista"] <= 50)
).astype(int)

#dummy generada con base a los valores de las empresas medianas
Comercio_al_por_Mayor["empresa_mediana_pesimista"] = (
    (Comercio_al_por_Mayor["pesimista"] > 50) &
    (Comercio_al_por_Mayor["pesimista"] <= 250)
).astype(int)

Comercio_al_por_Mayor["empresa_mediana_promedio"] = (
    (Comercio_al_por_Mayor["promedio"] > 50) &
    (Comercio_al_por_Mayor["promedio"] <= 250)
).astype(int)

Comercio_al_por_Mayor["empresa_mediana_optimista"] = (
    (Comercio_al_por_Mayor["optimista"] > 50) &
    (Comercio_al_por_Mayor["optimista"] <= 250)
).astype(int)

#dummy generada con base a los valores de las empresas grandes
Comercio_al_por_Mayor["empresa_grande_pesimista"] = (
    (Comercio_al_por_Mayor["pesimista"] > 250)
).astype(int)

Comercio_al_por_Mayor["empresa_grande_promedio"] = (
    (Comercio_al_por_Mayor["promedio"] > 250)
).astype(int)

Comercio_al_por_Mayor["empresa_grande_optimista"] = (
    (Comercio_al_por_Mayor["optimista"] > 250)
).astype(int)


###############################################################################
###############################################################################
"Para exportar a Excel los data frames creados con las matrices posteriormente creadas de:"

#matriz limpia del sector con el total empresas que son formales de ese sector (primera hoja de excel)
#matriz de empresas grandes de ese sector   (segunda hoja de excel) 
#matriz de empresas medianas de ese sector  (tercera hoja de excel)
#matriz de empresas pequeñas  de ese sector (cuarta hoja de excel)
#matriz de empresas micro de ese sector     (quinta hoja de excel)

import openpyxl
import pandas as pd

# Ruta de salida del archivo Excel
ruta_salida = "S:\Edward Files\DENUE Limpias\DENUE_Actividades_gubernamentales.xlsx"

# Exportar varios DataFrames a un mismo archivo Excel en diferentes hojas
with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
    Comercio_al_por_Mayor.to_excel(writer, sheet_name='Actividades_gubernamentales', index=True)
    grandes_empresas_pesimista.to_excel(writer, sheet_name='Grandes Empresas Pesimista', index=True)
    grandes_empresas_promedio.to_excel(writer, sheet_name='Grandes Empresas Promedio', index=True)
    grandes_empresas_optimista.to_excel(writer, sheet_name='Grandes Empresas Optimista', index=True)
    medianas_empresas_pesimista.to_excel(writer, sheet_name='Medianas Empresas Pesimista', index=True)
    medianas_empresas_promedio.to_excel(writer, sheet_name='Medianas Empresas Promedio', index=True)
    medianas_empresas_optimista.to_excel(writer, sheet_name='Medianas Empresas Optimista', index=True)
    pequeñas_empresas_pesimista.to_excel(writer, sheet_name='Pequeñas Empresas Pesimista', index=True)
    pequeñas_empresas_promedio.to_excel(writer, sheet_name='Pequeñas Empresas Promedio', index=True)
    pequeñas_empresas_optimista.to_excel(writer, sheet_name='Pequeñas Empresas Optimista', index=True)
    micro_empresas_pesimista.to_excel(writer, sheet_name='Micro Empresas Pesimista', index=True)
    micro_empresas_promedio.to_excel(writer, sheet_name='Micro Empresas Promedio', index=True)
    micro_empresas_optimista.to_excel(writer, sheet_name='Micro Empresas Optimista', index=True)


#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°


"VERFICICAION DE LOS DATOS" ###################################################
#Se observa un valor de la columna  para ver si coinciden con las columnas anteriores
#Creacion de data frame nuevo sin modificar , filtrando columnas necesarias y agregando nuevas necesarias.

Comercio_al_por_Mayor_original['per_ocu'].unique() #para conocer que valores estan contenidos dentro de la columna ("per_ocu")
Comercio_al_por_Mayor_original['per_ocu'] = Comercio_al_por_Mayor_original['per_ocu'].replace({'251 y más personas': '251 a 500 personas'}) 

#se realiza un nuevo acomodo de la matriz con columnas de importancia
Comercio_al_por_Mayor_original = Comercio_al_por_Mayor_original[['clee', 'nom_estab', 'raz_social', 
                                                                 'per_ocu','codigo_act','nombre_act', 
                                                                 'entidad', 'municipio', 'id']].fillna(0) 

#se crean dos columnas del la matriz original con la poblacion maxima y minima para que sea comparable con las anteriores
Comercio_al_por_Mayor_original[['poblacion_minima', 'poblacion_maxima']] = Comercio_al_por_Mayor_original['per_ocu'].astype(str).str.extract(r'(\d+\.?\d*)\D*(\d+\.?\d*)')


###############################################################################
###############################################################################

#para verificar que no se repitan datos se filtra un valor por si solo, creando una matriz que filtre solo datos que lo tengan contenido  
#para corroborrar si todos los valores del dato dan el numero total de los otros data frames y que no este agrupando de mas.
#a su vez encontrar valores raros y poder identificarlos mas facilmente para ver si se estan filtrando o agrupando bien.

dato_especificado = Comercio_al_por_Mayor_original[Comercio_al_por_Mayor_original["raz_social"] == "BARCEL SA DE CV"] #se filtra por razon social un valor especifico

dato_especificado = dato_especificado.groupby('raz_social')[['poblacion_minima', 'poblacion_maxima',
                                             "promedio","codigo_act", 'nom_estab', 'raz_social', 
                                             'nombre_act']].sum(inplace = True)    #se agrupa conteniendo esas columnas en el data frame


#se generan nuevas columnas donde nos tenga los datos de la poblacion maxima,  minima y se calcula el promedio. 
#(para ver si coincide con los cuadros limpios)
dato_especificado['poblacion_minima'] = pd.to_numeric(dato_especificado['poblacion_minima'], errors='coerce')
dato_especificado['poblacion_maxima'] = pd.to_numeric(dato_especificado['poblacion_maxima'], errors='coerce')
dato_especificado["promedio"] = (dato_especificado["poblacion_maxima"] + dato_especificado["poblacion_minima"])/2

grandes_empresas_optimista['optimista'].quantile(0.25)
grandes_empresas_optimista['optimista'].quantile(0.50)
grandes_empresas_optimista['optimista'].quantile(0.95)
grandes_empresas_optimista['optimista'].quantile(1)

x = grandes_empresas_optimista[(grandes_empresas_optimista['optimista'] > 2500 )]

len(x)

"HISTOGRAMAS"####################################################################

import matplotlib.pyplot as plt

histograma_micro_empresas = pd.DataFrame({'pesimista' : micro_empresas_pesimista["pesimista"], 'promedio' : micro_empresas_promedio["promedio"], 'optimista' : micro_empresas_optimista["optimista"]})
histograma_pequeñas_empresas = [pequeñas_empresas_pesimista["pesimista"], pequeñas_empresas_promedio["promedio"], pequeñas_empresas_optimista["optimista"]]
histograma_medianas_empresas = [medianas_empresas_pesimista["pesimista"], medianas_empresas_promedio["promedio"], medianas_empresas_optimista["optimista"]]
histograma_grandes_empresas = [grandes_empresas_pesimista["pesimista"], grandes_empresas_promedio["promedio"], grandes_empresas_optimista["optimista"]]

for col in histograma_micro_empresas:
    plt.figure()
    plt.hist(histograma_micro_empresas[col], bins=30, edgecolor='black', alpha=0.7)
    plt.title(f'Distribución de {col}')
    plt.xlabel(col)
    plt.ylabel('Frecuencia')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()














