import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import matplotlib.pyplot as plt
from scipy.stats import tmean, tstd, skew, kurtosis, chi2

#imputs o valores#
coeff = 5000
#diferencial de student, chi-squared, scale in exponential#
size = 10**6  #potencia en python es doble ** #
random_variable_type = "student"
#options:normal student uniform exponential chi-squared"
decimals = 5

#code#
str_title = random_variable_type
if random_variable_type == "normal":
    x = np.random.standard_normal(size = 10**6)
elif random_variable_type =="student":
    x = np.random.standard_t(df=coeff, size=size)
    str_title = str_title + "df=" +str(coeff)
elif random_variable_type == "uniform":
    x= np.random.uniform(size=size)
elif random_variable_type == "exponential":
    x = np.random.exponential(scale=coeff, size=size)
    str_title += "scale=" + str(coeff)
elif random_variable_type == "chi-squared" :
    x = np.random.chisquare(df=coeff, size=size)
    str_title += "df=" + str(coeff)
    
mu = np.mean(x)
sigma = np.std(x)
skew = skew(x)
kurt = kurtosis (x)

#test de normalidad Jarque Bera#
jb_stat = size/6 * (skew**2 + 1/4*kurt**2)
p_value = 1 - chi2.cdf(jb_stat, df=2) 
#calculo de la integral de p value a cero restandole 1 - la integral
is_normal = (p_value > 0.05) #equivalently jb < 6 
#ara bajo la curva, si la probabilidad de tener datos es mayor a 5% 
#jarque bera tiene que ser menor que 6
#si la probabilidad es menor, el punto es extremo
#probabilidad es < 5%, variable aleatoria no paso el test de normalidad


str_title += "\n" + "mean=" + str(np.round(mu, decimals)) \
    + "|" + "volatility=" + str(np.round(sigma, decimals))\
     + "\n" + "skewness=" + str(np.round(skew, decimals)) \
     + "|" + "kurtosis=" + str(np.round(kurt,decimals)) \
     + "\n" + "kurtosis=" + str(np.round(kurt,decimals)) \
         + "|" + "JB stat=" + str(np.round(jb_stat, decimals)) \
             + "/n" + "p-value=" + str(np.round(p_value, decimals)) \
             + "|" + "is_normal=" + str(is_normal)
    
              
#plot graficacion#
plt.figure()
plt.hist(x,bins=100)
plt.title(str_title)
plt.show()




         
         
         
         
         
         
         
         
         
         
         
         
