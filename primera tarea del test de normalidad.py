#librerias# paqueterias usadas para procesar y correr las funciones
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st 

#inputs# vectores que se les asigna un valor
coeff = 5
size = 10**6
random_variable_type = "normal" #variable aleatoria que se ocupara#
decimals = 5

#codigo# x = variable aleatoria | str_title = para las graficas
x= np.random.standard_normal(size=10**6)

#test de normalidad jarque bera# inputs
mu = st.tmean (x)
sigma = st.tstd(x)
skewness = st.skew(x)
kurtosis = st.kurtosis(x)


#codigo del test de normalidad# codigo
jb_stat = size/6 * (skewness**2 + 1/4*kurtosis**2)
p_value = 1 - st.chi2.cdf(jb_stat, df=2)
is_normal = (p_value > 0.0375)
  
  #titulo de la grafica , se le introducen los valores de las inputs#
str_title = "variable_normal aleatoria: \n" + \
    "mean=" + str(np.round(mu, decimals)) + " | " + \
    "volatility=" + str(np.round(sigma, decimals)) + "\n" + \
    "skewness=" + str(np.round(skewness, decimals)) + " | " + \
    "kurtosis=" + str(np.round(kurtosis, decimals)) + "\n" + \
    "JB stat=" + str(np.round(jb_stat, decimals)) + " | " + \
    "p-value=" + str(np.round(p_value, decimals)) + "\n" + \
    "is_normal=" + str(is_normal)


#grafica
plt.figure()
plt.hist(x, bins=100)
plt.title(str_title)
plt.show()


