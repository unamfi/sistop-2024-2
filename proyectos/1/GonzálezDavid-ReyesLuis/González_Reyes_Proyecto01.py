import tkinter as tk  # Importa el módulo tkinter para crear interfaces gráficas
from tkinter import ttk  # Importa ttk de tkinter para usar widgets modernos
from tkinter import messagebox  # Importa messagebox de tkinter para mostrar mensajes emergentes
from tkinter import filedialog  # Importa filedialog de tkinter para abrir y guardar archivos
from tkinter import scrolledtext  # Importa scrolledtext de tkinter para crear cuadros de texto con desplazamiento
import threading  # Importa threading para trabajar con hilos
import struct  # Importa struct para manejar datos binarios
import os  # Importa os para interactuar con el sistema operativo

# Definiendo constantes a emplear
SUPERBLOQUE_SIZE = 64  # Tamaño del superbloque en bytes
ENTRADA_DIRECTORIO_SIZE = 64  # Tamaño de una entrada de directorio en bytes
NUM_SECTORES_ENTRADA_DIRECTORIO = 1  # Número de sectores por entrada de directorio
CLUSTER_SIZE = 512  # Tamaño de un cluster en bytes
NUM_SECTORES_POR_CLUSTER = 4  # Número de sectores por cluster
DIRECTORIO_CLUSTER_INICIAL = 1  # Cluster inicial del directorio
NUMERO_SECTORES_SUPERBLOQUE = 1  # Número de sectores del superbloque
NUMERO_SECTORES_ENTRADA_DIRECTORIO = 4  # Número de sectores por entrada de directorio
NUMERO_ENTRADAS_DIRECTORIO = 16  # Número de entradas de directorio
FIUNAMFS_SIGNATURE = b"FiUnamFS"  # Firma del sistema de archivos FiUnamFS
VERSION_IMPLEMENTACION = "24-2"  # Versión de implementación del sistema de archivos
NOMBRE_FIUNAMFS_IMG = "fiunamfs.img"  # Nombre de la imagen del sistema de archivos
NOMBRE_ARCHIVO_DIRECTORIO = "directorio"

# Definir estructuras de datos
class EntradaDirectorio:
    def __init__(self, tipo_archivo, nombre_archivo, tamano_archivo, cluster_inicial, fecha_creacion, fecha_modificacion):
        self.tipo_archivo = tipo_archivo
        self.nombre_archivo = nombre_archivo
        self.tamano_archivo = tamano_archivo
        self.cluster_inicial = cluster_inicial
        self.fecha_creacion = fecha_creacion
        self.fecha_modificacion = fecha_modificacion

    def to_bytes(self):
        # Convierte la entrada del directorio a bytes
        tipo_archivo_bytes = self.tipo_archivo.encode("ascii")
        nombre_archivo_bytes = self.nombre_archivo.encode("ascii").ljust(15, b"\0")
        tamano_archivo_bytes = struct.pack("<I", self.tamano_archivo)
        cluster_inicial_bytes = struct.pack("<I", self.cluster_inicial)
        fecha_creacion_bytes = self.fecha_creacion.encode("ascii")
        fecha_modificacion_bytes = self.fecha_modificacion.encode("ascii")
        return tipo_archivo_bytes + nombre_archivo_bytes + tamano_archivo_bytes + cluster_inicial_bytes + fecha_creacion_bytes + fecha_modificacion_bytes

    @classmethod
    def from_bytes(cls, data):
        # Crea una instancia de EntradaDirectorio a partir de bytes
        if len(data) < 52:
            print(f"Longitud de los datos: {len(data)}")
            raise ValueError("Los datos de entrada no tienen la longitud esperada.")
        tipo_archivo = data[0:1].decode("ascii")
        nombre_archivo = data[1:16].rstrip(b"\0").decode("ascii")
        tamano_archivo = struct.unpack("<I", data[16:20])[0]
        cluster_inicial = struct.unpack("<I", data[20:24])[0]
        fecha_creacion = data[24:38].decode("ascii")
        fecha_modificacion = data[38:52].decode("ascii", errors="ignore")
        return cls(tipo_archivo, nombre_archivo, tamano_archivo, cluster_inicial, fecha_creacion, fecha_modificacion)


# Se definen funciones auxiliares
def leer_superbloque():
    # Lectura el superbloque del sistema de archivos
    with open(NOMBRE_FIUNAMFS_IMG, "rb") as img_file:
        superbloque_data = img_file.read(SUPERBLOQUE_SIZE)
        if superbloque_data[:8] != FIUNAMFS_SIGNATURE:
            raise Exception("No es un sistema de archivos FiUnamFS válido.")
        if superbloque_data[10:14].decode("ascii") != VERSION_IMPLEMENTACION:
            raise Exception("Versión de implementación incorrecta.")
        
        etiqueta_volumen = superbloque_data[20:36].decode("ascii").strip()
        tamano_cluster = struct.pack("<I", superbloque_data[40:44])[0]
        num_clusters_directorio = struct.pack("<I", superbloque_data[45:49])[0]
        num_clusters_total = struct.pack("<I", superbloque_data[50:54])[0]
        return etiqueta_volumen, tamano_cluster, num_clusters_directorio, num_clusters_total

# Define la clase para operaciones en hilos
class HiloOperacion(threading.Thread):
    def __init__(self, operacion, img_file, *args):
        threading.Thread.__init__(self)
        self.operacion = operacion # Tipo de operación a realizar
        self.img_file = img_file # Archivo de imagen del sistema de archivos
        self.args = args # Argumentos adicionales para la operación

    def run(self):
        # Ejecuta la operación correspondiente
        if self.operacion == "listar":
            listar_contenido_directorio(self.img_file)
        elif self.operacion == "copiar_desde":
            if len(self.args) == 1:
                copiar_desde_fiunamfs(self.img_file, *self.args)
            else:
                print("Número incorrecto de argumentos para la operación 'copiar_desde'.")

        elif self.operacion == "eliminar":
            nombre_archivo_fiunamfs = self.args[0]
            eliminar_archivo_fiunamfs(self.img_file, nombre_archivo_fiunamfs)
            print(f"El archivo {nombre_archivo_fiunamfs} ha sido eliminado.")


def listar_contenido_directorio(img_file):
    # Lista el contenido del directorio en el sistema de archivos
    contenido = ""
    img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
    directorio_data = img_file.read(CLUSTER_SIZE * NUM_SECTORES_ENTRADA_DIRECTORIO * NUMERO_ENTRADAS_DIRECTORIO)
    for i in range(NUMERO_ENTRADAS_DIRECTORIO):
        entrada_data = directorio_data[i * ENTRADA_DIRECTORIO_SIZE: (i + 1) * ENTRADA_DIRECTORIO_SIZE]
        # Verificar si la entrada está vacía o eliminada
        if entrada_data[0:1] == b'\0' or entrada_data[0:1] == b'/':
            continue
        if len(entrada_data) < 52:
            continue  # Saltar esta entrada si la longitud no es la esperada
        entrada = EntradaDirectorio.from_bytes(entrada_data)
        contenido += f"Nombre: {entrada.nombre_archivo}, Tamaño: {entrada.tamano_archivo},\nCluster inicial: {entrada.cluster_inicial}, Fecha de Creación: {entrada.fecha_creacion}, Fecha de Modificación: {entrada.fecha_modificacion}\n\n"
    return contenido

def copiar_desde_fiunamfs(img_file, nombre_archivo_fiunamfs):
    # Copia un archivo desde el sistema de archivos fiunamfs

    # Ruta de la carpeta "LocalSO" dentro de la carpeta actual del proyecto
    carpeta_localSO = os.path.join(os.getcwd(), "LocalSO")

    # Crear la carpeta "LocalSO" si no existe
    if not os.path.exists(carpeta_localSO):
        os.makedirs(carpeta_localSO)

    # Ruta del archivo local en la carpeta "LocalSO"
    nombre_archivo_local = os.path.join(carpeta_localSO, nombre_archivo_fiunamfs)

    with open(nombre_archivo_local, "wb") as local_file:
        img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
        for i in range(NUMERO_ENTRADAS_DIRECTORIO):
            entrada_data = img_file.read(ENTRADA_DIRECTORIO_SIZE)
            entrada = EntradaDirectorio.from_bytes(entrada_data)
            if os.path.basename(entrada.nombre_archivo).strip() == nombre_archivo_fiunamfs.strip():
                img_file.seek(entrada.cluster_inicial * CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER)
                while True:
                    data = img_file.read(CLUSTER_SIZE)
                    if not data:
                        break
                    local_file.write(data)
                print(f"Se ha copiado {nombre_archivo_fiunamfs} a la carpeta 'LocalSO'.")
                return  # Salir del bucle una vez que se haya copiado el archivo
        print(f"No se encontró el archivo {nombre_archivo_fiunamfs} en el FiUnamFS.")


def eliminar_archivo_fiunamfs(img_file, nombre_archivo_fiunamfs):
    # Elimina un archivo del sistema de archivos fiunamfs
    img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
    directorio_data = img_file.read(CLUSTER_SIZE * NUM_SECTORES_ENTRADA_DIRECTORIO * NUMERO_ENTRADAS_DIRECTORIO)

    for i in range(NUMERO_ENTRADAS_DIRECTORIO):
        entrada_data = directorio_data[i * ENTRADA_DIRECTORIO_SIZE: (i + 1) * ENTRADA_DIRECTORIO_SIZE]
        entrada = EntradaDirectorio.from_bytes(entrada_data)
        if entrada.nombre_archivo.strip() == nombre_archivo_fiunamfs:
            if entrada.tipo_archivo == "/":  # Verificar si ya ha sido eliminado
                print(f"El archivo {nombre_archivo_fiunamfs} ya ha sido eliminado anteriormente.")
                return "ya_eliminado"
            # Marcar la entrada como eliminada
            nueva_entrada_data = b"/" + b"\0" * 63
            directorio_data = directorio_data[:i * ENTRADA_DIRECTORIO_SIZE] + nueva_entrada_data + directorio_data[(i + 1) * ENTRADA_DIRECTORIO_SIZE:]

            # Escribir el directorio modificado de nuevo en el archivo
            img_file.seek(CLUSTER_SIZE * NUM_SECTORES_POR_CLUSTER * DIRECTORIO_CLUSTER_INICIAL)
            img_file.write(directorio_data)

            print(f"El archivo {nombre_archivo_fiunamfs} ha sido eliminado.")
            return "eliminado"

    print(f"El archivo {nombre_archivo_fiunamfs} no se encontró en el directorio.")
    return "no_encontrado"


def eliminar_archivo_hilo(img_file, nombre_archivo_fiunamfs):
    eliminar_archivo_fiunamfs(nombre_archivo_fiunamfs)


# Implementación de la interfaz de usuario
class InterfazUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz Micro Sistema de Archivos")
        self.root.geometry("800x500")

        self.tabControl = ttk.Notebook(root)

        self.tabEliminar = ttk.Frame(self.tabControl)
        self.tabCopiarAr = ttk.Frame(self.tabControl)

        # Pestañas de eliminación y copiado
        self.tabControl.add(self.tabEliminar, text="Eliminar")
        self.tabControl.add(self.tabCopiarAr, text="Copiar Archivos")

        self.tabControl.pack(expand=1, fill="both")

        # Inicialización de los hilos de copiado y eliminación
        self.init_eliminar_tab()
        self.init_copiarAr_tab()


        # Iniciar el hilo para listar contenido en la pestaña de eliminar
        self.hilo_listar_eliminar = threading.Thread(target=self.hilo_listar_eliminar_func)
        self.hilo_listar_eliminar.start()

        # Inicia el hilo para lsitar contenido en la pestaña de copiar Archivos
        self.hilo_listar_copiar_ar = threading.Thread(target=self.hilo_listar_copiarAr_func)
        self.hilo_listar_copiar_ar.start()


    # Pestaña de eliminación
    def init_eliminar_tab(self):
        label = ttk.Label(self.tabEliminar, text="Ingrese el nombre del archivo a eliminar del micro sistema externo:")
        label.pack()

        self.entry_eliminar = ttk.Entry(self.tabEliminar)
        self.entry_eliminar.pack()

        self.txtListarContenidoEliminar = scrolledtext.ScrolledText(self.tabEliminar, width=60, height=20)
        self.txtListarContenidoEliminar.pack(pady=10)

        button_eliminar = ttk.Button(self.tabEliminar, text="Eliminar", command=self.eliminar_thread)
        button_eliminar.pack()

        button_actualizar = ttk.Button(self.tabEliminar, text="Actualizar", command=self.actualizar_listado_eliminar)
        button_actualizar.pack()

    # Pestaña de copiado al sistema local
    def init_copiarAr_tab(self):
        label = ttk.Label(self.tabCopiarAr, text="Ingrese el nombre del archivo que desea copiar a su ordenador")
        label.pack()

        self.entry_copiarAr = ttk.Entry(self.tabCopiarAr)
        self.entry_copiarAr.pack()

        self.txtListarContenidoCopiarAr = scrolledtext.ScrolledText(self.tabCopiarAr, width=60, height=20)
        self.txtListarContenidoCopiarAr.pack(pady=10)

        button_copiar = ttk.Button(self.tabCopiarAr, text="Copiar", command=self.copiarAr_thread)
        button_copiar.pack()

        button_actualizar = ttk.Button(self.tabCopiarAr, text="Actualizar", command=self.actualizar_listado_copiarAr)
        button_actualizar.pack()

    

    # Hilo de copiado
    def copiarAr_thread(self):
        nombre_archivo = self.entry_copiarAr.get()
        hilo_copiarAr = threading.Thread(target=self.hilo_copiarAr_func, args=(nombre_archivo,))
        hilo_copiarAr.start()

    # Funcionalidad de hilo de copiado
    def hilo_copiarAr_func(self, nombre_archivo):
        try:
            carpeta_localSO = os.path.join(os.getcwd(), "LocalSO")
            nombre_archivo_local = os.path.join(carpeta_localSO, nombre_archivo)
            if os.path.exists(nombre_archivo_local):
                messagebox.showwarning("Copiar", f"El archivo {nombre_archivo} ya existe en la carpeta 'LocalSO'.")
                return
            with open(NOMBRE_FIUNAMFS_IMG, "r+b") as img_file:
                copiar_desde_fiunamfs(img_file, nombre_archivo)
                messagebox.showinfo("Copiar", f"El archivo {nombre_archivo} ha sido copiado a la carpeta 'LocalSO'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    # Hilo de eliminación
    def eliminar_thread(self):
        nombre_archivo = self.entry_eliminar.get()
        hilo_eliminar = threading.Thread(target=self.hilo_eliminar_func, args=(nombre_archivo,))
        hilo_eliminar.start()

    #Funcionamiento del hilo de eliminación
    def hilo_eliminar_func(self, nombre_archivo):
        try:
            with open(NOMBRE_FIUNAMFS_IMG, "r+b") as img_file:
                resultado = eliminar_archivo_fiunamfs(img_file, nombre_archivo)
                if resultado == "eliminado":
                    messagebox.showinfo("Eliminar", f"El archivo {nombre_archivo} ha sido eliminado correctamente.")
                elif resultado == "ya_eliminado":
                    messagebox.showinfo("Eliminar", f"El archivo {nombre_archivo} ya ha sido eliminado anteriormente.")
                elif resultado == "no_encontrado":
                    messagebox.showwarning("Eliminar", f"El archivo {nombre_archivo} no se encontró en el directorio.")
                self.actualizar_listado_eliminar()  # Actualizar la lista 
        except Exception as e:
            messagebox.showerror("Error", str(e))


    # Recuadro de despliegue del listado para la pestaña de eliminación
    def hilo_listar_eliminar_func(self):
        try:
            with open(NOMBRE_FIUNAMFS_IMG, "rb") as img_file:
                contenido = listar_contenido_directorio(img_file)
                self.txtListarContenidoEliminar.delete('1.0', tk.END)
                self.txtListarContenidoEliminar.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Recuadro de despliegue del listado para la pestaña de copiado
    def hilo_listar_copiarAr_func(self):
        try:
            with open(NOMBRE_FIUNAMFS_IMG, "rb") as img_file:
                contenido = listar_contenido_directorio(img_file)
                self.txtListarContenidoCopiarAr.delete('1.0', tk.END)
                self.txtListarContenidoCopiarAr.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Actualización del listado en la pestaña de eliminación
    def actualizar_listado_eliminar(self):
        self.hilo_listar_eliminar_func()

    # Actualización del listado en la pestaña de eliminación
    def actualizar_listado_copiarAr(self):
        self.hilo_listar_copiarAr_func()


def main():
    root = tk.Tk()
    interfaz = InterfazUsuario(root)
    root.mainloop()

if __name__ == "__main__":
    main()
