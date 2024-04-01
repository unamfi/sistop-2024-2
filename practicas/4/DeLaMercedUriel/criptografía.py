import random

matriz = [
    ["V","W","X","Y","Z"],
    ["Q","R","S","T","U"],
    ["L","M","N","O","P"],
    ["F","G","H","I","K"],
    ["A","B","C","D","E"]]
    #realizamos la matriz con cada una de las letras en su posición descrita en la tabla

def buscarPos(matriz,elemento_buscado):
  #buscamos la posición con los parámetros de cada letra a buscar y la matriz
  if elemento_buscado == "J":
    elemento_buscado="I"
  if elemento_buscado== " ":
    numero1 = random.randint(0,4)
    numero2 = random.randint(5,9)
    rand = str(numero1)+str(numero2)
    print(rand, end="")
    #si tenemos un "J" este será cambiado por un "I" para que tome la posición en la tabla
  for j, lista in enumerate(matriz):
    if elemento_buscado in lista:
      i = lista.index(elemento_buscado)
      print(f"{j+5}{i}",end="")#sumamos 5 para que sea la posición igual a la tabla dada

def normalizarCadena(cadena):
  # Eliminar espacios en blanco con replace
  #y convertir a mayúsculas con .upper
  #reemplazamos todas las "Ñ"" por "NN" con .replace
  cadenaNormalizada = cadena.upper()
  cadenaNormalizada = cadenaNormalizada.replace('Ñ', 'NN')
  return cadenaNormalizada

def codificar():
  cadenaIngresada = "Hola mundo" #cambiamos para codificar
  cadenaDeTexto= normalizarCadena(cadenaIngresada)
  #Codificamos el texto
  for v, elemento_buscado in enumerate(cadenaDeTexto):#del texto vamos tomando cada elemento hasta completar todas las letras
    buscarPos(matriz,elemento_buscado)

def decodificar():
  cadenaIngresada = "82737090187164729373" #cambiamos para decodificar
  cadenaDeTexto = normalizarCadena(cadenaIngresada)
  texto_decodificado = ""
  i = 0#para recorrer la cadena 
  while i < len(cadenaDeTexto):#mientras i sea menor a la longitud de la cadena
    fila = int(cadenaDeTexto[i]) - 5 #obtenemos el valor de la fila y restamos 5 para que sea igual a la tabla
    columna = int(cadenaDeTexto[i + 1])#obtenemos el valor de la columan y lo sumamos 1 para que sea igual a la tabla
    if fila < 0:
      fila += 5  # ajuste para la fila 
    try:
      letra_decodificada = matriz[fila][columna]
      texto_decodificado += letra_decodificada #se agrega al texto decodificado
      i += 2  # Avanzamos dos posiciones para el siguiente par de coordenada
    except: 
      texto_decodificado += " "
      i += 2
  print("El texto decodificado es:", texto_decodificado)


def main():
  print("la cadena a codificar es -Hola mundo-")
  codificar()
  print("\ndecodificamos lo de arriba")
  decodificar()


main()
