"""
Primera Tarea python conceptos basicos de clase 1:3
Curso de Python para Economista
@author: Jorge Diego Valdez Fonseca
"""
######################Nociones basicas tipos de caracteres#####################

base = 20 
altura = 5 
area = base * altura 
print(area) #para ver el resultado del comando
area #tambien poner directamente la variable para el resultado

int(1.3532) #valor entero del numero 1.3532 -> 1
float(2)   #valor decimal del valor 2 ->  2.0
#es la union de varios strings en una funcion
mi_nombre = "Hola" + "me" +"llamo" + "Diego"
mi_nombre*2 #se triplica la funcion 2 veces#
mi_nombre[0:3] #letras del cero a 3 de la funcion
mi_nombre[-2] #ultimas 2 letras de la funcion

mi_nombre = "Hola me llamo Gustavo"
print(mi_nombre) #para arrojar el resultado de la funcion mi_nombre
mi_nombre.replace("Gustavo", "Diego")

'Este es el numero de pi %d' %(3.1416) #%d #para reposicionar un valor
"Este es el numero de pi %.2f" %(3.1416)
############################# CORREGIR LO DE ARRIBA #############################

#Nociones basicas python# las listas siempre son con corchetes
#listas []
numeros_enteros = [1,2,3,4,5] #lista de valores int
numeros_decimales = [1.25, 35.2, 3.1416, 2.678] #lsita de valores float
palabras = ["perro", "gato", "vibora", "tlacuache"] #lista de valores string
numeros_enteros 
numeros_decimales
palabras

#lista, conformado por diferentes variables#
mix = [3, "pepe", 3.1416, [1,2,3,4]] 
mix

mix [0] #empieza desde el principio#
mix [-2] #empieza desde el final el segundo elemento#

mix [ 0 ] = "perro" #sustituye el elemento cero de la lista #
mix

lista = mix[0:3]
lista

nueva_lista = mix[0:3] + lista #se le agrega la sublista ##lista##
nueva_lista #esta es una nueva lista que incluye 2 listas#

len(nueva_lista) #esta funcion nos indica cuandos valores hay en lista

del nueva_lista [0] #eliminar el objeto 1 de la lista
nueva_lista #se elimino el valor "perro"

sorted ([1,5,3,9,2,32]) #funcion para ordernar valores ascedente


x = [1,3,50,12,8,32,5]   #funcion para ordenar la lista#
x.sort()
x
x[0] #para mandar a llamar el elemento 0
x.remove(1) #se remueve el valor 0 "1"
x[0] #ahora el elemento 0 es "3"
x.sort(reverse=True)
print(x)

animales = ["perro", "mono", "chango"]
frutas = ["manzana", "pera", "durazno"]
animales.append(frutas) #funcion para agregar cosas al final de la lista
animales  #a la lista de animales se le agregaron las frutas#

carros = ["bmw", "mercedes", "mini"]
x = carros.pop(1) #con esta funcion remueve el elemento 1
carros #solo esta bmw, mini

numeros_aburridos = 1,2,3
numeros_aburridos 

#####################  ARRAYS #######################
import array

# Crear un array de enteros
array_pirata = array.array('i', [1, 2, 3, 4, 5])
# Accediendo a los elementos
print(array_pirata[0])  
# Modificando un elemento
array_pirata[2] = 10
print(array_pirata)  

############################ Numpy###########################

import numpy as np
numeritos = np.array([1,2,3,4,5])
print(numeritos[3])
numeritos[2] = 10
print(numeritos)

#evaluar al cuadrado la funcion
numeritos_al_cuadrado = numeritos **2
numeritos_al_cuadrado

#calcular media con numpy
media_numeritos = np.mean(numeritos)
media_numeritos

#hacer la sumatoria con numpy
sumadevalores = np.sum(numeritos_al_cuadrado)
sumadevalores

 ###Tuple###   va con parentesis ()
 
carros = ("bmw", "mercedes", "mini") #vector todos deben ser de la mimsa naturaleza#
type(carros) #con parecentesis son tuple que es como un vector#
carros * 3 
nueva_lista + frutas #sumatoria de 2 listas#
#las tuplas no son editables#
#casi no se usan#
#no se le pueden sobreescribir elementos a las tuple#
#Se pueden usar para algo que no se sobreescriba o permute#

###########bucles##########

x,y,*z = 1,2,3,4,5  #se flitran los ultimos 3 valores correspondientes a z
print(x,y,z)       #se ven los ultimos valores 3,4,5

x,*y,z = 1,2,3,4,5  #se filtran los valores 3 valores correspondientes a y 
print(x,y,z)         #se ven los valores de y de enmedio 2,3,4

*x,y,z = 1,2,3,4,5  #se filtran los primeros 3 valores de x
print(x,y,z)        #se filtran los valores 1,2,3

#DICCIONARIOS#  se usan los valores de las llaves {}
x= {"key":"value"}   #le das un valor a un objeto sirve para una clasificacion
x["key"]
x

Cetes = {"Cete" : "Renta_fija", "valor_nominal":"diez_varos", "periodo": "noventa_y_uno_dias"}
Cetes
Cetes["propiedad"] = "Julio"  #para agregar una nueva informacion, en este caso el dueño"
Cetes

del Cetes["propiedad"] #se le elimina su propiedad al dueño
Cetes

#Union de diccionarios# 
CETES = {"periodo1": 28, "periodo2": 90, "periodo3": 180 }
Tasas = {"Periodo1": 10.10, "Periodo2": 10.35, "Periodo3": 10.56}
dict(CETES, **Tasas)

{**CETES,**Tasas}

#set conjuntos# 

set([1,2,11,1])
set([1,2,3]) ^ set ([2,3,4])

#para hacer bucles con python# 

#sirven para que implementen iteraciones, ejecuten un mismo bloque de codigo
#dos o mas veces mientras se cumple la condicion declarada#

for i in range(3): #recorre una cantidad especifica de veces#
    print(i)        #observa que parte desde el elemento 0
    
for i in range (1, 25): #valores de 5 a 11, pero no incluye el 200.
    print(i)
    
#else es pra determinar si el bucle sale con break o no#
for i in [1,10,19]:
    if i > 20:  #condicion del bucle
        break #detiene el bucle antes de que haya recorrido todos los elementos
else:  #y si no se cumple la condicion#
  print("Aqui no sucede i>20!")

for i in [1,10,19,21]:
    if i>20:
        break
else:
    print("valor incorrecto")

i = 4
while 1 < 3:
    i += 1 
print(i)


i = 0 
while i < 6:
    i += 1
    if i == 3:
        continue  #detiene la iterecacion actual del bucle y continua la siguiente
    print(i)

gustos = ["dormir", "comer", "jugar"]
niños = ["felipe", "gustavo", "mariana"]

for x in gustos:
    for y in niños:
        print(x,y)
        
#operadores logicos # VALORES BOLEANOS
#None
#False
#cero de cualquier numerico
#cualquier matriz o conjunto vacio
#clases definidas por el usuario, nonzero(), len()


bool ([])  

bool ([0])

bool([0,])

#se pueden usar or, not, and

1<2 and 2<3 or 3<1 #la primera no es condicional , la 2 y 3 si solo una puede ser#
#se cumple 1<2 , pero una de los siquientes se debe cumplir#

1<2 and not 2>3 or 1<3

(1,2,3) < (4,5,6)
 
(1,2,3) < ( 0,1,2)

camaron = [1,2,3]
[2,3,4] > camaron 

(1,2,3) < (5,2) #deben ser dos grupos para poder compararse

"one" in [22,["dos", "mascota", "arriba"]]
#one esta en esta lista de los elementos# falso

"dos" in [22,["dos", "mascota", "arriba"]]
#por que no esta dentro de la lista#

#se vuelve verdadero porque deja de ser elemento independiente y esta dentro
print("tres" in ["caracol", "tres", "ganso", ["perro"]])
# Esto es verdadero porque "tres" es un elemento independiente en la lista


# not in / no esta en 
# in / esta en 

"uno" in []

x = "es un string"
y = "es un string" 
x is y 
# a pesar de tener los mismos valores no son la misma funcion# 

x=y= "este es un string" 
id(x),id(y)   #identificador del codigo de python
x is y #se cumplen por que son lo mismo 

# NOCIONES BASICAS DE PYTHON PARTE 2  # 

############################### Bucles #################################

for i in range (3):  #recorre una cantidad especifica de veces
    print (i)  # observa que parde es desde el elemento 0

for i in range (10, 100): #observa valores de 10 a 100 / parte del 10 al 99
    print(i) 
    
#funciones:
    "for" #señala los elementos de donde parte
    "range" #selecciona el rango en una lista desde el inicio al final
    "while" #condicionador, de cuando se pone en marcha
    "else" #se usa para determinar el bucle si tiene un: #break#
    "break" #funcion de stop para el bucle 
    
funcion = [1,10,19]
funcion
   
for funcion in [1,10,19]:
    if funcion>20: #condicionador del bucle
      break #detiene la funcion antes de recorrer todos los elementos

else: #condicional de si no se cumple la condicion
    print("No paso nada") #mensaje que sale por el condicional

for edades in [5,10,15,17,12]:
    if edades >18:
        break
else:
    print("Son menores de edad")
    
i = 0 
while i < 3:
    i += 1
    print("i")

# Este bucle continua hasta que la expresion sea falsa # 

i = 5
while i < 3:
    i += 1 
    print(i)
    
    
#serie de bucle para parar en un valor y continuar en el siguiente#
i = 0
while i < 6:
    i +=1
    if i ==3:
        continue  #detiene la serie del bucle en 3 y continua en la siguiente
    print(i)
 #deteine la iteracion actual del bucle y continua con la siguiente

    ############################ SUMA DE MATRICES ############################
mercado = ["abarrotes", "pescaderia", "carniceria", "tienda de pinturas"]
clientes = ["Pancho", "Javier", "Fernanda", "Jessica"]

for x in mercado:
    for y in clientes:
        print(x,y)


###############################################################################
############################ -Operadores Logicos- #############################

"Funciones logicas"

# None
# False
# Cero de cualquier tipo numerico 0; Oj; OL; 0.0
# Cualquier vector o matriz, conjunto, lista, diccionario vacio o funcion vacia
# Clases que hayan sido definidas por el usuario:
   # Nonzero()
   # len()
"En estas clases el metodo devuelve el cero o valor boleano False"

bool([]) #lista vacia

bool({}) #diccionario vacio

bool(0)


bool([0,]) #Esta lista no esta vacia

3.2 < 10 < 20 

True

#Se pueden usar disyunciones (or), negaciones (not) y conjunciones (and).
1<2 and 2<3 or 3<1 #En este caso nos indica la primera funcion 1<2 y
#por lo que la 2da y 3ra una tiene que ser verdadera

1<2 and not 2>3 or 1<3 

#El parentesis indica una funcion donde se realiza comparaciones 
# de la misma naturaleza de la funcion.

(1,2,3) < (4,5,6) #indica que el valor de la comparacion de conjuntos es verdadero

(1,2,3) < (0,1,2) #la comparacion de conjuntos es falsa

#No se puede usar Comparaciones de funciones con strings, se usa correspondencia
#que son funciones con ==, siendo pruebas asociadas a la clave  "in"
"tres" in [1,["uno", "dos", "tres"]]
#se pregunta si esta elemento "tres" dentro de este conjunto

"cuatro" in [1,["uno", "dos", "tres"]] #se pregunta si esta este valor en la funcion

"tres" in [1, "tres", ["uno", "dos" ]] #debe de estar en la funcion principal
#para ser verdadero el valor de que pertenezca a ese conjunto

["perro", "camaleon",] not in [2,"dos",["perro", "camaleon"]]
#los valores si estan dentro de la funcion por eso es falso

["perro", "camaleon"] in [2, "dos", ["perro", "camaleon"]]
#los valores estan dentro de la funcion por eso es verdadero 

#Igualdad de funciones, cuando tiene las mismas variables
x = "uno", "dos", "tres"
y = "uno", "dos", "tres"
x is y 
#a pesar de tener las mismas variables son funciones independientes la una de 
#la otra

x == y #igualacion de funciones

#se puede comprobar el ID de los valores
x = y = "funciones"
id (x), id(y)
#muestra el ID de x , y

"Funcion de Singleton"
#Son patrones de diseño para crear una clase durante la vida util del programa
"sirve para limitar el acceso simultaneo a un recurso"
"sirve para crear un llave de identficador global a ese valor"
"sirve para una instancia de clase durante la vida util del programa"

###############################- Condicionales -###############################

#logicas matematicas 

a = 5
b = 3
a == b  #es igual a
a != b #no es igual
a < b #menor que 
a <= b #menor igual que
a > b #mayor que
a >= b #mayor igual que 

if 1 < 2:
    print("uno menos que dos")
    
a = 10
b = 25
if b > a:
    print("b es mayor que a")


a = 33
b = 33
if b > a:
    print("b es mayor que a")  #condiciona principal
elif a == b :  #condicion secundaria por si no se cumple
    print("a y b son iguales")

a = 15
if a < 10: 
    print("a menos que 10")
elif a > 20: 
    print("a mayor que 20")
else: 
    print("a otro caso")

x = 1 if (1>2) else 3 
x

#and sirve como operador logico para combinar condicionales

a = 50
b = 25
c = 100

if a > b and c > a:
    print("ambas condiciones son variedad")

#or sirve para combinar las condiciones 

a1 = 50 
a2 = 25
a3 = 10

if a > a1 or a2 < a3: 
    print("al menos una de las condiciones es verdad")

# not se usa para invertir el resultado de la declaracion condicional

ab = 33
ac = 200
if not ab > b:
    print("ab no es mayor que ac")

#se puede tener declaraciones if dentro de otras se llaman anidadas

x = 41 
if x > 10:
    print("Mas de 10,")
if x  > 20:
    print("y tambien mas de 20!")
else: 
    print("pero no por encima de 20.")
    
#Recopilar elementos a traves de bucles es tan comun en Python
    
out = [] #se crea una lista vacia
for i in range (10): #rango de valores de 10
    out.append (i**2) #funcion de i^2
out #Nuestra lista ya no esta vacia

15%15 #operador de modulo, busca residuos de division
#como el residuo es 0 aparece el resultado

5%2

for numero in range (1,11):
    if (numero %2 !=0):
        print(numero)

#Funciones  / bloques de codigo que generan un proceso, llamado parametro
#devuelve resultado despues del proceso

def buenas_tardes():
    print("Hola, buenas tardes joven")

buenas_tardes()

#esta funcion esta programada para dar las buenas tardes

activos = ["Amazon", "SP500", "Microsoft", "Nvidia", "Apple" ]
stock_price = [220, 3560, 345, 120 * 10 , 157]
def port_inv (activos, stock_price):
  
    print("Activos del portafolio: " + ", ".join(activos))
    print("Y este es su precio: " + ", ".join(map(str, stock_price)))

# Llama a la función
port_inv(activos, stock_price)

def mi_funcion(country = "Mexico"): #Parametro predeterminado
    print("Yo soy de " + country)

mi_funcion("Francia")
mi_funcion("India")
mi_funcion("Guatemala")
mi_funcion("Brasil")

def mercado_deuda(*instrumento):  #el asterisco es por si se desconoce el numero de argumentos
    print("instumentos de inversion seguros" + instrumento[0]) 

mercado_deuda("Cetes", "Treasure Bills", "BPAS") #tupla como argumento

def mercado_deuda(plazo):
    for x in plazo:
        print(x)

plazo = [28, 91, 180]

mercado_deuda(plazo)


tasa = ["diez punto treinta cinco", "diez punto cuarenta y cinco", "diez punto cincuenta y cinco"]

def mercado_deuda(X):
    return tasa + [X]

print(mercado_deuda("tasa 28 días"))
print(mercado_deuda("tasa 91 días"))
print(mercado_deuda("tasa 180 días"))

#segundo ejemplo 

def mi_funcion(x):
   return 3 * x #Definimos valores como retorno
print(mi_funcion(3))
print(mi_funcion(6))
print(mi_funcion(9))


