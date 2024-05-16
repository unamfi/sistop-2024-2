import os
import struct

TAMANO_CLUSTER = 1024
TAMANO_ENTRADA = 64
DIRECTORIO_INICIO = TAMANO_CLUSTER  
DIRECTORIO_TAMANO = 4 * TAMANO_CLUSTER  

def leer_superbloque(fiunamfs_img):
    with open(fiunamfs_img, 'rb') as f:
        f.seek(0)
        nombre_fs = f.read(8).decode('ascii').strip()
        f.seek(10)
        version = f.read(5).decode('ascii').rstrip('\x00').strip()
        print(f"Nombre FS leído: {nombre_fs}, Versión leída: {version}")
        if nombre_fs != "FiUnamFS" or version.replace('-', '.') != "24.2":
            print("Valores no coinciden, se esperaba FiUnamFS y 24.2")
        else:
            print("Superbloque válido") 

def listar_directorio(fiunamfs_img):
    with open(fiunamfs_img, 'rb') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            entrada = f.read(TAMANO_ENTRADA)
            tipo_archivo = entrada[0:1].decode('ascii')
            nombre = entrada[1:16].decode('ascii').rstrip()
            if nombre != '#' * 15:
                tam_archivo = struct.unpack('<I', entrada[16:20])[0]
                cluster_ini = struct.unpack('<I', entrada[20:24])[0]
                fecha_creacion = entrada[24:38].decode('ascii')
                fecha_modificacion = entrada[38:52].decode('ascii')
                print(f"Tipo: {tipo_archivo}, Nombre: {nombre}, Tamaño: {tam_archivo}, Cluster inicial: {cluster_ini}, Creación: {fecha_creacion}, Modificación: {fecha_modificacion}")

def menu_info():
    while True:
        print("\nMenú de Información - Sistema de Archivos FiUnamFS")
        print("1. Leer el superbloque")
        print("2. Listar directorio")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            leer_superbloque(fiunamfs_img)
        elif opcion == '2':
            listar_directorio(fiunamfs_img)
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

fiunamfs_img = r"C:\Users\migue\Downloads\PROYECTOSYS\fiunamfs.img"  

menu_info()
