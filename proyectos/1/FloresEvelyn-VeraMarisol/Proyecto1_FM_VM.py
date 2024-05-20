"""
Created on Mon May 19

@author: Flores Melquiades Evelyn Jasmin
         Vera Garmendia Miriam Marisol
         
"""
import os
import struct
import threading

TAMANO_CLUSTER = 512
TAM_ENTRADA = 64
# Cluster
DIRECTORIO_INICIO = TAMANO_CLUSTER
# 4 sectores
DIRECTORIO_TAMANO = 4 * TAMANO_CLUSTER 
# Tomando en cuenta que el tamaño total es 1440KB
MAXIMO_CLUSTERS = 1440 // 4 
#Semaforo para sincronizar la lectura de archivos
semaforo = threading.Semaphore(value=1)
#Sincronizar hilos
lock = threading.Lock()

def ENTERO(DIRECTORIO_INICIO, TAM_ENTRADA):
    with open(fiunamfs_img, "rb") as f:   
        f.seek(DIRECTORIO_INICIO)
        DATA = f.read(TAM_ENTRADA) 
        E = struct.unpack("<I", DATA)[0]  
        return E 
        
def CADENA(DIRECTORIO_INICIO, TAM_ENTRADA):
    with open(fiunamfs_img, "rb") as f:  
        f.seek(DIRECTORIO_INICIO)  
        CADENA = f.read(TAM_ENTRADA)              
        string = CADENA.decode("ascii").rstrip()    
        return string 

def LIST_DIRECTORIO(fiunamfs_img):
    with open(fiunamfs_img, 'rb') as f:
        for _ in range(0, DIRECTORIO_TAMANO, TAM_ENTRADA):
            nombre = CADENA(DIRECTORIO_TAMANO + _,15)
            tam= ENTERO(DIRECTORIO_TAMANO+_+16,4)
            if nombre != '/':
                print("\033[1m   Nombre\t\tTamaño   \033[0m")
                print(f"   {nombre}\t{tam} bytes")
                
#Funcion apara copiar al nuestro sistema
def COPY_TO_SYSTEM(fiunamfs_img, nombre_archivo, destino):

    #Adquirir semaforo
    semaforo.acquire()
    with open(fiunamfs_img, 'rb') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(0, DIRECTORIO_TAMANO * 4, TAM_ENTRADA):
            entrada = f.read(TAM_ENTRADA)
            tipo_archivo = entrada[0:1]
            if tipo_archivo == b'-':
                nombre, tam, cluster_ini = (
                    entrada[1:16].decode('ascii').rstrip(),
                    struct.unpack('<I', entrada[16:20])[0],
                    struct.unpack('<I', entrada[20:24])[0]
                )
                #Depurar
                print(f"Nombre encontrado: {nombre}, Tamaño: {tam}, Cluster inicial: {cluster_ini}")  
                if nombre.rstrip('\x00').strip() == nombre_archivo.rstrip('\x00').strip():
                    f.seek(cluster_ini * TAMANO_CLUSTER)
                    datos = f.read(tam)
                    with open(destino, 'wb') as archivo_destino:
                        archivo_destino.write(datos)
                    return
    semaforo.release()
    raise FileNotFoundError("El archivo no se encuentra FiUnamFS")

#Copiar a FIUNAM un archivo desde nuestro sistema
def COPY_TO_FIUNAM(fiunamfs_img, archivo_origen, nombre_destino):
    semaforo.acquire()
    with open(fiunamfs_img, 'r+b') as f:
        tam_origen = os.path.getsize(archivo_origen)
        cluster_libre = 5
        posicion_entrada_libre = None

        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAM_ENTRADA):
            posicion_actual = f.tell()
            entrada = f.read(TAM_ENTRADA)
            tipo_archivo = entrada[0:1]
            cluster_ini = struct.unpack('<I', entrada[20:24])[0]

            #Entrada vacia
            if tipo_archivo == b'/' and posicion_entrada_libre is None:  
                posicion_entrada_libre = posicion_actual
                #Depurar
                print(f"Encontrada entrada libre en posición {posicion_entrada_libre}") 

            if cluster_ini >= cluster_libre:
                cluster_libre = cluster_ini + 1
                print(f"Clouster libre: {cluster_libre}")  

        if posicion_entrada_libre is None:
            raise Exception("No hay espaciosuficiente")
        else:
            print(f"Entrada libre en: {posicion_entrada_libre}, Cluster libre para el archivo: {cluster_libre}")

        with open(archivo_origen, 'rb') as archivo_origen_f:
                 with look:
                     f.seek(cluster_libre * TAMANO_CLUSTER)
                     f.write(archivo_origen_f.read())

        f.seek(posicion_entrada_libre)
        f.write(b'-' + nombre_destino.ljust(15).encode('ascii'))
        f.write(struct.pack('<I', tam_origen))
        f.write(struct.pack('<I', cluster_libre))
    semaforo.release()

#Funcion apara eleiminar un archivo de FIUNAM
def DELETE(fiunamfs_img, nombre_archivo):
    semaforo.acquire()
    with open(fiunamfs_img, 'r+b') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAM_ENTRADA):
            posicion = f.tell()
            entrada = f.read(TAM_ENTRADA)
            nombre = entrada[1:16].decode('ascii').rstrip()
            if nombre.rstrip('\x00').strip() == nombre_archivo.rstrip('\x00').strip():
                f.seek(posicion)
                f.write(b'/' + b' ' * 15)
                print("Archivo eliminado con exito")
                return
    semaforo.release()
    raise FileNotFoundError("Archivo no encontrado en FiUnamFS")

def menu_principal():
    while True:
        print("\n- Sistema de Archivos FiUnamFS - ")
        print("1. Listar directorio")
        print("2. Copiar archivo de FiUnamFS a sistema")
        print("3. Copiar archivo de sistema a FiUnamFS")
        print("4. Eliminar archivo de FiUnamFS")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            LIST_DIRECTORIO(fiunamfs_img)

        elif opcion == '2':
            nombre_archivo = input("Ingresa el nombre del archivo en FiUnamFS(incluye extencion): ")
            destino = input("Ingresa la ruta de destino en el sistema (ENTER para la carpeta actual): ")
            if not destino:
                destino = os.path.join(os.getcwd(), nombre_archivo)  
            try:
                COPY_TO_SYSTEM(fiunamfs_img, nombre_archivo, destino)
                print("Archivo copiado con éxito a", destino)
            #Manejo de exepciones
            except Exception as e:
                print("Error al copiar el archivo:", e)

        elif opcion == '3':
            origen = input("Ingresa la ruta del archivo en el sistema: ")
            nombre_destino = input("Ingresa el nombre del archivo en FiUnamFS: ")
            COPY_TO_FIUNAM(fiunamfs_img, origen, nombre_destino)
        elif opcion == '4':
            nombre_archivo = input("Ingresa el nombre del archivo a eliminar de FiUnamFS(Incluye extension): ")
            DELETE(fiunamfs_img, nombre_archivo)
        elif opcion == '5':
            print("Vuelve pronto!")
            break
        else:
            print("Opción no válida. Vueleve aintentarlo")

# Archivo actualmente usando
fiunamfs_img = "fiunamfs.img" 
# Regresar el menu para ejecutar
menu_principal()


