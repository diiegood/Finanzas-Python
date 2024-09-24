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





























