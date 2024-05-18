import threading
import struct
import os


# Definiendo constantes a emplear
SUPERBLOQUE_SIZE = 64
ENTRADA_DIRECTORIO_SIZE = 64
NUM_SECTORES_ENTRADA_DIRECTORIO = 1
CLUSTER_SIZE = 512
NUM_SECTORES_POR_CLUSTER = 4
DIRECTORIO_CLUSTER_INICIAL = 1
NUMERO_SECTORES_SUPERBLOQUE = 1
NUMERO_SECTORES_ENTRADA_DIRECTORIO = 4
NUMERO_ENTRADAS_DIRECTORIO = 16
FIUNAMFS_SIGNATURE = b"FiUnamFS"
VERSION_IMPLEMENTACION = "24-2"
NOMBRE_FIUNAMFS_IMG = "fiunamfs.img"
# NOMBRE_FIUNAMFS_IMG = "FiiUnamFS.img"
NOMBRE_ARCHIVO_DIRECTORIO = "directorio"

# Definir estructuras de datos
class EntradaDirectorio:
    def __init__(self, tipo_archivo, nombre_archivo, tamano_archivo, cluster_inicial, fecha_creacion, fecha_modificacion):
        self.tipo_archivo = tipo_archivo
        self.nombre_archivo = nombre_archivo
        self.tamano_archivo = tamano_archivo
        self.cluster_inicial = cluster_inicial
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

    def to_bytes(self):
        # Convertir la entrada del directorio a bytes
        tipo_archivo_bytes = self.tipo_archivo.encode("ascii")
        nombre_archivo_bytes = self.nombre_archivo.encode("ascii").ljust(15, b"\0")
        tamano_archivo_bytes = struct.pack("<I", self.tamano_archivo)
        cluster_inicial_bytes = struct.pack("<I", self.cluster_inicial)
        fecha_creacion_bytes = self.fecha_creacion.encode("ascii")
        fecha_modificacion_bytes = self.fecha_modificacion.encode("ascii")
        return tipo_archivo_bytes + nombre_archivo_bytes + tamano_archivo_bytes + cluster_inicial_bytes + fecha_creacion_bytes + fecha_modificacion_bytes

    @classmethod
    def from_bytes(cls, data):
        if len(data) < 52:
            print(f"Longitud de los datos: {len(data)}")
            raise ValueError("Los datos de entrada no tienen la longitud esperada.")
        tipo_archivo = data[0:1].decode("ascii")
        nombre_archivo = data[1:16].rstrip(b"\0").decode("ascii")
        tamano_archivo = struct.unpack("<I", data[16:20])[0]
        cluster_inicial = struct.unpack("<I", data[20:24])[0]
        fecha_creacion = data[24:38].decode("ascii")
        fecha_modificacion = data[38:52].decode("ascii", errors="ignore")
        return cls(tipo_archivo, nombre_archivo, tamano_archivo, cluster_inicial, fecha_creacion, fecha_modificacion)


# Definir funciones auxiliares
def leer_superbloque():
    with open(NOMBRE_FIUNAMFS_IMG, "rb") as img_file:
        superbloque_data = img_file.read(SUPERBLOQUE_SIZE)
        if superbloque_data[:8] != FIUNAMFS_SIGNATURE:
            raise Exception("No es un sistema de archivos FiUnamFS válido.")
        if superbloque_data[10:14].decode("ascii") != VERSION_IMPLEMENTACION:
            raise Exception("Versión de implementación incorrecta.")
        etiqueta_volumen = superbloque_data[20:36].decode("ascii").strip()
        tamano_cluster = struct.pack("<I", superbloque_data[40:44])[0]
        num_clusters_directorio = struct.pack("<I", superbloque_data[45:49])[0]
        num_clusters_total = struct.pack("<I", superbloque_data[50:54])[0]
        return etiqueta_volumen, tamano_cluster, num_clusters_directorio, num_clusters_total


class HiloOperacion(threading.Thread):
    def __init__(self, operacion, img_file, *args):
        threading.Thread.__init__(self)
        self.operacion = operacion
        self.img_file = img_file
        self.args = args

    def run(self):
        if self.operacion == "listar":
            listar_contenido_directorio(self.img_file)
        elif self.operacion == "copiar_desde":
            if len(self.args) == 1:
                copiar_desde_fiunamfs(self.img_file, *self.args)
            else:
                print("Número incorrecto de argumentos para la operación 'copiar_desde'.")
        elif self.operacion == "copiar_hacia":
            if len(self.args) == 2:
                copiar_hacia_fiunamfs(self.img_file, *self.args)
            else:
                print("Número incorrecto de argumentos para la operación 'copiar_hacia'.")

        elif self.operacion == "eliminar":
            nombre_archivo_fiunamfs = self.args[0]
            eliminar_archivo_fiunamfs(self.img_file, nombre_archivo_fiunamfs)
            print(f"El archivo {nombre_archivo_fiunamfs} ha sido eliminado.")


def listar_contenido_directorio(img_file):
    contenido = ""
    img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
    directorio_data = img_file.read(CLUSTER_SIZE * NUM_SECTORES_ENTRADA_DIRECTORIO * NUMERO_ENTRADAS_DIRECTORIO)
    for i in range(NUMERO_ENTRADAS_DIRECTORIO):
        entrada_data = directorio_data[i * ENTRADA_DIRECTORIO_SIZE: (i + 1) * ENTRADA_DIRECTORIO_SIZE]
        # Verificar si la entrada está vacía o eliminada
        if entrada_data[0:1] == b'\0' or entrada_data[0:1] == b'/':
            continue
        if len(entrada_data) < 52:
            continue  # Saltar esta entrada si la longitud no es la esperada
        entrada = EntradaDirectorio.from_bytes(entrada_data)
        contenido += f"Nombre: {entrada.nombre_archivo}, Tamaño: {entrada.tamano_archivo},\nCluster inicial: {entrada.cluster_inicial}, Fecha de Creación: {entrada.fecha_creacion}, Fecha de Modificación: {entrada.fecha_modificacion}\n\n"
    return contenido


def copiar_hacia_fiunamfs(img_file, nombre_archivo_local, nombre_archivo_fiunamfs):
    with open(nombre_archivo_local, "rb") as local_file:
        contenido = local_file.read()
        img_file.seek(0, os.SEEK_END)
        img_file.write(contenido)

    img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
    directorio_data = img_file.read(CLUSTER_SIZE * NUM_SECTORES_ENTRADA_DIRECTORIO)
    espacio_encontrado = False
    for i in range(NUMERO_ENTRADAS_DIRECTORIO):
        entrada_data = directorio_data[i * ENTRADA_DIRECTORIO_SIZE: (i + 1) * ENTRADA_DIRECTORIO_SIZE]
        entrada = EntradaDirectorio.from_bytes(entrada_data)
        if entrada.tipo_archivo == "\0":
            espacio_encontrado = True
            break

    if not espacio_encontrado:
        print("No hay espacio disponible en el directorio FiUnamFS para copiar el archivo.")
        return

    entrada_nueva = EntradaDirectorio("-", nombre_archivo_fiunamfs, len(contenido), 0, "20240508131756", "20240508131756")
    directorio_data = directorio_data[:i * ENTRADA_DIRECTORIO_SIZE] + entrada_nueva.to_bytes() + directorio_data[(i + 1) * ENTRADA_DIRECTORIO_SIZE:]
    img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
    img_file.write(directorio_data)

    print(f"Se ha copiado {nombre_archivo_local} al disco FiUnamFS con el nombre {nombre_archivo_fiunamfs}.")


def copiar_desde_fiunamfs(img_file, nombre_archivo_fiunamfs):
    # Ruta de la carpeta "LocalSO" dentro de la carpeta actual del proyecto
    carpeta_localSO = os.path.join(os.getcwd(), "LocalSO")

    # Crear la carpeta "LocalSO" si no existe
    if not os.path.exists(carpeta_localSO):
        os.makedirs(carpeta_localSO)

    # Ruta del archivo local en la carpeta "LocalSO"
    nombre_archivo_local = os.path.join(carpeta_localSO, nombre_archivo_fiunamfs)

    with open(nombre_archivo_local, "wb") as local_file:
        img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
        for i in range(NUMERO_ENTRADAS_DIRECTORIO):
            entrada_data = img_file.read(ENTRADA_DIRECTORIO_SIZE)
            entrada = EntradaDirectorio.from_bytes(entrada_data)
            if os.path.basename(entrada.nombre_archivo).strip() == nombre_archivo_fiunamfs.strip():
                img_file.seek(entrada.cluster_inicial * CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER)
                while True:
                    data = img_file.read(CLUSTER_SIZE)
                    if not data:
                        break
                    local_file.write(data)
                print(f"Se ha copiado {nombre_archivo_fiunamfs} a la carpeta 'LocalSO'.")
                return  # Salir del bucle una vez que se haya copiado el archivo
        print(f"No se encontró el archivo {nombre_archivo_fiunamfs} en el FiUnamFS.")


def eliminar_archivo_fiunamfs(img_file, nombre_archivo_fiunamfs):
    img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
    directorio_data = img_file.read(CLUSTER_SIZE * NUM_SECTORES_ENTRADA_DIRECTORIO * NUMERO_ENTRADAS_DIRECTORIO)

    for i in range(NUMERO_ENTRADAS_DIRECTORIO):
        entrada_data = directorio_data[i * ENTRADA_DIRECTORIO_SIZE: (i + 1) * ENTRADA_DIRECTORIO_SIZE]
        entrada = EntradaDirectorio.from_bytes(entrada_data)
        if entrada.nombre_archivo.strip() == nombre_archivo_fiunamfs:
            if entrada.tipo_archivo == "/":  # Verificar si ya ha sido eliminado
                print(f"El archivo {nombre_archivo_fiunamfs} ya ha sido eliminado anteriormente.")
                return "ya_eliminado"
            # Marcar la entrada como eliminada
            nueva_entrada_data = b"/" + b"\0" * 63
            directorio_data = directorio_data[:i * ENTRADA_DIRECTORIO_SIZE] + nueva_entrada_data + directorio_data[(i + 1) * ENTRADA_DIRECTORIO_SIZE:]

            # Escribir el directorio modificado de nuevo en el archivo
            img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
            img_file.write(directorio_data)

            print(f"El archivo {nombre_archivo_fiunamfs} ha sido eliminado.")
            return "eliminado"

    print(f"El archivo {nombre_archivo_fiunamfs} no se encontró en el directorio.")
    return "no_encontrado"


def eliminar_archivo_hilo(img_file, nombre_archivo_fiunamfs):
    eliminar_archivo_fiunamfs(nombre_archivo_fiunamfs)

