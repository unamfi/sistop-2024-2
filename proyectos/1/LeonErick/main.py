#León Gómez Erick
#pip install prettytable
import os
import struct
import datetime
from time import sleep
from threading import Thread, Semaphore, Barrier, Lock
from prettytable import PrettyTable

# Variables globales
directorio_fisico = ""
ruta_FiUnamFS = ""
etiqueta_volumen = ""
tamano_cluster_bytes = 0
num_clusters_dir = 0
num_clusters_total = 0
mutex_archivo = Lock()
directorio = []

def show_menu():
    print("1. Listar los contenidos del directorio")
    print("2. Copiar un archivo de FiUnamFS hacia el sistema de archivos local")
    print("3. Copiar un archivo del sistema de archivos local hacia FiUnamFS")
    print("4. Eliminar un archivo de FiUnamFS")
    print("5. Salir")
    try:
        option = int(input("Seleccione una opción: "))
        if option < 1 or option > 5:
            print("Error: Opción no válida. Por favor, seleccione una opción entre 1 y 5.")
            return show_menu()
        # Exito
        return option
    except ValueError:
        print("Error: Entrada no válida. Por favor, ingrese un número.")
        return show_menu()

def obtener_FiUnamFS():
    global directorio_fisico
    global ruta_FiUnamFS
    # Obtener el directorio actual
    directorio_fisico = os.path.dirname(os.path.abspath(__file__))
    # Revisar si existe un archivo llamado fiunamfs.img 
    ruta_FiUnamFS = os.path.join(directorio_fisico, "fiunamfs.img")
    print(ruta_FiUnamFS)
    try:
        if not os.path.exists(ruta_FiUnamFS):
            print("Ingrese el nombre con el que se tiene guardado el sistema de archivos FiUnamFS: ")
            ruta_FiUnamFS = input()
            ruta_FiUnamFS = os.path.join(directorio_fisico, ruta_FiUnamFS)
            if not os.path.exists(ruta_FiUnamFS):
                print(ruta_FiUnamFS)
                print("Error: El archivo no existe.")
                return obtener_FiUnamFS()
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False

def leer_numero(posicion):
    global ruta_FiUnamFS
    # Leer el archivo
    mutex_archivo.acquire()
    try:
        with open(ruta_FiUnamFS, "rb") as f:
            f.seek(posicion)
            numero = struct.unpack('<I', f.read(4))
        mutex_archivo.release()
        return numero[0]
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        mutex_archivo.release()
        return False
    
def escribir_numero(posicion, numero):
    global ruta_FiUnamFS
    # Escribir en el archivo
    mutex_archivo.acquire()
    try:
        with open(ruta_FiUnamFS, "r+b") as f:
            f.seek(posicion)
            f.write(struct.pack('<I', numero))
        mutex_archivo.release()
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        mutex_archivo.release()
        return False
    
def leer_ascii8(posicion, longitud):
    global ruta_FiUnamFS
    # Leer el archivo
    mutex_archivo.acquire()
    try:
        with open(ruta_FiUnamFS, "rb") as f:
            f.seek(posicion)
            caracteres = f.read(longitud).decode('latin-1')
        mutex_archivo.release()
        return caracteres
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        mutex_archivo.release()
        return False
    
def escribir_caracteres(posicion, cadena):
    global ruta_FiUnamFS
    # Escribir en el archivo
    mutex_archivo.acquire()
    try:
        with open(ruta_FiUnamFS, "r+b") as f:
            f.seek(posicion)
            f.write(bytearray(cadena, 'latin-1'))
        mutex_archivo.release()
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        mutex_archivo.release()
        return False
    
def leer_ascii7(posicion, longitud):
    global ruta_FiUnamFS
    # Leer el archivo
    mutex_archivo.acquire()
    try:
        with open(ruta_FiUnamFS, "rb") as f:
            f.seek(posicion)
            caracteres = f.read(longitud).decode('ascii')
        mutex_archivo.release()
        return caracteres
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        mutex_archivo.release()
        return False

def escribir_ascii7(posicion, cadena):
    global ruta_FiUnamFS
    # Escribir en el archivo
    mutex_archivo.acquire()
    try:
        with open(ruta_FiUnamFS, "r+b") as f:
            f.seek(posicion)
            f.write(bytearray(cadena, 'ascii'))
        mutex_archivo.release()
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        mutex_archivo.release()
        return False

def validar_FiUnamFS():
    global ruta_FiUnamFS
    global etiqueta_volumen
    global tamano_cluster_bytes
    global num_clusters_dir
    global num_clusters_total
    # Verificar si el archivo es de tamaño 1440 Kilobytes
    try:
        if os.path.getsize(ruta_FiUnamFS) != 1440*1024:
            print("Error: El archivo no tiene el tamaño correcto. El tamaño debe ser de 1440 Kilobytes.")
            return False
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False
    # Verificar nombre del sistema de archivos
    nombre_FiUnamFS = leer_ascii8(0, 8)
    if nombre_FiUnamFS != "FiUnamFS":
        print("Error: El nombre del sistema de archivos no es correcto.")
        return False
    # Verificar versión de la implementación
    version_FiUnamFS = leer_ascii8(10, 4)
    if version_FiUnamFS != "24-2":
        print("Error: La versión de la implementación no es correcta.")
        return False
    etiqueta_volumen = leer_ascii7(20, 19)
    tamano_cluster_bytes = leer_numero(40)
    num_clusters_dir = leer_numero(45)
    num_clusters_total = leer_numero(50)
    print(etiqueta_volumen)
    print(tamano_cluster_bytes)
    print(num_clusters_dir)
    print(num_clusters_total)
    print("Sistema de archivos FiUnamFS cargado exitosamente.")
    
def obtener_fecha():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S")

def imprimir_fecha(fecha):
    return fecha[0:4] + "-" + fecha[4:6] + "-" + fecha[6:8] + " " + fecha[8:10] + ":" + fecha[10:12] + ":" + fecha[12:14]

class info_archivo:
    def __init__(self, nombre_archivo, tam_bytes, cluster_ini, creacion, modificacion):
        self.nombre_archivo = nombre_archivo
        self.tam_bytes = tam_bytes
        self.cluster_ini = cluster_ini
        self.creacion = creacion
        self.modificacion = modificacion
    
from prettytable import PrettyTable

def print_info_archivos():
    global directorio
    table = PrettyTable()
    table.field_names = ["  Nombre  ", "  Tamaño (bytes)  ", "  Cluster inicial  ", "  Fecha de creación  ", "  Fecha de modificación  "]
    for archivo in directorio:
        table.add_row([archivo.nombre_archivo, archivo.tam_bytes, archivo.cluster_ini, imprimir_fecha(archivo.creacion), imprimir_fecha(archivo.modificacion)])
    print(table)


def leer_directorio():
    global ruta_FiUnamFS
    global tamano_cluster_bytes
    global num_clusters_dir
    global directorio
    directorio = [] * num_clusters_dir
    print("Leyendo directorio")
    for i in range(tamano_cluster_bytes, tamano_cluster_bytes * (num_clusters_dir + 1), 64):
        tipo_archivo = leer_ascii8(i, 1)
        if tipo_archivo == "-":
            nombre_archivo = leer_ascii7(i + 1, 15)
            tam_bytes = leer_numero(i + 16)
            cluster_ini = leer_numero(i + 20)
            creacion = leer_ascii8(i + 24, 14)
            modificacion = leer_ascii8(i + 38, 14)
            archivo = info_archivo(nombre_archivo, tam_bytes, cluster_ini, creacion, modificacion)
            directorio.append(archivo)
    print_info_archivos()

    


# Función principal
if __name__ == "__main__":
    print("Bienvenido al sistema de archivos FiUnamFS")
    print("El programa solo funciona en Linux.")
    print("Por favor, siga las instrucciones para continuar.")
    print("--------------------------------------------------")
    obtener_FiUnamFS()
    validar_FiUnamFS()
    leer_directorio()
    pass