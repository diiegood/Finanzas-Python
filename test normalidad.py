import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import matplotlib.pyplot as plt
from scipy.stats import tmean, tstd, skew, kurtosis, chi2
import scipy.stats as st

# Inputs or values
coeff = 500
size = 10**6  # Power in Python is double **
random_variable_type = "normal"
# Options: normal, student, uniform, exponential, chi-squared
decimals = 5

# Code
str_title = random_variable_type
if random_variable_type == "normal":
    x = np.random.standard_normal(size=size)
elif random_variable_type == "student":
    x = np.random.standard_t(df=coeff, size=size)
    str_title += " df=" + str(coeff)
elif random_variable_type == "uniform":
    x = np.random.uniform(size=size)
elif random_variable_type == "exponential":
    x = np.random.exponential(scale=coeff, size=size)
    str_title += " scale=" + str(coeff)
elif random_variable_type == "chi-squared":
    x = np.random.chisquare(df=coeff, size=size)
    str_title += " df=" + str(coeff)

mu = tmean(x)
sigma = tstd(x)
skewness = skew(x)
kurt = kurtosis(x)

# For the normality test
jb_stat = size / 6 * (skewness**2 + 1/4 * kurt**2)
p_value = 1 - chi2.cdf(jb_stat, df=2)
is_normal = (p_value > 0.05)

str_title += "\n" + "mean=" + str(np.round(mu, decimals)) \
    + "|" + "volatility=" + str(np.round(sigma, decimals)) \
    + "\n" + "skewness=" + str(np.round(skewness, decimals)) \
    + "|" + "kurtosis=" + str(np.round(kurt, decimals)) \
    + "\n" + "JB stat=" + str(np.round(jb_stat, decimals)) \
    + "|" + "p-value=" + str(np.round(p_value, decimals)) \
    + "\n" + "is_normal=" + str(is_normal)

# Plotting
plt.figure()
plt.hist(x, bins=100)
plt.title(str_title)
plt.show()

# Running code separately
# Statistical test
n = 0
is_normal = True
str_title = "normal"

while is_normal and n < 500:
    x = np.random.standard_normal (size= 10**6)
    mu = st.tmean(x) #tmean
    sigma = st.tstd(x) #tstd
    skewness = st.skew(x) #skew
    kurt = st.kurtosis(x) #kurt
    #test de jarque bera#
    jb_stat = size/6 *(skewness**2 + 1/4*kurt**2)
    p_value = 1 - st.chi2.cdf(jb_stat, df=2)
    is_normal = (p_value > 0.05) #equivalently jb < 6
    print ("n=" + str(n) + "| is_normal=" +str(is_normal))
    n += 1
    

str_title += "\n" + "mean=" + str(np.round(mu, decimals)) \
    + "|" + "volatility=" + str(np.round(sigma, decimals)) \
    + "\n" + "skewness=" + str(np.round(skewness, decimals)) \
    + "|" + "kurtosis=" + str(np.round(kurt, decimals)) \
    + "\n" + "JB stat=" + str(np.round(jb_stat, decimals)) \
    + "|" + "p-value=" + str(np.round(p_value, decimals)) \
    + "\n" + "is_normal=" + str(is_normal)

plt.figure()
plt.hist(x, bins=100)
plt.title(str_title)
plt.show()
