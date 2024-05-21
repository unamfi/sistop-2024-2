import os
import struct
import datetime
from threading import Thread, Barrier
from tkinter import Tk, Label, Button, Entry, Text, messagebox, filedialog, END
from prettytable import PrettyTable

# Variables globales
directorio_fisico = "" # Directorio físico actual
ruta_FiUnamFS = "" # Ruta del archivo FiUnamFS
etiqueta_volumen = "" # Etiqueta del volumen 
tamano_cluster_bytes = 0 # Tamaño del clúster en bytes
num_clusters_dir = 0 # Número de clústeres del directorio
num_clusters_total = 0 # Número total de clústeres
directorio = [] # Lista para almacenar información del directorio
cluster_set = set() # Conjunto de clústeres disponibles
menu = 0 # Variable de menú (sin uso en el código)
# Barrera para sincronizar hilos 
barrier = Barrier(3)
cluster_ini = -1  # Clúster inicial 
tam_bytes = 0 # Tamaño en bytes del archivo
rvtb = False  # Resultado de verificación de tamaño
rbat = False # Resultado de verificación de archivo

#Clase para almacenar la información de un archivo en FiUnamFS.
    
class InfoArchivo: 
    def __init__(self, nombre_archivo, tam_bytes, cluster_ini, creacion, modificacion, pos):
        self.nombre_archivo = nombre_archivo
        self.tam_bytes = tam_bytes
        self.cluster_ini = cluster_ini
        self.creacion = creacion
        self.modificacion = modificacion
        self.pos = pos

#Obtiene la ruta del archivo FiUnamFS.
def obtener_FiUnamFS():
    global directorio_fisico, ruta_FiUnamFS
    directorio_fisico = os.path.dirname(os.path.abspath(__file__))
    ruta_FiUnamFS = os.path.join(directorio_fisico, "fiunamfs.img")
    if not os.path.exists(ruta_FiUnamFS):
        ruta_FiUnamFS = filedialog.askopenfilename(title="Seleccione el archivo FiUnamFS")
        if not ruta_FiUnamFS:
            return False
    return True

#Lee un número entero de 4 bytes desde una posición específica en #el archivo.
def leer_numero(file, posicion):
    file.seek(posicion)
    return struct.unpack('<I', file.read(4))[0]
#Escribe un número entero de 4 bytes en una posición específica #en el archivo.
def escribir_numero(file, posicion, numero):
    file.seek(posicion)
    file.write(struct.pack('<I', numero))
#Lee una cadena ASCII desde una posición específica en el #archivo.


def leer_ascii(file, posicion, longitud, encoding='latin-1'):
    file.seek(posicion)
    return file.read(longitud).decode(encoding)
#Escribe una cadena ASCII en una posición específica en el #archivo.
def escribir_ascii(file, posicion, cadena, encoding='latin-1'):
    file.seek(posicion)
    file.write(bytearray(cadena, encoding))
#Valida el archivo FiUnamFS asegurándose de que tiene el tamaño #correcto y la estructura adecuada.
def validar_FiUnamFS():
    global etiqueta_volumen, tamano_cluster_bytes, num_clusters_dir, num_clusters_total
    if os.path.getsize(ruta_FiUnamFS) != 1440*1024:
        messagebox.showerror("Error", "El archivo no tiene el tamaÃ±o correcto. El tamaÃ±o debe ser de 1440 Kilobytes.")
        return False
    with open(ruta_FiUnamFS, "rb") as f:
        nombre_FiUnamFS = leer_ascii(f, 0, 8)
        if nombre_FiUnamFS != "FiUnamFS":
            messagebox.showerror("Error", "El nombre del sistema de archivos no es correcto.")
            return False
        version_FiUnamFS = leer_ascii(f, 10, 4)
        if version_FiUnamFS != "24-2":
            messagebox.showerror("Error", "La versiÃ³n de la implementaciÃ³n no es correcta.")
            return False
        etiqueta_volumen = leer_ascii(f, 20, 19, encoding='ascii')
        tamano_cluster_bytes = leer_numero(f, 40)
        num_clusters_dir = leer_numero(f, 45)
        num_clusters_total = leer_numero(f, 50)
    messagebox.showinfo("Ã‰xito", "Sistema de archivos FiUnamFS cargado exitosamente.")
    return True
#Formatea una fecha en el formato YYYYMMDDHHMMSS.
def formato_fecha(fecha):
    return fecha.strftime("%Y%m%d%H%M%S")
#Imprime una fecha en el formato YYYY-MM-DD HH:MM:SS.
def imprimir_fecha(fecha):
    return f"{fecha[:4]}-{fecha[4:6]}-{fecha[6:8]} {fecha[8:10]}:{fecha[10:12]}:{fecha[12:14]}"
#Imprime la información de los archivos en una tabla.
def print_info_archivos():
    global directorio
    table = PrettyTable()
    table.field_names = ["Nombre", "TamaÃ±o (bytes)", "Cluster inicial", "Fecha de creaciÃ³n", "Fecha de modificaciÃ³n"]
    for archivo in directorio:
        table.add_row([archivo.nombre_archivo, archivo.tam_bytes, archivo.cluster_ini, imprimir_fecha(archivo.creacion), imprimir_fecha(archivo.modificacion)])
    return table
#Lee el directorio del sistema de archivos FiUnamFS.
def leer_directorio(show=True):
    global directorio, cluster_set
    cluster_set = set(range(num_clusters_dir + 1, num_clusters_total))
    directorio = []
    with open(ruta_FiUnamFS, "rb") as f:
        for i in range(tamano_cluster_bytes, tamano_cluster_bytes * (num_clusters_dir + 1), 64):
            tipo_archivo = leer_ascii(f, i, 1)
            if tipo_archivo == "-":
                nombre_archivo = leer_ascii(f, i + 1, 15, encoding='ascii').replace("#", "")
                dot = nombre_archivo.find(".")
                nombre_archivo = nombre_archivo[:dot] + "." + nombre_archivo[dot+1:dot+4]
                tam_bytes = leer_numero(f, i + 16)
                cluster_ini = leer_numero(f, i + 20)
                creacion = leer_ascii(f, i + 24, 14)
                modificacion = leer_ascii(f, i + 38, 14)
                archivo = InfoArchivo(nombre_archivo, tam_bytes, cluster_ini, creacion, modificacion, i)
                directorio.append(archivo)
                for j in range(cluster_ini, cluster_ini + ((tam_bytes + tamano_cluster_bytes - 1) // tamano_cluster_bytes)):
                    cluster_set.discard(j)
    if show:
        info_table = print_info_archivos()
        text_info.delete(1.0, END)
        text_info.insert(END, info_table)
#Busca un archivo por su nombre en el directorio.
def buscar_archivo(nombre_archivo):
    global directorio
    return next((archivo for archivo in directorio if archivo.nombre_archivo == nombre_archivo), None)
#Copia un archivo desde el sistema de archivos FiUnamFS al #sistema de archivos local.
def fiunamfs_to_local():
    nombre_archivo = entry_nombre_archivo.get()
    archivo = buscar_archivo(nombre_archivo)
    if archivo is None:
        messagebox.showerror("Error", "El archivo no existe.")
        return
    ruta_local = filedialog.asksaveasfilename(defaultextension="", title="Guardar archivo como")
    if not ruta_local:
        return
    try:
        with open(ruta_FiUnamFS, "rb") as f:
            f.seek(archivo.cluster_ini * tamano_cluster_bytes)
            info = f.read(archivo.tam_bytes)
        with open(ruta_local, "wb") as f_local:
            f_local.write(info)
        messagebox.showinfo("Ã‰xito", "Archivo copiado exitosamente.")
    except PermissionError:
        messagebox.showerror("Error", "No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
#Encuentra un espacio contiguo en el sistema de archivos para #almacenar un archivo.
def encontrar_contiguo(tam_bytes):
    global cluster_set
    contiguo = -1
    contiguo_actual = 0
    clusters_necesarios = (tam_bytes + tamano_cluster_bytes - 1) // tamano_cluster_bytes
    for cluster in cluster_set:
        contiguo_actual += 1
        if contiguo_actual == clusters_necesarios:
            contiguo = cluster - contiguo_actual + 1
            break
    return contiguo
#Verifica si el tamaño del archivo es adecuado para ser #almacenado en el sistema de archivos FiUnamFS.
def verify_tam_bytes(ruta_local):
    global cluster_ini, tam_bytes, rvtb
    tam_bytes = os.path.getsize(ruta_local)
    if tam_bytes > tamano_cluster_bytes * len(cluster_set):
        root.after(0, lambda: messagebox.showerror("Error", "El archivo es demasiado grande para ser almacenado en el sistema de archivos FiUnamFS."))
        rvtb = False
    else:
        cluster_ini = encontrar_contiguo(tam_bytes)
        if cluster_ini == -1:
            root.after(0, lambda: messagebox.showerror("Error", "No hay suficiente espacio contiguo en el sistema de archivos FiUnamFS."))
            rvtb = False
        else:
            rvtb = True
    barrier.wait()
#Hilo para buscar un archivo en el directorio.
def buscar_archivo_thread(nombre_archivo):
    global rbat
    archivo = buscar_archivo(nombre_archivo)
    if archivo is not None:
        root.after(0, lambda: messagebox.showerror("Error", "Ya existe un archivo con ese nombre."))
        rbat = False
    else:
        rbat = True
    barrier.wait()
#Copia un archivo desde el sistema de archivos local al sistema #de archivos FiUnamFS.
def local_to_fiunamfs():
    ruta_local = filedialog.askopenfilename(title="Seleccione el archivo a copiar")
    if not ruta_local:
        return
    nombre_archivo = entry_nombre_archivo.get()
    if not nombre_archivo:
        messagebox.showerror("Error", "Debe ingresar un nombre para el archivo en FiUnamFS.")
        return
    verify_thread = Thread(target=verify_tam_bytes, args=(ruta_local,))
    buscar_thread = Thread(target=buscar_archivo_thread, args=(nombre_archivo,))
    verify_thread.start()
    buscar_thread.start()
    barrier.wait()
    if not rvtb or not rbat:
        return
    try:
        with open(ruta_FiUnamFS, "r+b") as f:
            f.seek(cluster_ini * tamano_cluster_bytes)
            with open(ruta_local, "rb") as f_local:
                info = f_local.read()
                f.write(info)
            for i in range(cluster_ini, cluster_ini + ((tam_bytes + tamano_cluster_bytes - 1) // tamano_cluster_bytes)):
                cluster_set.discard(i)
            creacion = formato_fecha(datetime.datetime.fromtimestamp(os.path.getctime(ruta_local)))
            modificacion = formato_fecha(datetime.datetime.fromtimestamp(os.path.getctime(ruta_local)))
            for i in range(tamano_cluster_bytes, tamano_cluster_bytes * (num_clusters_dir + 1), 64):
                tipo_archivo = leer_ascii(f, i, 1)
                if tipo_archivo == "/":
                    escribir_ascii(f, i, "-")
                    escribir_ascii(f, i + 1, nombre_archivo, encoding='ascii')
                    escribir_numero(f, i + 16, tam_bytes)
                    escribir_numero(f, i + 20, cluster_ini)
                    escribir_ascii(f, i + 24, creacion)
                    escribir_ascii(f, i + 38, modificacion)
                    break
        leer_directorio(False)
        messagebox.showinfo("Ã‰xito", "Archivo copiado exitosamente.")
    except PermissionError:
        messagebox.showerror("Error", "No se tienen los permisos necesarios para acceder al archivo o directorio especificado.")
#Elimina un archivo del sistema de archivos FiUnamFS.
def eliminar_archivo():
    nombre_archivo = entry_nombre_archivo.get()
    archivo = buscar_archivo(nombre_archivo)
    if archivo is None:
        messagebox.showerror("Error", "El archivo no existe.")
        return
    with open(ruta_FiUnamFS, "r+b") as f:
        escribir_ascii(f, archivo.pos, "/")
        escribir_ascii(f, archivo.pos + 1, "###############", encoding='ascii')
    leer_directorio(False)
    messagebox.showinfo("Ã‰xito", "Archivo eliminado exitosamente.")
# Función principal que inicializa la interfaz gráfica y carga el #sistema de archivos FiUnamFS.
def main():
    global text_info, entry_nombre_archivo, root
    if not obtener_FiUnamFS():
        return
    if not validar_FiUnamFS():
        return

    root = Tk()
    root.title("Sistema de archivos FiUnamFS")

    Label(root, text="Nombre del archivo:").grid(row=0, column=0, padx=10, pady=10)
    entry_nombre_archivo = Entry(root)
    entry_nombre_archivo.grid(row=0, column=1, padx=10, pady=10)

    Button(root, text="Listar directorio", command=leer_directorio).grid(row=1, column=0, padx=10, pady=10)
    Button(root, text="Copiar a local", command=fiunamfs_to_local).grid(row=1, column=1, padx=10, pady=10)
    Button(root, text="Copiar a FiUnamFS", command=local_to_fiunamfs).grid(row=1, column=2, padx=10, pady=10)
    Button(root, text="Eliminar archivo", command=eliminar_archivo).grid(row=1, column=3, padx=10, pady=10)

    text_info = Text(root, wrap='none', width=80, height=20)
    text_info.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
