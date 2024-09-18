######################Nociones basicas tipos de caracteres#####################

base = 20 
altura = 5 
area = base * altura 
print(area) #para ver el resultado del comando
area #tambien poner directamente la variable para el resultado

int(1.3532) #valor entero del numero 1.3532 -> 1
float(2)   #valor decimal del valor 2 ->  2.0
#es la union de varios strings en una funcion
canaca = "y" + "mis" +"cincuentamil" + "pesos" + "que"
canaca*3 #se triplica la funcion 3 veces#
canaca[0:5] #letras del cero a 5 de la funcion
canaca[-5] #ultimas 5 letras de la funcion

canaca1 = "y mis cincuentamil pesos que"
print(canaca1) #para arrojar el resultado de la funcion canaca1
canaca1.replace("cincuentamil", "veintemil")

" y mis cincuenta mil pesos % " %(10) #para reposicionar un valor
"este es un numero flotante %.6f" %(3.14162115)


#Nociones basicas python# las listas siempre son con corchetes
#listas []
numeros_enteros = [1,2,3,4,5] #lista de valores int
numeros_decimales = [1.25, 35.2, 3.1416, 2.678] #lsita de valores float
palabras = ["perro", "gato", "vibora", "tlacuache"] #lista de valores string

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
Cetes["propiedad"] = "DonPendejo"  #para agregar una nueva informacion, en este caso el dueño"
Cetes

del Cetes["propiedad"] #se le elimina su propiedad al dueño
Cetes

#Union de diccionarios# 
CETES = {"periodo1": 28, "periodo2": 90, "periodo3": 180 }
Tasas = {"Periodo1": 10.10, "Periodo2": 10.35, "Periodo3": 10.56}
dict(CETES, **Tasas)

{**CETES,**Tasas}