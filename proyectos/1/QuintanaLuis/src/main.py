"""
Proyecto 1

"""
import pathlib

from sistema_archivos import SistemaArchivos
from pathlib import Path
from helper import *

# Se encuentran los archivos de ayuda y se almacenan los extraidos
# del sistema de archivos
RESOURCES_DIR = '../resources'


# Olvidará que existe tal archivo
def eliminar_archivo(cluster_inicial: int, tamano_bytes: int) -> bool:
    # hay 2048 bytes por cluster
    byte_inicial = cluster_inicial * 2048
    byte_final = byte_inicial + tamano_bytes

    with open(ruta_fs, "r+b") as archivo:
        archivo.seek(byte_inicial)
        archivo.write(b'\x00' * tamano_bytes)
        return True


if __name__ == "__main__":
    sistema_archivos = SistemaArchivos(ruta_sistema="../fiunamfs.img")

    #sistema_archivos.pull(84, 254484, RESOURCES_DIR + '/mensaje.jpg')
    #sistema_archivos.pull('README.org', RESOURCES_DIR + '/README.md')
    #sistema_archivos.pull(200, 855494, RESOURCES_DIR + '/prueba.jpeg')


    sistema_archivos.push(RESOURCES_DIR + '/imagen.jpeg')
    sistema_archivos.directorio.listar(detalles=True)
