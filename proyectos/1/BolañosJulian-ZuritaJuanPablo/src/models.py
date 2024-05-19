import os
import math
import struct
from datetime import datetime

class File():

    def __init__(self, name:str, size:int, initial_cluster:int, creation_date:str, update_date:str) -> None:
        self.name = name
        self.size = size
        self.initial_cluster = initial_cluster
        self.creation_date = self._formatDate(creation_date)
        self.update_date = self._formatDate(update_date)
        self.cluster_size = 2048
    
    def __str__(self) -> str:
        return self.name


    '''Formatea la fecha a un formato AAAA-MM-DD HH:MM:SS 
       por ejemplo 20221108182600 para 2022-11-08 18:26:00 '''
    def _formatDate(self, date:str) -> str:
        # Obtener los componentes de la fecha
        year = date[:4]
        month = date[4:6]
        day = date[6:8]
        hour = date[8:10]
        minute = date[10:12]
        second = date[12:14]

        # Formatear la fecha en el nuevo formato
        new_date = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        return new_date
    

    '''Obtiene el contenido del archivo en el directorio 'FiUnamFS' '''
    def _getFileContent(self):
        start = self.initial_cluster * self.cluster_size
        
        try:
            # Si la lectura es correcta se retorna el contenido leído 'content'
            # si presenta fallos en el proceso retorna 'None'
            with open('fiunamfs.img', 'rb') as FiUnamFS:
                FiUnamFS.seek(start)
                content = FiUnamFS.read(self.size + 1)
            
            return content
        except:
            return None
    

    '''Realiza una copia del archivo en 'FiUnamFS' hacia la computadora local.
       Retorna 'True' si la copia ha sido exitosa, 'False' si no ha sido así.'''
    def copyToSystem(self, path:str) -> bool:

        if not os.path.exists(path + f'/{self.name}'):
            content = self._getFileContent()

            try:
                with open(path + f'/{self.name}', 'wb') as new_file:
                    new_file.write(content)
                return True
            except:
                return False
    
    '''Retorna una tupla, en la primer pocisión existe el número de clusters que 
       ocupa el archivo, en la segunda pocisión existe una lista con los clusters usados. '''
    def getClustersTaken(self) -> tuple[int, list]:

        clusters_taken = []
        num_clusters_taken = math.ceil(self.size / self.cluster_size)

        for i in range(self.initial_cluster, self.initial_cluster + num_clusters_taken):
            clusters_taken.append(i)

        return (num_clusters_taken, clusters_taken)


class FiUnamFS():

    def __init__(self, path:str, directory_entry_size:int):
        self.path = path
        self.system_name = self._readStrFromFS(0,8)
        self.version = self._readStrFromFS(10, 4)
        self.volumen_label = self._readStrFromFS(20, 15)
        self.cluster_size = self._readIntFromFS(40, 4)
        self.num_clusters = self._readIntFromFS(45, 4)
        self.num_total_clusters = self._readIntFromFS(50, 4)
        self.directory_entry_size = directory_entry_size
    
    def __str__(self) -> str:
        return self.system_name
    
    def showDetails(self) -> None:
        print(f'Nombre Directorio: {self.system_name}\n' +
              f'Version: {self.version}\n' +
              f'Etiqueta de Volumen: {self.volumen_label}\n' +
              f'Tamaño de Cluster: {self.cluster_size}\n' +
              f'Num de Clusters: {self.num_clusters}\n' +
              f'Num Total de Clusters: {self.num_total_clusters}'
            )
    
    def _readIntFromFS(self, start:int, reading_size:int):
           
        with open(self.path, 'rb') as fs:
            fs.seek(start)
            content = fs.read(reading_size)
            c, = struct.unpack('<I', content)
            return c
       
    def _readStrFromFS(self, start:int, reading_size:int):

        with open(self.path, 'rb') as fs:
            fs.seek(start)
            content = fs.read(reading_size)
            return content.decode('ascii').strip()
        
    ''' 'readDirectory' retorna un dato de tipo <str> o bien <int> decimal según 
        lo que encuentre en el directorio mediante una lectura en modo binario a 
        partir una posición y desplazamiento definidos. '''
    # def _readDirectory(self, start:int, reading_size:int):

    #     with open(self.path, 'rb') as _FiUnamFS:
    #         _FiUnamFS.seek(start)
    #         content = _FiUnamFS.read(reading_size)

    #     try:
    #         c, = struct.unpack('<I', content)
    #         return c
        
    #     except:
    #         return content.decode('ascii')
    

    '''Retorna una lista de objetos 'File' equivalentes a los archivos (entradas)
       contenidos en el directorio.'''
    def getFiles(self) -> list:

        num_files = (self.cluster_size * self.num_clusters) // self.directory_entry_size
        files = []

        for i in range(num_files):
            start = self.cluster_size + (i * self.directory_entry_size)
            file_name = self._readStrFromFS(start, 15)
            
            if '-' in file_name:            
                files.append(
                    File(
                        name = file_name[1:].strip(),
                        size = self._readIntFromFS(start + 16, 4),
                        initial_cluster = self._readIntFromFS(start + 20, 4),
                        creation_date = self._readStrFromFS(start + 24, 13),
                        update_date = self._readStrFromFS(start + 38, 13)
                    )
                )
        
        return files
    
    '''Copia un archivo de fuera del directorio 'FiUnamFS' hacia dentro de
       este mismo, requiere la ubicación del archivo en la computadora
       incluyendo el nombre del archivo a copiar ej: '/d:archivos/archivo.jpg'''
    def copyFromSystem(self, path:str):

        # Revisamos que al archivo exista
        if not os.path.exists(path):
            return False
        
        # Tamaño del archivo a copiar
        new_file_size = os.path.getsize(path)

        # Obtenemos el cluster inicial de donde se comenzará a
        # alamacenar el contenido del archivo a copiar.
        initial_cluster = self._searchSpace(new_file_size)

        if initial_cluster != None:
            # Movemos nuestro 'apuntador' a donde inicia el cluster obtenido
            # (cluster inicial * tamaño de cluster)
            start = self.cluster_size * initial_cluster
            content = self._getContentFile(path)

            try:
                with open(self.path, 'rb+') as new_file:
                    new_file.seek(start)
                    new_file.write(content)
                
                # Si se copio con éxito
                self._insertIntoDirectory(path, initial_cluster)
                return True
            except:
                print('Error al copiar contenido.')
                return False
            
        print('No existe espacio suficiente para copiar el archivo.')
        return False


    def _searchSpace(self, new_file_size:int):

       files_in_fiunamfs = self.getFiles()
       clusters_taken = []
       all_clusters = [i for i in range(self.num_total_clusters)]
       necessary_clusters = math.ceil(new_file_size / self.cluster_size)
       
       for file in files_in_fiunamfs:
           clusters_taken.extend(file.getClustersTaken()[1])
       
       # Elimina de 'all_clusters' todos aquellos clusters que esten ocupados. 
       all_clusters.remove(0)
       all_clusters.remove(1)
       all_clusters.remove(2)
       all_clusters.remove(3)
       all_clusters.remove(4)
       for i in clusters_taken:
           if i in all_clusters:
               all_clusters.remove(i)

       # Buscamos una cantidad de clusters consecutivos del tamaño
       # necesario para almacenar el archivo nuevo (necessary_clusters).
       index = self._consecutiveSequence(all_clusters, necessary_clusters)
       if index != None:
           
           # Retorna el que deberá ser el cluster inicial
           return all_clusters[index]
       
       return None
           
        
    '''Busca una secuencia consecutiva de números en una lista, si la busqueda
       es exitosa retorna el índice de la lista donde inicia la secuencia.'''
    def _consecutiveSequence(self, lista, n):

        for i in range(len(lista) - n + 1):
            if all(lista[i + j] == lista[i] + j for j in range(n)):
                return i
              
        # Si no se encuentra ninguna secuencia consecutiva, devuelve None
        return None
    

    '''Obtiene el contenido de un archivo leído en modo binario. El archivo
       que se lee, es ajeno al directorio 'FiUnamFS', es decir, se encuentra
       fuera de este.'''
    def _getContentFile(self, path):
        
        try:
            with open(path, 'rb') as file:
                content = file.read()
            return content
        
        except:
            return None
    

    '''Inserta dentro del directorio 'FiUnamFS' los datos de entrada del archivo
       a copiar, busca espacio disponible entre los cluster 1-4.'''
    def _insertIntoDirectory(self, path:str, cluster:int) -> bool:

        # Buscamos algún espacio (64 bytes) para colocar la esntrada
        num_files = (self.cluster_size * self.num_clusters) // self.directory_entry_size
        start = self.cluster_size
        
        for i in range(num_files):   
            file_name = self._readStrFromFS(start + (i * self.directory_entry_size), 15)
            
            if '/' in file_name:

                # Si hay espacio disponible, entences obtenemos los datos del
                # archivo que está en la computadora
                name = ('-' + os.path.basename(path))
                
                # En el ciclo for agregamos el caracter 'espacio' para
                # completar el tamaño indicado de bytes
                for j in range(15 - len(name)):
                    name = name + ' '
                name = name.encode('utf-8')
                
                # Obtebenos el tamaño del archivo
                size = struct.pack('<I', os.path.getsize(path))
                initial_cluster = struct.pack('<I', cluster)

                # Obtener la fecha de creación del archivo y formatearla
                initial_date = datetime.fromtimestamp(os.path.getctime(path)).strftime('%Y%m%d%H%M%S').encode('utf-8')

                # Obtener la fecha de última modificación del archivo y formatearla
                update_date = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y%m%d%H%M%S').encode('utf-8')

                start = self.cluster_size + (i * self.directory_entry_size)
                with open(self.path, 'rb+') as _FiUnamFS:
                    _FiUnamFS.seek(start, 0)
                    _FiUnamFS.write(name)

                    _FiUnamFS.seek(start + 16, 0)
                    _FiUnamFS.write(size)

                    _FiUnamFS.seek(start + 20, 0)
                    _FiUnamFS.write(initial_cluster) 

                    _FiUnamFS.seek(start + 24, 0)
                    _FiUnamFS.write(initial_date)  

                    _FiUnamFS.seek(start + 38, 0)
                    _FiUnamFS.write(update_date)

                break

    
    def deleteFile(self, file_name:str) -> bool:

        # Validamos que el archivo exista en 'FiUnamFS'.
        files_in_directory = self.getFiles()
        for file in files_in_directory:
            if file.name == file_name:
                
                num_files = (self.cluster_size * self.num_clusters) // self.directory_entry_size
                start = self.cluster_size

                # Eliminamos la entrada de cada archivo
                for i in range(num_files):
                    file_to_delete = self._readStrFromFS(start + (i * self.directory_entry_size), 15)

                    if file_name == file_to_delete[1:].strip():
                        
                        try:
                            with open(self.path, 'rb+') as _FiUnamFS:
                                _FiUnamFS.seek(start + (i * self.directory_entry_size))
                                _FiUnamFS.write('/##############'.encode('utf-8'))
                            
                            return True
                        except:
                            return False
        
        # Si el archivo a eliminar no existe en el directorio
        return False


def system_validation(path:str) -> bool:

    with open(path, 'rb') as fs:
        fs.seek(0)
        content = fs.read(8)
        system_name = content.decode('ascii')

        if system_name == 'FiUnamFS':

            fs.seek(10)
            content = fs.read(4)
            version = content.decode('ascii')

            if version == '24-2':
                return True
            else:
                return False
        else:
            return False