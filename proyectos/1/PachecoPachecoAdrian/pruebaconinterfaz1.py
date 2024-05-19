#VERISON PRUEBA FINAL PROYECTO 1 
#SEMESTRE 2024-2
#ALUMNO:PACHECO PACHECO ADRIAN ALEJANDRO

import struct
import math
import os
import time
import threading
import queue
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Objeto usado para almacenar la informacion de los registros del directorio
class Registros:
    def __init__(self, tipo, nombre, tamano, cluster_inicial, creacion, modificacion, espacio_libre, registro):
        self.tipo = tipo
        self.nombre = nombre
        self.tamano = tamano
        self.cluster_inicial = cluster_inicial
        self.creacion = creacion
        self.modificacion = modificacion
        self.espacio_libre = espacio_libre
        self.registro = registro

sector = 512
cluster = sector * 4  # Cada cluster es de 4 sectores (2048 bytes)
lista_directorios = []

lock = threading.Lock()
event = threading.Event()
message_queue = queue.Queue()

# Configurar la ventana de tkinter
root = tk.Tk()
root.title("Monitor de Sistema de Archivos")
root.configure(bg="pink")

text_widget = ScrolledText(root, state=tk.DISABLED, bg="lightpink")
text_widget.pack(fill=tk.BOTH, expand=True)

def log_message(message):
    message_queue.put(message)

def process_queue():
    while not message_queue.empty():
        message = message_queue.get()
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, message + "\n")
        text_widget.see(tk.END)
        text_widget.config(state=tk.DISABLED)
    root.after(100, process_queue)

# Extrae el superbloque
def extraer_superbloque():
    global num_cluster_bytes
    global num_cluster_directorio
    global num_cluster_total
    with open('fiunamfs.img', 'rb') as archivo:
        entrada = 0
        while entrada < 64:
            if entrada == 0:
                contenido = archivo.read(8)
                nombre_sistema_archivos = contenido.decode('ascii').strip()
                if nombre_sistema_archivos == 'FiUnamFS':
                    log_message("Nombre de sistema de archivos: " + nombre_sistema_archivos)
                else:
                    log_message("Error de sistema de archivos")
                    return
                entrada += 8
            elif entrada == 10:
                contenido = archivo.read(4)
                version = contenido.decode('ascii').strip()
                if version == '24-2':
                    log_message("Version: " + version)
                else:
                    log_message("Error de version")
                    return
                entrada += 4
            elif entrada == 20:
                contenido = archivo.read(15)
                etiqueta = contenido.decode('ascii').strip()
                log_message("Etiqueta del volumen: " + etiqueta)
                entrada += 15
            elif entrada == 40:
                contenido = archivo.read(4)
                num_cluster_bytes = struct.unpack('<I', contenido)[0]
                log_message("Tamano del cluster en bytes: " + str(num_cluster_bytes))
                entrada += 4
            elif entrada == 45:
                contenido = archivo.read(4)
                num_cluster_directorio = struct.unpack('<I', contenido)[0]
                log_message("Numero de clusters del directorio: " + str(num_cluster_directorio))
                entrada += 4
            elif entrada == 50:
                contenido = archivo.read(4)
                num_cluster_total = struct.unpack('<I', contenido)[0]
                log_message("Numero de clusters de la unidad: " + str(num_cluster_total))
                entrada += 4
            else:
                archivo.read(1)
                entrada += 1
    log_message("Fin")

# Checa el contenido del directorio, si es un directorio activo, lo guarda en la lista recibida
def leer_directorio(entrada, lista_directorios):
    contador = 0
    with open('fiunamfs.img', 'rb') as archivo:
        inicio = (cluster * 1) + (64 * entrada)
        archivo.seek(inicio)
        while contador < 64:
            if contador == 0:
                contenido = archivo.read(1)
                tipo_archivo = int.from_bytes(contenido, byteorder='little')
                if tipo_archivo == 45:
                    lista_directorios.append(entrada)
                contador += 1
            elif contador == 1:
                archivo.read(15)
                contador += 15
            elif contador == 16:
                archivo.read(4)
                contador += 4
            elif contador == 20:
                archivo.read(3)
                contador += 3
            elif contador == 24:
                archivo.read(13)
                contador += 13
            elif contador == 38:
                archivo.read(13)
                contador += 13
            elif contador == 52:
                archivo.read(12)
                contador += 12
            else:
                archivo.read(1)
                contador += 1

# Crea objetos de los registros en la lista que pases
def llenar_directorio(entrada, lista_directorios):
    tipo_archivo = 0
    nombre_archivo = ""
    tamano_bytes = 0
    cluster_inicial = 0
    creacion = ""
    modificacion = ""
    espacio_libre = b""

    contador = 0
    with open('fiunamfs.img', 'rb') as archivo:
        inicio = (cluster * 1) + (64 * entrada)
        archivo.seek(inicio)
        while contador < 64:
            if contador == 0:
                contenido = archivo.read(1)
                tipo_archivo = int.from_bytes(contenido, byteorder='little')
                contador += 1
            elif contador == 1:
                nombre_archivo = archivo.read(15).decode('ascii').strip()
                contador += 15
            elif contador == 16:
                contenido = archivo.read(4)
                tamano_bytes = int.from_bytes(contenido, byteorder='little')
                contador += 4
            elif contador == 20:
                contenido = archivo.read(3)
                cluster_inicial = int.from_bytes(contenido, byteorder='little')
                contador += 3
            elif contador == 24:
                creacion = archivo.read(14).decode('ascii')
                contador += 14
            elif contador == 38:
                modificacion = archivo.read(13).decode('ascii')
                contador += 13
            elif contador == 52:
                espacio_libre = archivo.read(12)
                contador += 12
            else:
                archivo.read(1)
                contador += 1

        registro = Registros(tipo_archivo, nombre_archivo, tamano_bytes, cluster_inicial, creacion, modificacion, espacio_libre, entrada)
        lista_directorios.append(registro)

# Funcion que imprime los datos del registro ingresado
def imprimir_directorio(entrada):
    contador = 0
    log_message("\n")
    log_message("INFORMACION DEL REGISTRO")
    log_message("\n")
    with open('fiunamfs.img', 'rb') as archivo:
        inicio = (cluster * 1) + (64 * entrada)
        archivo.seek(inicio)
        while contador < 64:
            if contador == 0:
                contenido = archivo.read(1)
                log_message(str(contenido))
                contador += 1
            elif contador == 1:
                contenido = archivo.read(15)
                log_message(str(contenido))
                contador += 15
            elif contador == 16:
                contenido = archivo.read(4)
                log_message("Tamano del archivo:")
                log_message(str(contenido))
                log_message(str(int.from_bytes(contenido, byteorder='little')))
                contador += 4
            elif contador == 20:
                contenido = archivo.read(3)
                log_message("Cluster inicial:")
                log_message(str(contenido))
                log_message(str(int.from_bytes(contenido, byteorder='little')))
                contador += 3
            elif contador == 24:
                contenido = archivo.read(13)
                log_message("Fecha y hora de creacion:")
                log_message(str(contenido))
                contador += 13
            elif contador == 38:
                contenido = archivo.read(13)
                log_message("Fecha y hora de ultima modificacion:")
                log_message(str(contenido))
                contador += 13
            elif contador == 52:
                contenido = archivo.read(12)
                log_message("Espacio no utilizado:")
                log_message(str(contenido))
                contador += 12
            else:
                archivo.read(1)
                contador += 1
        log_message("\n")
        log_message("\n")

# Lista los directorios activos
def listar_directorios(lista_directorios):
    for i in range(128):
        leer_directorio(i, lista_directorios)
    log_message("Registros activos: ")
    log_message(str(lista_directorios))
    for j in lista_directorios:
        imprimir_directorio(j)

# Copia la informacion de un archivo del disco hacia un archivo externo
def copiar_archivo(directorio, archivo):
    lista_copia = []
    llenar_directorio(directorio, lista_copia)
    with open('fiunamfs.img', 'rb') as archivo_origen:
        inicio = (cluster * lista_copia[0].cluster_inicial)
        log_message("Copiando desde el cluster: " + str(lista_copia[0].cluster_inicial))
        archivo_origen.seek(inicio)
        # Leer el archivo en partes para evitar MemoryError
        with open(archivo, 'wb') as archivo_destino:
            tamano_restante = lista_copia[0].tamano
            while tamano_restante > 0:
                tamano_a_leer = min(tamano_restante, 1024*1024)  # Leer en partes de 1 MB
                bytes_leidos = archivo_origen.read(tamano_a_leer)
                if not bytes_leidos:
                    break
                archivo_destino.write(bytes_leidos)
                tamano_restante -= len(bytes_leidos)

# Funcion para eliminar registros del directorio
def eliminar_registro(registro):
    inicio = (cluster * 1) + (64 * registro)
    contador = 0
    with open('fiunamfs.img', 'rb') as archivo_origen:
        archivo_origen.seek(inicio)
        while contador < 1:
            contenido = archivo_origen.read(1)
            tipo_archivo = int.from_bytes(contenido, byteorder='little')
            if tipo_archivo == 45:
                log_message("Registro valido")
                with open('fiunamfs.img', 'r+b') as archivo_destino:
                    archivo_destino.seek(inicio)
                    archivo_destino.write(b'/')
            elif tipo_archivo == 47:
                log_message("Entrada vacia")
            else:
                log_message("Tipo de archivo desconocido")
            contador += 1

# Copia un archivo externo hacia el disco, agregandolo al directorio, y copiando su contenido de forma contigua.
def agregar_archivo_al_directorio(archivo_agregar):
    try:
        with open(archivo_agregar, 'rb') as archivo:
            nombre_completo_archivo = archivo.name
            if '.' in nombre_completo_archivo:
                extension = nombre_completo_archivo.split('.')[-1]
                nombre_archivo = archivo.name.split('.')[0]
            else:
                extension = "Sin extension"
            if len(nombre_archivo) < 16:
                fecha_creacion = os.path.getctime(nombre_completo_archivo)
                fecha = time.strftime("%Y%m%d%H%M%S", time.localtime(fecha_creacion))
                fecha_modificacion = os.path.getmtime(nombre_completo_archivo)
                fecha_ultima_modificacion = time.strftime("%Y%m%d%H%M%S", time.localtime(fecha_modificacion))
            
                lista_activos = []
                for i in range(128):
                    leer_directorio(i, lista_activos)

                lista_objetos = []
                for i in lista_activos:
                    llenar_directorio(i, lista_objetos)

                lista_ordenada = sorted(lista_objetos, key=lambda x: x.cluster_inicial)

                for i in range(128):
                    if i not in lista_activos:
                        nombre_bin = nombre_archivo.encode('us-ascii')
                        fecha_mod_bin = fecha_ultima_modificacion.encode('us-ascii')
                        fecha_crea_bin = fecha.encode('us-ascii')
                        
                        longitud_ultimo_archivo = ((lista_ordenada[-1].cluster_inicial) * cluster) + (lista_ordenada[-1].tamano)
                        cluster_siguiente = math.ceil(longitud_ultimo_archivo / cluster) + 1                  
                        cluster_inicial = cluster_siguiente.to_bytes(4, byteorder='little')
                        
                        tamano_archivo = os.path.getsize(archivo_agregar)
                        tamano_archivo_bin = tamano_archivo.to_bytes(4, byteorder='little')
                        
                        max_valor = (256 ** 4) - 1
                        if tamano_archivo <= max_valor:
                            archivo.seek(0)
                            contenido = archivo.read()
                            
                            with open('fiunamfs.img', 'r+b') as archivo_destino:
                                inicial = (cluster) + (64 * i)
                                archivo_destino.seek(inicial)
                                contador = 0
                                while contador < 64:
                                    if contador == 0:
                                        archivo_destino.write(b'-')
                                        contador += 1
                                    elif contador == 1:
                                        archivo_destino.write(nombre_bin)
                                        archivo_destino.seek(inicial + 16)
                                        contador += 15
                                    elif contador == 16:
                                        archivo_destino.write(tamano_archivo_bin)
                                        contador += 4
                                    elif contador == 20:
                                        archivo_destino.write(cluster_inicial)
                                        contador += 4
                                    elif contador == 24:
                                        archivo_destino.write(fecha_crea_bin)
                                        contador += 14
                                    elif contador == 38:
                                        archivo_destino.write(fecha_mod_bin)
                                        contador += 14
                                    else:
                                        archivo_destino.read(1)
                                        contador += 1
                                ubicacion_archivo = (cluster_siguiente * cluster)
                                archivo_destino.seek(ubicacion_archivo)
                                archivo_destino.write(contenido)
                        else:
                            log_message("Tamano invalido")
                        break
            else:
                log_message("Nombre demasiado largo")
    except FileNotFoundError:
        decision_excepcion()
    else:
        log_message('El archivo fue encontrado')

# Funcion para ingresar nombre del archivo del que se quiere copiar la informacion
def usuario_ingresa_archivo():
    archivo = input('Ingresa el nombre de tu archivo con extension: ')
    agregar_archivo_al_directorio(archivo)

# Funcion para imprimir error cuando suceda
def decision_excepcion():
    log_message('El archivo no ha sido encontrado dentro del directorio del programa')
    decision = input('¿Desea intentarlo de nuevo? (s/n) ')
    if decision.lower() == 's':
        usuario_ingresa_archivo()
    elif decision.lower() == 'n':
        log_message('Hasta luego')
    else:
        log_message('Input no valido')
        decision_excepcion()

# Hilos
def hilo_superbloque():
    log_message("\n[Hilo Superbloque] Leyendo el contenido del superbloque...\n")
    extraer_superbloque()

def hilo_directorios():
    log_message("\n[Hilo Directorios] Listando los directorios activos...\n")
    lista = []
    listar_directorios(lista)

# Crear los hilos
thread_superbloque = threading.Thread(target=hilo_superbloque)
thread_directorios = threading.Thread(target=hilo_directorios)

# Iniciar los hilos
thread_superbloque.start()
thread_directorios.start()

# Esperar a que los hilos terminen
thread_superbloque.join()
thread_directorios.join()

# Funcion que implementa un menu de seleccion de funciones
def menu():
    while True:
        log_message("INTERACTUE CON NUESTRO MENU DESDE LA TERMINAL!")
        log_message("1) Listar directorios activos")
        log_message("2) Copiar un archivo del disco")
        log_message("3) Insertar un archivo al disco")
        log_message("4) Eliminar un archivo del disco")
        log_message("5) Mostrar contenido de un directorio")
        log_message("6) Mostrar el contenido del superbloque")
        log_message("7) Salir")
        x = int(input("Seleccione una opcion: "))
        if x == 1:
            lista = []         
            listar_directorios(lista)
        elif x == 2:
            archivo2 = input("Ingresa el nombre del archivo completo donde quieres copiar la informacion: ")
            directorio2 = int(input("Ingresa el numero del directorio que deseas copiar: "))
            copiar_archivo(directorio2, archivo2)
        elif x == 3:
            usuario_ingresa_archivo()
        elif x == 4:
            directorio4 = int(input("Ingresa el numero del directorio que desea eliminar: "))
            eliminar_registro(directorio4)
        elif x == 5:
            directorio5 = int(input("Ingresa el numero del directorio: "))
            imprimir_directorio(directorio5)
        elif x == 6:
            extraer_superbloque()
        elif x == 7:
            root.quit()
            break

# Ejecutar el mainloop de tkinter
root.after(100, process_queue)
thread_menu = threading.Thread(target=menu)
thread_menu.start()
root.mainloop()
