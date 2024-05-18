import os
import struct
from time import sleep
from datetime import *
from math import ceil
# Ruta del sistema de archivos
sistemaArchivos = "fiunamfs.img"

def clear():
    os.system('clear')

def leer_superbloque():
    global sistemaArchivos
    with open(sistemaArchivos, 'rb') as file:
        file.seek(0)
        # Leer el primer cluster que es el superbloque
        superbloque = file.read(1024)
        # Extraer información del superbloque
        nombre = superbloque[0:8].decode().strip('\x00')
        version = superbloque[10:15].decode().strip('\x00')
        # Revisar validez del archivo 
        if nombre != "FiUnamFS":
            raise ValueError("El sistema de archivos no es FiUnamFS")
        if version != "24-2":
            raise ValueError("Versión del sistema de archivos no compatible")


def leerEnteros(cabezal,tam):
    global sistemaArchivos
    # Abrir el sistema de archivos
    with open(sistemaArchivos,'rb') as file:
        # Ubicar el cabezal
        file.seek(cabezal)
        contenido = file.read(tam)
        # Usamos unpack para la representación en 32 bits
        contenido, *resto = struct.unpack('<I',contenido)
        return contenido

def leerAscii(cabezal,tam):
    global sistemaArchivos
    with open(sistemaArchivos,'rb') as file:
        file.seek(cabezal)
        # Leemos la información y la decodificamos en Latin-1 -> ASCII 8 bits
        contenido = file.read(tam).decode('Latin-1')
        return contenido
    

def leerInfo(cabezal,tam):
    global sistemaArchivos
    with open(sistemaArchivos,'rb') as file:
        file.seek(cabezal)
        # Leemos la información
        contenido = file.read(tam)
        return contenido
    
def escribirAscii(cabezal,contenido):
    global sistemaArchivos
    with open(sistemaArchivos,'rb+') as file:
        file.seek(cabezal)
        # Escribir el contenido
        file.write(contenido.encode('Latin-1'))

def escribirEnteros(cabezal,contenido):
    global sistemaArchivos
    with open(sistemaArchivos,'rb+') as file:
        file.seek(cabezal)
        # Usamos pack para la representación en 32 bits
        file.write(struct.pack('<I',contenido))

#Variables locales con la información del sistema de archivos
identificador = leerAscii(0,8)
version = leerAscii(10,4)
etiquetaVolumen = leerAscii(20,19)
tamCluster = leerEnteros(40,4)
numClusterDir = leerEnteros(45,4)
clusterTotales = leerEnteros(50,4)
numEntradas = 128
entradasDirectorio = 64
tamSectores = 256
inicioDir = tamCluster
finDir = inicioDir + 4 * tamCluster

archivos = {}
entradasLibres = []