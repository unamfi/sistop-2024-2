#Creado por Pineda Galindo Ricardo Angel
from os import path #Se va a utilizar para ver si las rutas dadas existen o no en la computadora y obtener información de los archivos
from datetime import datetime #Esto me sirve para convertir los objetos que contienen las fechas de los archivos de la compu en cadenas
from math import ceil #Sirve para calcular el cluster inicial y redondear hacia arriba
from tabulate import tabulate #Se usa para mostrar los archivos de forma bonita
from threading import Semaphore, Thread #Permite crear hilos y sincronizarlos mediante semáforos

def leer_texto(desplazamiento,cantidadBytes):
#Para trabajar los bytes como cadenas con la codificacion ASCII 8 se utiliza la codificacion Latin-1 que es lo mismo o tambien iso-8859-1
    with open(rutaImagen,'rb') as imagen:
        imagen.seek(desplazamiento)
        texto = imagen.read(cantidadBytes).decode("latin-1") #Esta función de la libreria Bytes convierte los bytes a una cadena usando una codificación
        imagen.close()
    return texto

def leer_numEntero(desplazamiento,cantidadBytes):
    with open(rutaImagen,'rb') as imagen:
        imagen.seek(desplazamiento)
        numero = int.from_bytes(imagen.read(cantidadBytes),byteorder='little') #Esto convierte el conjunto de Bytes a un número entero sin signo
        imagen.close()
    return numero

def getInformacion(desplazamiento,cantidadBytes,ruta): #Se va a extraer la información de n bytes y se va a regresar
    with open(ruta,'rb') as imagen: #para poder copiar el contenido de un archivo del sistema a la computadora
        imagen.seek(desplazamiento)
        contenido = imagen.read(cantidadBytes)
        imagen.close()
    return contenido

def leerDirectorio():
    global infoArchivos, archivos, archivosLibres, espacioNoLibre
    inicio = 2048 #El inicio del directorio empieza en el cluster 1
    archivos = archivosLibres = espacioNoLibre = 0
    if not infoArchivos: infoArchivos.clear()
    while True:
        if inicio == 5*tamCluster: break #Esto evita que se lea más allá de los 4 clusters para el directorio
        tipoArchivo = leer_texto(inicio,1) #Si es una "/" entonces no hay nada, de lo contrario esta ocupado
        if tipoArchivo == '\x00': break #Cuando ya no hay archivos, el primer caracter que se lee es este y por eso se compara
        elif tipoArchivo == '-': #Si el archivo tiene contenido entonces procede a obtener la información faltante
            nombreArchivo = leer_texto(inicio+1,14)
            tamArchivo = leer_numEntero(inicio+16,4)
            clusterInicial = leer_numEntero(inicio+20,4)
            fechaCreacion = leer_texto(inicio+24,13)
            fechaModificacion = leer_texto(inicio+38,13)
            espacioNoLibre += tamArchivo
            if nombreArchivo not in infoArchivos.keys():
                infoArchivos[nombreArchivo] = [tamArchivo,clusterInicial,fechaCreacion,fechaModificacion,inicio]
            #Se guarda el inicio de la entrada de los archivos para acceder más fácil en el directorio
            archivos += 1
        else:
            archivosLibres += 1
        inicio += 64
    infoArchivos = dict(sorted(infoArchivos.items(), key=lambda item: item[1][1]))

def limpiarPantalla():
    print(chr(27) + "[2J" + chr(27) + "[H")

def escribirTexto(cadena,desplazamiento): #Convierte las cadenas en bytes con el formato adecuado
    texto = str.encode(cadena,"latin-1") #Para escribir en la imagen se debe codificar en ASCII de 8 bits
    with open(rutaImagen,'rb+') as archivo:
        archivo.seek(desplazamiento)
        archivo.write(texto)
        archivo.close()

def escribirNumeroEntero(num,desplazamiento): #Convierte los números enteros en bytes con el formato adecuado
    numero = int.to_bytes(num,4,byteorder="little") #y después escribe esos bytes en el archivo 
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

def imprimirMenu():
    print("\n" + espacio + "Manejador del Sistema de Archivos\n")
    print(espacio + "1. Listar los contenidos del directorio")
    print(espacio + "2. Copiar un archivo del sistema FiUnamFS hacia tu computadora")
    print(espacio + "3. Copiar un archivo de tu computadora hacia el sistema FiUnamFS")
    print(espacio + "4. Eliminar un archivo del FiUnamFS")
    print(espacio + "5. Mostrar información del sistema")
    print(espacio + "6. Salir del programa")

def listarContenido():
    archivosInfo = []
    for llave in infoArchivos.keys():
        fechaC = datetime.strptime(infoArchivos[llave][2],formatoFecha).strftime(formatoFechaBonita)
        fechaM = datetime.strptime(infoArchivos[llave][3],formatoFecha).strftime(formatoFechaBonita)
        archivosInfo.append([llave,str(infoArchivos[llave][0]),str(infoArchivos[llave][1]),fechaC,fechaM])
    print(tabulate(archivosInfo,headers=["Nombre","Tamaño(Bytes)","Cluster Inicial", "Fecha de Creación", "Fecha de Modificación"],showindex=True,tablefmt="heavy_grid",stralign='center',floatfmt='.6f'))
        
def copiarArchivoACompu(sem1,sem2):
    while True: 
        sem2.acquire() #Se bloquea inicialmente
        if menu == '6': break #Ya no le manda señal al hilo principal porque otros hilos tambien lo harian y se activaria el hilo con uno solo
        listarContenido()
        max = len(infoArchivos)
        try:
            opcion = int(input("\n\nEscribe el número del archivo que deseas copiar a tu computadora: "))
        except ValueError:
            print("Error 12: Por favor ingresa un número")
            sem1.release()
            continue
        if opcion < 0 or opcion > max-1:
            print("Error 10: La opción seleccionada no pertenece a ningún archivo")
            sem1.release()
            continue
        for llave in infoArchivos.keys():
            if opcion == 0: #Se obtiene la llave del archivo a copiar
                nombreArchivo = llave
                tamArchivo = infoArchivos[llave][0]#Se obtiene para saber cuantos bytes va a leer de la imagen
                clusterInicio = infoArchivos[llave][1] #Se obtiene para indicar a que byte desplazar el apuntador
                contenido = getInformacion(clusterInicio*tamCluster,tamArchivo,rutaImagen)
                break
            opcion -= 1
        ruta = input("\n\nEscribe la ruta hacia donde quieras guardar el archivo: ")
        if path.exists(ruta) == False: #Primero se revisa que la ruta exista
            print("Error 5: La ruta proporcionada no existe, revisa que la hayas escrito bien.")
            input("Presiona enter para continuar...")
            sem1.release()
            continue
        with open(ruta + '\\' + nombreArchivo,"wb+") as file: #Si ya existe el archivo entonces se va a sobreescribir
            file.write(contenido)
            file.close()
        print("El archivo se ha copiado con éxito!!")
        sem1.release() #Le dice al hilo principal que puede continuar

def copiarArchivoASistema(sem1,sem2):
    while True:
        sem2.acquire()
        if menu == '6': break
        rutaArchivo = input("Escriba la ruta del archivo que desea copiar al sistema de archivos:")
        if path.exists(rutaArchivo) == False: 
            print("Error 5: La ruta proporcionada no existe, revisa que la hayas escrito bien.")
            sem1.release()
            continue
        tamArchivo = path.getsize(rutaArchivo) #Se guarda esta información antes de dividir la cadena de la ruta
        if revisarEspacioParaDatos(tamArchivo):#Si el archivo se puede guardar en el sistema, va a revisar el formato del nombre
            rutaArchivo = rutaArchivo.split('\\')
            nombreArchivo =  rutaArchivo[-1] #Se divide la cadena solo para obtener el nombre que está en la última posición de la lista
            if nombreArchivo.isascii() == False:
                print("Error 8: El nombre del archivo solo puede contener caracteres pertenecientes a ASCII")
                input("Presiona enter para continuar...")
                sem1.release()
                continue
            tamNombre = len(nombreArchivo)
            if tamNombre < 14: #Si el nombre es menor a 14 bytes entonces se acompleta con espacios para cumplir el requisito de las entradas
                tamNombre = 14 - tamNombre
                nombreArchivo += " " * tamNombre
            elif tamArchivo > 14:
                print("Error 9: El nombre del archivo es muy grande, debe ser de máximo 14 caracteres")
                sem1.release()
                continue
            if nombreArchivo in infoArchivos.keys():#Se revisa que el nombre del archivo a ingresar no se encuentre en el diccionario
                print("Error 11: Este archivo ya se encuentra en el sistema")
                input("Presiona enter para continuar...")
                sem1.release()
                continue
            rutaArchivo = chr(92).join(rutaArchivo)#Como se habia separado la cadena, se vuelve a unir con el caracter \
            fechaCreacion = datetime.strftime(datetime.fromtimestamp(path.getctime(rutaArchivo)),formatoFecha)#Se pasa la fecha al formato adecuado para el directorio
            fechaModificacion = datetime.strftime(datetime.fromtimestamp(path.getmtime(rutaArchivo)),formatoFecha)
            clusterInicial = asignacionDeEspacioDatos(tamArchivo)
            desplazamientoDirectorio = asignacionEspacioDirectorio()
            escribirEnDirectorio(desplazamientoDirectorio,'-',nombreArchivo,tamArchivo,clusterInicial,fechaCreacion,fechaModificacion)
            escribirEnDatos(clusterInicial*tamCluster,tamArchivo,rutaArchivo,0)
            print("El archivo se copió con éxito!!")
            sem1.release()
        else:
            sem1.release()
            continue

def revisarEspacioParaDatos(tamArchivo):
    if archivosLibres == 0:  #Esto sirve para ver el espacio en el directorio
        print("Error 6: Se ha alcanzado el límite de archivos, si desea copiar un archivo primero borre alguno del sistema")
        return False
    if espacioLibre - tamArchivo < 0: #Esto sirve para ver los bytes disponibles del espacio de datos
        print("Error 7: El archivo que desea copiar al sistema es muy grande")
        return False 
    return True #Ya se revisó que si cabe la información del archivo tanto en el directorio como en el espacio de datos
    
def asignacionDeEspacioDatos(tamArchivo):
    if infoArchivos: #Si hay archivos en el diccionario va a buscar espacio entre ellos
        temp = espacioEntreDatos(tamArchivo) 
        if temp != False: #Si hay espacio entre 2 bloques de datos de archivos, entonces lo va a aprovechar el sistema
            return temp
    else:
        temp = 0 #Si no hay archivos entonces no se va a tomar en cuenta al momento de buscar espacio
    #Como no hay espacio entre archivos, va a buscar antes del primer archivo y después del último archivo
    inicio = 5 * tamCluster #Va a empezar a buscar espacio en el inicio del espacio de datos
    contador = 0 #Sirve para contar los bytes contiguos y ver si se podría guardar la información del archivo
    with open(rutaImagen,'rb') as imagen:
        while True:
            if contador < tamArchivo:
                imagen.seek(inicio)
                if imagen.read(1) == b'\x00': #Si el inicio está vació, empieza a revisar si alcanza el espacio
                    contador += 1
                else:
                    contador = 0 #Si no está vacío, se reinicia el contador
                    if temp != 0 and inicio < temp: #Si hubo archivos y el apuntador aún no llega al último archivo
                        inicio = temp  #Se desplaza hasta después del último byte de información de este último archivo
            elif contador == tamArchivo: #Si ya se encontró espacio, entonces se recupera el byte desde el cual se puede escribir
                inicio -= tamArchivo #Con esto se obtiene el byte desde el cual se puede empezar a escribir la información
                break
            if inicio > espacioTotal: break #Esto me va a permitir salir del ciclo si no se encontró espacio y ya se recorrió toda la imagen
            inicio += 1
        imagen.close()
    if inicio > espacioTotal and espacioLibre >= tamArchivo: #Si hay espacio disponible pero no se encontró la ubicación, se compacta para revisar
        compactacion()#Esto no asegura nada porque en el espacio disponible no se toma en cuenta que hay clusters con poca información pero que son reservados por un archivo
    return ceil(inicio/tamCluster)

def espacioEntreDatos(tamArchivo): #Sirve para revisar si el archivo cabe entre 2 archivos almacenados y ya no buscar otro lugar
    archivos = list(infoArchivos.values()) 
    for i in range(len(archivos)-1):
        despuesDeArchivo1 = ceil((archivos[i][1] * tamCluster + archivos[i][0] + 1)/tamCluster)#Esto me da el cluster donde puedo empezar a contar
        antesdeArchivo2 = (archivos[i+1][1] * tamCluster - 1)//tamCluster #Esto me da el cluster hasta donde puedo contar
        if despuesDeArchivo1 < antesdeArchivo2 and antesdeArchivo2 <= clustersUnidad-5:
            if (antesdeArchivo2*tamCluster - despuesDeArchivo1*tamCluster) >= tamArchivo: #Quiere decir que si cabe la info del nuevo archivo
                return ceil(despuesDeArchivo1/tamCluster)
        else:
            break
    #En este punto quiere decir que no cupo los datos del nuevo archivo entre los ya existentes
    return ceil((archivos[-1][1] * tamCluster + archivos[-1][0])/tamCluster)#Devuelve el cluster donde puede seguir buscando

def asignacionEspacioDirectorio():
    inicio = tamCluster #El directorio empieza en el cluster 1
    with open(rutaImagen,'rb+') as imagen:
        imagen.seek(inicio)
        while (imagen.read(1)).decode("latin-1") != '/' and inicio < tamCluster*(numClusters + 1):#Controla la lectura del cluster 1 al 4
            inicio += 64 #Si la entrada ya está ocupada se la salta
            imagen.seek(inicio)
        imagen.close()
    return inicio #Aqui ya encontró una entrada disponible. Esto sucede porque antes invocar a la función, se revisó que hubieran entradas libres

def compactacion():
    print("COMPACTANDO ARCHIVOS1")
    inicio = numClusters + 1 #Se va a empezar a compactar desde el inicio del cluster de datos
    for llave in infoArchivos.keys(): #Para cada archivo del directorio
        with open(rutaImagen,'rb+') as imagen:
            imagen.seek(inicio*tamCluster)
            if imagen.read(1) == b'\x00':#Si el primer byte del cluster está vacío entonces se va a mover toda la info del archivo a ese cluster
                contenido = getInformacion(inicio*tamCluster,infoArchivos[llave][0],rutaImagen)
                imagen.write(contenido)
                escribirEnDirectorio(infoArchivos[llave][4],'-',llave,infoArchivos[llave][0],inicio,
                                     infoArchivos[llave][2],infoArchivos[llave][3])
            inicio += infoArchivos[llave][0] #Si ya está ocupado ese cluster, entonces el apuntador se desplaza la cantidad de bytes que mide el archivo que ocupa el cluster
            inicio = ceil(inicio/tamCluster)#Después se obtiene el próximo cluster a ese archivo para seguir buscando
            imagen.close()

def eliminarArchivo(sem1,sem2):
    while True:
        sem2.acquire()#Se bloquea el candado hasta que sea invocado en el menú
        if menu == '6': break
        listarContenido()
        try:
            opcion = int(input("\n\nEscribe el número del archivo que deseas borrar: "))
        except ValueError:
            print("Error 12: Por favor ingresa un número")
            sem1.release()
            continue
        max = len(infoArchivos)#Se usa para asegurarse que solo se ingrese alguna opción que aparece en la terminal
        if opcion < 0 or opcion > max-1:
            print("Error 10: La opción seleccionada no pertenece a ningún archivo") 
            sem1.release()#Como no se pudo hacer nada, el hilo main puede continuar y este se va a volver a bloquear al regresar al inicio del bucle
            continue
        for llave in infoArchivos.keys():
            if opcion == 0: #Se obtiene la llave del archivo a copiar
                nombreArchivo = llave
                break
            opcion -= 1
        #A continuación se va a sobreescribir toda esa entrada por los valores default de una entrada vacía
        escribirEnDirectorio(infoArchivos[nombreArchivo][4],'/',"##############",0,0,"00000000000000","00000000000000")
        escribirEnDatos(infoArchivos[nombreArchivo][1]*tamCluster,infoArchivos[nombreArchivo][0],rutaImagen,1)
        infoArchivos.pop(nombreArchivo) #Se borra el archivo del diccionario
        print("El archivo se ha eliminado con éxito!!")
        sem1.release()#Se libera el semáforo para el hilo main y este hilo se va a bloquear de nuevo

def mostrarInfoSistema():
    print(espacio + "INFORMACIÓN DEL SISTEMA DE ARCHIVOS\n")
    print(espacio + "Nombre: " + nombreSistema + "\n" + espacio + "Versión: " + version+ "\n" + espacio + "Etiqueta del volumen: " + etiqueta)
    print(espacio + "Tamaño del cluster: " + str(tamCluster) + " bytes"+ "\n" + espacio + "Tamaño del directorio: " + str(numClusters) + " clusters")
    print(espacio + "Tamaño de la unidad completa: " + str(clustersUnidad) + " clusters")
    print(espacio + "Entradas Ocupadas: " + str(archivos) + "    || Entradas Disponibles: " + str(archivosLibres) )
    print(espacio + "Espacio Disponible: " + str(espacioLibre) + " Bytes  || Espacio Ocupado: " + str(espacioNoLibre) + " Bytes\n\n")

def validarSistema():
    if nombreSistema != "FiUnamFS":
        print("\nERROR 1: El sistema de archivos utilizado es incorrecto, verifica que sea el archivo adecuado")
        return False
    if version != "24-2":
        print("\nERROR 2: La versión actual del sistema de archivos no coincide, VERSIÓN CORRECTA: \"24-2\"   VERSIÓN ACTUAL: \"" + version + "\"")
        return False
    return True
def main(sem1,sem2,sem3,sem4):
    global espacioTotal, espacioLibre,menu
    if validarSistema():
        espacioTotal = tamCluster * (clustersUnidad -5)
        espacioLibre = espacioTotal - espacioNoLibre
        while menu != '0':
            leerDirectorio()
            imprimirMenu()
            menu = input("\n\n"+ espacio +"Escribe el número asociado a la opción que deseas acceder: ")
            limpiarPantalla()
            if menu == '1':
                listarContenido()
            elif menu == '2': 
                sem2.release()
                sem1.acquire()
                #sem2.release()
            elif menu == '3': 
                sem3.release()
                sem1.acquire()
                #sem3.release()
                espacioLibre = espacioTotal - espacioNoLibre
            elif menu == '4':
                sem4.release()
                sem1.acquire()
                #sem4.release()
                espacioLibre = espacioTotal - espacioNoLibre
            elif menu == '5': 
                mostrarInfoSistema()
            elif menu == '6': 
                sem2.release()#Como inicialmente se bloquean los demás hilos, se desbloquean para que terminen su función
                sem3.release()
                sem4.release()
                break
            else: 
                print("ERROR 3: Por favor seleccione una de las opciones mostradas en pantalla...")
            input("\n\nPRESIONE ENTER PARA CONTINUAR")
            limpiarPantalla()
    print("\nCerrando Sistema de Archivos...")

#Variables Globales
while True:
    rutaImagen = input("Ingrese la ruta donde se encuentra la imagen del Sistema de Archivos: ")
    if path.exists(rutaImagen) == False: 
        print("\nError 5: La ruta proporcionada no existe, revisa que la hayas escrito bien.\n")
    else:
        limpiarPantalla()
        break
formatoFecha = "%Y%m%d%H%M%S" #Es el formato definido para guardar en el directorio
formatoFechaBonita = "%Y/%m/%d %H:%M:%S" #Es el formato para imprimirse en la terminal
espacio = " " * 5 #Solo se definió para poder imprimir con un espacio antes del contenido
infoArchivos = {} #Aqui se van a guardar los nombres de los archivos y su información
nombreSistema = leer_texto(0,8)
version = leer_texto(10,4)
etiqueta = leer_texto(20,19) #En la descripción del proyecto hay un error con la cantidad de bytes
tamCluster = leer_numEntero(40,4)
numClusters = leer_numEntero(45,4)
clustersUnidad = leer_numEntero(50,4)
archivos = 0 #Indica la cantidad de archivos actual en el directorio
archivosLibres = 0 #Indica cuantas entradas sobran en el directorio
espacioTotal = 0 #Indica el espacio total para guardar datos
espacioNoLibre = 0  #Indica el espacio ocupado por los archivos
espacioLibre = 0 #Indica el espacio disponible para guardar datos
menu = '1' #Es global para cuando se finalice el programa, los hilos no muestren nada en pantalla

#Hilos y semáforos
menu = Semaphore(0) #Permite al hilo principal seguir la función principal
copiarSistema = Semaphore(0) #Sirve para indicarle al hilo de la función 2 que ejecute todas sus instrucciones
copiarCompu = Semaphore(0) #Sirve para indicarle al hilo de la función 3 que ejecute todas sus instrucciones
eliminar = Semaphore(0) #Sirve para indicarle al hilo de la función 4 que ejecute todas sus instrucciones
Thread(target=main,args=[menu,copiarSistema,copiarCompu,eliminar]).start()
Thread(target=copiarArchivoACompu,args=[menu,copiarSistema]).start()
Thread(target=copiarArchivoASistema,args=[menu,copiarCompu]).start()
Thread(target=eliminarArchivo,args=[menu,eliminar]).start()