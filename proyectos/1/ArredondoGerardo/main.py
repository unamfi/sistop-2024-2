import os
import struct
import time
import threading
from queue import Queue


ruta_imagen = "" #La ruta que se usará

def verificar_superbloque(ruta):
    with open(ruta, "rb") as archivo:
        datos = archivo.read(54) #obteniendo datos
        magic, version_bruta = struct.unpack("<8s6s", datos[:14]) #obteniendo más datos
        version = version_bruta[2:6].decode("ascii")
        if magic.decode("ascii") != "FiUnamFS": #Validando los datos con if
            return False
        if version != "24-2":
            return False
        print("\n\nEl sistema y la versión son correctos.\n\n")
        return True

def obtener_superbloque(ruta): 
    with open(ruta, "rb") as archivo:
        datos = archivo.read(54) #En las siguientes lineas convertiremos de 32 bits a bytes los diferentes datos que necesitemos, siguiendo la recomendación del profesor de usar
                    #unpack()
        _, etiqueta, _ = struct.unpack("<20s19s15s", datos) #El atributo entre paréntesis le indica a la función de donde a donde quiere obtener los datos
        _, tamaño_cluster, _ = struct.unpack("<40sI10s", datos)
        _, clusters_directorio, _ = struct.unpack("<45sI5s", datos)
        _, total_clusters = struct.unpack("<50sI", datos)

        print(f"Etiqueta: {etiqueta.decode('ascii').rstrip(chr(0))}") #Imprimimos los datos que obtuvimos
        print(f"Tamaño de clusters: {tamaño_cluster} bytes")
        print(f"Clusters del directorio: {clusters_directorio}")
        print(f"Clusters totales: {total_clusters}")

        return { #Los retornamos
            "etiqueta": etiqueta.decode("ascii").rstrip(chr(0)),
            "tamaño_cluster": tamaño_cluster,
            "clusters_directorio": clusters_directorio,
            "total_clusters": total_clusters
        }

def listar_archivos(ruta, cola):
    superblock = obtener_superbloque(ruta) #Primero que nada obtenemos el superbloque 

    if superblock: 
        with open(ruta, "rb") as archivo: #leemos la ruta del img
            archivo.seek(superblock["tamaño_cluster"])
            archivos = []
            for _ in range(superblock["clusters_directorio"]): #Por cada directorio que tengamos, lo vamos a leer para después mostrar su información
                entrada = archivo.read(64) #información de cada cluster
                tipo, nombre, tamaño, cluster_inicial, creacion, modificacion, _ = struct.unpack("<c15sI3s14s14s13s", entrada) #información específica

                nombre = nombre.decode("ascii").rstrip(chr(0))
                if nombre != "###############":
                    archivos.append((nombre, tamaño, int.from_bytes(cluster_inicial, 'little')))
            cola.put(archivos)























def listar_archivos_thread(ruta, cola):
    print("Listando archivos...")
    listar_archivos(ruta, cola)

def copiar_a_fiunamfs_thread(nombre_archivo, ruta_img, cola):
    print(f"Copiando {nombre_archivo} a FiUnamFS...")
    copiar_a_fiunamfs(nombre_archivo, ruta_img, cola)









if __name__ == "__main__":
    while True:
        print("\nSeleccione una opción:")
        print("1. Ver contenidos")
        print("2. Copiar de FiUnamFS al sistema operativo")
        print("3. Copiar del sistema operativo a FiUnamFS")
        print("4. Eliminar archivo")
        print("5. Salir")

        opcion = input("\n\nQué opción desea -----> ")
        if verificar_superbloque(ruta_imagen):
            if opcion == "1":
                listar_archivos(ruta_imagen)
            elif opcion == "2":
                nombre_archivo = input("Archivo en FiUnamFS a copiar al sistema:")
                copiar_desde_fiunamfs(nombre_archivo, ruta_imagen)
            elif opcion == "3":
                nombre_archivo = input("Archivo en el sistema a copiar a FiUnamFS:")
                copiar_a_fiunamfs(nombre_archivo, ruta_imagen)
            elif opcion == "4":
                nombre_archivo = input("Archivo a eliminar:")
                eliminar_archivo(nombre_archivo, ruta_imagen)
            elif opcion == "5":
                print("Gracias por usar :D")
                break
            else:
                print("Ingrese una opción válida.")
        else:
            print("Sistema no válido.")

