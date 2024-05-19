import os
import struct
import time
import threading
import tkinter as tk
from tkinter import filedialog

# Constantes
TAMANIO_SECTOR = 512
TAMANIO_CLUSTER = TAMANIO_SECTOR * 4
TAMANIO_ENTRADA_DIRECTORIO = 64
NUMERO_ENTRADAS_DIRECTORIO = 16  # 4 clusters * 16 entradas por cluster
DIRECTORIO_INICIO = 1 * TAMANIO_CLUSTER
DIRECTORIO_FIN = 4 * TAMANIO_CLUSTER

# Semáforo para controlar el acceso concurrente al recurso compartido
semaforo = threading.Semaphore(value=1)

# Función para leer enteros desde el archivo fuente
def leer_entero(posicion, longitud):
    with open("fiunamfs.img", "rb") as archivo:
        archivo.seek(posicion)
        bytes_entero = archivo.read(longitud)
        entero = int.from_bytes(bytes_entero, byteorder='little')
        return entero

# Función para leer cadenas desde el archivo fuente
def leer_cadena(posicion, longitud):
    with open("fiunamfs.img", "rb") as archivo:
        archivo.seek(posicion)
        bytes_cadena = archivo.read(longitud)
        cadena = bytes_cadena.decode("ascii")
        return cadena

# Función para leer una cadena de longitud fija desde el archivo
def leer_cadena2(archivo, posicion, longitud):
    archivo.seek(posicion)
    cadena = archivo.read(longitud)
    return cadena.decode('ascii').rstrip('\x00')
"""----------------------------------------------------------------------------"""
# Función para validar y mostrar información del servidor
def iniciar():
    nombre_sistema = leer_cadena(0, 9)
    version = leer_cadena(10, 5)
    etiqueta_volumen = leer_cadena(20, 20)
    tamanio_cluster = leer_entero(40, 4)
    num_clusters_directorio = leer_entero(45, 4)
    num_total_clusters = leer_entero(50, 4)

    if version != '24-2':
        print("La versión no es la adecuada, el sistema sólo admite 24-2")
        return False
    if nombre_sistema != 'FiUnamFS':
        print("El nombre del sistema no es el adecuado, el sistema sólo admite FiUnamFS")
        return False
    # Imprimir las características del sistema
    print("=== Información del Sistema de Archivos ===")
    print(f"Nombre del sistema: {nombre_sistema}")
    print(f"Versión: {version}")
    print(f"Etiqueta del volumen: {etiqueta_volumen}")
    print(f"Tamaño del cluster: {tamanio_cluster} bytes")
    print(f"Número de clusters en el directorio: {num_clusters_directorio}")
    print(f"Número total de clusters: {num_total_clusters}")

# Función para copiar un archivo desde FiUnamFS a tu sistema
def copiar_archivo_desde_fiunamfs(nombre_archivo):
    with open("fiunamfs.img", "rb") as archivo:
        # Buscar el archivo en el directorio
        for cluster in range(1, 5):
            inicio_cluster = (cluster - 1) * TAMANIO_CLUSTER
            for i in range(NUMERO_ENTRADAS_DIRECTORIO):
                entrada_posicion = inicio_cluster + i * TAMANIO_ENTRADA_DIRECTORIO
                tipo_archivo = leer_cadena2(archivo, entrada_posicion, 1)
                if tipo_archivo == '-' or tipo_archivo == '/':  # Archivo regular o vacío
                    nombre_archivo_actual = leer_cadena2(archivo, entrada_posicion + 1, 15)
                    if nombre_archivo_actual.strip() == nombre_archivo:
                        tamano_archivo = struct.unpack("<I", archivo.read(4))[0]
                        cluster_inicial = struct.unpack("<I", archivo.read(4))[0]
                        archivo.seek(TAMANIO_CLUSTER * cluster_inicial)
                        contenido_archivo = archivo.read(tamano_archivo)
                        return contenido_archivo
    return None

# Función para manejar la copia del archivo en un hilo separado
def copiar_archivo_thread(nombre_archivo):
    semaforo.acquire()
    try:
        contenido_archivo = copiar_archivo_desde_fiunamfs(nombre_archivo)
        if contenido_archivo:
            # Abrir un diálogo para que el usuario elija el directorio de destino
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal
            directorio_destino = filedialog.askdirectory(title="Seleccionar directorio de destino")
            if directorio_destino:
                # Guardar el archivo en el directorio seleccionado
                ruta_archivo_destino = os.path.join(directorio_destino, nombre_archivo)
                with open(ruta_archivo_destino, "wb") as archivo_destino:
                    archivo_destino.write(contenido_archivo)
                print(f"Archivo '{nombre_archivo}' copiado exitosamente a '{ruta_archivo_destino}'.")
            else:
                print("No se seleccionó ningún directorio.")
        else:
            print(f"Archivo '{nombre_archivo}' no encontrado en FiUnamFS.")
    finally:
        semaforo.release()

"""----------------------------------------------------------------------------"""

# Función para encontrar espacio libre en el disco
def encontrar_espacio_libre(disco, tamano_archivo):
    disco.seek(DIRECTORIO_FIN)  # Inicio del espacio de datos
    espacio_libre = b'\x00' * tamano_archivo  # Espacio libre requerido
    datos = disco.read()  # Leer todos los datos
    indice = datos.find(espacio_libre)  # Buscar la primera aparición del espacio libre
    if indice != -1:
        return DIRECTORIO_FIN + indice
    else:
        raise ValueError("No se encontró espacio suficiente para el archivo.")

# Función para mover un archivo desde la computadora al sistema FiUNAMFS
def moverCompuFI(ruta_archivo, nombre_archivo):
    tamano_archivo = os.path.getsize(ruta_archivo)
    nombre2, extension_archivo = os.path.splitext(nombre_archivo)
    if (len(nombre2) + len(extension_archivo)) > 15:
        raise ValueError("El nombre del archivo es demasiado grande.")

    nombre_archivo = (nombre2 + extension_archivo).ljust(15, ' ')

    with open("fiunamfs.img", "r+b") as disco:
        # Encontrar espacio libre en el disco
        posicion_espacio_libre = encontrar_espacio_libre(disco, tamano_archivo)

        # Escribir el archivo en el espacio libre encontrado
        with open(ruta_archivo, "rb") as archivo:
            contenido_archivo = archivo.read()
            disco.seek(posicion_espacio_libre)
            disco.write(contenido_archivo)

        # Actualizar el directorio
        for cluster in range(1, 5):
            inicio_cluster = (cluster - 1) * TAMANIO_CLUSTER
            for i in range(NUMERO_ENTRADAS_DIRECTORIO):
                entrada_posicion = inicio_cluster + i * TAMANIO_ENTRADA_DIRECTORIO
                disco.seek(entrada_posicion)
                tipo_archivo = disco.read(1).decode('ascii')
                if tipo_archivo == '/':
                    disco.seek(entrada_posicion)
                    disco.write(b'-')
                    disco.write(nombre_archivo.encode('ascii'))
                    disco.write(struct.pack("<I", tamano_archivo))
                    disco.write(struct.pack("<I", (posicion_espacio_libre // TAMANIO_CLUSTER)))

                    fecha_hora_actual = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    disco.write(fecha_hora_actual.encode('ascii'))
                    disco.write(fecha_hora_actual.encode('ascii'))
                    disco.write(b'\x00' * (TAMANIO_ENTRADA_DIRECTORIO - 52))
                    return

    raise ValueError("No se encontró una entrada de directorio libre.")

# Función para manejar el archivo con threading y semáforo
def copiar_archivo_con_semaforo():
    semaforo = threading.Semaphore(value=1)

    def tarea():
        semaforo.acquire()
        try:
            # Usar tkinter para seleccionar el archivo
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal de tkinter
            ruta_archivo = filedialog.askopenfilename(title="Selecciona un archivo")
            if not ruta_archivo:
                print("No se seleccionó ningún archivo.")
                return
            nombre_archivo = os.path.basename(ruta_archivo)
            moverCompuFI(ruta_archivo, nombre_archivo)
        finally:
            semaforo.release()

    hilo = threading.Thread(target=tarea)
    hilo.start()
    hilo.join()


# Función para listar los contenidos del directorio
def listar_contenidos_directorio():
    with open("fiunamfs.img", "rb") as archivo:
        # Leer el directorio ubicado en los clusters 1 a 4
        for cluster in range(1, 5):
            inicio_cluster = (cluster - 1) * TAMANIO_CLUSTER
            for i in range(NUMERO_ENTRADAS_DIRECTORIO):
                entrada_posicion = inicio_cluster + i * TAMANIO_ENTRADA_DIRECTORIO
                tipo_archivo = leer_cadena2(archivo, entrada_posicion, 1)
                if tipo_archivo == '-':  # Archivo regular
                    nombre_archivo = leer_cadena2(archivo, entrada_posicion + 1, 15)
                    tamano_archivo = struct.unpack("<I", archivo.read(4))[0]
                    cluster_inicial = struct.unpack("<I", archivo.read(4))[0]
                    hora_creacion = leer_cadena2(archivo, entrada_posicion + 24, 14)
                    hora_modificacion = leer_cadena2(archivo, entrada_posicion + 38, 14)
                    print(f"Nombre: {nombre_archivo}, Tamaño: {tamano_archivo} bytes, Cluster inicial: {cluster_inicial}, Creado: {hora_creacion}, Modificado: {hora_modificacion}")

# Función para borrar un archivo del sistema FiUNAMFS
def borrar_archivo(nombre_archivo):
    nombre_archivo = nombre_archivo.ljust(15, ' ')
    with open("fiunamfs.img", "r+b") as disco:
        # Buscar el archivo en el directorio
        for cluster in range(1, 5):
            inicio_cluster = (cluster - 1) * TAMANIO_CLUSTER
            for i in range(NUMERO_ENTRADAS_DIRECTORIO):
                entrada_posicion = inicio_cluster + i * TAMANIO_ENTRADA_DIRECTORIO
                disco.seek(entrada_posicion)
                tipo_archivo = disco.read(1).decode('ascii')
                if tipo_archivo == '-':
                    archivo_nombre = leer_cadena(disco, entrada_posicion + 1, 15)
                    if archivo_nombre == nombre_archivo:
                        # Marcar la entrada del archivo como vacía
                        disco.seek(entrada_posicion)
                        disco.write(b'/')  # Marcar como vacío
                        disco.write(b' ' * 63)  # Rellenar el resto de la entrada con '#'
                        return
    print("Archivo no encontrado en el sistema FiUNAMFS.")

def main():
    print("Bienvenido al Sistema de Archivos FiUnamFS\n")
    iniciar()
        
    while True:
        # Muestra el menú de opciones al usuario
        print("\nOpciones:")
        print("1. Listar contenidos de FIUNAMFS")
        print("2. Copiar archivo desde FIUNAMFS a tu equipo")
        print("3. Copiar archivo desde tu equipo a FIUNAMFS")
        print("4. Eliminar un archivo")
        print("5. Salir")
        # Solicita al usuario que seleccione una opción
        choice = input("Seleccione una opción (1-5): ")

        if choice == '1':
            # Lista los contenidos de FIUNAMFS
            # Llamar a la función para listar los contenidos del directorio
            listar_contenidos_directorio()

        elif choice == '2':
            nombre_archivo_a_copiar = input("Ingrese el nombre del archivo a copiar: ")
            # Llamar a la función para copiar el archivo en un hilo separado
            t = threading.Thread(target=copiar_archivo_thread, args=(nombre_archivo_a_copiar,))
            t.start()

        elif choice == '3':
            # Copia un archivo desde tu equipo a FIUNAMFS
            copiar_archivo_con_semaforo()
            print("Se copió correctamente")

        elif choice == '4':
            # Elimina un archivo
            nombre_archivo_a_borrar = input("Ingrese el nombre del archivo a borrar del sistema FiUNAMFS: ")
            borrar_archivo(nombre_archivo_a_borrar)
        
        elif choice == '5':
            # Sale del programa
            print("Saliendo del programa.")
            break

        else:
            # Maneja una opción no válida
            print("Opción no válida. Por favor, seleccione una opción del 1 al 5.")

if __name__ == "__main__":
    main()