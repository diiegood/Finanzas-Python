for numero in range(1,15):
    print("Hola simio", numero)

###############################################################################

print("hola mundo")

###############################################################################
#condicional de codigo 

print("Hola, ingresa tu nombre")
nombre=str(input())
print("Hola", nombre, "¿Como estas?")
respuesta = str(input())

if respuesta == "bien":
  print("Excelente, no te interesa una tarjeta de credito")
  respuesta2 =str(input())
  if respuesta2 == "si":
      print("Excelente, gracias por vender tu alma al diablo")
      print("bien decidido, ¿cuanto dinero necesitas?")
      adeudo = float(input())
      print ("¿En cuanto tiempo quieres que sea el pago (Cuantos pagos al año)?")
      years = float(input())
      print ("¿cada cuando quieres pagar?")
      m = float(input())    
      print("¿A que tasa?")
      tasa = float(input())
     
      adeudo = 150000  
      adeudo0 = adeudo
      tasa = 0.12      
      m = 4            
      n = 5            
      pagos = m * n  

      def unam_pago_amortizacion(adeudo, tasa, m, n):
          unam_pago_amortizacion = adeudo / ((1 - ((1 + tasa / m) ** (-m * n))) / (tasa / m))
          return round(unam_pago_amortizacion,2)

      amortizacion = unam_pago_amortizacion(adeudo, tasa,m,n)

      for i in range(0, pagos + 1):
          
          deuda = adeudo * (1 + tasa / m) ** i 
          if i == 0:
              deuda =  adeudo0
              amortizacion = 0
              saldo_insoluto = round(deuda-amortizacion,2)
              
          else: 
              deuda = saldo_insoluto * (1+tasa/m)
              amortizacion = unam_pago_amortizacion(adeudo0, tasa,m,n)
              saldo_insoluto = round(deuda - amortizacion,2)
              parche = saldo_insoluto + amortizacion
              deuda = saldo_insoluto * (1+tasa/m)
              
          
          print(i,"/", round(parche, 2), "/", amortizacion,"/", saldo_insoluto)
          

     
 
  elif respuesta2 == "no":
      print("vete a la mierda")
  else: 
      print("estas seguro, puedes hacer tus sueños realidad") 
      respuesta3 = str(input())
      if respuesta3 == "estoy seguro":
         print("tu te lo pierdes")
      if respuesta3 == "tal vez no":
          print("callese si acepte la oferta")

  
elif respuesta == "mal":
  print("Que triste, no te interesa una tarjeta de credito, para ahogar tus penas")
  respuesta2 =str(input())
  if respuesta2 == "si":
      print("Excelente, gracias por vender tu alma al diablo")
      print("bien decidido, ¿cuanto dinero necesitas?")
      adeudo = float(input())
      print ("¿En cuanto tiempo quieres que sea el pago (Cuantos pagos al año)?")
      years = float(input())
      print ("¿cada cuando quieres pagar?")
      m = float(input())      
  elif respuesta2 == "no":
      print("no estes molestando")
  else: 
      print("estas seguro, puedes hacer tus sueños realidad")   
      
      
elif respuesta == "regular":
  print("NTP, ¿np te interesa una tarjeta de credito para ahogar tus penas?")
  respuesta2 =str(input())
  if respuesta2 == "si":
      print("Excelente, gracias por vender tu alma al diablo")
      print("bien decidido, ¿cuanto dinero necesitas?")
      adeudo = float(input())
      print ("¿En cuanto tiempo quieres que sea el pago (Cuantos pagos al año)?")
      years = float(input())
      print ("¿cada cuando quieres pagar?")
      m = float(input())      
  elif respuesta2 == "no":
      print("no estes molestando")
  else: 
      print("estas seguro, puedes hacer tus sueños realidad")
      
      
      
      

###############################################################################





