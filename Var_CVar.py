import numpy as np
import pandas as pd
import matplotlib as mplt
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2

#inputs para generar el vector de variables aleatorias 
x_size = 10**6
degrees_freedom = 2 
type_random_variable = "normal"
        
#se genera las funciones condicionales por si es de diferente distribucion
        
if type_random_variable == "normal":
   x = np.random.standard_normal(size=x_size)
   x_str = type_random_variable
elif type_random_variable == "exponential":
    x = np.random.standard_exponential(size = x_size)
    x_str = type_random_variable
elif type_random_variable == "student":
    x = np.random.standard_t(size= x_size, df=degrees_freedom)
    x_str = type_random_variable + '(df= ' + str(degrees_freedom) + ')'
elif type_random_variable == "chi-squared":
    x = np.random.chisquare( size=x_size, df=degrees_freedom)
    x_str = type_random_variable + '(df= ' + str(degrees_freedom) + ')'
                        
#compute "risk metrics" / inputs para medir el riesgo / en mexico se usa VaR 99.5%
round_digits = 4
x_mean = np.mean(x)
x_stdev = np.std(x)
x_skew = skew(x)
x_kurt = kurtosis(x)  #exceso de curtosis
x_var_95 = np.percentile(x, 5) #mayor perdida esperada en el percentil
x_Cvar_95 = np.mean(x[x<= x_var_95]) #deficit esperado en promedio de la izquierda  
#CVaR teniendo el vector x se queda solo con los valores mas pequeños que el valor en riesgo (VaR) 
x_sharpe = x_mean / x_stdev * np.sqrt(252)                     #metrica de riesgo
jb = x_size/6*(x_skew**2 + 1/4*x_kurt**2)
p_value = 1 - chi2.cdf(jb, df=2)
is_normal = (p_value > 0.05)  #equivalently jb < 6
#para que sea una variable normal aleatoria el p-value debe ser mayor a 0.05
                    
#jarque_bera_str = 'mean' + str(np.round(x_mean,round_digits))\
#        + '/desv stand ' + str(np.round(x_stdev,round_digits))\
#        + '/skewness ' + str(np.round(x_skew,round_digits))\
#        + '/kurtosis ' + str(np.round(x_kurt,round_digits))\
#        + '/Sharpe ratio ' + str(np.round(x_sharpe,round_digits))
#plot_str = '/VaR 95% ' + str(np.round(x_var_95,round_digits))\
#        + '/CVaR 95% ' + str(np.round(x_Cvar_95,round_digits))\
#        + '/jarque_bera ' + str(np.round(jb,round_digits))\
#        + '/p_value ' + str(np.round(p_value,round_digits))\
#        + '/is_normal ' + str(is_normal)


#print metrics | se muestran los resultaos obtenidos 
print(x_str) #para mostrar que distribucion estamos viendo
print("mean " + str(x_mean))
print("std " + str(x_stdev))
print("skewness " + str(x_skew))
print("kurtosis " + str(x_kurt))
print("VaR 95% " + str(x_var_95)) #intervalo de confianza del 95% , se habla con un error del 5%, perdida en percentil de 5% 
print("CVaR 95% " + str(x_Cvar_95)) #promedio del intervalo de perdida a la izquierda del 5%
print("Jarque_Bera " + str(jb))
print("p-value " + str(p_value))  #el p value debe ser mayor a 0.05 osea mayor del 5%
print("is normal " + str(is_normal))
                    
                    
#Al calcular la estadistica de Jarque bera siginifica que esta en .78
                    
#Se grafica el histograma 
                    
#plot histogram
plt.figure()
plt.hist(x, bins=100)
plt.title("Histogram " + x_str)
plt.show()
            

