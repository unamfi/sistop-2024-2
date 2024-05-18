import os
from struct import *

#Abriendo el FS
img_FS="fiunamfs.img"
FS = open(img_FS,"r+b")

#Se muestran los datos del superbloque
FS.seek(0)
nombre_FS = FS.read(8).decode('ascii')
FS.seek(10)
version = FS.read(10).decode('ascii')
etiqueta_volumen = FS.read(20).decode('ascii')
totalsuperbloque = FS.read(54)
tamaño_cluster = unpack("i", totalsuperbloque[40:44])[0]
num_cluster_dir = unpack("i", totalsuperbloque[45:49])[0]
num_cluster_uni = unpack("i", totalsuperbloque[50:54])[0]

print("Nombre del sistema de archivos: ",nombre_FS,"\n",
      "Version: ",version,"\n",
      "Etiqueta del Volumen: ",etiqueta_volumen, "\n",
      "Tamaño del cluster: ",tamaño_cluster, "bytes", "\n",
      "Numero de cluster que mide el directorio: ",num_cluster_dir, "\n",
      "Numero de cluster que mide la unidad completa: ",num_cluster_uni)

def menu():
    while True:
        print("1. Listar el contenido del directorio")
        print("2. Copiar archivo de FiUnamFS a la computadora")
        print("3. Copiar archivo de la computadora hacia FiUnamFS")
        print("4. Borrar archivo de FiUnamFS")
        print("5. Salir")
        opcion = int(input("Ingresa una opción: "))
        if opcion == 1:
            
        #elif opcion == 2:
            
        #elif opcion == 3:
            
        #elif opcion == 4:
            
        #elif opcion == 5:
            break
        else:
            print("Opción inválida")

#Ejecuta el menu principal
#menu()