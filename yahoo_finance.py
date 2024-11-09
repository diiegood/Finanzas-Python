import pandas as pd 
import yfinance as yf
import random_variables

print(random_variables)

#equity americano / tickers 
"AMZN, META, GOOGL, AAPL, ^GSPC, CL=F "

#activo = yf.Ticker("AAPL")
#activo2 = yf.Ticker("GOOGL")
#activo3 = yf.Ticker("AMZN")
#activo4 = yf.Ticker("^GSPC")

#acciones = [activo, activo2, activo3, activo4 ]
#acciones

#activo_apple = activo.history(period= "1mo")
#activo_google =  activo2.history(period = "1mo")
#activo_amazon =  activo3.history(period = "1mo")
#activo_SP500 = activo4.history(period = "1mo")

#activo_inversionistas = activo.major_holders
#activo_inversionistas
#activo_cashflow = activo.balance_sheet
#activo_cashflow
################################ Equity Mexicano ##############################
#periodos de los tikcers precios del DataFrame

#en minutos “5m” y “5d” pero solo en periodo de 5 dias / 1d” y “5y” intervalor diario en 5 años
#en dias "1d, 5d, 10d, 15d, 30d"
#en meses "1mo, 3mo, 6mo"
#en años "1y, 2y, 5y, 10y"


GAPB = yf.Ticker("GAPB.MX")
activo_GAPB = GAPB.history(period="3mo")
activo_GAPB

Grupo_Carso = yf.Ticker("GCARSOA1.MX")
grupo_carso = Grupo_Carso.history(period = "3mo")
grupo_carso

Inbursa = yf.Ticker("4FY.SG")
GFI = Inbursa.history(period = "3mo")
GFI

###################### Practica de importaciono de modulos ####################

def funcion_yahoo():
    print("aqui hay apis de yahoo")

def saludar():
    print("hola")
    
def decir_hola():
    print("Hola Mundo")

def funcion_lista():
    x = [1,2,4,45,6]
    return x


class Punto:
 def __init__(self):
        print("Esto es el init")
        

        
