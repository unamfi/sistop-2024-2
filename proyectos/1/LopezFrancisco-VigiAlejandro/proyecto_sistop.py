import os               #Importa el módulo 'os' que proporciona funciones para interactuar con el sistema operativo
import struct           #Importa el módulo 'struct' que permite interpretar cadenas de bytes como estructuras binarias
import threading        #Importa el módulo 'threading' que proporciona funcionalidad de subprocesos para realizar múltiples tareas de forma simultánea
from os import system   # Importa solo la función 'system' del módulo 'os'

# Variables globales
sector = 512                            #La superficie del disco se divide en sectores de 512 bytes.
cluster = sector * 4                    #Cada cluster mide cuatro sectores.
direccionSistema = "fiunamfs.img"       #Direccion de el archivo fiunamfs.img            

# Función para leer un entero desde el archivo en una posición específica
def leerEntero(posicion, numero):
    with open(direccionSistema, "rb") as archivo:   #Abre el archivo en modo binario de solo lectura
        archivo.seek(posicion)                      #Mueve el puntero del archivo a la posición especificada
        dato = archivo.read(numero)                 #Lee el número de bytes especificado desde la posición actual
        num = struct.unpack("<I", dato)[0]          #Desempaqueta los bytes leídos en un entero (asumiendo formato little-endian)
        return num                                  #Devuelve el entero leído

# Función para leer una cadena desde el archivo en una posición específica
def leerCadena(posicion, numero):
    with open(direccionSistema, "rb") as archivo:   #Abre el archivo en modo binario de solo lectura
        archivo.seek(posicion)                      #Mueve el puntero del archivo a la posición especificada
        cadena = archivo.read(numero)               #Lee el número de bytes especificado desde la posición actual
        string = cadena.decode("ascii").strip()     #Decodifica los bytes leídos en una cadena ASCII y elimina espacios en blanco alrededor
        return string                               #Devuelve la cadena leída

# Función que recopila la información del server ubicada en el primer cluster
def validarSistemaArchivos():
    os.system("cls")                                #Limpia la pantalla de la consola (solo en sistemas Windows)
    nombreSistema = leerCadena(0, 9)                #Lee la cadena de nombre de sistema desde la posición 0 con longitud 9 bytes
    version = leerCadena(10, 5)                     #Lee la cadena de versión desde la posición 10 con longitud 5 bytes
    etiqueta = leerCadena(20, 16)                   #Lee la cadena de etiqueta del volumen desde la posición 20 con longitud 16 bytes
    tamaio_cluster = leerEntero(40, 4)              #Lee un entero que representa el tamaño del cluster desde la posición 40 con longitud 4 bytes
    cantidadclusters = leerEntero(44, 4)            #Lee un entero que representa la cantidad de clusters que mide el directorio desde la posición 44 con longitud 4 bytes
    ccl = leerEntero(48, 4)                         #Lee un entero que representa la cantidad de clusters que mide toda la unidad desde la posición 48 con longitud 4 bytes
    
    #Imprime información recopilada del sistema de archivos en formato listado
    print(f"\nEl sistema se llama: {nombreSistema}")
    print(f"La version es: {version}")
    print(f"Etiqueta del volumen: {etiqueta}")
    print(f"Tamaño del Cluster: {tamaio_cluster} bytes")
    print(f"Numero de clusters que mide el directorio: {cantidadclusters}")
    print(f"Numero de clusters que mide toda la unidad: {ccl}")

    #Espera a que el usuario presione enter para que sea mas intuitivo el proyecto
    input ("\nPresione 'enter' para continuar...")

# Función para mostrar el menú
def menu():
    while True:
        system("cls")                                          #Limpia la pantalla de la consola (solo en sistemas Windows)
        print("\nMenu:")
        print("1. Validar server")
        print("2. Listar archivos")
        print("3. Copiar archivo desde FiUnamFS")
        print("4. Eliminar archivo de FiUnamFS")
        print("5. Mover archivo a FiUnamFS")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")              #Solicita al usuario que seleccione una opción del menú
        
        if opcion == '1':
            validarSistemaArchivos()                           #Llama a la función para validar el sistema de archivos
        elif opcion == '2':
            #listar()                                                       #Lista los archivos existentes en FiUNAMFS
            a = input(print("Se listan los documentos contenidos"))
        elif opcion == '3':
            b = input(print("Ingresa el nombre a copiar desde FiUNAMFS"))   #Solicita al usuario el nombre del archivo a copiar desde FiUnamFS
        elif opcion == '4':
            c = input(print("Ingresa el nombre a eliminar de FiUNAMFS"))    #Solicita al usuario el nombre del archivo a eliminar de FiUnamFS
        elif opcion == '5':
            d = input(print("Ingresa el nombre a mover a FiUNAMFS"))        #Solicita al usuario el nombre del archivo a mover a FiUnamFS
        elif opcion == '6':
            break                                                           #Sale del bucle while para finalizar el programa
        else:
            print("\nOpción no válida")                         # Mensaje de error para opciones no válidas
            input("\nIngrese 'enter' para continuar...")        # Espera que el usuario presione Enter para continuar

# Ejecución del programa
if __name__ == "__main__":
    menu()                                                     # Llama a la función menu para comenzar la ejecución del programa