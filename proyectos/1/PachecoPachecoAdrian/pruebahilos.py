import struct
import math
import os
import time

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
                    print("Nombre de sistema de archivos: " + nombre_sistema_archivos)
                else:
                    print("Error de sistema de archivos")
                    return
                entrada += 8
            elif entrada == 10:
                contenido = archivo.read(4)
                version = contenido.decode('ascii').strip()
                if version == '24-2':
                    print("Version: " + version)
                else:
                    print("Error de version")
                    return
                entrada += 4
            elif entrada == 20:
                contenido = archivo.read(15)
                etiqueta = contenido.decode('ascii').strip()
                print("Etiqueta del volumen: " + etiqueta)
                entrada += 15
            elif entrada == 40:
                contenido = archivo.read(4)
                num_cluster_bytes = struct.unpack('<I', contenido)[0]
                print("Tamano del cluster en bytes: " + str(num_cluster_bytes))
                entrada += 4
            elif entrada == 45:
                contenido = archivo.read(4)
                num_cluster_directorio = struct.unpack('<I', contenido)[0]
                print("Numero de clusters del directorio: " + str(num_cluster_directorio))
                entrada += 4
            elif entrada == 50:
                contenido = archivo.read(4)
                num_cluster_total = struct.unpack('<I', contenido)[0]
                print("Numero de clusters de la unidad: " + str(num_cluster_total))
                entrada += 4
            else:
                archivo.read(1)
                entrada += 1
    print("Fin")

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
    print("INFO")
    with open('fiunamfs.img', 'rb') as archivo:
        inicio = (cluster * 1) + (64 * entrada)
        archivo.seek(inicio)
        while contador < 64:
            if contador == 0:
                contenido = archivo.read(1)
                print(contenido)
                contador += 1
            elif contador == 1:
                contenido = archivo.read(15)
                print(contenido)
                contador += 15
            elif contador == 16:
                contenido = archivo.read(4)
                print("Tamano del archivo:")
                print(contenido)
                print(int.from_bytes(contenido, byteorder='little'))
                contador += 4
            elif contador == 20:
                contenido = archivo.read(3)
                print("Cluster inicial:")
                print(contenido)
                print(int.from_bytes(contenido, byteorder='little'))
                contador += 3
            elif contador == 24:
                contenido = archivo.read(13)
                print("Fecha y hora de creacion:")
                print(contenido)
                contador += 13
            elif contador == 38:
                contenido = archivo.read(13)
                print("Fecha y hora de ultima modificacion:")
                print(contenido)
                contador += 13
            elif contador == 52:
                contenido = archivo.read(12)
                print("Espacio no utilizado:")
                print(contenido)
                contador += 12
            else:
                archivo.read(1)
                contador += 1
        print("\n")

# Lista los directorios activos
def listar_directorios(lista_directorios):
    for i in range(128):
        leer_directorio(i, lista_directorios)
    print("Registros activos: ")
    print(lista_directorios)
    for j in lista_directorios:
        imprimir_directorio(j)

# Copia la informacion de un archivo del disco hacia un archivo externo
def copiar_archivo(directorio, archivo):
    lista_copia = []
    llenar_directorio(directorio, lista_copia)
    with open('fiunamfs.img', 'rb') as archivo_origen:
        inicio = (cluster * lista_copia[0].cluster_inicial)
        print("Copiando desde el cluster: " + str(lista_copia[0].cluster_inicial))
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
    with open('fiunamfs.img', 'rb') as archivo:
        archivo.seek(inicio)
        while contador < 1:
            contenido = archivo.read(1)
            tipo_archivo = int.from_bytes(contenido, byteorder='little')
            if tipo_archivo == 45:
                print("Registro valido")
                with open('fiunamfs.img', 'r+b') as archivo_modificable:
                    archivo_modificable.seek(inicio)
                    archivo_modificable.write(b'/')
            elif tipo_archivo == 47:
                print("Entrada vacia")
            else:
                print("Tipo de archivo desconocido")
            contador += 1

# Copia un archivo externo hacia el disco, agregandolo al directorio, y copiando su contenido de forma contigua.
def agregar_archivo_a_directorio(archivo_a_agregar):
    try:
        with open(archivo_a_agregar, 'rb') as archivo:
            nombre_archivo_completo = archivo.name
            if '.' in nombre_archivo_completo:
                extension = nombre_archivo_completo.split('.')[-1]
                nombre_archivo = archivo.name.split('.')[0]
            else:
                extension = "Sin extension"
            if len(nombre_archivo) < 16:
                fecha_creacion = os.path.getctime(nombre_archivo_completo)
                fecha = time.strftime("%Y%m%d%H%M%S", time.localtime(fecha_creacion))
                fecha_modificacion = os.path.getmtime(nombre_archivo_completo)
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
                        
                        tam_arch = os.path.getsize(archivo_a_agregar)
                        tam_arch_bin = tam_arch.to_bytes(4, byteorder='little')
                        
                        max_valor = (256 ** 4) - 1
                        if tam_arch <= max_valor:
                            archivo.seek(0)
                            contenido = archivo.read()
                            
                            with open('fiunamfs.img', 'r+b') as archivo_modificable:
                                inicio = (cluster) + (64 * i)
                                archivo_modificable.seek(inicio)
                                contador = 0
                                while contador < 64:
                                    if contador == 0:
                                        archivo_modificable.write(b'-')
                                        contador += 1
                                    elif contador == 1:
                                        archivo_modificable.write(nombre_bin)
                                        archivo_modificable.seek(inicio + 16)
                                        contador += 15
                                    elif contador == 16:
                                        archivo_modificable.write(tam_arch_bin)
                                        contador += 4
                                    elif contador == 20:
                                        archivo_modificable.write(cluster_inicial)
                                        contador += 4
                                    elif contador == 24:
                                        archivo_modificable.write(fecha_crea_bin)
                                        contador += 14
                                    elif contador == 38:
                                        archivo_modificable.write(fecha_mod_bin)
                                        contador += 14
                                    else:
                                        archivo_modificable.read(1)
                                        contador += 1
                                ubicacion_archivo = (cluster_siguiente * cluster)
                                archivo_modificable.seek(ubicacion_archivo)
                                archivo_modificable.write(contenido)
                        else:
                            print("Tamano invalido")
                        break
            else:
                print("Nombre demasiado largo")
    except FileNotFoundError:
        manejar_excepcion_archivo()
    else:
        print('Archivo encontrado')

# Funcion para ingresar nombre del archivo del que se quiere copiar la informacion
def ingresar_nombre_archivo():
    archivo = input('Ingresa el nombre de tu archivo con extension: ')
    agregar_archivo_a_directorio(archivo)

# Funcion para imprimir error cuando suceda
def manejar_excepcion_archivo():
    print('El archivo no se encuentra dentro del directorio del programa')
    decision = input('¿Desea intentarlo de nuevo? (y/n) ')
    if decision.lower() == 'y':
        ingresar_nombre_archivo()
    elif decision.lower() == 'n':
        print('Adios')
    else:
        print('Input invalido')
        manejar_excepcion_archivo()

# Funcion que implementa un menu de seleccion de funciones
def menu():
    while True:
        print("1) Listar directorios activos")
        print("2) Copiar un archivo del disco")
        print("3) Meter un archivo al disco")
        print("4) Eliminar un archivo del disco")
        print("5) Mostrar contenido de un directorio")
        print("6) Mostrar el contenido del superbloque")
        print("7) Salir")
        opcion = int(input("Seleccione una opcion: "))
        if opcion == 1:
            lista = []         
            listar_directorios(lista)
        elif opcion == 2:
            archivo_destino = input("Ingresa el nombre del archivo completo donde quieres copiar la informacion: ")
            directorio_origen = int(input("Ingresa el numero del directorio que deseas copiar: "))
            copiar_archivo(directorio_origen, archivo_destino)
        elif opcion == 3:
            ingresar_nombre_archivo()
        elif opcion == 4:
            directorio_eliminar = int(input("Ingresa el numero del directorio que desea eliminar: "))
            eliminar_registro(directorio_eliminar)
        elif opcion == 5:
            directorio_mostrar = int(input("Ingresa el numero del directorio: "))
            imprimir_directorio(directorio_mostrar)
        elif opcion == 6:
            extraer_superbloque()
        elif opcion == 7:
            break

menu()
