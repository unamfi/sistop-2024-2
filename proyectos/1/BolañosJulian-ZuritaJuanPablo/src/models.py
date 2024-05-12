import os
import math

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
            '''Si la lectura es correcta se retorna el contenido leído 'content'
               si presenta fallos en el proceso retorna 'None' '''
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