#Importacion de modulos
import os               #Importa el módulo 'os' que proporciona funciones para interactuar con el sistema operativo
import struct           #Importa el módulo 'struct' que permite interpretar cadenas de bytes como estructuras binarias
import threading        #Importa el módulo 'threading' que proporciona funcionalidad de subprocesos para realizar múltiples tareas de forma simultánea
from os import system   #Importa solo la función 'system' del módulo 'os'

#Variables globales
sector = 512                            #La superficie del disco se divide en sectores de 512 bytes.
cluster = sector * 4                    #Cada cluster mide cuatro sectores.
direccionSistema = "fiunamfs.img"       #Dirección del archivo fiunamfs.img (puede ser en ruta absoluta o relativa)

#Función para verificar la existencia del archivo
def verificarExistenciaArchivo():
    if not os.path.exists(direccionSistema):        #Condicional para validar que exista el archivo
        print(f"Error: No se encontró el archivo del sistema de archivos, verifique se encuentre en la misma ruta o modifique la ruta de la ubicacion del archivo'{direccionSistema}'.")
        input("Presione 'enter' para salir del programa...")
        exit()

#Función para leer un entero desde el archivo en una posición específica
def leerEntero(posicion, numero):
    with open(direccionSistema, "rb") as archivo:   #Abre el archivo en modo binario de solo lectura
        archivo.seek(posicion)                      #Mueve el puntero del archivo a la posición especificada
        dato = archivo.read(numero)                 #Lee el número de bytes especificado desde la posición actual
        num = struct.unpack("<I", dato)[0]          #Desempaqueta los bytes leídos en un entero (asumiendo formato little-endian)
        return num                                  #Devuelve el entero leído

#Función para leer una cadena desde el archivo en una posición específica
def leerCadena(posicion, numero):
    with open(direccionSistema, "rb") as archivo:   #Abre el archivo en modo binario de solo lectura
        archivo.seek(posicion)                      #Mueve el puntero del archivo a la posición especificada
        cadena = archivo.read(numero)               #Lee el número de bytes especificado desde la posición actual
        string = cadena.decode("ascii").strip()     #Decodifica los bytes leídos en una cadena ASCII y elimina espacios en blanco alrededor
        return string                               #Devuelve la cadena leída

#Función que recopila la información del server ubicada en el primer cluster
def validarSistemaArchivos():
    os.system("cls")                                #Limpia la pantalla de la consola (solo en sistemas Windows)
    nombreSistema = leerCadena(0, 9)                #Lee la cadena de nombre de sistema desde la posición 0 con longitud 9 bytes
    version = leerCadena(10, 5)                     #Lee la cadena de versión desde la posición 10 con longitud 5 bytes
    etiqueta = leerCadena(20, 16)                   #Lee la cadena de etiqueta del volumen desde la posición 20 con longitud 16 bytes
    tamaio_cluster = leerEntero(40, 4)              #Lee un entero que representa el tamaño del cluster desde la posición 40 con longitud 4 bytes
    cantidadclusters = leerEntero(44, 4)            #Lee un entero que representa la cantidad de clusters que mide el directorio desde la posición 44 con longitud 4 bytes
    clustersUnidad = leerEntero(48, 4)                         #Lee un entero que representa la cantidad de clusters que mide toda la unidad desde la posición 48 con longitud 4 bytes
    
    #Imprime información recopilada del sistema de archivos en formato listado
    print(f"\nEl sistema se llama: {nombreSistema}")
    print(f"La version es: {version}")
    print(f"Etiqueta del volumen: {etiqueta}")
    print(f"Tamaño del Cluster: {tamaio_cluster} bytes")
    print(f"Numero de clusters que mide el directorio: {cantidadclusters}")
    print(f"Numero de clusters que mide toda la unidad: {clustersUnidad}")

    #Espera a que el usuario presione enter para que sea más intuitivo el proyecto
    input("\nPresione 'enter' para continuar...")

#Función que lista el contenido del directorio, ignorando las entradas vacías
def listado():
    os.system("cls")                                                #Limpia la pantalla de la consola (solo en sistemas Windows)
    print("Listado de archivos en el FiUNAMFS:")                    #Impresión de pantalla para una mejor visualización

    #Itera sobre las entradas del directorio en bloques de 64 bytes
    for i in range(0, cluster * 4, 64):
        tipo_archivo = leerCadena(cluster + i, 1)                   #Lee el tipo de archivo desde el cluster actual más el desplazamiento 'i' con longitud de 1 byte
        if tipo_archivo != "/":                                     #Verifica si el tipo de archivo es diferente de '/'
            nombre = leerCadena(cluster + i + 1, 15)                #Lee el nombre del archivo desde el cluster actual más el desplazamiento 'i' más 1 con longitud 15 bytes
            tamanio = leerEntero(cluster + i + 16, 4)               #Lee el tamaño del archivo desde el cluster actual más el desplazamiento 'i' más 16 con longitud 4 bytes
            cluster_inicial = leerEntero(cluster + i + 20, 4)       #Lee el número de cluster inicial del archivo desde el cluster actual más el desplazamiento 'i' más 20 con longitud 4 bytes
            fecha_creacion = leerCadena(cluster + i + 24, 14)       #Lee la fecha de creación del archivo desde el cluster actual más el desplazamiento 'i' más 24 con longitud 14 bytes
            fecha_modificacion = leerCadena(cluster + i + 38, 14)   #Lee la fecha de modificación del archivo desde el cluster actual más el desplazamiento 'i' más 38 con longitud 14 bytes
            
            #Muestra la información del archivo
            print(f"Archivo: {nombre}, Tamaño: {tamanio}, Cluster Inicial: {cluster_inicial}, Creado: {fecha_creacion}, Modificado: {fecha_modificacion}")

#Función para leer el contenido de un archivo desde fiunamfs.img
def leerContenidoArchivo(cluster_inicial, tamanio):
    with open(direccionSistema, "rb") as archivo:                   #Abre el archivo en modo binario de solo lectura
        archivo.seek(cluster_inicial * cluster)                     #Mueve el puntero del archivo al inicio del cluster inicial
        contenido = archivo.read(tamanio)                           #Lee el contenido del tamaño especificado
        return contenido

#Función para copiar un archivo desde fiunamfs.img al directorio local
def copiarArchivo(nombre_archivo):
    encontrado = False                                              #Variable auxiliar para validar que se encontro el archivo a copiar
    nombre_ascii = [ord(char) for char in nombre_archivo]           #Convertir el nombre del archivo proporcionado por el usuario a su representación ASCII

    #Itera sobre las entradas del directorio en bloques de 64 bytes
    for i in range(0, cluster * 4, 64):
        tipo_archivo = leerCadena(cluster + i, 1)                   #Lee el tipo de archivo desde el cluster actual más el desplazamiento 'i' con longitud de 1 byte
        if tipo_archivo != "/":                                     #Verifica si el tipo de archivo es diferente de '/'
            nombre = leerCadena(cluster + i + 1, 15)                #Lee el nombre del archivo desde el cluster actual más el desplazamiento 'i' más 1 con longitud 15 bytes
            nombre = nombre.strip()                                 #Elimina los espacios en blanco al final del nombre
            nombre_ascii_fs = [ord(char) for char in nombre]        #Convierte el nombre del archivo del sistema de archivos a su representación ASCII

            #Comparar los nombres ASCII
            if nombre_ascii_fs[:len(nombre_ascii)] == nombre_ascii:         #Compara los primeros len(nombre_ascii) caracteres
                encontrado = True                                           #Variable auxiliar para validar que se encontro el archivo a copiar
                tamanio = leerEntero(cluster + i + 16, 4)                   #Lee el tamaño del archivo desde el cluster actual más el desplazamiento 'i' más 16 con longitud 4 bytes
                cluster_inicial = leerEntero(cluster + i + 20, 4)           #Lee el número de cluster inicial del archivo desde el cluster actual más el desplazamiento 'i' más 20 con longitud 4 bytes
                contenido = leerContenidoArchivo(cluster_inicial, tamanio)  #Lee el contenido del archivo
                with open(nombre_archivo, "wb") as archivo_local:           #Abre el archivo local en modo binario de escritura
                    archivo_local.write(contenido)                          #Escribe el contenido en un archivo local
                
                print(f"Archivo '{nombre_archivo}' copiado exitosamente al directorio local.")
                # Espera que el usuario presione Enter para continuar
                input("\nIngrese 'enter' para continuar...")
                break
    
    #En caso de que no se haya encontrado el archivo a copiar, se hace una impresion en pantalla
    if not encontrado:
        print(f"No se encontró el archivo '{nombre_archivo}' en fiunamfs.img.")
        #Espera que el usuario presione Enter para continuar
        input("\nIngrese 'enter' para continuar...")

# Función para eliminar un archivo de FiUnamFS
def eliminarArchivo(nombre_archivo):
    encontrado = False                                                  #Variable auxiliar para validar que se encontro el archivo a copiar
    nombre_ascii = [ord(char) for char in nombre_archivo]               #Convertir el nombre del archivo proporcionado por el usuario a su representación ASCII

    # Itera sobre las entradas del directorio en bloques de 64 bytes
    for i in range(0, cluster * 4, 64):
        tipo_archivo = leerCadena(cluster + i, 1)                       #Lee el tipo de archivo desde el cluster actual más el desplazamiento 'i' con longitud de 1 byte
        if tipo_archivo != "/":                                         #Verifica si el tipo de archivo es diferente de '/'
            nombre = leerCadena(cluster + i + 1, 15)                    #Lee el nombre del archivo desde el cluster actual más el desplazamiento 'i' más 1 con longitud 15 bytes
            nombre = nombre.strip()                                     #Elimina los espacios en blanco al final del nombre
            nombre_ascii_fs = [ord(char) for char in nombre]            #Convierte el nombre del archivo del sistema de archivos a su representación ASCII

            #Compara los nombres ASCII
            if nombre_ascii_fs[:len(nombre_ascii)] == nombre_ascii:     #Compara los primeros len(nombre_ascii) caracteres
                encontrado = True                                       #Variable auxiliar para validar que se encontro el archivo a copiar
                
                # Marcar la entrada del archivo como eliminada (cambia el primer byte a '/')
                with open(direccionSistema, "r+b") as archivo:
                    archivo.seek(cluster + i)                           #Mueve el puntero del archivo a la posición de la entrada del directorio
                    archivo.write(b'/')                                 #Escribe '/' para marcar la entrada como eliminada

                #Se imprime en pantalla que se elimino de forma correcta el archivo de fiunamfs.img
                print(f"Archivo '{nombre_archivo}' eliminado exitosamente de FiUnamFS.")
                #Espera que el usuario presione Enter para continuar
                input("\nIngrese 'enter' para continuar...")
                break
    
    #En caso de que no se haya encontrado el archivo a eliminar, se hace una impresion en pantalla
    if not encontrado:
        print(f"No se encontró el archivo '{nombre_archivo}' en FiUnamFS.")
        #Espera que el usuario presione Enter para continuar
        input("\nIngrese 'enter' para continuar...")

#Función para mover un archivo desde el directorio local a FiUnamFS
def moverArchivo(nombre_archivo):
    #Verificar si el archivo existe en el directorio local
    if not os.path.exists(nombre_archivo):
        print(f"Error: No se encontró el archivo '{nombre_archivo}' en el directorio local.")
        #Espera que el usuario presione Enter para continuar
        input("\nIngrese 'enter' para continuar...")
        return

    tamanio_archivo = os.path.getsize(nombre_archivo)           #Obtenemos los metadatos del archivo nuevo      

    #Verificar si el archivo cabe en el sistema de archivos
    if tamanio_archivo > (cluster * 4) - 64:
        print("Error: El archivo es demasiado grande para ser almacenado en FiUnamFS.")
        #Espera que el usuario presione Enter para continuar
        input("\nIngrese 'enter' para continuar...")
        return

    #Buscar espacio suficiente en área de datos
    espacio_suficiente = False
    for i in range(0, cluster * 4, 64):
        tipo_archivo = leerCadena(cluster + i, 1)             #Lee el tipo de archivo desde el cluster actual más el desplazamiento 'i' con longitud de 1 byte
        if tipo_archivo == "/":                               #Verifica si el tipo de archivo es diferente de '/'
            espacio_suficiente = True
            break

    if not espacio_suficiente:
        print("Error: No hay espacio suficiente en FiUnamFS para almacenar el archivo.")
        #Espera que el usuario presione Enter para continuar
        input("\nIngrese 'enter' para continuar...")
        return

    #Copiar datos decodificados del archivo nuevo a sección asignada
    with open(nombre_archivo, "rb") as archivo_local:         #Abre el archivo en modo binario de solo lectura
        contenido_archivo = archivo_local.read()              #Lee todo el contenido del archivo y lo guarda en contenido_archivo

    # Buscar cluster libre en área de directorio
    cluster_libre = None
    for i in range(0, cluster * 4, 64):
        tipo_archivo = leerCadena(cluster + i, 1)             #Lee el tipo de archivo desde el cluster actual más el desplazamiento 'i' con longitud de 1 byte
        if tipo_archivo == "/":                               #Verifica si el tipo de archivo es diferente de '/'
            cluster_libre = i                                 #Si se encuentra un cluster libre, se guarda su índice
            break

    if cluster_libre is None:
        print("Error: No se encontró un cluster libre en el área de directorio de FiUnamFS.")
        # Espera que el usuario presione Enter para continuar
        input("\nIngrese 'enter' para continuar...")
        return

    #Copiar metadatos decodificados de archivo nuevo en cluster libre
    nombre_archivo_encoded = nombre_archivo.encode("ascii")                     #Codifica el nombre del archivo en formato ASCII
    nombre_archivo_encoded += b" " * (15 - len(nombre_archivo_encoded))         #Asegura que el nombre tenga exactamente 15 bytes
    tamanio_archivo_bytes = struct.pack("<I", tamanio_archivo)                  #Empaqueta el tamaño del archivo en un formato de 4 bytes
    cluster_inicio_bytes = struct.pack("<I", cluster_libre)                     #Empaqueta el número de cluster inicial del archivo en un formato de 4 bytes
    fecha_creacion_bytes = "fecha_creacion".encode("ascii")                     #Aquí deberías obtener la fecha de creación actual, codificada en ASCII
    fecha_creacion_bytes += b" " * (14 - len(fecha_creacion_bytes))             #Asegura que la fecha de creación tenga exactamente 14 bytes
    fecha_modificacion_bytes = "fecha_modificacion".encode("ascii")             #Aquí deberías obtener la fecha de modificación actual, codificada en ASCII
    fecha_modificacion_bytes += b" " * (14 - len(fecha_modificacion_bytes))     #Asegura que la fecha de modificación tenga exactamente 14 bytes

    with open(direccionSistema, "r+b") as archivo_fs:                           #Abre el archivo del sistema de archivos en modo lectura y escritura binaria
        archivo_fs.seek(cluster + cluster_libre)                                #Se posiciona en el inicio del cluster libre en el área de directorio
        archivo_fs.write(b'D')                                                  #Marca el cluster como ocupado ('D')
        archivo_fs.write(nombre_archivo_encoded)                                #Escribe el nombre del archivo en el área de directorio
        archivo_fs.write(tamanio_archivo_bytes)                                 #Escribe el tamaño del archivo en el área de directorio
        archivo_fs.write(cluster_inicio_bytes)                                  #Escribe el número de cluster inicial del archivo en el área de directorio
        archivo_fs.write(fecha_creacion_bytes)                                  #Escribe la fecha de creación del archivo en el área de directorio
        archivo_fs.write(fecha_modificacion_bytes)                              #Escribe la fecha de modificación del archivo en el área de directorio

        #Guardar contenido del archivo en la sección asignada
        archivo_fs.seek(cluster_libre * cluster)                                #Se posiciona en el inicio del cluster asignado para el contenido del archivo
        archivo_fs.write(contenido_archivo)                                     #Escribe el contenido del archivo en el sistema de archivos

    print(f"Archivo '{nombre_archivo}' movido exitosamente a FiUnamFS.")
    # Espera que el usuario presione Enter para continuar
    input("\nIngrese 'enter' para continuar...")

#Función para mostrar el menú
def menu():
    while True:
        system("cls")                                           #Limpia la pantalla de la consola (solo en sistemas Windows)
        print("\nMenu:")                                        #Menu
        print("1. Validar server")                              #Opcion 1 del menú
        print("2. Listar archivos")                             #Opcion 2 del menú
        print("3. Copiar archivo desde FiUnamFS")               #Opcion 3 del menú
        print("4. Eliminar archivo de FiUnamFS")                #Opcion 4 del menú
        print("5. Mover archivo a FiUnamFS")                    #Opcion 5 del menú
        print("6. Salir")                                       #Opcion 6 del menú
        opcion = input("Seleccione una opción: ")               #Solicita al usuario que seleccione una opción del menú
        
        if opcion == '1':                                       #Opcion 1 del menú
            validarSistemaArchivos()                            #Llama a la función para validar el sistema de archivos

        elif opcion == '2':                                     #Opcion 2 del menú
            listado()                                           #Llama a la función para listar los archivos
            input("\nIngrese 'enter' para continuar...")        #Espera que el usuario presione Enter para continuar
        
        elif opcion == '3':                                     #Opcion 3 del menú
            listado()                                           #Se imprimen los archivos del directorio fiunamfs.img
            nombre_archivo = input("\nIngrese el nombre del archivo a copiar a su directorio local: ")  #Solicitar al usuario que ingrese el nombre del archivo a copiar desde fiunamfs.img
            copiarArchivo(nombre_archivo)                       #Funcion para mover un archivo de fiunamfs al directorio actual
        
        elif opcion == '4':                                     #Opcion 4 del menú
            listado()                                           #Se imprimen los archivos del directorio fiunamfs.img
            nombre_archivo = input("\nIngrese el nombre del archivo a eliminar de FiUnamFS: ")  #Solicita al usuario que ingrese el nombre del archivo a eliminar de FiUnamFS
            eliminarArchivo(nombre_archivo)                     #Llamar a la función eliminarArchivo con el nombre del archivo proporcionado por el usuario

        elif opcion == '5':                                     #Opcion 5 del menú
            nombre_archivo = input("Ingrese el nombre del archivo a mover a FiUnamFS: ")    #Solicita al usuario el nombre del archivo a mover a FiUnamFS
            moverArchivo(nombre_archivo)                        #Llamar a la función moverArchivo con el nombre del archivo proporcionado por el usuario
        
        elif opcion == '6':                                     #Opcion 6 del menú
            break                                               #Sale del bucle while para finalizar el programa
        
        else:                                                   #Caso en el que no se elige alguna opcion deseada
            print("\nOpción no válida")                         #Mensaje de error para opciones no válidas
            input("\nIngrese 'enter' para continuar...")        #Espera que el usuario presione Enter para continuar

# Ejecución del programa
if __name__ == "__main__":
    verificarExistenciaArchivo()
    menu()  # Llama a la función menu para comenzar la ejecución del programa

