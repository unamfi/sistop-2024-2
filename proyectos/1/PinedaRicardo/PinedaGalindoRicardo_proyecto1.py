"""
    Creado por Pineda Galindo Ricardo Angel
    Fecha de creación: 12/05/2024
    Primera modificación: Creación de la función para listar el contenido y otra función para mostrar la 
    información del sistema

    NOTA: Aún no se ordena el código, primero me encargo de que funcione el programa

"""

#Parte 1: Definición de funciones para poder leer la informacion de la imagen del sistema de archivos
"""
    ACLARACIÓN:
   * Para trabajar con la imagen del sistema de archivos es necesario abrirlo como un archivo binario para poder utilizar la función SEEK,
     la cual es una pieza fundamental en el proyecto para poder trabajar con bytes específicos dentro del archivo
"""
def leer_texto(desplazamiento,cantidadBytes):
#Para trabajar los bytes como cadenas con la codificacion ASCII 8 se utiliza la codificacion Latin-1 que es lo mismo o tambien iso-8859-1
    with open("fiunamfs.img",'rb') as imagen: #Es una forma eficiente de abrir un archivo, trabajar con él y después cerrarlo
        imagen.seek(desplazamiento) #Primero se desplaza el apuntador hasta el byte deseado
        texto = imagen.read(cantidadBytes).decode("latin-1") #Esta función de la libreria Bytes convierte los bytes a una cadena usando una codificación
        imagen.close() #Antes de cerrar el archivo se guarda la cadena generada en otra variable
    return texto

def leer_numEntero(desplazamiento,cantidadBytes):
    with open("fiunamfs.img",'rb') as imagen:
        imagen.seek(desplazamiento)
    #Esto permite convertir el conjunto de Bytes ordenado con Little Endian a un número entero sin signo
        numero = int.from_bytes(imagen.read(cantidadBytes),byteorder='little') 
        imagen.close()
    return numero

espacio = " " * 5 #Solo se definió para poder imprimir con un espacio antes del contenido

def limpiarPantalla():
    print(chr(27) + "[2J" + chr(27) + "[H") #Esto fue proporcionado por el profesor

#Parte 2: Definición del menú 
def imprimirMenu():
    #Ponerlo mas bonito despues
    print(espacio + "Manejador del Sistema de Archivos")
    print(espacio + "1. Listar los contenidos del directorio")
    print(espacio + "2. Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema")
    print(espacio + "3. Copiar un archivo de tu computadora hacia tu FiUnamFS")
    print(espacio + "4. Eliminar un archivo del FiUnamFS")
    print(espacio + "5. Mostrar información del sistema")
    print(espacio + "6. Salir del programa")

#Parte 3: Definición de funciones para poder trabajar con la informacion de la imagen del sistema de archivos

infoArchivos = {} #Aqui se van a guardar los nombres de los archivos y su tamaño en bytes

def listarContenido():
    apuntador = 2048 #Va a empezar a leer el contenido desde el cluster 1
    cantidadArchivos = 0 #Solo es un contador par ver la cantidad de archivos
    while True:
        tipoArchivo = leer_texto(apuntador,1) #Si es una "/" entonces no hay nada, de lo contrario esta ocupado
        if tipoArchivo == '\x00': #Cuando ya no hay archivos, el primer caracter que se lee es este y por eso se compara
            break
        if tipoArchivo != "/": #Si el archivo tiene contenido entonces procede a obtener la información faltante
            nombreArchivo = leer_texto(apuntador+1,14)   
            tamArchivo = leer_numEntero(apuntador+16,4)
            clusterInicial = leer_numEntero(apuntador+21,2)
            horaCreacion = leer_texto(apuntador+24,13)
            horaModificacion = leer_texto(apuntador+38,13)
            infoArchivos[nombreArchivo] = tamArchivo
            print(espacio + "ARCHIVO #" + str((cantidadArchivos + 1)))
            print(espacio + ("."*5) + "Nombre: " + nombreArchivo)
            print(espacio + ("."*5) + "Tamaño: " + str(tamArchivo) + " bytes")
            print(espacio + ("."*5) + "Cluster Inicial: " + str(clusterInicial))
            print(espacio + ("."*5) + "Fecha de creación: " + horaCreacion) #Crear función para imprimir fecha **Posible hilo??
            print(espacio + ("."*5) + "Fecha de última modificación: " + horaModificacion)
            cantidadArchivos +=1 
        apuntador += 64 #Se traslada 64 bytes para leer la siguiente entrada
    
"""
Formato para las entradas del directorio (cada una mide 64 bytes)
Bytes - Descripcion
0    (1 byte)    - Tipo de archivo que generalmente debe ser el caracter '-'. Cuando la entrada esta vacia se indica con el caracter '/'
1/15 (14 bytes)  - Nombre del archivo
16/20 (4 bytes)  - Tamaño del archivo en bytes
21/23 (2 bytes)  - Cluster inicial 
24/37 (13 bytes) - Hora y fecha de creación del archivo, especificando AAAAMMDDHHMMSS (Es una cadena de texto)
38/51 (13 bytes) - Hora y fecha de última modificación del archivo, especificando AAAAMMDDHHMMSS
52/64 (12 bytes) - Espacio no utilizado

"""

def copiarSistemaCompu():
    #Aqui se podria poner un hilo para que cuando se haga esta funcion mande una señal para imprimir los nombres de los archivos
    #y ya después pedir que escriba el nombre del archivo a borrar

    #Puse global la cantidad de archivos por si nada mas quiero poner opciones
    print(espacio + "Archivos Disponibles")
    if not infoArchivos: #Si el diccionario está vacío entonces lista el contenido y borra la pantalla inmediatamente
        listarContenido()
        limpiarPantalla()
    indiceArchivos =  list(enumerate(infoArchivos.keys())) #Recorre las llaves del diccionario y 
    #crea una tupla donde las va enumerando (indice,nombre) para que posteriormente todas las tuplas se guarden en una lista 
    for i, nombre in indiceArchivos: 
        print(f"{espacio}{i+1}. {nombre}")
    opcion = int(input(espacio + "\n\nEscribe el número del archivo que deseas borrar: "))
    #A partir del numero asociado al nombre guardado en la lista, se recupera el nombre para buscar en el diccionario
    #El tamaño del archivo y así poder desplazarse en el archivo para buscar la info y copiarlo en un nuevo archivo
    tamArchivo = infoArchivos[indiceArchivos[opcion-1][1]] 
    archivo = open("fiunamfs.img",'rb')

    archivo.close()
    """ nombreArchivo = input("Escribe el nombre del archivo que deseas borrar")
    with open("fiunamfs.img",'rb') as p:
        p.seek(10240)
        print(p.read(31222))
        p.close() """
"""
    Información Importante
    El directorio ocupa 4 clusters y después ya está disponible la información o los datos.
    Cluster 0 empieza en 0 y termina el 2047 (Cada Cluster ocupa 2048 bytes)
    Cluster 1 empieza en 2048 y termina en 4095
    Cluster 2 empieza en 4096 y termina en 6143
    Cluster 3 empieza en 6144 y termina en 8191
    Cluster 4 empieza en 8192 y termina en 10239
    Cluster 5 empieza en 10240
"""

    

def copiarCompuSistema():
    print("Hola desde opcion 3")

def eliminarArchivo():
    print("Hola desde opcion 4")

def mostrarInfoSistema():
    #Se debe realizar una validación de la información del sistema de archivos para verificar que sea el correcto
    nombreSistema = leer_texto(0,8)
    if nombreSistema != "FiUnamFS":
        print("ERROR 1: El sistema de archivos utilizado es incorrecto, verifica que sea el archivo adecuado")
        return False #Error general para finalizar el programa
    version = leer_texto(10,4)
    if version != "24-2":
        print("ERROR 2: La versión actual del sistema de archivos no coincide, VERSIÓN CORRECTA: \"24-2\"   VERSIÓN ACTUAL: \"" + version + "\"")
        return False
    etiqueta = leer_texto(20,19) #En la descripción del proyecto hay un error con la cantidad de bytes
    tamCluster = leer_numEntero(40,4)
    numClusters = leer_numEntero(45,4)
    clustersUnidad = leer_numEntero(50,4)
    print(espacio + "INFORMACIÓN DEL SISTEMA DE ARCHIVOS\n")
    print(espacio + "Nombre: " + nombreSistema + "\n" + espacio + "Versión: " + version+ "\n" + espacio + "Etiqueta del volumen: " + etiqueta)
    print(espacio + "Tamaño del cluster: " + str(tamCluster) + " bytes"+ "\n" + espacio + "Tamaño del directorio: " + str(numClusters) + " clusters")
    print(espacio + "Tamaño de la unidad completa: " + str(clustersUnidad) + " clusters")

#Esto ya no es parte de la funcion, ya es el main
menu = 8
while menu != 0:
    imprimirMenu()
    menu = int(input("\n\n"+ espacio +"Escribe la opción a la que deseas acceder: "))
    limpiarPantalla()
    if menu == 1:
        listarContenido()
    elif menu == 2:
        copiarSistemaCompu()
    elif menu == 3:
        copiarCompuSistema()
    elif menu == 4:
        eliminarArchivo()
    elif menu == 5:
        if mostrarInfoSistema() is False:
            menu = 0
    elif menu == 6:
        menu = 0
    else: 
        print("ERROR 3: Por favor seleccione una de las opciones mostradas en pantalla...")
    input("\n\nPRESIONE ENTER PARA CONTINUAR")
    limpiarPantalla()
print("Cerrando Sistema de Archivos...")
""" 
Esta seria otra forma de abrir el archivo, se abre, hace lo que queramos y ya despues se cierra

Funciones para los archivos
seek(desplazamiento,desde_donde) Solo funciona con archivos binarios, no de texto 

tell() devuelve un entero que indica la posicion del apuntador, si no se pone nada se desplaza al final y si se 
pone un 0 se pone en el inicio

read() lee el archivo completo, salvo que se indique la cantidad de  bytes a leer 

write()

MODOS DE APERTURA
 
r - solo sirve para leer el archivo
w - sirve para sobreescribir
a - permite escribir en el final del archivo 

Si se le agrega un + a cualquiera de los modos permite leer y escribir

b - abre archivos en binario y se puede combinar con los anteriores 

with open ("archivotext.txt", "w") as f: #Creamos el archivo
    f.write("Creando archivo de texto en python usando whit as") #<-Escribimos en el
    f.close()

Info para decodificar bytes en cadenas de ascii 8 
La funcion decode recibe como parametro la codificacion como por ejemplo utf-8
Para invocarlo puede ser bytes.decode()
Ejemplo de uso b'\x80abc'.decode(utf-8) Le dice al interprete como trabajar con esos bytes

Para convertir a bytes, es decir lo opuesto a lo que se hizo antes es la funcion encode
str.encode() que devuelve una representacion en bytes de la cadena mandada en la codificacion solicitada

Cual codificacion se debe usar? Latin-1 (iso-8859-1) es la que utiliza solo 8 bits 
Info de aqui: https://docs.python.org/es/3/library/codecs.html

NOTA= Lo anterior solo aplica si voy a trabajar con cadenas de texto, si quiero usar numeros enteros ya se ocupa otra cosa, una funcion
llamada int.from_bytes() con la cual se mandan los bytes y si los bytes estan el little o big endian
INFO: https://www.tutorialspoint.com/how-to-convert-bytes-to-int-in-python

 """
