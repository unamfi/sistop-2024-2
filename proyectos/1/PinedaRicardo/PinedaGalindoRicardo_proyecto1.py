"""
    Creado por Pineda Galindo Ricardo Angel
    Fecha de creación: 12/05/2024
    Última Modificación: 13/05/2024
    Primera modificación: Creación de la función para listar el contenido y otra función para mostrar la 
    información del sistema
    Segunda modificación: Reestructuración del código modularizando las funciones, creación de la función
    para borrar los archivos del sistema de archivos y otra función para copiar archivos del sistema a la computadora

    NOTA: Aún no se implementan hilos, primero debe funcionar bien el programa

"""
from os import path #Se va a utilizar para ver si las rutas dadas existen o no en la computadora

#Parte 1: Definición de funciones para poder leer la informacion de la imagen del sistema de archivos
"""
    ACLARACIÓN:
   * Para trabajar con la imagen del sistema de archivos es necesario abrirlo como un archivo binario para poder utilizar la función SEEK,
     la cual es una pieza fundamental en el proyecto para poder trabajar con bytes específicos dentro del archivo
"""
def leer_texto(desplazamiento,cantidadBytes):
#Para trabajar los bytes como cadenas con la codificacion ASCII 8 se utiliza la codificacion Latin-1 que es lo mismo o tambien iso-8859-1
    with open(rutaImagen,'rb') as imagen: #Es una forma eficiente de abrir un archivo, trabajar con él y después cerrarlo
        imagen.seek(desplazamiento) #Primero se desplaza el apuntador hasta el byte deseado
        texto = imagen.read(cantidadBytes).decode("latin-1") #Esta función de la libreria Bytes convierte los bytes a una cadena usando una codificación
        imagen.close() #Antes de cerrar el archivo se guarda la cadena generada en otra variable
    return texto

def leer_numEntero(desplazamiento,cantidadBytes):
    with open(rutaImagen,'rb') as imagen:
        imagen.seek(desplazamiento)
    #Esto permite convertir el conjunto de Bytes ordenado con Little Endian a un número entero sin signo
        numero = int.from_bytes(imagen.read(cantidadBytes),byteorder='little') 
        imagen.close()
    return numero

def getInformacion(desplazamiento,cantidadBytes): #Se va a extraer la información de n bytes y se va a regresar
    with open(rutaImagen,'rb') as imagen: #para poder copiar el contenido de un archivo del sistema a la computadora
        imagen.seek(desplazamiento)
        contenido = imagen.read(cantidadBytes)
        imagen.close()
    return contenido

def leerDirectorio(entradaConInfo,entradaSinInfo):
    inicio = 2048 #El inicio del directorio empieza en el cluster 1
    while True:
        tipoArchivo = leer_texto(inicio,1) #Si es una "/" entonces no hay nada, de lo contrario esta ocupado
        if tipoArchivo == '\x00': #Cuando ya no hay archivos, el primer caracter que se lee es este y por eso se compara
            break
        elif tipoArchivo == '-': #Si el archivo tiene contenido entonces procede a obtener la información faltante
            nombreArchivo = leer_texto(inicio+1,14)   
            tamArchivo = leer_numEntero(inicio+16,4)
            clusterInicial = leer_numEntero(inicio+20,4)
            horaCreacion = leer_texto(inicio+24,13)
            horaModificacion = leer_texto(inicio+38,13)
            infoArchivos[nombreArchivo] = [tamArchivo,clusterInicial,horaCreacion,horaModificacion,inicio]
            #Se guarda el inicio de la entrada de los archivos para acceder más fácil en el directorio
            entradaConInfo += 1
        else:
            entradaSinInfo += 1
        inicio += 64 #Se desplaza 64 bytes para leer la siguiente entrada
    return entradaConInfo,entradaSinInfo

def limpiarPantalla():
    print(chr(27) + "[2J" + chr(27) + "[H") #Esto fue proporcionado por el profesor

#Parte 2: Definición de funciones para poder escribir informacion en la imagen del sistema de archivos

def escribirTexto(cadena,desplazamiento): #Convierte las cadenas en bytes con el formato adecuado
    texto = str.encode(cadena,"latin-1") #Para escribir en la imagen se debe codificar en ASCII de 8 bits
    with open(rutaImagen,'rb+') as archivo:
        archivo.seek(desplazamiento)
        archivo.write(texto)
        archivo.close()

def escribirNumeroEntero(num,desplazamiento): #Convierte los números enteros en bytes con el formato adecuado
    numero = int.to_bytes(num,4,byteorder="little") #y después escribe en el archivo esos bytes
    with open(rutaImagen,'rb+') as archivo:
        archivo.seek(desplazamiento)
        archivo.write(numero)
        archivo.close()

def escribirEnDirectorio(desplazamiento,tipo,nombre,tam,clusterInicial,horaCreacion,horaModificacion):
    escribirTexto(tipo,desplazamiento)
    escribirTexto(nombre,desplazamiento+1)
    escribirNumeroEntero(tam,desplazamiento+16)
    escribirNumeroEntero(clusterInicial,desplazamiento+20)
    escribirTexto(horaCreacion,desplazamiento+24)
    escribirTexto(horaModificacion,desplazamiento+38)

#Parte 3: Definición del menú 
def imprimirMenu():
    #Ponerlo mas bonito despues
    print(espacio + "Manejador del Sistema de Archivos")
    print(espacio + "1. Listar los contenidos del directorio")
    print(espacio + "2. Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema")
    print(espacio + "3. Copiar un archivo de tu computadora hacia tu FiUnamFS")
    print(espacio + "4. Eliminar un archivo del FiUnamFS")
    print(espacio + "5. Mostrar información del sistema")
    print(espacio + "6. Salir del programa")

#Parte 4: Definición de funciones para poder trabajar con la informacion de la imagen del sistema de archivos

def listarContenido():
    print("Entradas Ocupadas: " + str(archivos) + "|| Entradas Disponibles: " + str(archivosLibres))
    for i,llave in enumerate(infoArchivos.keys()):
        print(espacio + str(i+1) + ". " + llave)
        print(espacio + ("."*5) + "Tamaño: " + str(infoArchivos[llave][0]) + " bytes")
        print(espacio + ("."*5) + "Cluster Inicial: " + str(infoArchivos[llave][1]))
        print(espacio + ("."*5) + "Fecha de creación: " + infoArchivos[llave][2]) #Crear función para imprimir fecha **Posible hilo??
        print(espacio + ("."*5) + "Fecha de última modificación: " + infoArchivos[llave][3])

def copiarArchivoACompu():
    archivos = list(enumerate(infoArchivos.keys()))
    for i,llave in archivos:
        print(espacio + str(i+1) + ". " + llave)
    opcion = int(input("\n\nEscribe el número del archivo que deseas copiar a tu computadora: "))
    opcion -= 1 #Solo fue porque en pantalla mostre los números partiendo del 1
    nombreArchivo = archivos[opcion][1] #Se obtiene el nombre para poder obtener su información del diccionario
    tamArchivo = infoArchivos[nombreArchivo][0]#Se obtiene para saber cuantos bytes va a leer de la imagen
    clusterInicio = infoArchivos[nombreArchivo][1] #Se obtiene para indicar a que byte desplazar el apuntador
    contenido = getInformacion(clusterInicio*tamCluster,tamArchivo)
    ruta = input("\n\nEscribe la ruta hacia donde quieras guardar el archivo: ")
    if path.exists(ruta) == False: #Esta condición solo es para entrar en el while y poder escribir la ruta varias veces
        print("Error 5: La ruta proporcionada no existe, revisa que la hayas escrito bien.")
        input("Presiona enter para continuar...")
        limpiarPantalla()
        ruta = input("\n\nEscribe la ruta hacia donde quieras guardar el archivo: ")
        if path.exists(ruta) == False: #Solo tiene 2 oportunidades para escribir bien la ruta
            print("\n\nError 5: La dirección ingresada no existe, regresando al menú")
            return -1 #Indica una manipulación incorrecta del programa
    with open(ruta + '\\' + nombreArchivo,"wb+") as file: #Si ya existe el archivo entonces se va a sobreescribir
        file.write(contenido)
        file.close()
    print("El archivo se ha copiado con éxito!!")

def copiarArchivoASistema():
#PENDIENTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    rutaArchivo = input("Escriba la ruta del archivo que desea copiar al sistema de archivos:")
    if path.exists(rutaArchivo) == False: 
        print("Error 5: La ruta proporcionada no existe, revisa que la hayas escrito bien.")
        input("Presiona enter para continuar...")
        limpiarPantalla()
        rutaArchivo = input("\n\nEscribe la ruta hacia donde quieras guardar el archivo: ")
        if path.exists(rutaArchivo) == False: #Solo tiene 2 oportunidades para escribir bien la ruta
            print("\n\nError 5: La dirección ingresada no existe, regresando al menú")
            return -1 #Indica una manipulación incorrecta del programa
    
def eliminarArchivo():
#Para eliminar un archivo hay que borrarlo del directorio y sustituir todo su contenido por los caracteres indicados en las especificaciones
#del proyecto
    archivos = list(enumerate(infoArchivos.keys()))
    for i,llave in archivos:
        print(espacio + str(i+1) + ". " + llave)
    opcion = int(input("\n\nEscribe el número del archivo que deseas copiar a tu computadora: "))
    opcion -= 1
    nombreArchivo = archivos[opcion][1]
    #A continuación se va a sobreescribir toda esa entrada por los valores default de una entrada vacía
    escribirEnDirectorio(infoArchivos[nombreArchivo][4],'/',"##############",0,0,"00000000000000","00000000000000")
    #Falta borrar el archivo del diccionario
    infoArchivos.pop(nombreArchivo)
    print("El archivo se ha eliminado con éxito!!")

def mostrarInfoSistema():
    #Se debe realizar una validación de la información del sistema de archivos para verificar que sea el correcto
    if nombreSistema != "FiUnamFS":
        print("ERROR 1: El sistema de archivos utilizado es incorrecto, verifica que sea el archivo adecuado")
        return False #Error general para finalizar el programa
    if version != "24-2":
        print("ERROR 2: La versión actual del sistema de archivos no coincide, VERSIÓN CORRECTA: \"24-2\"   VERSIÓN ACTUAL: \"" + version + "\"")
        return False
    print(espacio + "INFORMACIÓN DEL SISTEMA DE ARCHIVOS\n")
    print(espacio + "Nombre: " + nombreSistema + "\n" + espacio + "Versión: " + version+ "\n" + espacio + "Etiqueta del volumen: " + etiqueta)
    print(espacio + "Tamaño del cluster: " + str(tamCluster) + " bytes"+ "\n" + espacio + "Tamaño del directorio: " + str(numClusters) + " clusters")
    print(espacio + "Tamaño de la unidad completa: " + str(clustersUnidad) + " clusters")

#Variables Globales

rutaImagen = "fiunamfs.img"
espacio = " " * 5 #Solo se definió para poder imprimir con un espacio antes del contenido
infoArchivos = {} #Aqui se van a guardar los nombres de los archivos y su tamaño en bytes
nombreSistema = leer_texto(0,8)
version = leer_texto(10,4)
etiqueta = leer_texto(20,19) #En la descripción del proyecto hay un error con la cantidad de bytes
tamCluster = leer_numEntero(40,4)
numClusters = leer_numEntero(45,4)
clustersUnidad = leer_numEntero(50,4)
archivos = 0 #Indica la cantidad de archivos actual en el directorio
archivosLibres = 0 #Indica cuantas entradas sobran en el directorio

#Esto ya no es parte de la funcion, ya es el main
archivos,archivosLibres = leerDirectorio(archivos,archivosLibres) #Se debe ir actualizando constantemente
while True:
    imprimirMenu()
    menu = int(input("\n\n"+ espacio +"Escribe la opción a la que deseas acceder: "))
    limpiarPantalla()
    if menu == 1:
        listarContenido()
    elif menu == 2:
        copiarArchivoACompu()
    elif menu == 3:
        copiarArchivoASistema()
        archivosLibres = 0
        archivos = 0
        archivos,archivosLibres = leerDirectorio(archivos,archivosLibres)
    elif menu == 4:
        eliminarArchivo()
        archivosLibres = 0
        archivos = 0
        archivos,archivosLibres = leerDirectorio(archivos,archivosLibres)
    elif menu == 5:
        if mostrarInfoSistema() is False:
            menu = 0
    elif menu == 6:
        break
    else: 
        print("ERROR 3: Por favor seleccione una de las opciones mostradas en pantalla...")
    input("\n\nPRESIONE ENTER PARA CONTINUAR")
    limpiarPantalla()
print("Cerrando Sistema de Archivos...")