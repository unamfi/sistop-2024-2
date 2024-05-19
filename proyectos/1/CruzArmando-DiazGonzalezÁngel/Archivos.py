import threading
import struct
import queue
import os

class FiUnamFS:
    # Definición de constantes del sistema de archivos
    SECTOR_SIZE = 1024
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
        direct_size = 4 * cluster_size  # Tamaño total del directorio
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
            file_type = entry[0:1]
            file_name = entry[1:16].decode('ascii').strip()
            file_size, = struct.unpack('<I', entry[16:20])
            cluster_start, = struct.unpack('<I', entry[20:24])
            creation_time = entry[24:38].decode('ascii').strip()
            modification_time = entry[38:52].decode('ascii').strip()

            # Filtrar entradas vacías o no válidas
            if not file_name or file_name == "---------------" or file_name.startswith('.'):
                continue

            if file_size > 0 and cluster_start > 0 and creation_time and modification_time:
                # Mostrar información del archivo
                print(f"ARCHIVO: {file_name}, TAMAÑO: {file_size}, "
                      f"CLUSTER INICIAL: {cluster_start}, "
                      f"FECHA CREACION: {creation_time}, "
                      f"FECHA MODIFICACION: {modification_time}\n")

    def copy_file_to_system(self, filename, destination_path):
        # Copia un archivo desde el sistema de archivos FiUnamFS al sistema local
        print(f"Copying {filename} to {destination_path}...")
        direc_inicio = self.superblock['direc_inicio']  # Punto de inicio del directorio en el sistema de archivos
        direct_size = self.superblock['direct_size']  # Tamaño total del directorio en bytes
        entrada_direc_size = self.superblock['entrada_direc_size']  # Tamaño de cada entrada de directorio en bytes
        cluster_size = self.superblock['cluster_size']  # Tamaño de un clúster en bytes
        
        with open(self.disk_file, 'rb') as f:
            f.seek(direc_inicio)  # Mover a la posición del inicio del directorio
            directory_data = f.read(direct_size)  # Leer los datos del directorio
            encontrado = False  # Bandera para indicar si se encuentra el archivo en el directorio
            
            # Buscar el archivo en el directorio
            for i in range(0, direct_size, entrada_direc_size):
                entrada = directory_data[i:i + entrada_direc_size]  # Obtener la entrada de directorio actual
                nombre_archivo = entrada[1:15].decode().strip()  # Nombre del archivo en la entrada
                tamano_archivo, cluster_start = struct.unpack('<I', entrada[16:20])[0], struct.unpack('<I', entrada[20:24])[0]  # Tamaño y cluster de inicio del archivo
    
                # Verificar si la entrada corresponde al archivo buscado
                if nombre_archivo == filename and tamano_archivo > 0:
                    encontrado = True
                    break
            
            # Si el archivo no se encuentra en el directorio, mostrar un mensaje y salir
            if not encontrado:
                print(f"Archivo '{filename}' no encontrado en FiUnamFS")
                return
            
            start_point = cluster_start * cluster_size  # Calcular el punto de inicio del archivo en el disco
            f.seek(start_point)  # Mover el puntero del archivo al inicio del archivo
            datos_archivo = f.read(tamano_archivo)  # Leer los datos del archivo
            
            # Escribir los datos del archivo en el destino del sistema local
            with open(destination_path, 'wb') as archivo:
                archivo.write(datos_archivo)
            
            print(f"Archivo '{filename}' copiado a '{destination_path}'.")


    def copy_file_to_fiunamfs(self, filename, origin_path):
        # Copia un archivo desde el sistema local al sistema de archivos FiUnamFS
        with open(self.disk_file, 'r+b') as f:
            tamano_o = os.path.getsize(filename)  # Obtener el tamaño del archivo a copiar
            cluster_libre = 5  # Número de clúster inicial para buscar espacio libre
            posicion_entrada_libre = None  # Inicializar la posición de la entrada de directorio libre
            
            f.seek(self.superblock['direc_inicio'])  # Mover el puntero al inicio del directorio
            for i in range(self.superblock['direct_size'] // self.FILE_ENTRY_SIZE):
                posicion_actual = f.tell()  # Guardar la posición actual
                entrada = f.read(self.FILE_ENTRY_SIZE)  # Leer una entrada de directorio
                tipo_archivo = entrada[0:1]  # Obtener el tipo de archivo
                cluster_ini = struct.unpack('<I', entrada[20:24])[0]  # Obtener el número de clúster inicial
                
                # Verificar si la entrada es libre y guardar su posición si es necesario
                if tipo_archivo == b'/' and posicion_entrada_libre is None:
                    posicion_entrada_libre = posicion_actual
                    print(f"Hay posición en {posicion_entrada_libre}")
    
                # Actualizar el número de clúster libre máximo encontrado
                if cluster_ini >= cluster_libre:
                    cluster_libre = cluster_ini + 1
                    print(f"Nuevo cluster libre: {cluster_libre}")
    
            # Verificar si se encontró espacio libre para el archivo
            if posicion_entrada_libre is None:
                raise Exception("No hay espacio")
            else:
                print(f"Espacio libre en: {posicion_entrada_libre}, Cluster libre para el archivo: {cluster_libre}")
    
            # Escribir los datos del archivo en el sistema de archivos FiUnamFS
            with open(filename, 'rb') as archivo_origen_f:
                data = archivo_origen_f.read()  # Leer los datos del archivo
                f.seek(cluster_libre * self.CLUSTER_SIZE)  # Mover el puntero al inicio del clúster libre
                f.write(data)  # Escribir los datos del archivo en el clúster libre
    
            nombre_destino = os.path.basename(filename)  # Obtener el nombre del archivo
            f.seek(posicion_entrada_libre)  # Mover el puntero a la posición de la entrada libre
            f.write(b'-' + nombre_destino.ljust(15).encode('ascii'))  # Escribir el nombre del archivo en la entrada
            f.write(struct.pack('<I', tamano_o))  # Escribir el tamaño del archivo en la entrada
            f.write(struct.pack('<I', cluster_libre))  # Escribir el número de clúster inicial en la entrada
    

    def delete_file(self, filename):
        # Elimina un archivo del sistema de archivos FiUnamFS
        direc_inicio = self.superblock['direc_inicio']  # Obtener el inicio del directorio
        entrada_direc_size = self.superblock['entrada_direc_size']  # Obtener el tamaño de la entrada de directorio
        cluster_size = self.CLUSTER_SIZE  # Obtener el tamaño del clúster
        
        with open(self.disk_file, 'r+b') as f:
            f.seek(direc_inicio)  # Mover el puntero al inicio del directorio
            for _ in range(cluster_size // entrada_direc_size):
                posicion = f.tell()  # Guardar la posición actual
                entrada = f.read(entrada_direc_size)  # Leer una entrada de directorio
                nombre = entrada[1:16].decode('ascii').rstrip()  # Obtener el nombre del archivo
                
                # Verificar si la entrada corresponde al archivo buscado
                if nombre.rstrip('\x00').strip() == filename.rstrip('\x00').strip():
                    f.seek(posicion)  # Mover el puntero a la posición de la entrada
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
    
            command = input("\nElegir opción (1,2,3,4 o 5): ")  # Solicitar al usuario que elija una opción
            if command == "5":
                self.is_running = False  # Marcar que el programa debe finalizar
                self.command_queue.put(("exit", None))  # Poner una señal de salida en la cola de comandos
                break
    
            args = None
            if command in ("2", "3", "4"):  # Si el comando requiere argumentos
                file_name = input("Ingrese el nombre del archivo: ")  # Solicitar al usuario el nombre del archivo
                if command == "2":
                    destination_path = input("Ingrese la ruta de destino en su sistema (incluyendo el nombre del archivo): ")
                    args = (file_name, destination_path)
                elif command == "3":
                    origin_path = input("Ingrese la ruta de origen en su sistema (incluyendo el nombre del archivo): ")
                    args = (file_name, origin_path)
                else:
                    args = (file_name,)
            elif command not in ("1", "5"):
                print("Opción no válida")  # Notificar al usuario si la opción elegida no es válida
                continue
    
            self.command_queue.put((command, args))  # Poner el comando y sus argumentos en la cola de comandos


    def process_commands(self):
        # Procesa los comandos encolados, asegurando sincronización con lock
        while self.is_running:
            command_args = self.command_queue.get()  # Obtener el siguiente comando de la cola de comandos
            if command_args is None:
                self.list_contents()  # Si no hay comando, listar el contenido del directorio
            else:
                command, args = command_args
                with self.lock:  # Asegurar que solo un hilo ejecute el bloque de código a la vez
                    if command == "1":
                        self.list_contents()  # Si el comando es listar, mostrar el contenido del directorio
                    elif command == "2":
                        filename, destination_path = args
                        self.copy_file_to_system(filename, destination_path)  # Copiar archivo del FiUnamFS al sistema
                    elif command == "3":
                        filename, origin_path = args
                        self.copy_file_to_fiunamfs(filename, origin_path)  # Copiar archivo del sistema al FiUnamFS
                    elif command == "4":
                        filename, = args
                        self.delete_file(filename)  # Eliminar archivo del FiUnamFS
    
            self.command_queue.task_done()  # Indicar que la tarea del comando ha sido completada


    def main(self):
        # Inicializa y gestiona hilos para obtener y procesar comandos
        producer_thread = threading.Thread(target=self.get_user_commands)  # Hilo para obtener comandos del usuario
        producer_thread.start()  # Iniciar el hilo
    
        consumer_thread = threading.Thread(target=self.process_commands)  # Hilo para procesar comandos
        consumer_thread.start()  # Iniciar el hilo
    
        producer_thread.join()  # Esperar a que el hilo de obtención de comandos termine
        consumer_thread.join()  # Esperar a que el hilo de procesamiento de comandos termine

if __name__ == "__main__":
    fiunamfs = FiUnamFS('fiunamfs.img')  # Crear una instancia de FiUnamFS con el archivo de imagen
    fiunamfs.main()  # Llamar al método principal para iniciar el programa
