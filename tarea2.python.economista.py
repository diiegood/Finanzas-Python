" tarea 2 practica de python para economsita" #con base a la secion 4 
"Jorge  Diego Valdez Fonseca"

#Se importa la libreria de numpy que es para gestion de matrices.
import numpy as np  #su llmamiento es con : np 

array1 = np.array([1,2,3,4,5])
array1

type(array1)

#numpy sirve para poder crear listas de matrices y funciones complejas con mayor velocidad
# y mayor cantidad de datos los cuales nos genera una ventaja de hasta 50% veces mas rapido

#el objeto matriz de numpy se llama --> ndarray 

valor = np.array([1,2,3,4,5,6,7,8,9])
valor[1]

valor = np.array([0], np.int16)
valor

x = np.array(range(7), dtype=int)
x[1] 
x

#x[1] = "is this a string"

#matrices multidimensionales (son las que siguen el mismo patron)


a = np.array([[1,3],[4,5]])
a

a = np.array([[1,0,0], [0,1,0],[0,0,1]])
a

a = np.arange(10)
a

a = np.ones((3,3)) #np.ones devuelve una matriz
a #asignandosele un tamaño a la matriz

a = np.linspace(0,10,20) #Devuelve numeros espaciados uniformemente
a #durante un intervalo especifico

X,Y = np.meshgrid([1,2,3],[4,5,6]) #Devuelve una tupla de matrices de coordenadas
X # a partir de vectores de coordenadas.

Y #matriz Y

a = np.zeros((3,3)) #Devuelve una nueva matriz de ceros
a

###############################################################################
############################# Apilamiento de matrices #########################

numeros_aleatorios = np.arange(5)
numeros_definidos = ([9,10,11,12,13])
numeros_aleatorios
numeros_definidos

np.hstack([numeros_aleatorios, numeros_definidos]) #apilamiento horizontal
np.vstack([numeros_aleatorios, numeros_definidos]) #apilamiento vertical

np.c_[numeros_aleatorios, numeros_aleatorios] #apilar colummnas
np.r_[numeros_definidos, numeros_definidos] #apilar filas

######################### Duplicacion de matrices Numpy #######################

x = list(range(1, 30))

x = np.arange(4)
x

np.repeat(x,3) #repite los valores de la matriz del 0 al 3

np.tile(x,(10,1)) 

matriz = np.arange(10).reshape(5,2)
matriz

matriz.transpose() #se transpone la matriz 

matriz.T #es la misma funcion que la de arriba

######################## Operacion de matrices logicas ########################

matriz_grande = np.arange(50).reshape(5,10) #se crea una matriz que va del 0 al 49
matriz_grande  #esta matriz tiene valores del 10 en 10 hasta el 50

matriz_grande[:,0]  #valores que tienen un cero

matriz_grande[4,:]  #valores que tienen un 4

############################ Unfuc de Numpy ###################################

#se crea una funcion
def myfunction (x,y):
    return x+y
myfunction = np.frompyfunc(myfunction,2,1)
myfunction([0,1,2,3],[9,10,11,12])

########################### Artimetica simple #################################

#suma: add
#resta: subtract
#multiplicacion: multiply
#division: divide
#potencia: power
#absoluto: abs

array1 = np.array([10,11,12,13,14,15])
array2 = np.array([20,21,22,23,24,25])

arr1_plus_arr2 = np.add(array1, array2) #funcion suma las matrices creadas
arr1_plus_arr2

arr1_arr2_rest = np.subtract(array1, array2) #se restan las matrices creadas
arr1_arr2_rest 

############################### Redondeo de decimales #########################

#Truncamiento elimina decimales y devuelve el numero mas cercano a un cero de un floot
#se usa  (.trunc o .fix)

#Redondeo: incremento del digito o decimal anterior en 1 si>5
#; de lo contrario, no hace nada,  (.around)

#Piso: redondea el decimal al entero inferior mas cercano (.floor)

#techo: redondeo del decimal al entero superior mas cercano (.ceil)

np.trunc ([-4.1666, 5.7667]) #se redondean los numeros al mas bajo

np.fix([-1.112312, 2.12312])  # se redondean los numeros al mas bajo

array0 = np.around(3.14163, 3) #muestra solo 3 decimales del numero
array0

array01 = np.floor([-4.2332340, 32.666237]) #rendondea al numero mas alto
array01

array02 = np.ceil([-4.2332340, 32.666237]) #muestra solo entero
array02

################################## Logaritmos #################################

#Base 2: usando       (.log2)
#Base 10: usando      (.log10)
#Base e o natural:    (.log)

array03 = np.arange(12, 120)
array03

np.log2(array03) #logaritmo a base 2 de la serie anterior

np.log10(array03) #logaritmo a base 10 de al serie anterior

np.log(array03) #logaritmo de la serie anterior

#se usa la funcion frompyfunc para tomar registro de cualquier base y math.log 
#para tener parametros de entrada y salida.

from math import log
import numpy as np
nplog = np.frompyfunc(log, 2, 1)
print(nplog(77, 5))