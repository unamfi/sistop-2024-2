## Definición de la clase y funcion básica de validación
import os
import struct
from threading import Thread, Lock


class FiUnamFS:
    def __init__(self, filepath):
        # Inicializa la clase con la ruta al archivo del sistema de archivos, establece un bloqueo para acceso concurrente
        # y lee el superbloque (primer cluster de 1024 bytes) para obtener la información inicial del sistema de archivos.
        self.filepath = filepath
        self.filepath = filepath
        self.lock = Lock()
        with open(self.filepath, 'r+b') as f:
            self.superblock = f.read(1024)  # Leer superbloque (primer cluster)

    def validate_fs(self):
        # Valida que el sistema de archivos sea FiUnamFS versión '24-2' leyendo y verificando campos específicos del superbloque.
        # Si no coincide, se lanza una excepción indicando incompatibilidad o corrupción.
        name = struct.unpack('8s', self.superblock[0:8])[0].decode('ascii').strip('\x00')
        version = struct.unpack('5s', self.superblock[10:15])[0].decode('ascii').strip('\x00')
        if name != 'FiUnamFS' or version != '24-2':
            raise ValueError("Sistema de archivos no compatible o corrupto")

if __name__ == "__main__":
    ##El path depende del sistema, para este caso se utilizó WINDOWS
    fs = FiUnamFS(r'C:\Users\AlamLR\Desktop\proyectoSO\fiunamfs.img')
    fs.validate_fs()
