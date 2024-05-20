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

	# Este método elimina un archivo del sistema

    def _eliminar_archivo(self, nombre_archivo: str) -> None:
        # Verificamos si el archivo que se quiere eliminar existe en el sistema
        index_archivo, validacion = self.verificar_archivo(nombre_archivo)
        if not validacion:
            print("El archivo no existe")
            return

    
        archivo_borrar = self.file_list[index_archivo]

        
        del self.file_list[index_archivo]

        
        with open(self.file_path, "r+b") as sistema_archivos:
            sistema_archivos.seek(1024 + index_archivo * 64)
            sistema_archivos.write(b'\x00' * 64)

           
            sistema_archivos.seek(archivo_borrar.first_cluster * self.size_cluster)
            sistema_archivos.write(b'\x00' * archivo_borrar.size)

       
        self._init_files()

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
		    
            print("3")
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


