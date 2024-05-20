import os
import struct
import time
import threading
import tkinter as tk
from tkinter import filedialog

# Constantes
TAMANIO_SECTOR = 512
TAMANIO_CLUSTER = TAMANIO_SECTOR * 4
TAMANIO_ENTRADA_DIRECTORIO = 64
NUMERO_ENTRADAS_DIRECTORIO = 16  # 4 clusters * 16 entradas por cluster
DIRECTORIO_INICIO = 1 * TAMANIO_CLUSTER
DIRECTORIO_FIN = 4 * TAMANIO_CLUSTER

# Semáforo para controlar el acceso concurrente al recurso compartido
semaforo = threading.Semaphore(value=1)

# Función para leer enteros desde el archivo fuente
def leer_entero(posicion, longitud):
    with open("fiunamfs.img", "rb") as archivo:
        archivo.seek(posicion)
        bytes_entero = archivo.read(longitud)
        entero = int.from_bytes(bytes_entero, byteorder='little')
        return entero

# Función para leer cadenas desde el archivo fuente
def leer_cadena(posicion, longitud):
    with open("fiunamfs.img", "rb") as archivo:
        archivo.seek(posicion)
        bytes_cadena = archivo.read(longitud)
        cadena = bytes_cadena.decode("ascii")
        return cadena

# Función para leer una cadena de longitud fija desde el archivo
def leer_cadena2(archivo, posicion, longitud):
    archivo.seek(posicion)
    cadena = archivo.read(longitud)
    return cadena.decode('ascii').rstrip('\x00')
"""----------------------------------------------------------------------------"""

# Función para listar los contenidos del directorio
def listar_contenidos_directorio():
    def regresar_menu(event=None):
        ventana_listado.destroy()  # Ocultar la ventana actual
        root.deiconify()  # Mostrar la ventana principal

    # Crear una nueva ventana para mostrar los contenidos del directorio
    root.withdraw()  # Ocultar la ventana principal
    ventana_listado = tk.Toplevel(root)
    ventana_listado.title("Contenido de FiUnamFS")
    ventana_listado.geometry("800x600")
    ventana_listado.configure(bg="black")

    # Crear etiquetas con los contenidos del directorio
    with open("fiunamfs.img", "rb") as archivo:
        contenido = tk.Text(ventana_listado, bg="black", fg="white")
        contenido.pack(expand=True, fill="both")

        # Leer el directorio ubicado en los clusters 1 a 4
        for cluster in range(1, 5):
            inicio_cluster = (cluster - 1) * TAMANIO_CLUSTER
            for i in range(NUMERO_ENTRADAS_DIRECTORIO):
                entrada_posicion = inicio_cluster + i * TAMANIO_ENTRADA_DIRECTORIO
                tipo_archivo = leer_cadena2(archivo, entrada_posicion, 1)
                if tipo_archivo == '-':  # Archivo regular
                    contenido.insert(tk.END, "Categoría: Archivo Regular\n")
                    nombre_archivo = leer_cadena2(archivo, entrada_posicion + 1, 15)
                    tamano_archivo = struct.unpack("<I", archivo.read(4))[0]
                    cluster_inicial = struct.unpack("<I", archivo.read(4))[0]
                    hora_creacion = leer_cadena2(archivo, entrada_posicion + 24, 14)
                    hora_modificacion = leer_cadena2(archivo, entrada_posicion + 38, 14)
                    contenido.insert(tk.END, f"Nombre: {nombre_archivo}\n")
                    contenido.insert(tk.END, f"Tamaño: {tamano_archivo} bytes\n")
                    contenido.insert(tk.END, f"Cluster inicial: {cluster_inicial}\n")
                    contenido.insert(tk.END, f"Creado: {hora_creacion}\n")
                    contenido.insert(tk.END, f"Modificado: {hora_modificacion}\n")
                    contenido.insert(tk.END, "------------------------------------\n")

    # Botón para regresar al menú principal
    ventana_listado.bind("<F1>", regresar_menu)
"""---------------------------------------------------------"""
# Función para copiar un archivo desde FiUnamFS a tu sistema
def copiar_archivo_desde_fiunamfs(nombre_archivo):
    with open("fiunamfs.img", "rb") as archivo:
        # Buscar el archivo en el directorio
        for cluster in range(1, 5):
            inicio_cluster = (cluster - 1) * TAMANIO_CLUSTER
            for i in range(NUMERO_ENTRADAS_DIRECTORIO):
                entrada_posicion = inicio_cluster + i * TAMANIO_ENTRADA_DIRECTORIO
                tipo_archivo = leer_cadena2(archivo, entrada_posicion, 1)
                if tipo_archivo == '-' or tipo_archivo == '/':  # Archivo regular o vacío
                    nombre_archivo_actual = leer_cadena2(archivo, entrada_posicion + 1, 15)
                    if nombre_archivo_actual.strip() == nombre_archivo:
                        tamano_archivo = struct.unpack("<I", archivo.read(4))[0]
                        cluster_inicial = struct.unpack("<I", archivo.read(4))[0]
                        archivo.seek(TAMANIO_CLUSTER * cluster_inicial)
                        contenido_archivo = archivo.read(tamano_archivo)
                        return contenido_archivo
    return None

# Función para manejar la copia del archivo en un hilo separado
def copiar_archivo_thread(nombre_archivo, ventana):
    semaforo.acquire()
    try:
        contenido_archivo = copiar_archivo_desde_fiunamfs(nombre_archivo)
        contenido = tk.Text(ventana, bg="black", fg="white")
        contenido.pack(expand=True, fill="both")

        if contenido_archivo:
            # Abrir un diálogo para que el usuario elija el directorio de destino
            directorio_destino = filedialog.askdirectory(title="Seleccionar directorio de destino")
            if directorio_destino:
                # Guardar el archivo en el directorio seleccionado
                ruta_archivo_destino = os.path.join(directorio_destino, nombre_archivo)
                with open(ruta_archivo_destino, "wb") as archivo_destino:
                    archivo_destino.write(contenido_archivo)
                contenido.insert(tk.END, f"Archivo '{nombre_archivo}' copiado exitosamente a '{ruta_archivo_destino}'.\n")
            else:
                contenido.insert(tk.END, "No se seleccionó ningún directorio.\n")
        else:
            contenido.insert(tk.END, f"Archivo '{nombre_archivo}' no encontrado en FiUnamFS.\n")

        contenido.insert(tk.END, "Presiona F1 para regresar al menú principal.\n")

    finally:
        semaforo.release()

    ventana.bind("<F1>", lambda event: regresar_menu(ventana))

def regresar_menu(ventana):
    ventana.destroy()
    root.deiconify()

def copiar():
    ventana = tk.Toplevel(root)
    ventana.title("Copiar Archivo desde FiUnamFS a tu equipo")
    ventana.geometry("800x600")
    ventana.configure(bg="black")

    # Ocultar la ventana principal
    root.withdraw()

    # Etiqueta con las condiciones
    condiciones_label = tk.Label(ventana, text="Introduce el nombre del archivo a copiar desde FiUnamFS:", font=("Arial", 12), bg="black", fg="white")
    condiciones_label.pack(pady=10)

    # Entrada para el nombre del archivo
    nombre_archivo_entry = tk.Entry(ventana, font=("Arial", 12))
    nombre_archivo_entry.pack(pady=5)

    # Botón para iniciar la copia
    copiar_button = tk.Button(ventana, text="Copiar Archivo", command=lambda: copiar2(nombre_archivo_entry.get(), ventana))
    copiar_button.pack(pady=10)

def copiar2(nombre_archivo, ventana):
    t = threading.Thread(target=copiar_archivo_thread, args=(nombre_archivo, ventana))
    t.start()
"""---------------------------------------------------------"""
# Función para encontrar espacio libre en el disco
def encontrar_espacio_libre(disco, tamano_archivo):
    disco.seek(DIRECTORIO_FIN)  # Inicio del espacio de datos
    espacio_libre = b'\x00' * tamano_archivo  # Espacio libre requerido
    datos = disco.read()  # Leer todos los datos
    indice = datos.find(espacio_libre)  # Buscar la primera aparición del espacio libre
    if indice != -1:
        return DIRECTORIO_FIN + indice
    else:
        raise ValueError("No se encontró espacio suficiente para el archivo.")

def moverCompuFI(ruta_archivo, nombre_archivo):
    tamano_archivo = os.path.getsize(ruta_archivo)
    nombre2, extension_archivo = os.path.splitext(nombre_archivo)
    if (len(nombre2) + len(extension_archivo)) > 15:
        raise ValueError("El nombre del archivo es demasiado grande.")

    nombre_archivo = (nombre2 + extension_archivo).ljust(15, ' ')

    with open("fiunamfs.img", "r+b") as disco:
        # Encontrar espacio libre en el disco
        posicion_espacio_libre = encontrar_espacio_libre(disco, tamano_archivo)

        # Escribir el archivo en el espacio libre encontrado
        with open(ruta_archivo, "rb") as archivo:
            contenido_archivo = archivo.read()
            disco.seek(posicion_espacio_libre)
            disco.write(contenido_archivo)

        # Actualizar el directorio
        for cluster in range(1, 5):
            inicio_cluster = (cluster - 1) * TAMANIO_CLUSTER
            for i in range(NUMERO_ENTRADAS_DIRECTORIO):
                entrada_posicion = inicio_cluster + i * TAMANIO_ENTRADA_DIRECTORIO
                disco.seek(entrada_posicion)
                tipo_archivo = disco.read(1).decode('ascii')
                if tipo_archivo == '/':
                    disco.seek(entrada_posicion)
                    disco.write(b'-')
                    disco.write(nombre_archivo.encode('ascii'))
                    disco.write(struct.pack("<I", tamano_archivo))
                    disco.write(struct.pack("<I", (posicion_espacio_libre // TAMANIO_CLUSTER)))

                    fecha_hora_actual = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    disco.write(fecha_hora_actual.encode('ascii'))
                    disco.write(fecha_hora_actual.encode('ascii'))
                    disco.write(b'\x00' * (TAMANIO_ENTRADA_DIRECTORIO - 52))
                    return

    raise ValueError("No se encontró una entrada de directorio libre.")

def copiar_archivo_con_semaforo():
    semaforo = threading.Semaphore(value=1)

    def regresar_menu(event=None):
        ventana_copia.destroy()  # Destruir la ventana actual
        root.deiconify()  # Mostrar la ventana principal

    ventana_copia = tk.Toplevel(root)
    ventana_copia.title("Copiar archivo desde tu equipo a FiUnamFS")
    ventana_copia.geometry("800x600")
    ventana_copia.configure(bg="black")
    def tarea():
        semaforo.acquire()
        try:
            root.withdraw()  # Ocultar la ventana principal

            contenido = tk.Text(ventana_copia, bg="black", fg="white")
            contenido.pack(expand=True, fill="both")

            ruta_archivo = filedialog.askopenfilename(title="Selecciona un archivo")
            if not ruta_archivo:
                contenido.insert(tk.END, "No se seleccionó ningún archivo.\nF1 Regresar a inicio\n")
            else:
                nombre_archivo = os.path.basename(ruta_archivo)
                try:
                    moverCompuFI(ruta_archivo, nombre_archivo)
                    contenido.insert(tk.END, f"Archivo '{nombre_archivo}' copiado exitosamente a FiUnamFS.\nF1 Regresar a inicio\n")
                except ValueError as e:
                    contenido.insert(tk.END, f"Error: {str(e)}\nF1 Regresar a inicio\n")

            # Bind F1 key to return to the main menu
            ventana_copia.bind("<F1>", regresar_menu)

        finally:
            semaforo.release()

    hilo = threading.Thread(target=tarea)
    hilo.start()
"""---------------------------------------------------------"""

# Función para borrar un archivo en FiUnamFS
def borrar_archivo(nombre_archivo):
    nombre_archivo = nombre_archivo.ljust(15, ' ')
    with open("fiunamfs.img", "r+b") as disco:
        # Buscar el archivo en el directorio
        for cluster in range(1, 5):
            inicio_cluster = (cluster - 1) * TAMANIO_CLUSTER
            for i in range(NUMERO_ENTRADAS_DIRECTORIO):
                entrada_posicion = inicio_cluster + i * TAMANIO_ENTRADA_DIRECTORIO
                disco.seek(entrada_posicion)
                tipo_archivo = disco.read(1).decode('ascii')
                if tipo_archivo == '-':
                    archivo_nombre = leer_cadena2(disco, entrada_posicion + 1, 15)
                    if archivo_nombre == nombre_archivo:
                        # Marcar la entrada del archivo como vacía
                        disco.seek(entrada_posicion)
                        disco.write(b'/')  # Marcar como vacío
                        disco.write(b'\x00' * 63)  # Rellenar el resto de la entrada con 00
                        return True  # Archivo encontrado y marcado como borrado
    return False  # Archivo no encontrado

def eliminar_archivo_fi():
    def regresar_menu(event=None):
        ventana_eliminar.destroy()  # Destruir la ventana actual
        root.deiconify()  # Mostrar la ventana principal

    def realizar_borrado():
        nombre_archivo_a_borrar = entrada_nombre.get().strip()
        if borrar_archivo(nombre_archivo_a_borrar):
            resultado.set(f"Archivo '{nombre_archivo_a_borrar}' borrado exitosamente.\nF1 Regresar a inicio")
        else:
            resultado.set(f"Archivo '{nombre_archivo_a_borrar}' no encontrado en FiUnamFS.\nF1 Regresar a inicio")

    root.withdraw()  # Ocultar la ventana principal

    ventana_eliminar = tk.Toplevel(root)
    ventana_eliminar.title("Eliminar Archivo de FiUnamFS")
    ventana_eliminar.geometry("800x600")
    ventana_eliminar.configure(bg="black")

    etiqueta_condiciones = tk.Label(ventana_eliminar, text="Introduce el nombre del archivo a borrar de FiUnamFS:", font=("Arial", 12), bg="black", fg="white")
    etiqueta_condiciones.pack(pady=10)

    entrada_nombre = tk.Entry(ventana_eliminar, font=("Arial", 12))
    entrada_nombre.pack(pady=5)

    boton_borrar = tk.Button(ventana_eliminar, text="Borrar Archivo", command=realizar_borrado, bg="black", fg="white", font=("Arial", 12))
    boton_borrar.pack(pady=10)

    resultado = tk.StringVar()
    etiqueta_resultado = tk.Label(ventana_eliminar, textvariable=resultado, font=("Arial", 12), bg="black", fg="white")
    etiqueta_resultado.pack(pady=20)

    ventana_eliminar.bind("<F1>", regresar_menu)

"""---------------------------------------------------------"""

def listar_contenido_fiunamfs():
    print("Listando contenido de FiUnamFS...")
    listar_contenidos_directorio()

def copiar_archivo_fiunamfs():
    print("Copiando archivo desde FiUnamFS a tu equipo...")
    copiar()

def copiar_archivo_equipo_fiunamfs():
    print("Copiando archivo desde tu equipo a FiUnamFS...")
    copiar_archivo_con_semaforo()

def eliminar_archivo_fiunamfs():
    eliminar_archivo_fi()

def revisar_informacion_disco():
    print("Revisando información del disco...")
    revisar_info_disco()

def salir_programa():
    print("Saliendo del programa.")
    root.destroy()
"""---------------------------------------------------------"""
# Función para iniciar y mostrar información del disco
def iniciar():
    nombre_sistema = leer_cadena(0, 9)
    version = leer_cadena(10, 5)
    etiqueta_volumen = leer_cadena(20, 20)
    tamanio_cluster = leer_entero(40, 4)
    num_clusters_directorio = leer_entero(45, 4)
    num_total_clusters = leer_entero(50, 4)

    informacion = (
        "=== Información del Sistema de Archivos ===\n"
        f"Nombre del sistema: {nombre_sistema}\n"
        f"Versión: {version}\n"
        f"Etiqueta del volumen: {etiqueta_volumen}\n"
        f"Tamaño del cluster: {tamanio_cluster} bytes\n"
        f"Número de clusters en el directorio: {num_clusters_directorio}\n"
        f"Número total de clusters: {num_total_clusters}\n"
    )

    return informacion

# Función para revisar información del disco
def revisar_info_disco():
    def regresar_menu(event=None):
        ventana_informacion.destroy()  # Destruir la ventana actual
        root.deiconify()  # Mostrar la ventana principal

    root.withdraw()  # Ocultar la ventana principal

    ventana_informacion = tk.Toplevel(root)
    ventana_informacion.title("Información del Sistema de Archivos")
    ventana_informacion.geometry("800x600")
    ventana_informacion.configure(bg="black")

    encabezado = "Programa creado por De La Merced Soriano Uriel Benjamín y Hernández Gutiérrez Carlos Mario"
    informacion = iniciar()
    mensaje_completo = f"{encabezado}\n\n{informacion}\nF1 Regresar a inicio"

    etiqueta_informacion = tk.Label(ventana_informacion, text=mensaje_completo, font=("Arial", 12), bg="black", fg="white", justify=tk.LEFT)
    etiqueta_informacion.pack(pady=10, padx=10)

    ventana_informacion.bind("<F1>", regresar_menu)
"""---------------------------------------------------------"""
# Definir las opciones del menú
opciones_menu = {
    "F1": ("F1. Listar contenido de FiUnamFS", listar_contenido_fiunamfs),
    "F2": ("F2. Copiar archivo desde FiUnamFS a tu equipo", copiar_archivo_fiunamfs),
    "F3": ("F3. Copiar archivo desde tu equipo a FiUnamFS", copiar_archivo_equipo_fiunamfs),
    "F4": ("F4. Eliminar archivo de FiUnamFS", eliminar_archivo_fiunamfs),
    "F5": ("F5. Revisar información del disco", revisar_informacion_disco),
    "F6": ("F6. Salir del programa", salir_programa)
}

def capturar_tecla(event):
    key = event.keysym
    if key in opciones_menu:
        opciones_menu[key][1]()

def mostrar_menu_principal():
    # Crear la etiqueta de instrucciones
    label = tk.Label(root, text="Por favor, selecciona una opción del menú (F1-F6):", fg="white", bg="black", font=("Arial", 14))
    label.pack(pady=20)  # Agregar un espacio en la parte superior e inferior

    # Crear los botones para cada opción del menú
    for key, (text, command) in opciones_menu.items():
        button = tk.Button(root, text=text, command=command, bg="black", fg="white", font=("Arial", 12))
        button.pack(pady=10)  # Agregar un espacio entre los botones

    # Capturar la entrada del usuario
    root.bind("<Key>", capturar_tecla)

# Crear la ventana principal
root = tk.Tk()
root.title("Proyecto: (Micro) sistema de archivos multihilos")
root.geometry("600x400")  # Establecer el tamaño de la ventana
root.configure(bg="black")  # Establecer el fondo negro


# Función para mostrar el menú principal cuando se inicia el programa
mostrar_menu_principal()

# Ejecutar el bucle de eventos
root.mainloop()
