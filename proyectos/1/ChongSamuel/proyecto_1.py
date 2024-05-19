import struct
import math
from typing import List, Optional

class FIUnamFS:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.size_cluster = self._unpack_datos(40, 4)
        self.dir_clusters = self._unpack_datos(45, 4)
        self.un_clusters = self._unpack_datos(50, 4)
        self.dir_size = 64
        self.file_list: List[File] = []
        self.storage_map: List[int] = []
        self._inicializar_()
        self._lista_archivos()

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
            print("2")
        elif opcion == '3':
            print("3")
        elif opcion == '4':
            print("4")
        elif opcion == '5':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")
desplegar_menu()

