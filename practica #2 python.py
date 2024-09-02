

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import matplotlib.pyplot as plt 
from scipy.stats import skew, kurtosis, chi2 

#imputs# #son los valores que se le asigna a las distribuciones#
coeff = 10 #en la exponencial modifica la escala de x#
scale= 50
degrees_freedom = 7  #son los grados de libertad#
size = 10**6    
nb_sims= 10**6
k= 10  #para la chi-squared (grados de libertad#
decimals = 4 #decimales que va mostrar#

random_variable_type = "chi-square"  #entradas de la variable#
#normal, student, uniform, exponential, chi-squared#
x = np.random.chisquare(df=k, size=10**6)   
#para estas funciones primero se debe importar la libreria#
#import scipy #
#funcion de skwness#
#from scipy.stats import skew#
#funcion de kurtosis#
#from  scipy.stats  import kurtosis as krt #

#funcion de chi-cuadrada#
from scipy.stats  import chi2 
#code#
#str_tittle = random_variable_type#

if random_variable_type == "normal":
   x = np.random.standard_normal(size = 10**6)
elif random_variable_type == "student":
   x = np.random.standard_t(df=coeff, size=size)
   str_tittle ="df="  + str(coeff)
elif random_variable_type == "exponential":
   x = np.random.uniform(size=size)
   str_tittle = str_tittle + " scale=" + str(coeff)
elif random_variable_type ==  "chi-squared":
    x = np.random.chisquare(df=k, size=10**6)   
    
mu = np.mean(x)  
sigma = np.std(x)
  
kurt= kurtosis(x)  #en este caso se indica que la variable curtosis es x#
#la cual se muestra en la tabla de explorador de variables con el valor #

skew = skew(x) #la variable que tiene skwe que calcula la skewness/asimetria#

#con este se pone un titulo con doble renglon y muestra el valor de la skew#
str_tittle = "\n" +"mean=" +str(np.round(skew,decimals)) \
+"\n" + "kurtosis="  +str(np.round(kurt,decimals)) \
+"\n" + "skewness="  +str(np.round(skew,decimals)) \
+"\n" + "volatility=" +str(np.round(sigma,decimals)) \
  # x= np.random.exponential(scale=coeff, size=size)#
#plote-graficacion#
plt.figure()
plt.hist(x,bins=100)
plt.title(random_variable_type)
plt.show()




 
 