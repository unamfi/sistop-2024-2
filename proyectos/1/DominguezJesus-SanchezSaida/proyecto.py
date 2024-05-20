import os
from struct import *
import struct
import threading

#Abriendo el FS
img_FS="fiunamfs.img"
FS = open(img_FS,"r+b")

#Se muestran los datos del superbloque
FS.seek(0)
nombre_FS = FS.read(8).decode('ascii')
FS.seek(10)
version = FS.read(10).decode('ascii')
etiqueta_volumen = FS.read(20).decode('ascii')
totalsuperbloque = FS.read(54)
tamaño_cluster = unpack("<I", totalsuperbloque[40:44])[0]
num_cluster_dir = unpack("<I", totalsuperbloque[45:49])[0]
num_cluster_uni = unpack("<I", totalsuperbloque[50:54])[0]

print("Nombre del sistema de archivos: ",nombre_FS,"\n",
      "Version: ",version,"\n",
      "Etiqueta del Volumen: ",etiqueta_volumen, "\n",
      "Tamaño del cluster: ",tamaño_cluster, "bytes", "\n",
      "Numero de cluster que mide el directorio: ",num_cluster_dir, "\n",
      "Numero de cluster que mide la unidad completa: ",num_cluster_uni)

#Inicializamos variables globales
tamanoClusters = 0 
num_cluster_dir = 0
num_cluster_uni = 0
tamanoDirectorio = 0
id_FS = ""
version = ""
etiqueta_volumen = ""

#Lista y clase de archivos del directorio
archivos = []
class archivo:
    def _init_(self, nombre, tamano, clusterInicial,): 
        self.nombre = nombre
        self.tamano = tamano
        self.clusterInicial = clusterInicial

#Leer datos enteros
def leerDatos(inicio,tamano):
    global FS
    FS.seek(inicio)
    return FS.read(tamano)

#Leer datos ASCII
def leerDatosASCII(inicio,tamano):
    global FS 
    FS.seek(inicio)
    datos = FS.read(tamano)
    return datos.decode("ascii")

#Convertir datos ASCII
def datoUnpack(inicio, tamano):
    global FS
    FS.seek(inicio)
    dato = FS.read(tamano)
    return struct.unpack('<i', dato)[0]

#Escribir datos al sistema de archivos
def datosPack(inicio, dato):
    global FS
    FS.seek(inicio)
    dato = struct.pack('<i', dato)
    return FS.write(dato)

#Leer los datos del archivo en ASCII
def leerDatosArchivo(posicion):
    inicio = 1024 + (posicion * 64)
    nombre = leerDatosASCII(inicio + 1, 14)
    if nombre.strip('.') != "":
        tamano = datoUnpack(inicio + 16, 4)
        clusterInicial = datoUnpack(inicio+20,4)
        return archivo(nombre, tamano, clusterInicial)
    return None

#Escribir datos ASCII al sistema de archivos
def escribirDatosASCII(inicio, dato):
    global FS
    FS.seek(inicio)
    dato = dato.encode("ascii")  # Mantener "ascii"
    return FS.write(dato)


"""Inicio de actividaades"""

#Recopilará la información de cada archivo
def listarArchivos():
    global FS,tamaño_cluster
    infoArchivo = []
    for i in range (64):
        tam = 1024 + (i*64)
        FS.seek(tam)
        lectura = FS.read(15)
        if lectura != b'/##############':
            FS.seek(tam+0)
            print("Tipo de archivo: ",FS.read(1).decode().strip())

            FS.seek(tam+1)
            print("Archivo: ",FS.read(15).decode().strip())

            FS.seek(tam+24)
            Hora_Fecha = FS.read(14).decode().strip()
            print("Fecha de creación del archivo: ", Hora_Fecha[0:4],"-",Hora_Fecha[4:6],"-", Hora_Fecha[6:8]," ",Hora_Fecha[8:10],":", Hora_Fecha[10:12],":",Hora_Fecha[12:14])

            FS.seek(tam+38)
            Hora_Fecha = FS.read(14).decode().strip()
            print("Fecha de modificación del archivo: ", Hora_Fecha[0:4],"-",Hora_Fecha[4:6],"-", Hora_Fecha[6:8]," ",Hora_Fecha[8:10],":", Hora_Fecha[10:12],":",Hora_Fecha[12:14])
            print("\n")

# Verificamos si el archivo existe en nuestro directorio
def verificarArchivo(nombreCopia):
    global archivos
    for i in archivos:
        if i.nombre.strip() == nombreCopia.strip():
            return archivos.index(i), True
    return -1,False

# Función para copiar un archivo del sistema de archivos a la computadora
def exportar(nombreCopia, rutaNueva):
    # Verificamos si el archivo que se quiere copiar existe en nuestro directorio
    indexArchivo, validacion = verificarArchivo(nombreCopia)
    if not validacion:
        print("El archivo no existe")
        return

    # Archivo que se quiere copiar
    archivoC = archivos[indexArchivo]

    print(f"tamano del archivo a copiar: {archivoC.tamano}")

    # Crear el archivo en la ruta especificada
    if os.path.exists(rutaNueva):
        if os.path.isfile(os.path.join(rutaNueva, nombreCopia)):
            rutaArchivoDestino = os.path.join(rutaNueva, "copia de " + nombreCopia)
        else:
            rutaArchivoDestino = os.path.join(rutaNueva, nombreCopia)

        with open(rutaArchivoDestino, "wb") as destino:
            inicio_lectura = archivoC.clusterInicial * tamanoClusters
            FS.seek(inicio_lectura)
            datos_archivo = FS.read(archivoC.tamano)
            destino.write(datos_archivo)

        print("Archivo copiado con éxito")
    else:
        print("La ruta especificada no existe")

def borrarArchivo(nombreArchivo):
    global archivos
    global tamanoClusters
    global FS

    # Verificamos si el archivo que se quiere borrar existe en nuestro directorio
    indexArchivo, validacion = verificarArchivo(nombreArchivo)
    if validacion != True:
        print("El archivo no existe")
        return

    # Archivo que se quiere borrar
    archivoBorrar = archivos[indexArchivo]

    # Eliminamos el archivo del directorio
    archivos.pop(indexArchivo)

    # Marcar la entrada en el directorio como eliminada
    FS.seek(1024 + indexArchivo * 64)
    FS.write(b'\x00')

    # Marcamos los clusters correspondientes como libres
    FS.seek(archivoBorrar.clusterInicial * tamanoClusters)
    FS.write(b'\x00' * archivoBorrar.tamano)

    # Recargar la lista de archivos del directorio
    archivos = []
    listarDirectorio()

    print("Archivo eliminado con éxito")

def datosEstaticos():
    global nombre_FS
    global version
    global etiqueta_volumen
    global tamano_cluster
    global num_cluster_dir
    global num_cluster_uni
    global tamanoDirectorio

    #Identificación del sistema de archivos por defecto
    id_FS = leerDatosASCII(0,8)

    #Versión de la implementación
    version = leerDatosASCII(10,4)

    #Etiqueta del volumen
    etiqueta_volumen = leerDatosASCII(20,19)

    #tamano de un cluster
    tamanoClusters = datoUnpack(40,4)

    #Número de clusters que mide el directorio
    num_cluster_dir = datoUnpack(45,4)

    #Número de clusters que mide la unidad completa
    num_cluster_uni = datoUnpack(50,4)

    #tamano del directorio por defecto
    tamanoDirectorio = 64


def menu():
    while True:
        print("1. Listar el contenido del directorio")
        print("2. Copiar archivo de FiUnamFS a la computadora")
        print("3. Copiar archivo de la computadora hacia FiUnamFS")
        print("4. Borrar archivo de FiUnamFS")
        print("5. Salir")
        opcion = int(input("Ingresa una opción: "))
        if opcion == 1:
            listarArchivos()
        elif opcion == 2:
            nombreCopia = input("Ingresa el nombre del archivo que deseas exportar (incluye la extensión): ")
            #Si se desea copiar a la ruta en donde se encuentra este archivo:
            rutaCopiar = os.path.dirname(os.path.abspath(__file__))

            #Si se desea copiar a una ruta específica:
            #rutaCopiar = input("Ingresa la ruta donde deseas copiar el archivo: ").replace("\\","/")
            exportar(nombreCopia, rutaCopiar)
        ##elif opcion == 3:
            ##importar(input("Ingresa la ruta de donde deseas copiar el archivo (incluye el archivo con su extensión): ").replace("\\","/"))
        elif opcion == 4:
            nombreArchivo = input("Ingresa el nombre del archivo que deseas borrar (incluye la extensión): ")
            borrarArchivo(nombreArchivo)
        elif opcion == 5:
            break
        else:
            print("Opción inválida")


menu()