import struct
import math
import os
from typing import List, Optional, Tuple

class FIUnamFS:

    def __init__(self, file_path: str):
        self.file_path = file_path # Ruta del archivo del sistema de archivos
        self.size_cluster = self._unpack_datos(40, 4) # Tamaño de un cluster
        self.dir_clusters = self._unpack_datos(45, 4) # Número de clusters del directorio
        self.un_clusters = self._unpack_datos(50, 4) # Número de clusters sin utilizar
        self.dir_size = 64 # Tamaño del directorio
        self.file_list: List[File] = [] # Lista de archivos
        self.storage_map: List[int] = [] # Mapa de almacenamiento
        self._inicializar_() 
        self._lista_archivos()
        self.number_of_clusters = 720

    def _verificar_archivo(self, nombre_copia: str) -> Tuple[int, bool]:
        for index, archivo in enumerate(self.file_list):
            if archivo.name == nombre_copia:
                return index, True
        return -1, False

    # Copia un archivo desde el sistema FIUnamFS al sistema local
    def _copiar_archivo(self, nombre_copia: str, ruta_nueva: str) -> None:
        # Verificamos si el archivo que se quiere copiar existe en nuestro directorio
        index_archivo, validacion = self._verificar_archivo(nombre_copia)
        if not validacion:
            print("El archivo no existe en el sistema")
            return

        # Archivo que se quiere copiar
        archivo_c = self.file_list[index_archivo]

        print(f"Tamaño del archivo a copiar: {archivo_c.size}")

        # Crear el archivo en la ruta especificada
        if os.path.exists(ruta_nueva):
            if os.path.isfile(os.path.join(ruta_nueva, nombre_copia)):
                ruta_archivo_destino = os.path.join(ruta_nueva, "copia_de_" + nombre_copia)
            else:
                ruta_archivo_destino = os.path.join(ruta_nueva, nombre_copia)

            with open(self.file_path, "rb") as sistema_archivos, open(ruta_archivo_destino, "wb") as destino:
                inicio_lectura = archivo_c.first_cluster * self.size_cluster
                sistema_archivos.seek(inicio_lectura)
                datos_archivo = sistema_archivos.read(archivo_c.size)
                destino.write(datos_archivo)

            print("Archivo copiado con éxito")
        else:
            print("La ruta especificada no existe")

    # Lee datos binarios desde el archivo
    def _leer_datos(self, start: int, size: int) -> bytes:
        with open(self.file_path, "rb") as img:
            img.seek(start)
            return img.read(size)

    def _unpack_datos(self, start: int, size: int) -> int:
        data = self._leer_datos(start, size)
        return struct.unpack('<i', data)[0]

    def _unpack_datos_ascii(self, start: int, size: int) -> str:
        data = self._leer_datos(start, size)
        return data.decode("ascii")

    # Mapa de almacenamiento con valores por defecto
    def _inicializar_(self) -> None:
        self.storage_map = [1] * 5 + [0] * (720 - 5)

    # Actualiza el mapa de almacenamiento basado en los archivos actuales
    def _actualizar_(self) -> None:
        self._inicializar_()
        for archivo in self.file_list:
            for j in range(archivo.num_clusters):
                self.storage_map[archivo.first_cluster + j] = 1

    # Obtiene datos de un archivo en una posición específica        
    def _get_data(self, position: int) -> Optional['File']:
        start = 1024 + (position * 64)
        if self._unpack_datos_ascii(start + 1, 14) != "--------------":
            name = self._unpack_datos_ascii(start + 1, 14)
            size = self._unpack_datos(start + 16, 4)
            first_cluster = self._unpack_datos(start + 20, 4)
            date = self._unpack_datos_ascii(start + 24, 14)
            if size != 0:
                return File(name, size, first_cluster, date, self.size_cluster)
        return None

    # Inicializa la lista de archivos leyendo el directorio principal
    def _lista_archivos(self) -> None:
        size_dir = int((self.size_cluster * self.dir_clusters) / self.dir_size)
        for x in range(size_dir):
            file_data = self._get_data(x)
            if file_data:
                self.file_list.append(file_data)
        self._actualizar_()

    # Muestra los archivos en el directorio principal
    def _mostrar_directorio(self) -> None:
        for f in self.file_list:
            print(f"{f.name}        {f.size} bytes")

    def _encontrar_espacio(self, tamano_archivo: int) -> int:
        clusters_ocupados = set()
        for archivo in self.file_list:
            clusters = [archivo.first_cluster + i for i in range((archivo.size + self.size_cluster - 1) // self.size_cluster)]
            clusters_ocupados.update(clusters)

        for i in range(5, self.number_of_clusters):
            if i not in clusters_ocupados:
                if (i + (tamano_archivo + self.size_cluster - 1) // self.size_cluster) <= self.number_of_clusters:
                    return i
        return -1

    def _agregar_al_directorio(self, archivo: 'File') -> None:
        with open(self.file_path, "r+b") as sistema_archivos:
            for i in range(len(self.file_list)):
                start = 1024 + i * 64
                sistema_archivos.seek(start)
                if sistema_archivos.read(1) == b'\x00':
                    sistema_archivos.seek(start)
                    sistema_archivos.write(archivo.name.ljust(14).encode('ascii'))
                    sistema_archivos.write(struct.pack('<i', archivo.size))
                    sistema_archivos.write(struct.pack('<i', archivo.first_cluster))
                    sistema_archivos.write(archivo.date.ljust(14).encode('ascii'))
                    break

    def _copiar_archivo_a_sistema(self, ruta_archivo: str) -> None:
        if not os.path.exists(ruta_archivo):
            print("El archivo no existe.")
            return

        nombre_archivo = os.path.basename(ruta_archivo)
        
        if self._verificar_archivo(nombre_archivo)[1]:
            print("El archivo ya existe en el sistema de archivos.")
            return

        tamano_archivo = os.path.getsize(ruta_archivo)
        espacio_disponible = self._encontrar_espacio(tamano_archivo)
        print(f"Espacio disponible: {espacio_disponible}")

        if espacio_disponible == -1:
            print("No hay suficiente espacio en el sistema de archivos para copiar el archivo.")
            return

        with open(ruta_archivo, "rb") as archivo_computadora, open(self.file_path, "r+b") as sistema_archivos:
            contenido = archivo_computadora.read()
            inicio_escritura = espacio_disponible * self.size_cluster
            print("Inicio escritura: ", inicio_escritura)
            sistema_archivos.seek(inicio_escritura)
            sistema_archivos.write(contenido)

        nuevo_archivo = File(nombre_archivo, tamano_archivo, espacio_disponible, "", self.size_cluster)
        print("Nombre del archivo: ", nuevo_archivo.name)
        self.file_list.append(nuevo_archivo)
        self._agregar_al_directorio(nuevo_archivo)
        self._update_map()
        print("Archivo copiado con éxito al sistema de archivos")

    def borrar_archivo(self, nombre_archivo: str) -> None:
        index_archivo, validacion = self._verificar_archivo(nombre_archivo)
        if not validacion:
            print("El archivo no existe")
            return

        archivo_borrar = self.file_list[index_archivo]
        del self.file_list[index_archivo]

        with open(self.file_path, "r+b") as sistema_archivos:
            # Marcar la entrada del archivo en el directorio como eliminada
            sistema_archivos.seek(1024 + index_archivo * 64)
            sistema_archivos.write(b'\x00' * 64)

            # Marcar los clusters ocupados por el archivo como libres en el mapa de almacenamiento
            for i in range(archivo_borrar.num_clusters):
                cluster_pos = archivo_borrar.first_cluster + i
                self.storage_map[cluster_pos] = 0
                # Limpiar los datos en el archivo físico (opcional)
                sistema_archivos.seek(cluster_pos * self.size_cluster)
                sistema_archivos.write(b'\x00' * self.size_cluster)

        self._actualizar_()
        print("Archivo eliminado con éxito")

class File:
    def __init__(self, name: str, size: int, first_cluster: int, date: str, size_cluster: int):
        self.name = name.replace(" ", "")
        self.size = size
        self.first_cluster = first_cluster
        self.date = date
        self.num_clusters = math.ceil(size / size_cluster)

def desplegar_menu():
    fs = FIUnamFS("fiunamfs.img")
    print("Bienvenidx a FIUnamFS")
    while True:
        print("\n-------------------------Menú de opciones--------------------------------")
        print("1. Listar los contenidos del directorio")
        print("2. Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema")
        print("3. Copiar un archivo de tu computadora hacia tu FiUnamFS")
        print("4. Eliminar un archivo del FiUnamFS")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("El contenido del directorio es \n")
            fs._mostrar_directorio()
        elif opcion == '2':
                    copia_archivo = input("Ingrese el nombre del archivo a copiar en su equipo: ")
                    ruta_archivo = input("Ingrese la ruta del directorio a donde se copiará el archivo: ") 
                    fs._copiar_archivo(copia_archivo, ruta_archivo)
        elif opcion == '3':
            ruta_archivo = input("Ingrese la ruta del archivo a copiar: ").strip()
            fs._copiar_archivo_a_sistema(ruta_archivo)
        elif opcion == '4':
                    print("4")
                    archivo_a_eliminar = input("Ingrese el nombre a eliminar del sistema FIUnamFS: ").strip()
                    _eliminar_archivo(archivo_a_eliminar)
        elif opcion == '5':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")
desplegar_menu()


