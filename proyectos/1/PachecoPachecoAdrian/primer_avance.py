import struct
import os

# Objeto usado para almacenar la informacion de los registros del directorio
class Registros:
    def __init__(self, tipo, nombre, tamano, cluster_inicial, creacion, modificacion, espacio_libre, registro):
        self.tipo = tipo
        self.nombre = nombre
        self.tamano = tamano
        self.cluster_inicial = cluster_inicial
        self.creacion = creacion
        self.modificacion = modificacion
        self.espacio_libre = espacio_libre
        self.registro = registro

sector = 512
cluster = sector * 4  # Cada cluster es de 4 sectores (2048 bytes)
lista_directorios = []

# Extrae el superbloque
def extraer_superbloque():
    global num_cluster_bytes
    global num_cluster_directorio
    global num_cluster_total
    with open('fiunamfs.img', 'rb') as archivo:
        entrada = 0
        while entrada < 64:
            if entrada == 0:
                contenido = archivo.read(8)
                nombre_sistema_archivos = contenido.decode('ascii').strip()
                if nombre_sistema_archivos == 'FiUnamFS':
                    print("Nombre de sistema de archivos: " + nombre_sistema_archivos)
                else:
                    print("Error de sistema de archivos")
                    return
                entrada += 8
            elif entrada == 10:
                contenido = archivo.read(4)
                version = contenido.decode('ascii').strip()
                if version == '24-2':
                    print("Version: " + version)
                else:
                    print("Error de version")
                    return
                entrada += 4
            elif entrada == 20:
                contenido = archivo.read(15)
                etiqueta = contenido.decode('ascii').strip()
                print("Etiqueta del volumen: " + etiqueta)
                entrada += 15
            elif entrada == 40:
                contenido = archivo.read(4)
                num_cluster_bytes = struct.unpack('<I', contenido)[0]
                print("Tamano del cluster en bytes: " + str(num_cluster_bytes))
                entrada += 4
            elif entrada == 45:
                contenido = archivo.read(4)
                num_cluster_directorio = struct.unpack('<I', contenido)[0]
                print("Numero de clusters del directorio: " + str(num_cluster_directorio))
                entrada += 4
            elif entrada == 50:
                contenido = archivo.read(4)
                num_cluster_total = struct.unpack('<I', contenido)[0]
                print("Numero de clusters de la unidad: " + str(num_cluster_total))
                entrada += 4
            else:
                archivo.read(1)
                entrada += 1
    print("Fin")
