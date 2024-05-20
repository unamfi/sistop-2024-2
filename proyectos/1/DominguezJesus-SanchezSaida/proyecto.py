import os
import struct
from struct import *
import threading

# Abrir el archivo
img_FS = "fiunamfs.img"
FS = open(img_FS, "r+b")

def info_sistema():
    #Se muestran los datos del superbloque
    FS.seek(0)
    nombre_FS = FS.read(8).decode('ascii')
    FS.seek(10)
    version = FS.read(10).decode('ascii')
    etiqueta_volumen = FS.read(20).decode('ascii')
    totalsuperbloque = FS.read(54)
    FS.seek(40)
    tamaño_cluster = unpack("<I", FS.read(4))[0]
    FS.seek(45)
    num_cluster_dir = unpack("<I", FS.read(4))[0]
    FS.seek(50)
    num_cluster_uni = unpack("<I", FS.read(4))[0]

    print("Nombre del sistema de archivos: ",nombre_FS,"\n",
      "Version: ",version,"\n",
      "Etiqueta del Volumen: ",etiqueta_volumen, "\n",
      "Tamaño del cluster: ",tamaño_cluster, "bytes", "\n",
      "Numero de cluster que mide el directorio: ",num_cluster_dir, "\n",
      "Numero de cluster que mide la unidad completa: ",num_cluster_uni)

# Inicializar variables globales
#"" son para modificar a lo largo del proyecto
tamanoClusters = 0
num_cluster_dir = 0
num_cluster_uni = 0
tamanoDirectorio = 0
id_FS = ""
version = ""
etiqueta = ""

# Lista de archivos del directorio
archivos = []
# Lock para acceso seguro a la lista de archivos
archivo_lock = threading.Lock()  

class archivo:
    def __init__(self, nombre, tamano, clusterInicial):
        self.nombre = nombre
        self.tamano = tamano
        self.clusterInicial = clusterInicial

# Estructura para la tabla de asignación de archivos
class tablas:
    def __init__(self):
        self.tabla = {}
        # Lock para acceso seguro a la tabla
        self.lock = threading.Lock() 

    def agregar_archivo(self, nombre_archivo, cluster_inicial, tamano):
        with self.lock:
            self.tabla[nombre_archivo] = {'cluster_inicial': cluster_inicial, 'tamano': tamano}

    def eliminar_archivo(self, nombre_archivo):
        with self.lock:
            if nombre_archivo in self.tabla:
                del self.tabla[nombre_archivo]

    def obtener_archivo(self, nombre_archivo):
        with self.lock:
            return self.tabla.get(nombre_archivo)

    def mostrar_tabla(self):
        with self.lock:
            for nombre, detalles in self.tabla.items():
                print(f"Archivo: {nombre}, Cluster Inicial: {detalles['cluster_inicial']}, Tamaño: {detalles['tamano']} bytes")

tabla_asignacion = tablas()

# Función para leer los datos del archivo enteros
def leerDatos(inicio, tamano):
    global FS
    FS.seek(inicio)
    return FS.read(tamano)

# Función para leer los datos ASCII del FS
def leerASCII(inicio, tamano):
    global FS
    FS.seek(inicio)
    datos = FS.read(tamano)
    return datos.decode("ascii")

# Para convertir los datos de ASCII
def datoUnpack(inicio, tamano):
    global FS
    FS.seek(inicio)
    dato = FS.read(tamano)
    return struct.unpack('<i', dato)[0]

# Para escribir datos al sistema de archivos
def datosPack(inicio, dato):
    global FS
    FS.seek(inicio)
    dato = struct.pack('<i', dato)
    return FS.write(dato)

# Función para leer los datos del archivo en ASCII
def leerArchivo(posicion):
    inicio = 1024 + (posicion * 64)
    nombre = leerASCII(inicio + 1, 14)
    if nombre.strip('.') != "":
        tamano = datoUnpack(inicio + 16, 4)
        clusterInicial = datoUnpack(inicio + 20, 4)
        return archivo(nombre, tamano, clusterInicial)
    return None

# Para escribir datos ASCII al sistema de archivos
def escribirDatosASCII(inicio, dato):
    global FS
    FS.seek(inicio)
    dato = dato.encode("ascii")
    return FS.write(dato)

# Función para agregar un archivo al directorio
def agregar(nuevoArchivo):
    global FS
    global tamanoClusters
    global tamanoDirectorio

    with archivo_lock:
        # Buscar una entrada libre en el directorio
        entradaLibre = -1
        for i in range(tamanoDirectorio // 64):
            FS.seek(1024 + i * 64)
            if FS.read(1) == b'\x00':
                entradaLibre = i
                break
        if entradaLibre == -1:
            print("No hay espacio en el directorio para agregar el archivo.")
            return False
        else:
            # Escribir los datos del nuevo archivo en la entrada libre
            inicio = 1024 + entradaLibre * 64
            escribirDatosASCII(inicio + 1, nuevoArchivo.nombre)
            datosPack(inicio + 16, nuevoArchivo.tamano)
            datosPack(inicio + 20, nuevoArchivo.clusterInicial)
            return True

# Enlistar los archivos del directorio
def listarArchivos():
    global FS, tamanoClusters
    with archivo_lock:
        infoArchivo = []
        for i in range(64):
            tam = 1024 + (i * 64)
            FS.seek(tam)
            lectura = FS.read(15)
            if lectura != b'/##############':
                FS.seek(tam + 0)
                print("Tipo de archivo: ", FS.read(1).decode().strip())

                FS.seek(tam + 1)
                print("Archivo: ", FS.read(15).decode().strip())

                FS.seek(tam + 24)
                Hora_Fecha = FS.read(14).decode().strip()
                print("Fecha de creación del archivo: ", Hora_Fecha[0:4], "-", Hora_Fecha[4:6], "-", Hora_Fecha[6:8], " ", Hora_Fecha[8:10], ":", Hora_Fecha[10:12], ":", Hora_Fecha[12:14])

                FS.seek(tam + 38)
                Hora_Fecha = FS.read(14).decode().strip()
                print("Fecha de modificación del archivo: ", Hora_Fecha[0:4], "-", Hora_Fecha[4:6], "-", Hora_Fecha[6:8], " ", Hora_Fecha[8:10], ":", Hora_Fecha[10:12], ":", Hora_Fecha[12:14])
                print("\n")

# Enlistar los archivos del directorio y agregarlos al arreglo
def listarEnDirectorio():
    global tamanoClusters, num_cluster_dir, tamanoDirectorio, archivos

    with archivo_lock:
        archivos = []

        print("   Nombre archivo\t\tTamaño   ")
        for i in range(int((tamanoClusters * num_cluster_dir) / tamanoDirectorio)):
            aux = leerArchivo(i)
            if aux and aux.tamano != 0:
                print(f"   {aux.nombre}\t{aux.tamano} bytes")
                archivos.append(aux)

# Verificamos si el archivo existe en nuestro directorio
def verificarArchivo(nombreCopia):
    global archivos
    with archivo_lock:
        for i in archivos:
            if i.nombre.strip() == nombreCopia.strip():
                return archivos.index(i), True
        return -1, False

# Función para copiar un archivo del sistema de archivos a la computadora
def exportar(nombreCopia, rutaNueva):
    # Verificamos si el archivo que se quiere copiar existe en nuestro directorio
    indexArchivo, validacion = verificarArchivo(nombreCopia)
    if not validacion:
        print("El archivo no existe")
        return

    # Archivo que se quiere copiar
    archivoC = archivos[indexArchivo]

    print(f"Tamaño del archivo a copiar: {archivoC.tamano}")

    # Crear el archivo en la ruta especificada
    if os.path.exists(rutaNueva):
        if os.path.isfile(os.path.join(rutaNueva, nombreCopia)):
            rutaArchivoDestino = os.path.join(rutaNueva, "copia de " + nombreCopia)
        else:
            rutaArchivoDestino = os.path.join(rutaNueva, nombreCopia)

        with open(rutaArchivoDestino, "wb") as destino:
            inicio_lectura = archivoC.clusterInicial * tamanoClusters
            FS.seek(inicio_lectura)
            datos_archivo = FS.read(archivoC.tamano)
            destino.write(datos_archivo)

        print("Archivo copiado con éxito")
    else:
        print("La ruta especificada no existe")

# Función para copiar un archivo de la computadora al sistema de archivos
"""def importar(rutaArchivo):
    global FS, tabla_asignacion, archivos, tamanoClusters

    if not os.path.exists(rutaArchivo):
        print("El archivo no existe.")
        return

    nombreArchivo = os.path.basename(rutaArchivo)

    # validar si el archivo ya existe en el sistema de archivos
    if verificarArchivo(nombreArchivo)[1]:
        print("El archivo ya existe en el sistema de archivos.")
        return

    tamanoArchivo = os.path.getsize(rutaArchivo)
    espacioDisponible = verEspacioDisponible(tamanoArchivo)
    print(f"Espacio disponible: {espacioDisponible}")

    if espacioDisponible == -1:
        print("No hay suficiente espacio en el sistema de archivos para copiar el archivo.")
        return

    with open(rutaArchivo, "rb") as archivoComputadora:
        contenido = archivoComputadora.read()

        # Escribir en el espacio disponible encontrado
        inicio_escritura = espacioDisponible
        print("Inicio escritura: ", inicio_escritura)
        FS.seek(inicio_escritura)
        FS.write(contenido)

    nuevoArchivo = archivo(nombreArchivo, tamanoArchivo, espacioDisponible)
    print("Nombre del archivo: ", nuevoArchivo.nombre)
    with archivo_lock:
        archivos.append(nuevoArchivo)
        agregar(nuevoArchivo)
    print("Archivo copiado con éxito al sistema de archivos")

def verEspacioDisponible(tamanoArchivo):
    global FS, archivos, tamanoClusters, num_cluster_dir

    with archivo_lock:
        # Conjunto de todos los clusters ocupados por archivos existentes
        clustersOcupados = set()

        # Tenemos que calcular los clusters ocupados en el estado actual
        for archivo in archivos:
            clusters = [archivo.clusterInicial + i for i in range((archivo.tamano + tamanoClusters - 1) // tamanoClusters)]
            clustersOcupados.update(clusters)

        # Busca un espacio libre
        espacioLibre = -1
        i = 0
        while i < num_cluster_dir:
            if i not in clustersOcupados and i * tamanoClusters > 54:  # Excluye los primeros 54 bytes
                inicio = i * tamanoClusters
                FS.seek(inicio)
                # Verifica si el espacio libre encontrado es suficiente para el archivo que se va a escribir
                if (i + (tamanoArchivo + tamanoClusters - 1) // tamanoClusters) < num_cluster_dir:
                    return i  # Devuelve el índice del espacio libre encontrado
            i += 1
        return -1  # Si no se encuentra ningún espacio libre, devuelve -1"""

# Función para copiar un archivo de la computadora al sistema de archivos
def importar(rutaArchivo):
    global tabla_asignacion
    global archivos
    global tamanoClusters
    global FS

    if not os.path.exists(rutaArchivo):
        print("El archivo no existe.")
        return

    # Obtener el nombre del archivo
    nombreArchivo = os.path.basename(rutaArchivo)
    
    #validar si el archivo ya existe en el sistema de archivos
    if verificarArchivo(nombreArchivo)[1]:
        print("El archivo ya existe en el sistema de archivos.")
        return

    # Obtener el tamaño del archivo
    tamanoArchivo = os.path.getsize(rutaArchivo)
    espacioDisponible = encontrarEspacioDisponible(tamanoArchivo)
    print(f"Espacio disponible: {espacioDisponible}")

    if espacioDisponible == -1:
        print("No hay suficiente espacio en el sistema de archivos para copiar el archivo.")
        return

    with open(rutaArchivo, "rb") as archivoComputadora:
        contenido = archivoComputadora.read()

        # Escribir en el espacio disponible encontrado
        inicio_escritura = espacioDisponible 
        print("Inicio escritura: ", inicio_escritura)
        FS.seek(inicio_escritura)
        FS.write(contenido)

    nuevoArchivo = archivo(nombreArchivo, tamanoArchivo, espacioDisponible)
    print("Nombre del archivo: ", nuevoArchivo.nombre)
    archivos.append(nuevoArchivo)
    agregar(nuevoArchivo)
    print("Archivo copiado con éxito al sistema de archivos")

def encontrarEspacioDisponible(tamanoArchivo):
    global archivos
    global tamanoClusters
    global num_cluster_dir
    global FS

    # Conjunto de todos los clusters ocupados por archivos existentes
    clustersOcupados = set()

    for archivo in archivos:
        # Calcula todos los clusters ocupados por el archivo actual
        clusters = [archivo.clusterInicial + i for i in range((archivo.tamano + tamanoClusters - 1) // tamanoClusters)]
        clustersOcupados.update(clusters)

    # Busca un espacio libre
    espacioLibre = -1
    i = 0
    while i < num_cluster_dir:
        if i not in clustersOcupados and i * tamanoClusters > 54:  # Excluye los primeros 54 bytes
            inicio = i * tamanoClusters
            FS.seek(inicio)
            # Verifica si el espacio libre encontrado es suficiente para el archivo que se va a escribir
            if (i + (tamanoArchivo + tamanoClusters - 1) // tamanoClusters) < num_cluster_dir:
                return i  # Devuelve el índice del espacio libre encontrado
        i += 1
    return -1  # Si no se encuentra ningún espacio libre, devuelve -1

def datos():
    global id_FS
    global version
    global etiqueta
    global tamanoClusters
    global num_cluster_dir
    global num_cluster_uni
    global tamanoDirectorio

    # Identificación del sistema de archivos por defecto
    id_FS = leerASCII(0, 8)

    # Versión de la implementación
    version = leerASCII(10, 4)

    # Etiqueta del volumen
    etiqueta = leerASCII(20, 19)

    # Tamaño de un cluster
    tamanoClusters = datoUnpack(40, 4)

    # Número de clusters que mide el directorio
    num_cluster_dir = datoUnpack(45, 4)

    # Número de clusters que mide la unidad completa
    num_cluster_uni = datoUnpack(50, 4)

    # Tamaño del directorio por defecto
    tamanoDirectorio = 64

def eliminar(nombreArchivo):
    global archivos
    global tamanoClusters
    global FS

    # Verificamos si el archivo que se quiere borrar existe en nuestro directorio
    indexArchivo, validacion = verificarArchivo(nombreArchivo)
    if validacion != True:
        print("El archivo no existe")
        return

    # Archivo que se quiere borrar
    archivoBorrar = archivos[indexArchivo]

    # Eliminamos el archivo del directorio
    archivos.pop(indexArchivo)

    # Marcar la entrada en el directorio como eliminada
    FS.seek(1024 + indexArchivo * 64)
    FS.write(b'\x00')

    # Marcamos los clusters correspondientes como libres
    FS.seek(archivoBorrar.clusterInicial * tamanoClusters)
    FS.write(b'\x00' * archivoBorrar.tamano)

    # Recargar la lista de archivos del directorio
    archivos = []
    listarEnDirectorio()

    print("Archivo eliminado con éxito") 

def menu():
    while True:
        print("\n1. Listar el contenido del directorio")
        print("2. Copiar archivo del sistema a la computadora")
        print("3. Copiar archivo de la computadora al sistema")
        print("4. Borrar archivo del sistema")
        print("5. Salir")
        try:
            opcion = int(input("Ingresa una opción: "))
            if opcion == 1:
                listarArchivos()
            elif opcion == 2:
                listarEnDirectorio()
                nombreCopia = input("Ingresa el nombre del archivo que deseas copiar (incluye la extensión): ")
                rutaCopiar = os.path.dirname(os.path.abspath(__file__))
                threading.Thread(target=exportar, args=(nombreCopia, rutaCopiar)).start()
            elif opcion == 3:
                rutaArchivo = input("Ingresa la ruta de donde deseas copiar el archivo (incluye el archivo con su extensión): ").replace("\\", "/")
                threading.Thread(target=importar, args=(rutaArchivo,)).start()
            elif opcion == 4:
                listarEnDirectorio()
                nombreArchivo = input("Ingresa el nombre del archivo que deseas borrar (incluye la extensión): ")
                #threading.Thread(target=eliminar, args=(nombreArchivo,)).start()
                threading.Thread(target=eliminar, args=(nombreArchivo,)).start()
            elif opcion == 5:
                break
            else:
                print("Opción inválida")
        except ValueError:
            print("Por favor, ingrese un número válido")


datos()
info_sistema()
menu()
