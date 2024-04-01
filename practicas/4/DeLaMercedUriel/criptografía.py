import copy

def invertirMatriz(matriz, clave):
  '''
  Invierte una matriz dada en función de una clave específica.

  Recibe una lista que sera la matriz a invertir, y una clave que será para la inversion
  Retorna: La matriz invertida.

  '''
  matriz2 = copy.deepcopy(matriz)
  for i in range(len(matriz2)):
      for j in range(len(matriz2[i])):
          matriz2[i][j] = matriz[i][clave - j - 1]
  return matriz2

def leerMatrizPorColumna(matriz, anchoLista):
  '''
  Lee una matriz por columnas y devuelve una cadena concatenada.
      Recibe la matriz a leer y el ancho de la lista.

  Retorna  La cadena resultante de leer la matriz por columna.
  '''
  cadena = ""
  for j in range(anchoLista):
      for i in range(len(matriz)):
          cadena += matriz[i][j]
  return cadena

def textoAMatrizPorClave(texto, clave):
  '''
  Convierte un texto en una matriz usando una clave específica.
  Recibe El texto a convertir y la clave para la conversión.

  Retorna la matriz resultante de convertir el texto en una matriz.

  Ejemplo:
      >>> textoAMatrizPorClave('abcde', 2)
      [['a', 'b'], ['c', 'd'], ['e', 'X']]

  '''
  # Calculamos la longitud original del texto
  longitud_original = len(texto)

    # Calculamos la longitud mínima requerida para que el texto sea divisible por la clave
  longitud_minima = (longitud_original // clave + 1) * clave

    # Completamos el texto con caracteres 'X' hasta alcanzar la longitud mínima
  texto_completado = texto.ljust(longitud_minima, 'X')

  matriz = []
  lista = []

  for i in range(len(texto_completado)):
    lista.append(texto_completado[i])
    if len(lista) == clave:
      matriz.append(lista)
      lista = []

  return matriz

def normalizarCadena(cadena):
  '''
  Normaliza una cadena eliminando espacios y convirtiendo a mayúsculas.

  Recibe: La cadena a normalizar.

  Retorna: La cadena normalizada.

  Ejemplo:
      >>> normalizarCadena('abc def')
      'ABCDEF'
  '''
  cadenaNormalizada = cadena.replace(" ", "").upper()
  return cadenaNormalizada

def leerMatrizPorFilas(matriz):
  '''
  Lee una matriz por filas y devuelve una cadena concatenada.

  Recibe una matriz a leer.

  Retorna: La cadena resultante de leer la matriz por filas.

  '''
  cadena = ""
  for i in range(len(matriz)):
      for j in range(len(matriz[i])):
          cadena += matriz[i][j]
  return cadena

def separaTextoALista(texto, clave):
  '''
  Separa un texto en una lista de subtextos basada en una clave.

  Recibe: El texto a separar y la clave que es el numero de columnas para la tabla decifrado.

  Retorna:La lista de subtextos.

  Ejemplo:
      >>> separaTextoALista('LCICXENRIXTEAFLNGAIAIIITI', 5)
      ['LCICX', 'ENRIX', 'TEAFL', 'NGAIA', 'IIITI']
  '''
  lista = []
  cadena = ""
  i = 0
  while i < len(texto):
      cadena = texto[i:i + len(texto) // clave]
      lista.append(cadena)
      i += len(texto) // clave
  return lista

def añadirLetrasAMatriz(lista, numLtrElemento):
  '''
  Añade letras de una lista a una matriz.

  Recibe: La lista de letras y el número de letras por elemento.

  Regresa: La matriz resultante.

  Ejemplo:
      >>> añadirLetrasAMatriz(['LCICX', 'ENRIX', 'TEAFL', 'NGAIA', 'IIITI'], 5)
      [['L', 'E', 'T', 'N', 'I'], ['C', 'N', 'E', 'G', 'I'], ['I', 'R', 'A', 'A', 'I'], ['C', 'I', 'F', 'I', 'T'], ['X', 'X', 'L', 'A', 'I']]

  '''
  matriz = []
  for i in range(numLtrElemento):
      lista2 = []
      for j in range(len(lista)):
          lista2.append(lista[j][i])
      matriz.append(lista2)
  return matriz



def cifrarTexto(texto, clave):
  '''
  Cifra un texto dado utilizando una clave.

  Recibe: El texto que se va a cifrar y la clave para el cifrado.
  Retorna el texto cifrado.
  '''
  texto = normalizarCadena(texto)
  matriz = textoAMatrizPorClave(texto, clave)
  matriz = invertirMatriz(matriz, clave)
  return leerMatrizPorColumna(matriz, clave)

def descifrarTexto(texto, clave):
  '''
  Descifra un texto cifrado utilizando una clave.

  Recibe el texto cifrad y la clave en que esta cifrado el texto.

  Retorna: El texto descifrado.

  Ejemplo:
      >>> descifrarTexto('LCICXENRIXTEAFLNGAIAIIITI', 5)
      'INTELIGENCIAARITIFICIALXX'
  '''
  lista = separaTextoALista(texto, clave)
  matriz = añadirLetrasAMatriz(lista, len(texto) // clave)
  matriz = invertirMatriz(matriz, clave)
  return leerMatrizPorFilas(matriz)


def main():

  '''
  Ejemplo para cifrar un texto:

      >>> cifrarTexto('Hola que tal', 4)
      'ATXLEXOULHQA'
      >>> cifrarTexto('La criptografia es romantica', 4)
      'ROFSACXCTAEMIXAPRAOTXLIGIRNA'

      >>> cifrarTexto('Ciudad universitaria', 6)
      'DRIXAERXDVAXUITXINIXCUSA'

      >>> cifrarTexto('Ingenieria computacion', 4)
      'EROTOXGECUIXNIAPCXINIMAN'

      >>> cifrarTexto('Saludo secreto', 2)
      'AUOERTXSLDSCEO'


  Ejemplos para descifrar un texto:

      >>> descifrarTexto('ROFSACXCTAEMIXAPRAOTXLIGIRNA', 4)
      'LACRIPTOGRAFIAESROMANTICAXXX'

      >>> descifrarTexto('LNUIGXAATRNX', 2)
      'ALANTURINGXX'

      >>> descifrarTexto('EECTXGTEEXANSRO', 3)
      'AGENTESECRETOXX'

      >>> descifrarTexto('URNNXPONAXMDOMXOAVUXCTAEN', 5)
      'COMPUTADORAVONNEUMANNXXXX'
  '''

if __name__ == "__main__":
  import doctest
  doctest.testmod()