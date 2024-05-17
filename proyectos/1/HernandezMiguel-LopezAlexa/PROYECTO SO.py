import os
import struct
import threading

TAMANO_CLUSTER = 1024
TAMANO_ENTRADA = 64
DIRECTORIO_INICIO = TAMANO_CLUSTER  # Cluster 1
DIRECTORIO_TAMANO = 4 * TAMANO_CLUSTER  # 4 clusters para el directorio
MAXIMO_CLUSTERS = 1440 // 4  # Asumiendo que el tamaño total es 1440KB

lock = threading.Lock()

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

def copiar_a_sistema(fiunamfs_img, nombre_archivo, destino):
    with lock:
        print("Adquiriendo candado (Lock) para copiar a sistema...")
    with open(fiunamfs_img, 'rb') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            entrada = f.read(TAMANO_ENTRADA)
            tipo_archivo = entrada[0:1]
            if tipo_archivo == b'-':
                nombre, tam, cluster_ini = (
                    entrada[1:16].decode('ascii').rstrip(),
                    struct.unpack('<I', entrada[16:20])[0],
                    struct.unpack('<I', entrada[20:24])[0]
                )
                if nombre.rstrip('\x00').strip() == nombre_archivo.rstrip('\x00').strip():
                    f.seek(cluster_ini * TAMANO_CLUSTER)
                    datos = f.read(tam)
                    with open(destino, 'wb') as archivo_destino:
                        archivo_destino.write(datos)
                    return

def copiar_a_fiunamfs(fiunamfs_img, archivo_origen, nombre_destino):
    with lock:
        print("Adquiriendo candado (Lock) para copiar a FiUnamFS...")
    with open(fiunamfs_img, 'r+b') as f:
        tam_origen = os.path.getsize(archivo_origen)
        cluster_libre = 5
        posicion_entrada_libre = None

        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            posicion_actual = f.tell()
            entrada = f.read(TAMANO_ENTRADA)
            tipo_archivo = entrada[0:1]
            cluster_ini = struct.unpack('<I', entrada[20:24])[0]

            if tipo_archivo == b'/' and posicion_entrada_libre is None:
                posicion_entrada_libre = posicion_actual

            if cluster_ini >= cluster_libre:
                cluster_libre = cluster_ini + 1

        if posicion_entrada_libre is None:
            raise Exception("No hay espacio en el directorio")
        else:
            with open(archivo_origen, 'rb') as archivo_origen_f:
                f.seek(cluster_libre * TAMANO_CLUSTER)
                f.write(archivo_origen_f.read())

            f.seek(posicion_entrada_libre)
            f.write(b'-' + nombre_destino.ljust(15).encode('ascii'))
            f.write(struct.pack('<I', tam_origen))
            f.write(struct.pack('<I', cluster_libre))

def menu_principal():
    while True:
        print("\nMenú Principal - Sistema de Archivos FiUnamFS")
        print("1. Leer el superbloque")
        print("2. Listar directorio")
        print("3. Copiar archivo de FiUnamFS a sistema")
        print("4. Copiar archivo de sistema a FiUnamFS")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            leer_superbloque(fiunamfs_img)
        elif opcion == '2':
            listar_directorio(fiunamfs_img)
        elif opcion == '3':
            nombre_archivo = input("Ingresa el nombre del archivo en FiUnamFS: ")
            destino = input("Ingresa la ruta de destino en el sistema (deja en blanco para la carpeta actual): ")
            if not destino:
                destino = os.path.join(os.getcwd(), nombre_archivo)  
            try:
                copiar_a_sistema(fiunamfs_img, nombre_archivo, destino)
                print("Archivo copiado con éxito a", destino)
            except Exception as e:
                print("Error al copiar el archivo:", e)
        elif opcion == '4':
            origen = input("Ingresa la ruta del archivo en el sistema: ")
            nombre_destino = input("Ingresa el nombre del archivo en FiUnamFS: ")
            copiar_a_fiunamfs(fiunamfs_img, origen, nombre_destino)
        elif opcion == '5':
            nombre_archivo = input("Ingresa el nombre del archivo a eliminar de FiUnamFS: ")
            eliminar_archivo(fiunamfs_img, nombre_archivo)
        elif opcion == '6':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

# Configuración inicial
fiunamfs_img = r"C:\Users\migue\Downloads\PROYECTOSYS\fiunamfs.img"  # Cambia la ruta por la ubicación de tu archivo .img

# Ejecutar el menú principal
menu_principal()