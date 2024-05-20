#León Gómez Erick
import os
import struct
import datetime
from threading import Thread, Barrier
from prettytable import PrettyTable

# Variables globales
directorio_fisico = ""
ruta_FiUnamFS = ""
etiqueta_volumen = ""
tamano_cluster_bytes = 0
num_clusters_dir = 0
num_clusters_total = 0
directorio = []
cluster_set = set()
menu = 0
# Barrera para sincronizar hilos
# Se utilizan 3 hilos para verificar las condiciones
# 2 trabajadores y 1 principal
barrier = Barrier(3)
cluster_ini = -1
tam_bytes = 0
rvtb = False
rbat = False

# Clase para almacenar la información de los archivos como objetos en una lista
class info_archivo:
    def __init__(self, nombre_archivo, tam_bytes, cluster_ini, creacion, modificacion, pos):
        self.nombre_archivo = nombre_archivo
        self.tam_bytes = tam_bytes
        self.cluster_ini = cluster_ini
        self.creacion = creacion
        self.modificacion = modificacion
        # Posición en el directorio
        self.pos = pos

# Formato para imprimir texto con colores
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

# Función que imprime el menú de opciones hasta que el usuario seleccione una opción válida
def show_menu():
    prLightPurple("--------------------------------------------------")
    prRed("Menú de opciones")
    prLightPurple("--------------------------------------------------")
    print()
    print("Ingrese el número de la acción que desea realizar:")
    print("1. Listar los contenidos del directorio")
    print("2. Copiar un archivo de FiUnamFS hacia el sistema de archivos local")
    print("3. Copiar un archivo del sistema de archivos local hacia FiUnamFS")
    print("4. Eliminar un archivo de FiUnamFS")
    print("5. Salir")
    print()
    try:
        option = int(input("Seleccione una opción: "))
        if option < 1 or option > 5:
            print("Error: Opción no válida. Por favor, seleccione una opción entre 1 y 5.")
            return show_menu()
        return option
    except ValueError:
        print("Error: Entrada no válida. Por favor, ingrese un número.")
        return show_menu()

# Función que obiene la ruta del archivo FiUnamFS
def obtener_FiUnamFS():
    global directorio_fisico
    global ruta_FiUnamFS
    # Se obtiene el directorio donde se encuentra el archivo main.py
    directorio_fisico = os.path.dirname(os.path.abspath(__file__))
    # Se revisa si existe un archivo llamado fiunamfs.img 
    ruta_FiUnamFS = os.path.join(directorio_fisico, "fiunamfs.img")
    # Si no existe, se solicita al usuario que ingrese el nombre del archivo
    try:
        if not os.path.exists(ruta_FiUnamFS):
            print("Ingrese el nombre (o la ruta relativa) del sistema de archivos FiUnamFS: ")
            ruta_FiUnamFS = input()
            ruta_FiUnamFS = os.path.join(directorio_fisico, ruta_FiUnamFS)
            if not os.path.exists(ruta_FiUnamFS):
                print("Error: El archivo no existe.")
                return obtener_FiUnamFS()
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False

# Función para leer un número de 4 bytes en formato little-endian
def leer_numero(posicion):
    global ruta_FiUnamFS
    try:
        with open(ruta_FiUnamFS, "rb") as f:
            f.seek(posicion)
            numero = struct.unpack('<I', f.read(4))
        return numero[0]
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False

# Función para escribir un número de 4 bytes en formato little-endian
def escribir_numero(posicion, numero):
    global ruta_FiUnamFS
    try:
        with open(ruta_FiUnamFS, "r+b") as f:
            f.seek(posicion)
            f.write(struct.pack('<I', numero))
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False

# Función para leer cadenas de caracteres en formato ASCII 8-bit
def leer_ascii8(posicion, longitud):
    global ruta_FiUnamFS
    try:
        with open(ruta_FiUnamFS, "rb") as f:
            f.seek(posicion)
            caracteres = f.read(longitud).decode('latin-1')
        return caracteres
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False

# Funciones para escribir cadenas de caracteres en formato ASCII 8-bit
def escribir_ascii8(posicion, cadena):
    global ruta_FiUnamFS
    try:
        with open(ruta_FiUnamFS, "r+b") as f:
            f.seek(posicion)
            f.write(bytearray(cadena, 'latin-1'))
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False

# Funciones para leer cadenas de caracteres en formato ASCII 7-bit
def leer_ascii7(posicion, longitud):
    global ruta_FiUnamFS
    try:
        with open(ruta_FiUnamFS, "rb") as f:
            f.seek(posicion)
            caracteres = f.read(longitud).decode('ascii')
        return caracteres
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False

# Funciones para escribir cadenas de caracteres en formato ASCII 7-bit
def escribir_ascii7(posicion, cadena):
    global ruta_FiUnamFS
    try:
        with open(ruta_FiUnamFS, "r+b") as f:
            f.seek(posicion)
            f.write(bytearray(cadena, 'ascii'))
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False

# Función para validar el sistema de archivos FiUnamFS en base al superbloque
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
    # Se obtiene la información restante del superbloque
    etiqueta_volumen = leer_ascii7(20, 19)
    tamano_cluster_bytes = leer_numero(40)
    num_clusters_dir = leer_numero(45)
    num_clusters_total = leer_numero(50)
    print("Sistema de archivos FiUnamFS cargado exitosamente.")

# Funciones para dar formato a las fechas
def formato_fecha(fecha):
    return fecha.strftime("%Y%m%d%H%M%S")
def imprimir_fecha(fecha):
    return fecha[0:4] + "-" + fecha[4:6] + "-" + fecha[6:8] + " " + fecha[8:10] + ":" + fecha[10:12] + ":" + fecha[12:14]

# Función para imprimir la información de los archivos en el directorio de manera más legible
def print_info_archivos():
    # Lista con toda la información de los archivos
    global directorio
    table = PrettyTable()
    table.field_names = ["  Nombre  ", "  Tamaño (bytes)  ", "  Cluster inicial  ", "  Fecha de creación  ", "  Fecha de modificación  "]
    for archivo in directorio:
        table.add_row([archivo.nombre_archivo, archivo.tam_bytes, archivo.cluster_ini, imprimir_fecha(archivo.creacion), imprimir_fecha(archivo.modificacion)])
    print(table)

# Función para leer los clusters del directorio y obtener la información de los archivos
def leer_directorio(show=True):
    global ruta_FiUnamFS
    global tamano_cluster_bytes
    global num_clusters_dir
    global directorio
    global cluster_set
    # Se crea un conjunto con los clusters disponibles
    for i in range(num_clusters_dir + 1, num_clusters_total):
        cluster_set.add(i)
    directorio = [] * num_clusters_dir
    # Se lee la información de los archivos en el directorio de 64 en 64 bytes
    for i in range(tamano_cluster_bytes, tamano_cluster_bytes * (num_clusters_dir + 1), 64):
        tipo_archivo = leer_ascii8(i, 1)
        if tipo_archivo == "-":
            nombre_archivo = leer_ascii7(i + 1, 15)
            # Para tener compatibilidad con el estado inicial del sistema de archivos
            # se eliminan los caracteres "#" que se encuentren en el nombre del archivo
            # y se limita la extensión a 3 caracteres
            nombre_archivo = nombre_archivo.replace("#", "")
            dot = nombre_archivo.find(".")
            nombre_archivo = nombre_archivo[:dot] + "." + nombre_archivo[dot+1:dot+4]
            tam_bytes = leer_numero(i + 16)
            cluster_ini = leer_numero(i + 20)
            creacion = leer_ascii8(i + 24, 14)
            modificacion = leer_ascii8(i + 38, 14)
            archivo = info_archivo(nombre_archivo, tam_bytes, cluster_ini, creacion, modificacion, i)
            # Se añade el archivo a la lista de archivos y se eliminan los clusters del conjunto de disponibles
            directorio.append(archivo)
            for j in range(cluster_ini, cluster_ini + ((tam_bytes+tamano_cluster_bytes-1) // tamano_cluster_bytes)):
                if j in cluster_set:
                    cluster_set.remove(j)
    if show:
        print_info_archivos()

# Función para buscar un archivo en el directorio por su nombre
def buscar_archivo(nombre_archivo):
    global directorio
    for archivo in directorio:
        if archivo.nombre_archivo == nombre_archivo:
            return archivo
    return None

# Función para copiar un archivo de FiUnamFS hacia el sistema de archivos local
# Recibe el nombre del archivo en FiUnamFS y la ruta donde se guardará el archivo localmente
def fiunamfs_to_local(nombre_archivo, ruta_local):
    archivo = buscar_archivo(nombre_archivo)
    if archivo is None:
        print("Error: El archivo no existe.")
        return False
    cluster_actual = archivo.cluster_ini
    tam_bytes = archivo.tam_bytes
    archivo_local = os.path.join(directorio_fisico, ruta_local)
    try:
        with open(ruta_FiUnamFS, "rb") as f:
            f.seek(cluster_actual * tamano_cluster_bytes)
            info = f.read(tam_bytes)
        with open(archivo_local, "wb") as f:
            f.write(info)
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False


# Función para encontrar un cluster contiguo de tamaño suficiente para almacenar un archivo de tamaño tam_bytes
def encontrar_contiguo(tam_bytes):
    global cluster_set
    contiguo = -1
    contiguo_actual = 0
    for cluster in cluster_set:
        contiguo_actual += 1
        if contiguo_actual == (tam_bytes+tamano_cluster_bytes-1) // tamano_cluster_bytes:
            contiguo = cluster - contiguo_actual + 1
            break
    return contiguo

# Función que verifica si hay espacio suficiente en el sistema de archivos para almacenar un archivo externo
def verify_tam_bytes(ruta_local):
    global directorio
    global cluster_set
    # Funciones globales que referencan los resultados de esta función
    global cluster_ini
    global tam_bytes
    global rvtb
    tam_bytes = os.path.getsize(os.path.join(directorio_fisico, ruta_local))
    if tam_bytes > tamano_cluster_bytes * len(cluster_set):
        print("Error: El archivo es demasiado grande para ser almacenado en el sistema de archivos FiUnamFS.")
        rvtb = False
        barrier.wait()
        return
    # Se encuentra un cluster donde se pueda almacenar el archivo
    cluster_ini = encontrar_contiguo(tam_bytes)
    if cluster_ini == -1:
        print("Error: No hay suficiente espacio contiguo en el sistema de archivos FiUnamFS.")
        rvtb = False
        barrier.wait()
        return
    rvtb = True
    barrier.wait()

# Función sincronizada que busca si ya existe un archivo con el mismo nombre
def buscar_archivo_thread(nombre_archivo):
    global rbat
    archivo = buscar_archivo(nombre_archivo)
    if archivo is not None:
        print("Error: Ya existe un archivo con ese nombre.")
        rbat = False
        barrier.wait()
        return
    rbat = True
    barrier.wait()

# Función para copiar un archivo del sistema de archivos local hacia FiUnamFS
def local_to_fiunamfs(ruta_local, nombre_archivo):
    # Se crean dos hilos para verificar las condiciones necesarias para copiar el archivo
    verify_thread = Thread(target=verify_tam_bytes, args=(ruta_local,))
    buscar_thread = Thread(target=buscar_archivo_thread, args=(nombre_archivo,))
    verify_thread.start()
    buscar_thread.start()
    # Se espera a que ambos hilos terminen para continuar
    barrier.wait()
    # Si no se cumple alguna de las condiciones, se cancela la operación
    # El motivo lo imprime el hilo correspondiente
    if not rvtb or not rbat:
        return False
    try:
        with open(ruta_FiUnamFS, "r+b") as f:
            f.seek(cluster_ini * tamano_cluster_bytes)
            with open(os.path.join(directorio_fisico, ruta_local), "rb") as f_local:
                info = f_local.read()
                f.write(info)
        # Se actualiza el conjunto de clusters disponibles
        for i in range(cluster_ini, cluster_ini + ((tam_bytes+tamano_cluster_bytes-1) // tamano_cluster_bytes)):
            if i in cluster_set:
                cluster_set.remove(i)
        # Se obtiene la fecha de creación y modificación del archivo de los metadatos y se le da formato
        creacion = formato_fecha(datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(directorio_fisico, ruta_local))))
        modificacion = formato_fecha(datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(directorio_fisico, ruta_local))))
        # Se escribe la información del archivo en el directorio
        for i in range(tamano_cluster_bytes, tamano_cluster_bytes * (num_clusters_dir + 1), 64):
            tipo_archivo = leer_ascii8(i, 1)
            if tipo_archivo == "/":
                escribir_ascii8(i, "-")
                escribir_ascii7(i + 1, nombre_archivo)
                escribir_numero(i + 16, tam_bytes)
                escribir_numero(i + 20, cluster_ini)
                escribir_ascii8(i + 24, creacion)
                escribir_ascii8(i + 38, modificacion)
                break
        # Se actualiza la información del directorio sin imprimirlo
        leer_directorio(False)
        return True
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False

# Función para eliminar un archivo del directorio
def eliminar_archivo(nombre_archivo):
    global directorio
    archivo = buscar_archivo(nombre_archivo)
    if archivo is None:
        print("Error: El archivo no existe.")
        return False
    print("Borrando archivo...")
    # Si encuentra el archivo unicamente se borra en el directorio
    escribir_ascii8(archivo.pos, "/")
    escribir_ascii7(archivo.pos+1, "###############")
    leer_directorio(False)

# Función principal
def main():
    # Verificaciones iniciales
    global menu
    print()
    prGreen("Bienvenido al sistema de archivos FiUnamFS")
    print()
    print("Por favor, siga las instrucciones para continuar.")
    prLightPurple("--------------------------------------------------")
    obtener_FiUnamFS()
    validar_FiUnamFS()
    # Control del menú de opciones
    while menu != 5:
        menu = show_menu()
        if menu == 1:
            leer_directorio()
        elif menu == 2:
            print("Ingrese el nombre del archivo que desea copiar: ")
            nombre_archivo = input()
            print("Ingrese el nombre (o la ruta relativa) donde desea guardar el archivo: ")
            ruta_local = input()
            fiunamfs_to_local(nombre_archivo, ruta_local)
        elif menu == 3:
            print("Ingrese el nombre (o la ruta relativa) del archivo que desea copiar: ")
            ruta_local = input()
            print("Ingrese el nombre del archivo en FiUnamFS: ")
            nombre_archivo = input()
            local_to_fiunamfs(ruta_local, nombre_archivo)
        elif menu == 4:
            print("Ingrese el nombre del archivo que desea eliminar: ")
            nombre_archivo = input()
            eliminar_archivo(nombre_archivo)
    print("Saliendo del programa...")

# Instrucciones a ejecutarse si el archivo es ejecutado directamente
if __name__ == "__main__":
    main()