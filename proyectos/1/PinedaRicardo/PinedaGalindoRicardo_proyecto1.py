"""
    Creado por Pineda Galindo Ricardo Angel
"""
from os import path #Se va a utilizar para ver si las rutas dadas existen o no en la computadora y obtener información de los archivos
from time import localtime 
from datetime import datetime #Esto me sirve para convertir los objetos que contienen las fechas de los archivos de la compu en cadenas
from math import ceil #Sirve para calcular el cluster inicial y redondear hacia arriba
from tabulate import tabulate #Se usa para mostrar los archivos de forma bonita
#Parte 1: Definición de funciones para poder leer la informacion de la imagen del sistema de archivos

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

def getInformacion(desplazamiento,cantidadBytes,ruta): #Se va a extraer la información de n bytes y se va a regresar
    with open(ruta,'rb') as imagen: #para poder copiar el contenido de un archivo del sistema a la computadora
        imagen.seek(desplazamiento)
        contenido = imagen.read(cantidadBytes)
        imagen.close()
    return contenido

def leerDirectorio(entradaConInfo,entradaSinInfo,espacioOcupado):
    inicio = 2048 #El inicio del directorio empieza en el cluster 1
    infoArchivos.clear()
    while True:
        if inicio == 5*tamCluster: break #Esto evita que se lea más allá de los 4 clusters para el directorio
        tipoArchivo = leer_texto(inicio,1) #Si es una "/" entonces no hay nada, de lo contrario esta ocupado
        if tipoArchivo == '\x00': break#Cuando ya no hay archivos, el primer caracter que se lee es este y por eso se compara
        elif tipoArchivo == '-': #Si el archivo tiene contenido entonces procede a obtener la información faltante
            nombreArchivo = leer_texto(inicio+1,14)   
            tamArchivo = leer_numEntero(inicio+16,4)
            clusterInicial = leer_numEntero(inicio+20,4)
            fechaCreacion = leer_texto(inicio+24,13)
            fechaModificacion = leer_texto(inicio+24,13)
            espacioOcupado += tamArchivo
            if nombreArchivo not in infoArchivos.keys():
                infoArchivos[nombreArchivo] = [tamArchivo,clusterInicial,fechaCreacion,fechaModificacion,inicio]
            #Se guarda el inicio de la entrada de los archivos para acceder más fácil en el directorio
            entradaConInfo += 1
        else:
            entradaSinInfo += 1
        inicio += 64 #Se desplaza 64 bytes para leer la siguiente entrada
    return entradaConInfo,entradaSinInfo,espacioOcupado

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

def escribirEnDatos(desplazamiento,cantidadBytes,rutaArchivo,modo):
    if modo == 0: #Con este modo se va a leer la información de un archivo y se va a guardar en la imagen del sistema
        contenido = getInformacion(0,cantidadBytes,rutaArchivo)
    if modo == 1: #Con este modo se va a sobreescribir la información en el espacio de datos por caracteres nulos
        contenido = b'\x00'*cantidadBytes
    with open(rutaImagen,'rb+') as imagen:
        imagen.seek(desplazamiento)
        imagen.write(contenido)
        imagen.close()

#Parte 3: Definición del menú 
def imprimirMenu():
    #Ponerlo mas bonito despues
    print(espacio + "Manejador del Sistema de Archivos")
    print(espacio + "1. Listar los contenidos del directorio")
    print(espacio + "2. Copiar un archivo del sistema FiUnamFS hacia tu computadora")
    print(espacio + "3. Copiar un archivo de tu computadora hacia el sistema FiUnamFS")
    print(espacio + "4. Eliminar un archivo del FiUnamFS")
    print(espacio + "5. Mostrar información del sistema")
    print(espacio + "6. Salir del programa")

#Parte 4: Definición de funciones para poder trabajar con la informacion de la imagen del sistema de archivos

def listarContenido():
    archivosInfo = []
    print(espacio + "Entradas Ocupadas: " + str(archivos) + "    || Entradas Disponibles: " + str(archivosLibres) )
    print(espacio + "Espacio Disponible: " + str(espacioLibre) + " Bytes  || Espacio Ocupado: " + str(espacioNoLibre) + " Bytes\n\n")
    for llave in infoArchivos.keys():
        fechaC = datetime.strptime(infoArchivos[llave][2],formatoFecha).strftime(formatoFechaBonita)
        fechaM = datetime.strptime(infoArchivos[llave][3],formatoFecha).strftime(formatoFechaBonita)
        archivosInfo.append([llave,str(infoArchivos[llave][0]),str(infoArchivos[llave][1]),fechaC,fechaM])
    print(tabulate(archivosInfo,headers=["Nombre","Tamaño(Bytes)","Cluster Inicial", "Fecha de Creación", "Fecha de Modificación"],showindex=True,tablefmt="heavy_grid",stralign='center',floatfmt='.6f'))
        

def copiarArchivoACompu():
    max = 0
    archivos = list(enumerate(infoArchivos.keys()))
    for i,llave in archivos:
        print(espacio + str(i+1) + ". " + llave)
    
    max = len(archivos)
    opcion = int(input("\n\nEscribe el número del archivo que deseas copiar a tu computadora: "))
    opcion -= 1 #Solo fue porque en pantalla mostre los números partiendo del 1
    if opcion < 0 or opcion > max-1:
        print("Error 10: La opción seleccionada no pertenece a ningún archivo")
        return -1
    nombreArchivo = archivos[opcion][1] #Se obtiene el nombre para poder obtener su información del diccionario
    tamArchivo = infoArchivos[nombreArchivo][0]#Se obtiene para saber cuantos bytes va a leer de la imagen
    clusterInicio = infoArchivos[nombreArchivo][1] #Se obtiene para indicar a que byte desplazar el apuntador
    contenido = getInformacion(clusterInicio*tamCluster,tamArchivo,rutaImagen)
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
#Ya se ocuparon 5 clusters: 0,1,2,3 y 4 Por lo tanto, hay 10239 bytes apartados
#En total hay 1,464,320 bytes libres para información (720 clusters * 2048 c/u - 5 * 2048 c/u)
    rutaArchivo = input("Escriba la ruta del archivo que desea copiar al sistema de archivos:")
    if path.exists(rutaArchivo) == False: 
        print("Error 5: La ruta proporcionada no existe, revisa que la hayas escrito bien.")
        input("Presiona enter para continuar...")
        limpiarPantalla()
        rutaArchivo = input("\n\nEscribe la ruta hacia donde quieras guardar el archivo:  ")
        if path.exists(rutaArchivo) == False: #Solo tiene 2 oportunidades para escribir bien la ruta
            print("\n\nError 5: La dirección ingresada no existe, regresando al menú")
            return -1 #Indica una manipulación incorrecta del programa
    tamArchivo = path.getsize(rutaArchivo) #Se guarda esta información antes de dividir la cadena de la ruta
    if revisarEspacioParaDatos(tamArchivo):#Si el archivo se puede guardar en el sistema, va a revisar el formato del nombre
        rutaArchivo = rutaArchivo.split('\\')
        nombreArchivo =  rutaArchivo[-1] #Se divide la cadena solo para obtener el nombre que está en la última posición de la lista
        if nombreArchivo.isascii() == False:
            print("Error 8: El nombre del archivo solo puede contener caracteres pertenecientes a ASCII")
            input("Presiona enter para continuar...")
            return False
        tamNombre = len(nombreArchivo)
        if tamNombre < 14:
            tamNombre = 14 - tamNombre
            nombreArchivo += " " * tamNombre
        elif tamArchivo > 14:
            print("Error 9: El nombre del archivo es muy grande, debe ser de máximo 14 caracteres")
            return -1
        rutaArchivo = chr(92).join(rutaArchivo)
        #Mientras se va asumir que ya está bien el formato
        fechaCreacion = datetime.strftime(datetime.fromtimestamp(path.getctime(rutaArchivo)),formatoFecha)
        fechaModificacion = datetime.strftime(datetime.fromtimestamp(path.getmtime(rutaArchivo)),formatoFecha)
        #Ya solo falta ver el cluster donde se va a almacenar
        clusterInicial = asignacionDeEspacioDatos(tamArchivo)
        desplazamientoDirectorio = asignacionEspacioDirectorio()
        escribirEnDirectorio(desplazamientoDirectorio,'-',nombreArchivo,tamArchivo,clusterInicial,fechaCreacion,fechaModificacion)
        escribirEnDatos(clusterInicial*tamCluster,tamArchivo,rutaArchivo,0)
        print("El archivo se copió con éxito!!")
    else:
        return False

def revisarEspacioParaDatos(tamArchivo):
    if archivosLibres == 0:  #Esto sirve para ver el espacio en el directorio
        print("Error 6: Se ha alcanzado el límite de archivos, si desea copiar un archivo primero borre alguno del sistema")
        return False
    if espacioLibre - tamArchivo < 0: #Esto sirve para ver los bytes disponibles del espacio de datos
        print("Error 7: El archivo que desea copiar al sistema es muy grande")
        return False 
    return True #Ya se revisó que si cabe la información del archivo tanto en el directorio como en el espacio de datos
    
def asignacionDeEspacioDatos(tamArchivo):
    temp1,temp2 = espacioEntreDatos(tamArchivo) #Es una variable temporal por si no hay espacio, ya no se ocupe después
    if temp1 != False: #Si hay espacio entre 2 bloques de datos de archivos, entonces lo va a aprovechar el sistema
        return ceil(temp1/tamCluster)
    #Como no hay espacio entre archivos, va a buscar antes del primer archivo y después del último
    inicio = 5 * tamCluster
    contador = 0 #Sirve para contar los bytes contiguos y ver si se podría guardar la información del archivo
    with open(rutaImagen,'rb') as imagen:
        while True:
            if contador < tamArchivo:
                imagen.seek(inicio)
                if imagen.read(1) == b'\x00':
                    contador += 1
                else:
                    contador = 0
                    if inicio < temp2:
                        inicio = temp2 #Como el inicio está ocupado, va a revisar después del último archivo
            elif contador == tamArchivo:
                inicio -= tamArchivo #Con esto se obtiene en byte desde el cual se puede empezar a escribir la información
                break
            if inicio > espacioTotal: break
            inicio += 1
        imagen.close()
    if inicio > espacioTotal and espacioLibre >= tamArchivo: compactacion()
    return ceil(inicio/tamCluster)

def espacioEntreDatos(tamArchivo): #Sirve para revisar si el archivo cabe entre 2 archivos almacenados y ya no buscar otro lugar
    archivos = list(infoArchivos.values()) 
    for i in range(len(archivos)-1):
        despuesDeArchivo1 = archivos[i][1] * tamCluster + archivos[i][0] + 1#Esto me da el byte donde puedo empezar a contar
        antesdeArchivo2 = archivos[i+1][1] * tamCluster - 1 #Esto me da el byte hasta donde puedo contar
        if (antesdeArchivo2 - despuesDeArchivo1) >= tamArchivo: #Quiere decir que si cabe la info del nuevo archivo
            return despuesDeArchivo1,0
    #En este punto quiere decir que no cupo los datos del nuevo archivo entre los ya existentes
    return False,archivos[-1][1] * tamCluster + archivos[-1][0]

def asignacionEspacioDirectorio():
    inicio = tamCluster #El directorio empieza en el cluster 1
    with open(rutaImagen,'rb+') as imagen:
        imagen.seek(inicio)
        while (imagen.read(1)).decode("latin-1") != '/' and inicio < tamCluster*(numClusters + 1):#Esto evita que lea solo del cluster 1 al 4
            inicio += 64
            imagen.seek(inicio)
        imagen.close()
    return inicio #Aqui ya encontró una entrada disponible

def compactacion():
    inicio = numClusters + 1
    for llave in infoArchivos.keys():
        with open(rutaImagen,'rb+') as imagen:
            imagen.seek(inicio*tamCluster)
            if imagen.read(1) == b'\x00':
                contenido = getInformacion(inicio*tamCluster,infoArchivos[llave][0],rutaImagen)
                imagen.write(contenido)
                escribirEnDirectorio(infoArchivos[llave][4],'-',llave,infoArchivos[llave][0],inicio,
                                     infoArchivos[llave][2],infoArchivos[llave][3])
            inicio += infoArchivos[llave][0]
            inicio = ceil(inicio/tamCluster)
            imagen.close()
        

def eliminarArchivo():
    archivos = list(enumerate(infoArchivos.keys()))
    for i,llave in archivos:
        print(espacio + str(i+1) + ". " + llave)
    opcion = int(input("\n\nEscribe el número del archivo que deseas copiar a tu computadora: "))
    opcion -= 1
    max = len(archivos)
    if opcion < 0 or opcion > max-1:
        print("Error 10: La opción seleccionada no pertenece a ningún archivo")
        return -1
    nombreArchivo = archivos[opcion][1]
    #A continuación se va a sobreescribir toda esa entrada por los valores default de una entrada vacía
    escribirEnDirectorio(infoArchivos[nombreArchivo][4],'/',"##############",0,0,"00000000000000","00000000000000")
    escribirEnDatos(infoArchivos[nombreArchivo][1]*tamCluster,infoArchivos[nombreArchivo][0],rutaImagen,1)
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
formatoFecha = "%Y%m%d%H%M%S"
formatoFechaBonita = "%Y/%m/%d %H:%M:%S"
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
espacioTotal = 0 #Indica el espacio disponible para guardar datos
espacioNoLibre = 0
espacioLibre = 0

#MAIN
archivos,archivosLibres,espacioNoLibre = leerDirectorio(archivos,archivosLibres,espacioNoLibre) #Se debe ir actualizando constantemente
espacioTotal = tamCluster * (clustersUnidad -5)
espacioLibre = espacioTotal - espacioNoLibre
menu = '1'
while menu != '0':
    imprimirMenu()
    menu = input("\n\n"+ espacio +"Escribe la opción a la que deseas acceder: ")
    limpiarPantalla()
    if menu == '1':
        listarContenido()
    elif menu == '2':
        copiarArchivoACompu()
    elif menu == '3':
        copiarArchivoASistema()
        archivosLibres = 0
        archivos = 0
        espacioNoLibre = 0
        archivos,archivosLibres,espacioNoLibre = leerDirectorio(archivos,archivosLibres,espacioNoLibre)
        espacioLibre = espacioTotal - espacioNoLibre
    elif menu == '4':
        eliminarArchivo()
        archivosLibres = 0
        archivos = 0
        espacioNoLibre = 0
        archivos,archivosLibres,espacioNoLibre = leerDirectorio(archivos,archivosLibres,espacioNoLibre)
        espacioLibre = espacioTotal - espacioNoLibre
    elif menu == '5':
        if mostrarInfoSistema() is False:
            menu = 0
    elif menu == '6':
        break
    else: 
        print("ERROR 3: Por favor seleccione una de las opciones mostradas en pantalla...")
    input("\n\nPRESIONE ENTER PARA CONTINUAR")
    limpiarPantalla()
print("Cerrando Sistema de Archivos...")