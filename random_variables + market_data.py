# Data Frame convertir rendimientos en fechas para serie de tiempo
# Creación de data frame con valores para crear el vector de rendimiento
# Pandas puede calcular vectores de las tablas, operaciones con tablas como si fueran matrices 

################################   Librerías ##################################

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import scipy.stats as st
import os

######################### Directorio + datos que jala #########################
# Inputs
ric = 'AAPL'  # 1

# Definir el directorio donde se encuentran los archivos
directorio = 'C:\\Users\\creep\\.spyder-py3\\stocks\\'  # 2

# Leer el archivo CSV
path = os.path.join(directorio, f"{ric}.csv")
raw_data = pd.read_csv(path)  # Entrada para leer csv

###############################################################################
# DATA FRAME Y VECTORES DE PRECIOS PARA EL RENDIMIENTO Y LA SERIE DE TIEMPO #

t = pd.DataFrame()  # Crear un nuevo data frame vacío.

# Proceso de datos para realizar los cálculos
t["date"] = pd.to_datetime(raw_data["Date"], dayfirst=True, errors='coerce')  # Convertir la columna "Date" a datetime
t["close"] = raw_data["Close"]  # Asignar la columna "Close"
t = t.sort_values(by="date", ascending=True)  # Ordenar por fecha
t["close_previous"] = t["close"].shift(1)  # Crear columna del cierre anterior

# Calcular el rendimiento del activo
t["return_close"] = t["close"] / t["close_previous"] - 1
t = t.dropna()  # Eliminar filas con valores NaN
t = t.reset_index(drop=True)  # Reiniciar el índice

######################## Funcion del objeto simulador #########################

class SimulationInputs:
    def __init__(self):
        self.df = None
        self.scale = None
        self.mean = None
        self.std = None
        self.rv_type = None
        self.size = None
        self.decimals = None

class Simulator:
    # Constructor
    def __init__(self, inputs):
        self.inputs = inputs
        self.str_title = None
        self.vector = None
        self.mean = None
        self.volatility = None
        self.skewness = None
        self.kurtosis = None
        self.jb_stat = None
        self.p_value = None
        self.is_normal = None
        
    def generate_vector(self):
        self.str_title = self.inputs.rv_type
        if self.inputs.rv_type == 'standard_normal':
            self.vector = np.random.standard_normal(self.inputs.size)
        elif self.inputs.rv_type == 'normal':
            self.vector = np.random.normal(self.inputs.mean, self.inputs.std, self.inputs.size)
        elif self.inputs.rv_type == 'student':
            self.vector = np.random.standard_t(df=self.inputs.df, size=self.inputs.size)
            self.str_title += f' df={self.inputs.df}'
        elif self.inputs.rv_type == 'uniform':
            self.vector = np.random.uniform(size=self.inputs.size)
        elif self.inputs.rv_type == 'exponential':
            self.vector = np.random.exponential(scale=self.inputs.scale, size=self.inputs.size)
            self.str_title += f' scale={self.inputs.scale}'
        elif self.inputs.rv_type == 'chi-squared':
            self.vector = np.random.chisquare(df=self.inputs.df, size=self.inputs.size)
            self.str_title += f' df={self.inputs.df}'
            
    def compute_stats(self):
        self.mean = st.tmean(self.vector)
        self.volatility = st.tstd(self.vector)
        self.skewness = st.skew(self.vector)
        self.kurtosis = st.kurtosis(self.vector)
        self.jb_stat = self.inputs.size / 6 * (self.skewness**2 + 1/4 * self.kurtosis**2)
        self.p_value = 1 - st.chi2.cdf(self.jb_stat, df=2)
        self.is_normal = (self.p_value > 0.05)  # Equivalente a jb < 6
        
    def plot(self):
        self.str_title += f'\nmean={np.round(self.mean, self.inputs.decimals)} | volatility={np.round(self.volatility, self.inputs.decimals)}' \
                          f'\nskewness={np.round(self.skewness, self.inputs.decimals)} | kurtosis={np.round(self.kurtosis, self.inputs.decimals)}' \
                          f'\nJB stat={np.round(self.jb_stat, self.inputs.decimals)} | p-value={np.round(self.p_value, self.inputs.decimals)}' \
                          f'\nis_normal={self.is_normal}'
        plt.figure()
        plt.hist(self.vector, bins=100)
        plt.title(self.str_title)
        plt.show()

################################ Inputs para la simulación ###################
inputs = SimulationInputs()
inputs.rv_type = ric + '| real time '
inputs.decimals = 5  # Decimales a mostrar

# Cálculos y simulación
sim = Simulator(inputs)
sim.vector = t['return_close'].values # Generar vector
sim.inputs.size = len(sim.vector)
sim.str_title = sim.inputs.rv_type
sim.compute_stats()  # Calcular estadísticas
sim.plot()  # Graficar

