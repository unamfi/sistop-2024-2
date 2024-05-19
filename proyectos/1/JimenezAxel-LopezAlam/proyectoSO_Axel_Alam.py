## Definición de la clase y funcion básica de validación
import os
import struct
from threading import Thread, Lock


class FiUnamFS:
    def __init__(self, filepath):
        # Inicializa la clase con la ruta al archivo del sistema de archivos, establece un bloqueo para acceso concurrente
        # y lee el superbloque (primer cluster de 1024 bytes) para obtener la información inicial del sistema de archivos.
        self.filepath = filepath
        self.filepath = filepath
        self.lock = Lock()
        with open(self.filepath, 'r+b') as f:
            self.superblock = f.read(1024)  # Leer superbloque (primer cluster)

    def validate_fs(self):
        # Valida que el sistema de archivos sea FiUnamFS versión '24-2' leyendo y verificando campos específicos del superbloque.
        # Si no coincide, se lanza una excepción indicando incompatibilidad o corrupción.
        name = struct.unpack('8s', self.superblock[0:8])[0].decode('ascii').strip('\x00')
        version = struct.unpack('5s', self.superblock[10:15])[0].decode('ascii').strip('\x00')
        if name != 'FiUnamFS' or version != '24-2':
            raise ValueError("Sistema de archivos no compatible o corrupto")
    
     
    def list_files(self):
        # Lista los archivos en el directorio principal del FiUnamFS, excluyendo entradas vacías y no utilizadas.
        # Lee las entradas del directorio después de saltar el superbloque.
        with self.lock:
            with open(self.filepath, 'r+b') as f:
                f.seek(1024)  # Posicionarse al inicio del directorio
                entries = []
                for _ in range(64):
                    entry = f.read(64)
                    filename = entry[1:16].decode('ascii', 'ignore').replace('\x00', ' ').strip()
                    if filename and filename != '###############':  # Filtrar entradas vacías y marcadas como no utilizadas
                        entries.append(filename)
        return entries
    

# Copia un archivo desde FiUnamFS al sistema del usuario, buscando por nombre y leyendo su tamaño y posición.
# Es necesario asegurarse que el directorio de destino termine en el separador de carpetas adecuado.
def copy_file_from_fs(fs, filename, destination_dir):
    with fs.lock:
        with open(fs.filepath, 'rb') as disk:
            disk.seek(1024)  # Saltar superbloque
            for _ in range(64):
                entry = disk.read(64)
                file_name = struct.unpack('15s', entry[1:16])[0].decode('ascii').strip('\x00').strip()
                if file_name == filename.strip():
                    file_size = struct.unpack('<I', entry[16:20])[0]
                    start_cluster = struct.unpack('<I', entry[20:24])[0]
                    start_byte = 1024 * start_cluster
                    disk.seek(start_byte)
                    data = disk.read(file_size)

                    # Asegurarse de que el destino_dir termine con un separador de carpetas
                    if not destination_dir.endswith(os.path.sep):
                        destination_dir += os.path.sep

                    # Construir la ruta completa del archivo de destino
                    destination_file_path = destination_dir + filename.strip()
                    with open(destination_file_path, 'wb') as new_file:
                        new_file.write(data)
                    return "Archivo copiado con exito"
            return "Archivo no encontrado"
# Busca y retorna el índice del primer cluster libre en el disco.
# Comienza la búsqueda después del superbloque y verifica si cada cluster está vacío comparando con una secuencia de ceros.
def find_free_cluster(disk, num_clusters, cluster_size):
    free_cluster = -1
    disk.seek(cluster_size)  # Saltar el superbloque
    for i in range(1, num_clusters):
        disk.seek(cluster_size * i)
        if disk.read(cluster_size) == b'\x00' * cluster_size:
            free_cluster = i
            break
    return free_cluster



# Copia un archivo desde el sistema del usuario al FiUnamFS.
# Primero, verifica la disponibilidad de espacio en el directorio y clusters libres.
# Luego, copia los datos del archivo al cluster libre y actualiza la entrada del directorio.
def copy_file_to_fs(fs, source, filename):
    with fs.lock:
        with open(fs.filepath, 'r+b') as disk:
            disk.seek(0)  # Posicionarse al inicio del archivo para leer el superbloque
            superblock = disk.read(1024)  # Leer el superbloque completo
            
            cluster_size = struct.unpack('<I', superblock[40:44])[0]
            total_clusters = struct.unpack('<I', superblock[50:54])[0]

            disk.seek(1024)  # Posicionarse al inicio del directorio
            empty_entry_index = -1
            for i in range(64):
                entry = disk.read(64)
                file_name = struct.unpack('15s', entry[1:16])[0].decode('ascii').rstrip('\x00').strip()
                print(f"Entry {i}: '{file_name}'")  # Imprime cada nombre de archivo encontrado en el directorio
                if file_name == '##############':  # Usar 14 signos # para estar en línea con los resultados observados
                    empty_entry_index = i
                    break

            if empty_entry_index == -1:
                print("Debug: No space in directory")  # Mensaje de depuración adicional
                return "Sin espacio en el disco"

            free_cluster = find_free_cluster(disk, total_clusters, cluster_size)
            if free_cluster == -1:
                print("Debug: No free cluster available")  # Mensaje de depuración adicional
                return "No hay un cluster libre disponible"

            with open(source, 'rb') as file:
                data = file.read()
                file_size = len(data)

            disk.seek(cluster_size * free_cluster)
            disk.write(data)

            disk.seek(1024 + 64 * empty_entry_index)
            filename_encoded = filename.encode('ascii')
            filename_padded = filename_encoded.ljust(15, b' ')  # Rellenar con espacios si es necesario
            entry_data = struct.pack('<c15sII52s', b'-', filename_padded, file_size, free_cluster, b'\x00' * 52)
            print(f"Writing entry data at index {empty_entry_index}: {entry_data}")  # Debugging output
            disk.seek(1024 + 64 * empty_entry_index)
            disk.write(entry_data)
            
            return "Archivo copiado exitosamente"


# Elimina un archivo de FiUnamFS marcando su entrada de directorio como no utilizada.
# Busca el archivo por nombre, y si lo encuentra, reescribe su entrada en el directorio con un patrón que indica borrado.   
def delete_file(fs, filename):
    filename = filename.strip()  # Asegúrate de que el nombre del archivo no tenga espacios al inicio ni al final
    with fs.lock:
        with open(fs.filepath, 'r+b') as disk:
            disk.seek(1024)  # Saltar el superbloque
            for i in range(64):
                entry = disk.read(64)
                file_name = entry[1:16].decode('ascii').replace('\x00', '').strip()
                if file_name == filename:
                    disk.seek(1024 + 64 * i)
                    # Escribir exactamente 64 bytes, llenando con ceros después de '/###############'
                    disk.write(b'/###############' + b'\x00' * (64 - 17))  # Asegura exactamente 64 bytes
                    return "Archivo borrado exitosamente"
            return "Archivo no encontrado"

# Ejecuta tareas especificadas (listar, copiar desde/hacia FS, eliminar) en un hilo separado.
# Esto permite realizar operaciones de I/O sin bloquear la interfaz de usuario principal.
def threaded_task(fs, task, *args):
    if task == "list":
        print("\nListando archivos...")
        print(fs.list_files())
    elif task == "copy_from_fs":
        filename, destination = args
        print(f"\Copiando {filename} desde FS a {destination}...")
        print(copy_file_from_fs(fs, filename, destination))
    elif task == "copy_to_fs":
        source, filename = args
        print(f"\Copiando {source} a FS desde {filename}...")
        print(copy_file_to_fs(fs, source, filename))
    elif task == "delete":
        filename = args[0]
        print(f"\Borrando {filename}...")
        print(delete_file(fs, filename))


def main_menu(fs):
    # Presenta un menú continuo que permite al usuario interactuar con el sistema FiUnamFS a través de varias opciones.
    # Utiliza hilos para gestionar las operaciones sin bloquear la interacción del usuario con el menú.
    while True:
        print("\nMenu:")
        print("Nota: El formato para pasar la ruta debe ser C:\\Users\\YourUsername\\Desktop--ComoEjemplo\\Carpeta\\nombreArchivo.terminacion")
        print("1. Listar los contenidos del directorio")
        print("2. Copiar un archivo del FiUnamFS a tu sistema")
        print("3. Copiar un archivo de tu computadora al FiUnamFS")
        print("4. Eliminar un archivo del FiUnamFS")
        print("5. Salir")
        choice = input("Ingrese su elección: ")

        if choice == '1':
            thread = Thread(target=threaded_task, args=(fs, "list"))
            thread.start()
            thread.join()
        elif choice == '2':
            filename = input("Ingrese el nombre del archivo a copiar del FiUnamFS: ")
            destination = input("Ingrese la ruta de destino en su sistema: ")
            thread = Thread(target=threaded_task, args=(fs, "copy_from_fs", filename, destination))
            thread.start()
            thread.join()
        elif choice == '3':
            source = input("Ingrese la ruta del archivo en su sistema para copiar al FiUnamFS: ")
            filename = input("Ingrese el nombre bajo el cual guardar el archivo en el FiUnamFS: ")
            thread = Thread(target=threaded_task, args=(fs, "copy_to_fs", source, filename))
            thread.start()
            thread.join()
        elif choice == '4':
            filename = input("Ingrese el nombre del archivo a eliminar del FiUnamFS: ")
            thread = Thread(target=threaded_task, args=(fs, "delete", filename))
            thread.start()
            thread.join()
        elif choice == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor intente de nuevo.")


if __name__ == "__main__":
    ##El path depende del sistema, para este caso se utilizó WINDOWS
    fs = FiUnamFS(r'C:\Users\AlamLR\Desktop\proyectoSO\fiunamfs.img')
    fs.validate_fs()
    main_menu(fs)

