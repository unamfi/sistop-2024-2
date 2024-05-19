import threading
import struct
import queue

class FiUnamFS:
    # Definición de constantes del sistema de archivos
    SECTOR_SIZE = 512
    CLUSTER_SIZE = 4 * SECTOR_SIZE
    VOLUME_SIZE = 1440 * 1024  # 1440 KB
    FILE_ENTRY_SIZE = 64

    def __init__(self, disk_file):
        # Inicialización de variables y lectura del superbloque
        self.disk_file = disk_file
        self.superblock = self.read_superblock()
        self.lock = threading.Lock()  # Lock para sincronización de hilos
        self.command_queue = queue.Queue()  # Cola de comandos para gestionar operaciones
        self.is_running = True  # Bandera para controlar la ejecución de los hilos

    def read_sector(self, sector_number):
        # Lectura de un sector específico del archivo de disco
        with open(self.disk_file, 'rb') as f:
            f.seek(sector_number * self.SECTOR_SIZE)
            return f.read(self.SECTOR_SIZE)

    def write_sector(self, sector_number, data):
        # Escritura de un sector específico del archivo de disco
        with open(self.disk_file, 'r+b') as f:
            f.seek(sector_number * self.SECTOR_SIZE)
            f.write(data)

    def read_superblock(self):
        # Lectura del superbloque para obtener información del sistema de archivos
        superblock_data = self.read_sector(0)
        identifier = superblock_data[0:9].decode('ascii').strip('\x00')
        version = superblock_data[10:15].decode('ascii').strip('\x00')
        if identifier != "FiUnamFS":
            raise Exception("El sistema de archivos no es FiUnamFS")
        if version != "24-2":
            raise Exception("La versión del sistema de archivos no es compatible")

        volume_label = superblock_data[20:36].decode('ascii')
        cluster_size = struct.unpack('<I', superblock_data[40:44])[0]
        directory_clusters = struct.unpack('<I', superblock_data[45:49])[0]
        total_clusters = struct.unpack('<I', superblock_data[50:54])[0]
        direc_inicio = 1 * cluster_size  # Inicio del directorio
        direct_size = directory_clusters * cluster_size  # Tamaño total del directorio
        entrada_direc_size = 64  # Tamaño de cada entrada de directorio

        return {
            'volume_label': volume_label,
            'cluster_size': cluster_size,
            'directory_clusters': directory_clusters,
            'total_clusters': total_clusters,
            'direc_inicio': direc_inicio,
            'direct_size': direct_size,
            'entrada_direc_size': entrada_direc_size
        }

    def list_contents(self):
        # Listado de los contenidos del directorio del sistema de archivos
        directory_data = b""
        for i in range(self.superblock['directory_clusters']):
            directory_data += self.read_sector(i + 1)
    
        entry_size = 64
        for i in range(0, len(directory_data), entry_size):
            entry = directory_data[i:i + entry_size]
            file_name = entry[1:15].decode().strip()
    
            # Sirve para no mostrar los que no tengan nombre
            if not file_name or file_name == "---------------" or file_name.startswith('.'):
                continue
    
            file_size, cluster_start = struct.unpack('<I', entry[16:20])[0], struct.unpack('<I', entry[20:24])[0]
            creation_time, modification_time = entry[24:38].decode().strip(), entry[38:52].decode().strip()
    
            if file_size > 0 and cluster_start > 0 and creation_time and modification_time:
                print(f"ARCHIVO: {file_name}, TAMAÑO: {file_size}, "
                      f"CLUSTER INICIAL: {cluster_start}, "
                      f"FECHA CREACION: {creation_time}, "
                      f"FECHA MODIFICACION: {modification_time}\n")

    def copy_file_to_system(self, filename):
        # Copia un archivo desde el sistema de archivos FiUnamFS al sistema local
        file_data = self.read_file(filename)
        with open(filename, 'wb') as f:
            f.write(file_data)

    def copy_file_to_fiunamfs(self, filename):
        # Copia un archivo desde el sistema local al sistema de archivos FiUnamFS
        with open(filename, 'rb') as f:
            file_data = f.read()

        free_cluster = self.find_free_cluster()
        if free_cluster is None:
            raise Exception("No hay clusters disponibles")

        self.write_file(filename, file_data, free_cluster)

    def delete_file(self, filename):
        # Elimina un archivo del sistema de archivos FiUnamFS
        entry_index = self.find_file_entry(filename)
        if entry_index is None:
            raise Exception(f"Archivo '{filename}' no encontrado")

        self.mark_file_deleted(entry_index)
        self.release_clusters(filename)

    def get_user_commands(self):
        # Obtiene comandos del usuario y los pone en la cola de comandos
        while self.is_running:
            print("\nOpciones disponibles:")
            print("1. Listar los contenidos del directorio")
            print("2. Copiar un archivo dentro del FiUnamFS hacia el sistema")
            print("3. Copiar un archivo de la computadora hacia el FiUnamFS")
            print("4. Eliminar un archivo del FiUnamFS")
            print("5. Salir del programa")

            command = input("\nElegir opción (1,2,3,4 o 5): ")
            if command == "5":
                self.is_running = False
                self.command_queue.put(("exit", None))
                break

            args = None
            if command in ("2", "3", "4"):
                file_name = input("Ingrese el nombre del archivo: ")
                args = (command, file_name)
            elif command not in ("1", "5"):
                print("Opción no válida")
                continue

            self.command_queue.put(args)

    def process_commands(self):
        # Procesa los comandos encolados, asegurando sincronización con lock
        while self.is_running:
            command_args = self.command_queue.get()
            if command_args is None:
                self.list_contents()
            else:
                command, args = command_args
                with self.lock:
                    if command == "1":
                        self.list_contents()
                    elif command == "2":
                        self.copy_file_to_system(args)
                    elif command == "3":
                        self.copy_file_to_fiunamfs(args)
                    elif command == "4":
                        self.delete_file(args)

            self.command_queue.task_done()

    def main(self):
        # Inicializa y gestiona hilos para obtener y procesar comandos
        producer_thread = threading.Thread(target=self.get_user_commands)
        producer_thread.start()

        consumer_thread = threading.Thread(target=self.process_commands)
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

if __name__ == "__main__":
    fiunamfs = FiUnamFS('fiunamfs.img')
    fiunamfs.main()
