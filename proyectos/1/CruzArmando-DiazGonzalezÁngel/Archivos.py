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
        superblock_data = self.read_sector(0)  # Leer el primer sector donde se encuentra el superbloque
        identifier = superblock_data[0:9].decode('ascii').strip('\x00')  # Identificador del sistema de archivos
        version = superblock_data[10:15].decode('ascii').strip('\x00')  # Versión del sistema de archivos
        if identifier != "FiUnamFS":
            raise Exception("El sistema de archivos no es FiUnamFS")
        if version != "24-2":
            raise Exception("La versión del sistema de archivos no es compatible")

        # Extraer información del superbloque
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
            directory_data += self.read_sector(i + 1)  # Leer todos los sectores del directorio
    
        entry_size = 64  # Tamaño de cada entrada de directorio
        for i in range(0, len(directory_data), entry_size):
            entry = directory_data[i:i + entry_size]
            file_name = entry[1:15].decode().strip()
    
            # Filtrar entradas vacías o no válidas
            if not file_name or file_name == "---------------" or file_name.startswith('.'):
                continue
    
            # Extraer información del archivo
            file_size, cluster_start = struct.unpack('<I', entry[16:20])[0], struct.unpack('<I', entry[20:24])[0]
            creation_time, modification_time = entry[24:38].decode().strip(), entry[38:52].decode().strip()
    
            if file_size > 0 and cluster_start > 0 and creation_time and modification_time:
                # Mostrar información del archivo
                print(f"ARCHIVO: {file_name}, TAMAÑO: {file_size}, "
                      f"CLUSTER INICIAL: {cluster_start}, "
                      f"FECHA CREACION: {creation_time}, "
                      f"FECHA MODIFICACION: {modification_time}\n")

    def copy_file_to_system(self, filename, destination_path):
        # Copia un archivo desde el sistema de archivos FiUnamFS al sistema local
        print(f"Copiando {filename} a {destination_path}...")
        direc_inicio = self.superblock['direc_inicio']
        direct_size = self.superblock['direct_size']
        entrada_direc_size = self.superblock['entrada_direc_size']
        cluster_size = self.superblock['cluster_size']
        
        with open(self.disk_file, 'rb') as f:
            f.seek(direc_inicio)  # Mover a la posición del inicio del directorio
            directory_data = f.read(direct_size)
            encontrado = False
            
            for i in range(0, direct_size, entrada_direc_size):
                entrada = directory_data[i:i + entrada_direc_size]
                nombre_archivo = entrada[1:15].decode().strip()
                tamano_archivo, cluster_start = struct.unpack('<I', entrada[16:20])[0], struct.unpack('<I', entrada[20:24])[0]

                if nombre_archivo == filename and tamano_archivo > 0:
                    encontrado = True
                    break
            if not encontrado:
                print(f"Archivo '{filename}' no encontrado en FiUnamFS")
                return
            start_point = cluster_start * cluster_size  # Calcular el punto de inicio del archivo
            f.seek(start_point)
            datos_archivo = f.read(tamano_archivo)
            
            # Escribir los datos del archivo en el destino del sistema local
            with open(destination_path, 'wb') as archivo:
                archivo.write(datos_archivo)
            
            print(f"Archivo '{filename}' copiado exitosamente a '{destination_path}'.")

    def copy_file_to_fiunamfs(self, filename):
        # Copia un archivo desde el sistema local al sistema de archivos FiUnamFS
        free_cluster = self.find_free_cluster()  # Encontrar un cluster libre
        if free_cluster is None:
            raise Exception("No hay clusters disponibles")

        # Lógica para escribir el archivo en el sistema de archivos FiUnamFS

    def delete_file(self, filename):
        # Elimina un archivo del sistema de archivos FiUnamFS
        direc_inicio = self.superblock['direc_inicio']
        entrada_direc_size = self.superblock['entrada_direc_size']
        cluster_size = self.CLUSTER_SIZE
        with open(self.disk_file, 'r+b') as f:
            f.seek(direc_inicio)  # Mover a la posición del inicio del directorio
            for _ in range(cluster_size // entrada_direc_size):
                posicion = f.tell()  # Guardar la posición actual
                entrada = f.read(entrada_direc_size)
                nombre = entrada[1:16].decode('ascii').rstrip()
                if nombre.rstrip('\x00').strip() == filename.rstrip('\x00').strip():
                    f.seek(posicion)
                    # Marcar la entrada como eliminada
                    f.write(b'/' + b' ' * 15)
                    print("Archivo eliminado de FiUnamFS")
                    return
        print("Archivo no encontrado en FiUnamFS")

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
                if command == "2":
                    destination_path = input("Ingrese la ruta de destino en su sistema (incluyendo el nombre del archivo): ")
                    args = (file_name, destination_path)
                else:
                    args = (file_name,)
            elif command not in ("1", "5"):
                print("Opción no válida")
                continue

            self.command_queue.put((command, args))

    def process_commands(self):
        # Procesa los comandos encolados, asegurando sincronización con lock
        while self.is_running:
            command_args = self.command_queue.get()
            if command_args is None:
                self.list_contents()
            else:
                command, args = command_args
                with self.lock:  # Asegura que solo un hilo ejecute el bloque de código a la vez
                    if command == "1":
                        self.list_contents()
                    elif command == "2":
                        filename, destination_path = args
                        self.copy_file_to_system(filename, destination_path)
                    elif command == "3":
                        self.copy_file_to_fiunamfs(args)
                    elif command == "4":
                        filename, = args
                        self.delete_file(filename)

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

