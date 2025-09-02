import pandas as pd
import os

#Carga del archivo y los diccionarios

ii_pe_ecic = pd.read_excel('S:\Edward Files\CPIS\ii_pe_ecic - aleatorios.xlsx','COPIA')

df_clasif_mdo = pd.read_excel('S:\Edward Files\CPIS 2.0\Diccionarios.xlsx', "clasif_mdo")

df_pais = pd.read_excel('S:\Edward Files\CPIS 2.0\Diccionarios.xlsx', "paises")

df_moneda = pd.read_excel('S:\Edward Files\CPIS 2.0\Diccionarios.xlsx', "monedas")

df_sector = pd.read_excel('S:\Edward Files\CPIS 2.0\Diccionarios.xlsx', "sector")

#Corrección organismo internacional

ii_pe_ecic.loc[ii_pe_ecic['sector_esp'].str.contains("organismo internacional", na=False), 'residencia_legal'] = "organismo internacional"

#Recortamos espacios en las variables de interes y cambiamos NaN por celdas vacías

ii_pe_ecic['clasif_mdo'] = ii_pe_ecic['clasif_mdo'].str.strip().fillna('')

ii_pe_ecic['residencia_legal'] = ii_pe_ecic['residencia_legal'].str.strip().fillna('')

ii_pe_ecic['oficinas_principales'] = ii_pe_ecic['oficinas_principales'].str.strip().fillna('')

ii_pe_ecic['moneda_esp'] = ii_pe_ecic['moneda_esp'].str.strip().fillna('')

ii_pe_ecic['sector_esp'] = ii_pe_ecic['sector_esp'].str.strip().fillna('')

#Creamos los diccionarios para corregir typos y convertir las variables a inglés

dic_clasif_mdo = dict(zip(df_clasif_mdo['español'], df_clasif_mdo['ingles']))

dic_pais = dict(zip(df_pais['español'], df_pais['ingles']))

dic_moneda = dict(zip(df_moneda['español'], df_moneda['ingles']))

dic_sector = dict(zip(df_sector['español'], df_sector['ingles']))

#Reemplazamos usando los diccionarios

ii_pe_ecic['clasif_mdo'] = ii_pe_ecic['clasif_mdo'].replace(dic_clasif_mdo)

ii_pe_ecic['residencia_legal'] = ii_pe_ecic['residencia_legal'].replace(dic_pais)

ii_pe_ecic['oficinas_principales'] = ii_pe_ecic['oficinas_principales'].replace(dic_pais)

ii_pe_ecic['moneda_esp'] = ii_pe_ecic['moneda_esp'].replace(dic_moneda)

ii_pe_ecic['sector_esp'] = ii_pe_ecic['sector_esp'].replace(dic_sector)

#Verificamos la unicidad de los registros en cada variable

print(sorted(ii_pe_ecic['clasif_mdo'].unique()))

print(sorted(ii_pe_ecic['residencia_legal'].unique()))

print(sorted(ii_pe_ecic['oficinas_principales'].unique()))

print(sorted(ii_pe_ecic['moneda_esp'].unique()))

print(sorted(ii_pe_ecic['sector_esp'].unique()))

#Añadimos la columna de códigos

df_codigo = pd.read_excel('S:\Edward Files\CPIS 2.0\Diccionarios.xlsx', "codigo")

dic_codigo = dict(zip(df_codigo['pais'], df_codigo['codigo']))

ii_pe_ecic['codigo'] = ii_pe_ecic['residencia_legal'].replace(dic_codigo)

print(sorted(ii_pe_ecic['codigo'].unique()))

#Fijamos nuestro directorio de salida

os.chdir('S:\Edward Files\CPIS 2.0')

#Exportamos nuestro archivo

ii_pe_ecic.to_excel('ii_pe_ecic_limpio.xlsx', index = False)
