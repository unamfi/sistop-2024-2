import os
import struct
import threading
import datetime
from os import path

# Constantes
TAMANO_CLUSTER = 2048  # Tamaño del cluster en bytes
DIRECTORIO_INICIO = TAMANO_CLUSTER  # Inicio del directorio
TAMANO_ENTRADA = 64  # Tamaño de cada entrada del directorio
DIRECTORIO_TAMANO = TAMANO_CLUSTER * 4  # Tamaño total del directorio
ENTRADA_VACIA = b'###############'  # Marca de entrada vacía
lock = threading.Lock()

class EntradaArchivo:
    def __init__(self, datos):
        self.tipo = datos[0]
        self.nombre = datos[1:16].decode('ascii', 'ignore').rstrip('\x00')
        self.tamano = struct.unpack('<I', datos[16:20])[0]
        self.cluster = struct.unpack('<I', datos[20:24])[0]
        self.fecha_creacion = datos[24:38].decode('ascii', 'ignore')
        self.fecha_modificacion = datos[38:52].decode('ascii', 'ignore')

def leer_directorio(archivo):
    archivo.seek(DIRECTORIO_INICIO)  # El directorio comienza en el segundo cluster
    entradas = []
    for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
        datos = archivo.read(TAMANO_ENTRADA)
        if datos[1:16] != ENTRADA_VACIA:
            entradas.append(EntradaArchivo(datos))
    return entradas

def listar_directorio(fiunamfs_img):
    with lock:
        print("Estado del Lock: Adquirido (Listar Directorio)")
    with open(fiunamfs_img, 'rb') as archivo:
        for entrada in leer_directorio(archivo):
            print(f'Nombre: {entrada.nombre}, Tamaño: {entrada.tamano}, Fecha de creación: {entrada.fecha_creacion}, Fecha de modificación: {entrada.fecha_modificacion}')
    with lock:
        print("Estado del Lock: Liberado (Listar Directorio)")

def copiar_a_fiunamfs(fiunamfs_img, archivo_origen, nombre_destino):
    with lock:
        print("Estado del Lock: Adquirido (Copiar a FiUnamFS)")
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
            fecha_actual = datetime.datetime.now().strftime('%Y%m%d%H%M%S').encode('ascii')
            f.write(fecha_actual)  # Fecha de creación
            f.write(fecha_actual)  # Fecha de modificación

    with lock:
        print("Estado del Lock: Liberado (Copiar a FiUnamFS)")

# Función para copiar un archivo del FiUnamFS al sistema actual
def copiar_desde_fiunamfs(fiunamfs_img, nombre_archivo):
    with lock:
        print("Estado del Lock: Adquirido (Copiar desde FiUnamFS)")
    with open(fiunamfs_img, 'rb') as archivo:
        for entrada in leer_directorio(archivo):
            if entrada.nombre.strip() == nombre_archivo.strip():
                archivo.seek((entrada.cluster + 1) * TAMANO_CLUSTER)
                datos = archivo.read(entrada.tamano)
                with open(nombre_archivo.strip(), 'wb') as archivo_salida:
                    archivo_salida.write(datos)
                with lock:
                    print("Estado del Lock: Liberado (Copiar desde FiUnamFS)")
                return True
    with lock:
        print("Estado del Lock: Liberado (Copiar desde FiUnamFS)")
    return False


def verificar_superbloque(fiunamfs_img):
    with open(fiunamfs_img, 'rb') as f:
        nombre_fs = f.read(8).decode('ascii').strip()
        version = f.read(7).decode('ascii').strip().replace('-', '.')
        
        print(f"Nombre FS leído: {nombre_fs}, Versión leída: {version}")
        
        resultado = f"Nombre del sistema de archivos: {nombre_fs}, Versión: {version}\n"
        if nombre_fs != "FiUnamFS" and version != "24.2":
            resultado += f"¡ERROR! La versión o el sistema de archivos no coinciden con FiUnamFS versión 24.2. Se esperaba 'FiUnamFS' y '24.2' pero se encontró '{nombre_fs}' y '{version}'\n"
            return resultado
        else:
            resultado += "Superbloque válido\n"
    return resultado

def eliminar(nombre_archivo, fiunamfs_img):
    with lock:
        print("Estado del Lock: Adquirido (Eliminar de FiUnamFS)")
    with open(fiunamfs_img, 'r+b') as archivo:
        archivo.seek(1024)  # Saltar el superbloque
        for _ in range(64):
            entrada = archivo.read(64)
            nombre = entrada[1:16].rstrip(b'\x00').decode('ascii', errors='ignore').strip()
            if nombre == nombre_archivo:
                archivo.seek(-64, os.SEEK_CUR)
                # Escribir exactamente 64 bytes, llenando con ceros después de '/###############'
                archivo.write(b'/###############' + b'\x00' * (64 - 17))  # Asegura exactamente 64 bytes
                print("Archivo borrado exitosamente")
                return
    print("Archivo no encontrado en el directorio")