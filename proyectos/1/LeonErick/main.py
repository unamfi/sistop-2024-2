#León Gómez Erick 
import os
import struct
import datetime
from threading import Thread, Semaphore

# Variables globales
directorio_fisico = ""
ruta_FiUnamFS = ""
mutex_archivo = Semaphore(1)

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

def validar_FiUnamFS():
    global ruta_FiUnamFS
    # Verificar si el archivo es de tamaño 1MB
    try:
        if os.path.getsize(ruta_FiUnamFS) != 1440*1024:
            print("Error: El archivo no tiene el tamaño correcto. El tamaño debe ser de 1440 Kilobytes.")
            return False
    except PermissionError:
        print("Error: No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
        return False



# Función principal
if __name__ == "__main__":
    print("Bienvenido al sistema de archivos FiUnamFS")
    print("El programa solo funciona en Linux.")
    print("Por favor, siga las instrucciones para continuar.")
    print("--------------------------------------------------")
    obtener_FiUnamFS()
    validar_FiUnamFS()
    pass