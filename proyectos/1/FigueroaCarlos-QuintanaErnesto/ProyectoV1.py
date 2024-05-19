import os
import struct
from time import sleep
from datetime import *
from math import ceil
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
#Ruta del sistema de archivos
sistema_archivos = "fiunamfs.img"

def clear():
    os.system('clear')

def leer_superbloque():
    global sistema_archivos
    with open(sistema_archivos, 'rb') as file:
        file.seek(0)
        #Leer el primer cluster que es el superbloque
        superbloque = file.read(1024)
        #Extraer información del superbloque
        nombre = superbloque[0:8].decode().strip('\x00')
        version = superbloque[10:15].decode().strip('\x00')
        #Revisar validez del archivo 
        if nombre != "FiUnamFS":
            raise ValueError("El sistema de archivos no es FiUnamFS")
        if version != "24-2":
            raise ValueError("Versión del sistema de archivos no compatible")


def leer_enteros(cabezal,tam):
    global sistema_archivos
    #Abrir el sistema de archivos
    with open(sistema_archivos,'rb') as file:
        #Ubicar el cabezal
        file.seek(cabezal)
        contenido = file.read(tam)
        #Usamos unpack para la representación en 32 bits
        contenido, *resto = struct.unpack('<I',contenido)
        return contenido

def leer_ascii(cabezal,tam):
    global sistema_archivos
    with open(sistema_archivos,'rb') as file:
        file.seek(cabezal)
        #Leemos la información y la decodificamos en Latin-1 -> ASCII 8 bits
        contenido = file.read(tam).decode('Latin-1')
        return contenido
    

def leer_info(cabezal,tam):
    global sistema_archivos
    with open(sistema_archivos,'rb') as file:
        file.seek(cabezal)
        #Leemos la información
        contenido = file.read(tam)
        return contenido
    
def escribir_ascii(cabezal,contenido):
    global sistema_archivos
    with open(sistema_archivos,'rb+') as file:
        file.seek(cabezal)
        #Escribir el contenido
        file.write(contenido.encode('Latin-1'))

def escribir_enteros(cabezal,contenido):
    global sistema_archivos
    with open(sistema_archivos,'rb+') as file:
        file.seek(cabezal)
        #Usamos pack para la representación en 32 bits
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
    guardar_info_archivos()

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

def eliminar_info(cabezal,tam):
    with open(sistema_archivos,'rb+') as file:
        file.seek(cabezal)
        file.write(b'\x00' * tam)


def guardar_info_archivos():
    #Se mostrarán únicamente los archivos que tienen un nombre específico
    #Se deberá de recorrer el directorio
    cabezal = inicio_dir
    global num_entradas
    global archivos
    archivos.clear()
    num_entradas = 128
    #Guarda la informacion de los archivos en el diccionario 'archivos'
    while(cabezal != fin_dir):
        archivo = {}
        with open(sistema_archivos,'rb') as file:
            file.seek(cabezal)
            #Comprueba si la entrada tiene algun contenido o esta vacia
            entrada = leer_ascii(cabezal,1)
            if entrada == '-':
                #Lee la informacion del archivo por partes
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

                #Se guarda la informacion recabada de los archivos
                archivos[archivo['nombre'].rstrip()] = archivo
                cabezal += 64
                num_entradas -= 1
                pass
            else:
                #Es ignorado y deja avanzar el cabezal
                entradas_libres.append(cabezal)
                cabezal += 64
#Listar los elementos del directorio
def listar_contenidos():
    archivo_sist=[]
    #Recorremos los archivos, sólo se mostrarán los que tengan nombre
    for i,archivo in enumerate(archivos.items()):
        archivo_sist.append(f"{i:>5}- {archivo[0]:<14}|{archivo[1]['tam']:<10}|{archivo[1]['fecha_creacion']}|{archivo[1]['fecha_modificacion']}")
    mssbx= "\n".join(repr(item) for item in archivo_sist)  
    messagebox.showinfo("Archivos",mssbx)

def copiar_archivo_a_sistema():
    ruta = filedialog.askdirectory()
    ruta.rstrip().lstrip()
    nombre = simpledialog.askstring("Copiar archivo", "Ingrese el nombre del archivo a copiar:")
    nombre.rstrip().lstrip()
    #Validamos que el archivo exista en FIunamfs
    if nombre in archivos:
        #Si no existen archivos con el mismo nombre en la ubicación especificada, procedemos a copiar el archivo
        if (os.path.exists(ruta + "/" + nombre) == False):
            #Almacenamos el contenido del archivo en una variable
            contenido = leer_info(archivos[nombre]['cluster_inicial'] * tam_cluster,archivos[nombre]['tam'])
            #Generamos y escribimos un archivo en la ruta especificada con la información recopilada
            with open(ruta + "/" + nombre,'wb') as archivo:
                archivo.write(contenido)
            messagebox.showinfo("Aviso","Archivo guardado con éxito")
        else:
            messagebox.showinfo("ERROR","Un archivo del mismo nombre está en el directorio") 
    else:
        messagebox.showinfo("ERROR","No existe un archivo con ese nombre") 

def eliminar_archivo():
    nombre = simpledialog.askstring("Eliminar archivo", "Ingrese el nombre del archivo a eliminar:")
    nombre.rstrip().lstrip()
    # Validamos que el archivo exista
    if nombre in archivos:
        informacion = archivos[nombre]
        # Eliminamos toda información del archivo 
        eliminar_dir(informacion['cluster_directorio'])
        eliminar_info(informacion['cluster_inicial'] * tam_cluster,informacion['tam'])
        messagebox.showinfo("Aviso","Archivo eliminado exitosamente")
    else: 
         messagebox.showinfo("ERROR","No existe un archivo con ese nombre")
    guardar_info_archivos()


def copiar_archivo_a_FiUnamFs():
    #Verificar que el directorio tenga entradas libres
    if (len(archivos) == num_entradas): 
        messagebox.showinfo("ERROR","No se puede agregar más archivos al directorio")
        return
    else:
        archivo_sistema = filedialog.askopenfilename()
        #Es necesario validar la ruta y la restricción de tamaño
        if os.path.exists(archivo_sistema):
            try:
                with open(archivo_sistema,"rb") as file:
                    nombre = os.path.basename(archivo_sistema)
                    #Que el nombre del archivo no exceda los 14 caracteres.
                    if len(nombre) > 14:
                        messagebox.showinfo("ERROR","El nombre del archivo es demasiado largo para el sistema.")
                        return
                    #El archivo no puede superar los (716 * tam_cluster)
                    tam = os.path.getsize(archivo_sistema)
                    if tam > (cluster_totales - num_clusterDir - 1) * tam_cluster:
                        messagebox.showinfo("ERROR","El tamaño del archivo es demasiado grande para el sistema.")
                        return
                    
                    fecha_modificacion = str(datetime.fromtimestamp(os.path.getmtime(archivo_sistema)))[0:19].replace("-","").replace(" ","").replace(":","")
                    fecha_creacion = str(datetime.fromtimestamp(os.path.getctime(archivo_sistema)))[0:19].replace("-","").replace(" ","").replace(":","")
                    # En este punto, ya se dispone de la información.Es necesario analizar si hay suficiente espacio para la asignación de memoria.
                    cluster_inicial = asignar_espacio(tam)
                    if cluster_inicial == False: 
                        messagebox.showinfo("ERROR","No hay suficiente espacio de almacenamiento para el archivo seleccionado")
                        return
                    else:
                        #Se escribe el archivo 
                        contenido = file.read()
                        #Se escribe en el espacio para archivos.También hay que actualizar el directorio
                        escribir_dir(nombre,tam,cluster_inicial,fecha_modificacion,fecha_creacion)
                        escribir_info(cluster_inicial,contenido)
                        messagebox.showinfo("Aviso","Archivo copiado exitósamente")
            except:
                messagebox.showinfo("ERROR","No fue posible abrir el archivo")
                return
        else:
            messagebox.showinfo("ERROR","No se encontró la ruta")
            return

def asignar_espacio(tam):
    cluster_necesarios = ceil(tam/tam_cluster)
    almacenamiento = []
    #Comienza por el cluster siguiente al directorio
    cluster = 5 
    for archivo in archivos.items():
        almacenamiento.append((archivo[1]['cluster_inicial'],archivo[1]['cluster_inicial'] + ceil(archivo[1]['tam'] / tam_cluster)))
    almacenamiento.sort()
    while(cluster < 720):
        #Si el cabezal se encuentra con un clúster que ya está en uso, lo pasa por alto
        if len(almacenamiento) != 0 and cluster == almacenamiento[0][0]: 
            cluster = almacenamiento[0][1] + 1
            #Se saca el cluster
            almacenamiento.pop(0) 
        else:
            #Colisiona con otro archivo
            if len(almacenamiento) != 0 and (cluster + cluster_necesarios > almacenamiento[0][0]): 
                cluster = almacenamiento[0][1] + 1
                almacenamiento.pop(0)
            #Se puede almacenar el archivo
            else: 
                return cluster * tam_cluster
        #Se puede almacenar el archivo despues de los demas
        if len(almacenamiento) == 0 and (cluster + cluster_necesarios) < 720:
            return cluster * tam_cluster
        else:
            return False 
            
    return False

def mostrar_menu():
    root = tk.Tk()
    root.title("Sistema de Archivos FIUNAMFS")
    root.geometry("400x400")

    # Crear botones para cada operación
    btn_listar_contenidos = tk.Button(root, text="Listar contenidos", command=listar_contenidos)
    btn_listar_contenidos.pack(pady=10)

    btn_copiar_a_fiunamfs = tk.Button(root, text="Copiar archivo del sistema a FIUNAMFS", command=copiar_archivo_a_FiUnamFs)
    btn_copiar_a_fiunamfs.pack(pady=10)

    btn_copiar_a_sistema = tk.Button(root, text="Copiar archivo de FIUNAMFS al sistema", command=copiar_archivo_a_sistema)
    btn_copiar_a_sistema.pack(pady=10)

    btn_eliminar_archivo = tk.Button(root, text="Eliminar archivo de FIUNAMFS", command=eliminar_archivo)
    btn_eliminar_archivo.pack(pady=10)

    btn_salir = tk.Button(root, text="Salir", command=root.quit)
    btn_salir.pack(pady=10)

    root.mainloop()

guardar_info_archivos()
mostrar_menu()