import os
import struct
import threading
from queue import Queue

ruta_imagen = input("Ingresa la ruta en donde se encuentra el archivo img, añadiendo el nombre del archivo ---> ")


def verificar_superbloque(ruta):
    with open(ruta, "rb") as archivo:
        datos = archivo.read(54) #obteniendo datos
        magic, version_bruta = struct.unpack("<8s6s", datos[:14]) #obteniendo más datos
        version = version_bruta[2:6].decode("ascii")
        if magic.decode("ascii") != "FiUnamFS": #Validando los datos con if
            return False
        if version != "24-2":
            return False
        print("\n\nEl sistema y la versión son correctos.\n")
        return True

def obtener_superbloque(ruta): 
    with open(ruta, "rb") as archivo:
        datos = archivo.read(54) #En las siguientes lineas convertiremos de 32 bits a bytes los diferentes datos que necesitemos, siguiendo la recomendación del profesor de usar
                    #unpack()
        _, categoria, _ = struct.unpack("<20s19s15s", datos) #El atributo entre paréntesis le indica a la función de donde a donde quiere obtener los datos
        _, tamaño_cluster, _ = struct.unpack("<40sI10s", datos)
        _, clusters_directorio, _ = struct.unpack("<45sI5s", datos)
        _, total_clusters = struct.unpack("<50sI", datos)
        
        print(f"\nCategoría: {categoria.decode('ascii').rstrip(chr(0))}") #Imprimimos los datos que obtuvimos
        print(f"E tamaño de clusters es: {tamaño_cluster} bytes")
        print(f"Cantidad de clusters en el directorio: {clusters_directorio}")
        print(f"Clusters totales: {total_clusters}")
        print("\n")

        return { #Los retornamos
            "categoria": categoria.decode("ascii").rstrip(chr(0)),
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


def copiar_desde_fiunamfs(nombre_archivo, ruta_img): 
    superblock = obtener_superbloque(ruta_img)

    if superblock:
        with open(ruta_img, "rb") as archivo: #Leemos la ruta del img
            archivo.seek(superblock["tamaño_cluster"])
            for _ in range(superblock["clusters_directorio"]):#Una vez iteramos por todos los directorios que tengamos
                entrada = archivo.read(64)#Info
                tipo, nombre, tamaño, cluster_inicial, _, _, _ = struct.unpack("<c15sI3s14s14s13s", entrada)#Info específica
                
                #obtendremos información importante para poder identificar correctamente el nombre del archivo en FiUnamFS
                largo = len(nombre_archivo)
                nombre_a_decode = nombre.decode("ascii")
                nombre = nombre_a_decode[0:largo]
                if nombre == nombre_archivo and tipo == b'-': #Confirmamos que nos encontramos en el archivo correcto para copiar
                    #Abriremos el archivo para poder escribirlo en el directorio de nuestra computadora en donde nos encontremos
                    with open(nombre_archivo, "wb") as destino:
                        cluster_inicial_int = int.from_bytes(cluster_inicial, "little")
                        archivo.seek(cluster_inicial_int * superblock["tamaño_cluster"])
                        contenido = archivo.read(tamaño) #Leemos el contenido del archivo (dependiendo su tamaño será lo que leamos)
                        destino.write(contenido) #escribiremos el contenido en nuestro directorio
                        print(f"-------------------->Archivo {nombre_archivo} copiado exitosamente.")
                        return

        print(f"No se encontró el archivo {nombre_archivo} en FiUnamFS.")

def copiar_a_fiunamfs(nombre_archivo, ruta_img, cola):#Función para copiar hacia FiUnamFS
    superblock = obtener_superbloque(ruta_img)


def eliminar_archivo(nombre_archivo, ruta_img):
    superblock = obtener_superbloque(ruta_img) #Obtenemos el superbloque

    if superblock:
        with open(ruta_img, "rb+") as archivo:
            archivo.seek(superblock["tamaño_cluster"])
            for _ in range(superblock["clusters_directorio"]): #navegamos entre los directorios que tenemos
                entrada = archivo.read(64)
                tipo, nombre, _, _, _, _, _ = struct.unpack("<c15sI3s14s14s13s", entrada)#La información específica
                

                #Obtenemos de manera correcta el nombre del archivo
                largo = len(nombre_archivo)
                nombre_a_decode = nombre.decode("ascii")
                nombre = nombre_a_decode[0:largo]

                if nombre == nombre_archivo and tipo == b'-': #Si conincidimos en el archivo procedemos a eliminarlo
                    archivo.seek(archivo.tell() - 64)
                    archivo.write(struct.pack("<c15sI3s14s14s13s", b'/', "###############".ljust(15, chr(0)).encode('ascii'), 0, struct.pack("<I", 0), b'', b'', b'')) #Modificamos el archivo en .img
                    print(f"-------------------->Archivo {nombre_archivo} eliminado exitosamente.") #Ya no existe el archivo :c
                    return

            print(f"No se encontró el archivo {nombre_archivo} en FiUnamFS.")




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
        #case para las opciones
        opcion = input("\n\nQué opción desea -----> ")
        if verificar_superbloque(ruta_imagen):
            cola = Queue()
            if opcion == "1":
                hilo_listar = threading.Thread(target=listar_archivos_thread, args=(ruta_imagen, cola)) #Aquí es donde se implementa el primer hilo, siendo este para 
                                    #el listado de los archivos dentro de FiUnamFS
                hilo_listar.start()
                hilo_listar.join()
                archivos = cola.get()
                for archivo in archivos:
                    print(f"Nombre: {archivo[0]} \t\tTamaño: {archivo[1]} \t\tCluster Inicial: {archivo[2]}")
                #listar_archivos(ruta_imagen)


            elif opcion == "2":
               nombre_archivo = input("Archivo en FiUnamFS a copiar al sistema:")
               copiar_desde_fiunamfs(nombre_archivo, ruta_imagen)



            elif opcion == "3":
                print("No se logró implementar esta opción")



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

