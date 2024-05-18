import os
import struct
from time import sleep
from datetime import *
from math import ceil
# Ruta del sistema de archivos
sistema_archivos = "fiunamfs.img"

def clear():
    os.system('clear')

def leer_superbloque():
    global sistema_archivos
    with open(sistema_archivos, 'rb') as file:
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


def leer_enteros(cabezal,tam):
    global sistema_archivos
    # Abrir el sistema de archivos
    with open(sistema_archivos,'rb') as file:
        # Ubicar el cabezal
        file.seek(cabezal)
        contenido = file.read(tam)
        # Usamos unpack para la representación en 32 bits
        contenido, *resto = struct.unpack('<I',contenido)
        return contenido

def leer_ascii(cabezal,tam):
    global sistema_archivos
    with open(sistema_archivos,'rb') as file:
        file.seek(cabezal)
        # Leemos la información y la decodificamos en Latin-1 -> ASCII 8 bits
        contenido = file.read(tam).decode('Latin-1')
        return contenido
    

def leer_info(cabezal,tam):
    global sistema_archivos
    with open(sistema_archivos,'rb') as file:
        file.seek(cabezal)
        # Leemos la información
        contenido = file.read(tam)
        return contenido
    
def escribir_ascii(cabezal,contenido):
    global sistema_archivos
    with open(sistema_archivos,'rb+') as file:
        file.seek(cabezal)
        # Escribir el contenido
        file.write(contenido.encode('Latin-1'))

def escribir_enteros(cabezal,contenido):
    global sistema_archivos
    with open(sistema_archivos,'rb+') as file:
        file.seek(cabezal)
        # Usamos pack para la representación en 32 bits
        file.write(struct.pack('<I',contenido))

#Variables locales con la información del sistema de archivos
identificador = leer_ascii(0,8)
version = leer_ascii(10,4)
etiqueta_volumen = leer_ascii(20,19)
tam_cluster = leer_enteros(40,4)
num_clusterDir = leer_enteros(45,4)
cluster_totales = leer_enteros(50,4)
num_entradas = 128
entradas_directorio = 64
tam_sectores = 256
inicio_dir = tam_cluster
fin_dir = inicio_dir + 4 * tam_cluster

archivos = {}
entradas_libres = []


#Funcion encarga de escribir la informacion de un directorio en el sistema de archivos
def escribir_dir(nombre,tam,cabezal,fecha_modificacion,fecha_creacion):
    global sistema_archivos
    global num_entradas
    num_entradas -= 1
    nombre = nombre.ljust(14)
    directorio = entradas_libres.pop(0)
    escribir_ascii(directorio,'-')
    escribir_ascii(directorio + 1,nombre)
    escribir_enteros(directorio + 16, tam)
    escribir_enteros(directorio + 20, ceil(cabezal/tam_cluster))
    escribir_ascii(directorio + 24,fecha_creacion)
    escribir_ascii(directorio + 38,fecha_modificacion)

def escribir_info(cabezal,contenido):
    global sistema_archivos
    global num_entradas
    with open(sistema_archivos,'rb+') as file:
        file.seek(cabezal)
        file.write(contenido)
    #guardarInformacionArchivos()

#Elimina el un directorio del sistema de archivos
def eliminar_dir(cabezal):
    global num_entradas
    global entradas_libres
    entradas_libres.append(cabezal)
    entradas_libres.sort()
    num_entradas += 1
    escribir_ascii(cabezal,'/..............')
    escribir_ascii(cabezal + 24,'0000000000000000000000000000')
    with open(sistema_archivos,'rb+') as file:
        file.seek(cabezal + 16)
        file.write(b'\x00' * 9)
        file.seek(cabezal + 52)
        file.write(b'\x00' * 12)

def eliminarInfo(cabezal,tam):
    with open(sistema_archivos,'rb+') as file:
        file.seek(cabezal)
        file.write(b'\x00' * tam)


def guardar_info_archivos():
    # Se mostrarán únicamente los archivos que tienen un nombre específico
    # Se deberá de recorrer el directorio
    cabezal = inicio_dir
    global num_entradas
    global archivos
    archivos.clear()
    num_entradas = 128
    #Guarda la informacion de los archivos en el diccionario 'archivos'
    while(cabezal != finDir):
        archivo = {}
        with open(sistema_archivos,'rb') as file:
            file.seek(cabezal)
            # Comprueba si la entrada tiene algun contenido o esta vacia
            entrada = leer_ascii(cabezal,1)
            if entrada == '-':
                # Lee la informacion del archivo por partes
                archivo['nombre'] = leer_ascii(cabezal + 1, 14) #Nombre 
                archivo['tam'] = leer_enteros(cabezal + 16, 4) # Tamaño
                archivo['cluster_inicial'] = leer_enteros(cabezal + 20, 4) #Tamanio del cluster
                fecha_objeto = datetime.strptime(leer_ascii(cabezal + 24, 13), "%Y%m%d%H%M%S")
                cadena_formateada = fecha_objeto.strftime("%Y-%m-%d %H:%M:%S")
                archivo['fecha_creacion'] = cadena_formateada #fecha de creación del archivo
                fecha_objeto = datetime.strptime(leer_ascii(cabezal + 38, 13), "%Y%m%d%H%M%S")
                cadena_formateada = fecha_objeto.strftime("%Y-%m-%d %H:%M:%S")
                archivo['fecha_modificacion'] = cadena_formateada #fecha de modificacion del archivo
                archivo['cluster_directorio'] = cabezal

                # Se guarda la informacion recabada de los archivos
                archivos[archivo['nombre'].rstrip()] = archivo
                cabezal += 64
                num_entradas -= 1
                pass
            else:
                #Es ignorado y deja avanzar el cabezal
                entradas_libres.append(cabezal)
                cabezal += 64