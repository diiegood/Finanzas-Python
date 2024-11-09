#como puedo hacer un modelo consturctor de python con dos modulos diferentes


#se importan las librerias #
import  yfinance as yf 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

#se crea la funcion ticker para el activo
ticker = yf.Ticker("AAPL")

#poner el parametro de obtencion de datos en el periodo 
apple = ticker.history(period="1mo")

print(apple)  

apple['Rendimiento'] = apple['Close'].pct_change() 
plt.figure(figsize=(10, 5))
plt.plot(apple.index, apple['Rendimiento'], marker='o', linestyle='-')
plt.title('Rendimientos diarios de AAPL (últimos 30 días)')
plt.xlabel('Fecha')
plt.ylabel('Rendimiento diario')
plt.grid()
plt.show() 


rendimientos_cuadro = apple[['Close', 'Rendimiento']]
print(rendimientos_cuadro)

# Graficar los rendimientos
plt.figure(figsize=(10, 5))
plt.plot(apple.index, apple['Rendimiento'], marker='o', linestyle='-')
plt.title('Rendimientos diarios de AAPL (últimos 30 días)')
plt.xlabel('Fecha')
plt.ylabel('Rendimiento diario')
plt.grid()
plt.show()

#Practica 2 para analisis de inf bursatil # 

# create ticker for Apple Stock
ticker = yf.Ticker('AAPL')
# get data of the most recent date
todays_data = ticker.history(period='1d')

print(todays_data)


#para obtener datos de la FED

import pandas_datareader.data as web
import datetime

# Define las fechas de inicio y fin
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2024, 9, 21)

# Obtén datos de la serie de tasas de interés (por ejemplo, la tasa de fondos federales)
df = web.DataReader('FEDFUNDS', 'fred', start, end)

print(df)

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2024, 9, 21)

# Obtén datos de la serie de tasas de interés (por ejemplo, la tasa de fondos federales)
df = web.DataReader('FEDFUNDS', 'fred', start, end)

# Grafica los datos
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['FEDFUNDS'], label='Tasa de Fondos Federales', color='blue')
plt.title('Tasa de Fondos Federales (FEDFUNDS)')
plt.xlabel('Fecha')
plt.ylabel('Tasa (%)')
plt.grid()
plt.legend()
plt.show()





#python para correo 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(remitente, destinatario, asunto, mensaje, contrasena):
    # Configurar el servidor SMTP
    servidor = "smtp.gmail.com"
    puerto = 587

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        # Conectar al servidor
        with smtplib.SMTP(servidor, puerto) as server:
            server.starttls()  # Activar TLS
            server.login(remitente, contrasena)  # Iniciar sesión
            server.send_message(msg)  # Enviar el mensaje
        print("Correo enviado con éxito.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Configura tus datos
remitente = "tu_correo@gmail.com"
destinatario = "destinatario@gmail.com"
asunto = "Notificación"
mensaje = "Este es un mensaje de notificación."
contrasena = "tu_contrasena"

# Enviar el correo
enviar_correo(remitente, destinatario, asunto, mensaje, contrasena)
#Autenticación: Si usas Gmail, es posible que necesites habilitar "Acceso de aplicaciones menos seguras" en la configuración de tu cuenta o usar un "App Password" si tienes habilitada la verificación en dos pasos.

#Seguridad: No incluyas contraseñas directamente en el código. Considera usar variables de entorno o un archivo de configuración.

#Otras plataformas: Si no usas Gmail, necesitarás cambiar el servidor SMTP y el puerto según tu proveedor de correo