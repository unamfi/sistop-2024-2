import os
import struct
import threading
import tkinter as tk #FAVOR DE QUE AL CORRER EL PROGRAMA, AMPLIAR LA INTERFAZ A PANTALLA COMPLETA PARA VISUALIZAR LAS OPCIONES
from tkinter import filedialog, messagebox, simpledialog #INTERFAZ GRAFICA

TAMANO_CLUSTER = 1024
TAMANO_ENTRADA = 64
DIRECTORIO_INICIO = TAMANO_CLUSTER  # Cluster 1
DIRECTORIO_TAMANO = 4 * TAMANO_CLUSTER  # 4 clusters para el directorio
MAXIMO_CLUSTERS = 1440 // 4  # Asumiendo que el tamaño total es 1440KB

lock = threading.Lock()
#PRIMER CPOMMIT
def leer_superbloque(fiunamfs_img):
    resultado = ""
    with open(fiunamfs_img, 'rb') as f:
        f.seek(0)
        nombre_fs = f.read(8).decode('ascii').strip()
        f.seek(10)
        version = f.read(5).decode('ascii').rstrip('\x00').strip()
        resultado += f"Nombre FS leído: {nombre_fs}, Versión leída: {version}\n"
        if nombre_fs != "FiUnamFS" or version.replace('-', '.') != "24.2":
            resultado += "Valores no coinciden, se esperaba FiUnamFS y 24.2\n"
        else:
            resultado += "Superbloque válido\n"
    return resultado
#SEGUNDO COMMIT
def listar_directorio(fiunamfs_img):
    resultado = ""
    with open(fiunamfs_img, 'rb') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            entrada = f.read(TAMANO_ENTRADA)
            tipo_archivo = entrada[0:1].decode('ascii')
            nombre = entrada[1:16].decode('ascii').rstrip()
            if nombre != '#' * 15:
                tam_archivo = struct.unpack('<I', entrada[16:20])[0]
                cluster_ini = struct.unpack('<I', entrada[20:24])[0]
                fecha_creacion = entrada[24:38].decode('ascii')
                fecha_modificacion = entrada[38:52].decode('ascii')
                resultado += f"Tipo: {tipo_archivo}, Nombre: {nombre}, Tamaño: {tam_archivo}, Cluster inicial: {cluster_ini}, Creación: {fecha_creacion}, Modificación: {fecha_modificacion}\n"
    return resultado
#TERCER COMMIT
def copiar_a_sistema(fiunamfs_img, nombre_archivo, destino):
    with lock:
        app.lock_label.config(text="Estado del Lock: Adquirido (Copiar a sistema)")
    with open(fiunamfs_img, 'rb') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            entrada = f.read(TAMANO_ENTRADA)
            tipo_archivo = entrada[0:1]
            if tipo_archivo == b'-':
                nombre, tam, cluster_ini = (
                    entrada[1:16].decode('ascii').rstrip(),
                    struct.unpack('<I', entrada[16:20])[0],
                    struct.unpack('<I', entrada[20:24])[0]
                )
                if nombre.rstrip('\x00').strip() == nombre_archivo.rstrip('\x00').strip():
                    f.seek(cluster_ini * TAMANO_CLUSTER)
                    datos = f.read(tam)
                    with open(destino, 'wb') as archivo_destino:
                        archivo_destino.write(datos)
                    return

def copiar_a_fiunamfs(fiunamfs_img, archivo_origen, nombre_destino):
    with lock:
        app.lock_label.config(text="Estado del Lock: Adquirido (Copiar a FiUnamFS)")
    with open(fiunamfs_img, 'r+b') as f:
        tam_origen = os.path.getsize(archivo_origen)
        cluster_libre = 5
        posicion_entrada_libre = None

        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            posicion_actual = f.tell()
            entrada = f.read(TAMANO_ENTRADA)
            tipo_archivo = entrada[0:1]
            cluster_ini = struct.unpack('<I', entrada[20:24])[0]

            if tipo_archivo == b'/' and posicion_entrada_libre is None:
                posicion_entrada_libre = posicion_actual

            if cluster_ini >= cluster_libre:
                cluster_libre = cluster_ini + 1

        if posicion_entrada_libre is None:
            raise Exception("No hay espacio en el directorio")
        else:
            with open(archivo_origen, 'rb') as archivo_origen_f:
                f.seek(cluster_libre * TAMANO_CLUSTER)
                f.write(archivo_origen_f.read())

            f.seek(posicion_entrada_libre)
            f.write(b'-' + nombre_destino.ljust(15).encode('ascii'))
            f.write(struct.pack('<I', tam_origen))
            f.write(struct.pack('<I', cluster_libre))
#CUARTO COMMIT
def eliminar_archivo(fiunamfs_img, nombre_archivo):
    with lock:
        app.lock_label.config(text="Estado del Lock: Adquirido (Eliminar archivo)")
    with open(fiunamfs_img, 'r+b') as f:
        f.seek(DIRECTORIO_INICIO)
        for _ in range(DIRECTORIO_TAMANO // TAMANO_ENTRADA):
            posicion = f.tell()
            entrada = f.read(TAMANO_ENTRADA)
            nombre = entrada[1:16].decode('ascii').rstrip()
            if nombre.rstrip('\x00').strip() == nombre_archivo.rstrip('\x00').strip():
                f.seek(posicion)
                f.write(b'/' + b' ' * 15)
                return
#INTERFAZ GRAFICA, QUINTPO COMMIT
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Archivos FiUnamFS")
        self.geometry("800x500")  # Ajustar tamaño de ventana

        # Configuración inicial
        self.fiunamfs_img = r"fiunamfs.img"  # Cambia la ruta por la ubicación de tu archivo .img

        self.create_widgets()

    def create_widgets(self):
        self.resultado_texto = tk.Text(self, height=30, width=100)  # Ajustar el tamaño del cuadro de texto
        self.resultado_texto.pack(fill=tk.BOTH, expand=True)  # Hacer que el cuadro de texto se expanda

        self.lock_label = tk.Label(self, text="Estado del Lock: Desbloqueado")
        self.lock_label.pack()

        tk.Button(self, text="Leer el superbloque", command=self.leer_superbloque).pack(fill=tk.X, pady=5)
        tk.Button(self, text="Listar directorio", command=self.listar_directorio).pack(fill=tk.X, pady=5)
        tk.Button(self, text="Copiar archivo de FiUnamFS a sistema", command=self.copiar_a_sistema).pack(fill=tk.X, pady=5)
        tk.Button(self, text="Copiar archivo de sistema a FiUnamFS", command=self.copiar_a_fiunamfs).pack(fill=tk.X, pady=5)
        tk.Button(self, text="Eliminar archivo de FiUnamFS", command=self.eliminar_archivo).pack(fill=tk.X, pady=5)
        tk.Button(self, text="Salir", command=self.quit).pack(fill=tk.X, pady=5)

    def leer_superbloque(self):
        resultado = leer_superbloque(self.fiunamfs_img)
        self.mostrar_resultado(resultado)

    def listar_directorio(self):
        resultado = listar_directorio(self.fiunamfs_img)
        self.mostrar_resultado(resultado)

    def mostrar_resultado(self, resultado):
        self.resultado_texto.delete(1.0, tk.END)  # Limpiar el contenido anterior
        self.resultado_texto.insert(tk.END, resultado)

    def copiar_a_sistema(self):
        nombre_archivo = simpledialog.askstring("Nombre del archivo", "Ingresa el nombre del archivo en FiUnamFS:")
        if nombre_archivo:
            destino = filedialog.asksaveasfilename(initialfile=nombre_archivo)
            if destino:
                try:
                    copiar_a_sistema(self.fiunamfs_img, nombre_archivo, destino)
                    messagebox.showinfo("Éxito", f"Archivo copiado con éxito a {destino}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al copiar el archivo: {e}")

    def copiar_a_fiunamfs(self):
        origen = filedialog.askopenfilename(title="Selecciona el archivo a copiar")
        if origen:
            nombre_destino = simpledialog.askstring("Nombre del archivo", "Ingresa el nombre del archivo en FiUnamFS:")
            try:
                copiar_a_fiunamfs(self.fiunamfs_img, origen, nombre_destino)
                messagebox.showinfo("Éxito", "Archivo copiado con éxito a FiUnamFS")
            except Exception as e:
                messagebox.showerror("Error", f"Error al copiar el archivo: {e}")

    def eliminar_archivo(self):
        nombre_archivo = simpledialog.askstring("Nombre del archivo", "Ingresa el nombre del archivo a eliminar de FiUnamFS:")
        if nombre_archivo:
            try:
                eliminar_archivo(self.fiunamfs_img, nombre_archivo)
                messagebox.showinfo("Éxito", "Archivo eliminado con éxito")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el archivo: {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()