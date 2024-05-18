import os
from struct import *
import threading

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
tamaño_cluster = unpack("<I", totalsuperbloque[40:44])[0]
num_cluster_dir = unpack("<I", totalsuperbloque[45:49])[0]
num_cluster_uni = unpack("<I", totalsuperbloque[50:54])[0]

print("Nombre del sistema de archivos: ",nombre_FS,"\n",
      "Version: ",version,"\n",
      "Etiqueta del Volumen: ",etiqueta_volumen, "\n",
      "Tamaño del cluster: ",tamaño_cluster, "bytes", "\n",
      "Numero de cluster que mide el directorio: ",num_cluster_dir, "\n",
      "Numero de cluster que mide la unidad completa: ",num_cluster_uni)

#Recopilará la información de cada archivo
def listarArchivos():
    global FS,tamaño_cluster
    infoArchivo = []
    for i in range (64):
        tam = 1024 + (i*64)
        FS.seek(tam)
        lectura = FS.read(15)
        if lectura != b'/##############':
            FS.seek(tam+0)
            print("Tipo de archivo: ",FS.read(1).decode().strip())

            FS.seek(tam+1)
            print("Archivo: ",FS.read(15).decode().strip())

            FS.seek(tam+24)
            Hora_Fecha = FS.read(14).decode().strip()
            print("Fecha de creación del archivo: ", Hora_Fecha[0:4],"-",Hora_Fecha[4:6],"-", Hora_Fecha[6:8]," ",Hora_Fecha[8:10],":", Hora_Fecha[10:12],":",Hora_Fecha[12:14])

            FS.seek(tam+38)
            Hora_Fecha = FS.read(14).decode().strip()
            print("Fecha de modificación del archivo: ", Hora_Fecha[0:4],"-",Hora_Fecha[4:6],"-", Hora_Fecha[6:8]," ",Hora_Fecha[8:10],":", Hora_Fecha[10:12],":",Hora_Fecha[12:14])
            print("\n")

#Hilos
hilolistar = threading.Thread(target=listarArchivos)

def menu():
    while True:
        print("1. Listar el contenido del directorio")
        print("2. Copiar archivo de FiUnamFS a la computadora")
        print("3. Copiar archivo de la computadora hacia FiUnamFS")
        print("4. Borrar archivo de FiUnamFS")
        print("5. Salir")
        opcion = int(input("Ingresa una opción: "))
        if opcion == 1:
            hilolistar.start()
        #elif opcion == 2:
            
        #elif opcion == 3:
            
        #elif opcion == 4:
            
        #elif opcion == 5:
            break
        else:
            print("Opción inválida")

#Ejecuta el menu principal
menu()

