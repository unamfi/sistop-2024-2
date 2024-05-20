from math import ceil
import os
from datetime import datetime
from struct import pack, unpack
import sys
from PyInquirer import prompt
from rich import print as richPrint
from copy import deepcopy
from rich.console import Console
from rich.table import Table
from rich.pretty import pprint
from rich.panel import Panel
class Disc:
    def __init__(self,filePath):
        try:
            self.file = open(filePath, 'r+b')
        except:
            raise Exception('No se pudo abrir el archivo')
    def close(self):
        self.file.close()
    def write(self, start, bytes):
        if start < 0:
            raise Exception('No se puede escribir un archivo con un indice negativo')
        if start + bytes.__len__() > self.file.seek(0, 2):
            raise Exception('No se puede escribir un archivo con un indice mayor al tamaño del archivo')
        self.file.seek(start)
        self.file.write(bytes)

    def read(self, start, numBytes):
        if start < 0:
            raise Exception('No se puede leer un archivo con un indice negativo')
        if numBytes < 0:
            raise Exception('No se puede leer un archivo con un numero de bytes negativo')
        if start + numBytes > self.file.seek(0, 2):
            raise Exception('No se puede leer un archivo con un indice mayor al tamaño del archivo')
        self.file.seek(start)
        return self.file.read(numBytes)


class FileData:
    def __init__(self, bytes: bytes, addressInDirectory):
        if bytes.__len__() > 64:
            raise Exception('La metainformación del archivo no puede ser mayor a 64 bytes')
        self.data = {
            'type': bytes[0:1].decode(encoding='ascii'),
            'name': bytes[1:16].decode(encoding='ascii'),
            'size': int(unpack('<I', bytes[16:20])[0]),
            'cluster': int(unpack('<I', bytes[20:24])[0]),
            'end_cluster': int(unpack('<I', bytes[20:24])[0]) + ceil(int(unpack('<I', bytes[16:20])[0]) / 2048) - 1,
            'date': bytes[24:38].decode(encoding='ascii'),
            'last_modification': bytes[38:52].decode(encoding='ascii'),
            'address_in_directory': addressInDirectory
        }
    def empty(self):
        return self.data['type'] == '/'
    def __str__(self):
        return f"{self.data['name']} {self.data['size']} {self.data['date']} {self.data['last_modification']}"
    def __repr__(self):
        return self.__str__()
    def getData(self):
        return deepcopy(self.data)

class Directory:
    def __init__(self, bytes: bytes,sizeFileData=64,sizeCluster=2048):
        if bytes.__len__() % sizeFileData != 0:
            raise Exception('El directorio no tiene un tamaño correcto')
        if bytes.__len__() % sizeCluster != 0:
            raise Exception('El directorio no tiene un tamaño correcto')
        self.files = [FileData(bytes[i:i+sizeFileData],i) for i in range(0, bytes.__len__(), 64)]

class FileSystemFiUNAMFS:
    def bitMap(self):
        bitMap = [1,1,1,1]
        previous = 4
        files = sorted(self.getFiles(),key= lambda file: file.getData()['cluster'])
        for file in files:
            if not file.empty():
                cluster = file.getData()['cluster']
                if cluster < previous:
                    raise Exception('El cluster del archivo no puede ser menor al cluster anterior')
                bitMap += [0] * (cluster - previous)
                numClusters = ceil(file.getData()['size'] / self.specifications['sizeCluster'])
                bitMap += [1] * numClusters
                previous = cluster + numClusters
        bitMap += [0] * (self.specifications['totalClusters'] - previous)
        return bitMap
    def __init__(self,disc:Disc):
        self.disc = disc

        self.specifications = {
            'system': self.disc.read(0,8).decode(encoding='ascii'),
            'version': self.disc.read(10,4).decode(encoding='ascii'),
            'volumen_label': self.disc.read(20,15).decode(encoding='ascii'),
            'sizeCluster': int(unpack('<I', self.disc.read(40,4))[0]),
            'numClusters': int(unpack('<I', self.disc.read(45,4))[0]),
            'totalClusters': int(unpack('<I', self.disc.read(50,4))[0]),
            'cluster_directory': 1,
            'size_cluster_directory': 3,
            'sizeFileData': 64,
            'bitMap': []
        }
        self.specifications['bitMap'] = self.bitMap()
        spec = self.specifications
        if spec['version'] != '24-2':
            raise Exception('La versión del sistema de archivos no es compatible')
        if spec['system'] != 'FiUnamFS':
            raise Exception('El sistema de archivos no es compatible')
        
        self.preprocessToShowFields = {
            'name': lambda name : name.rstrip().rstrip('\x00').strip() if name != None else '',
            'size': lambda size: f"{size}(B)",
            'cluster': lambda cluster:f"#{cluster}" if cluster != None else '',
            'date': lambda date: datetime.strptime(date,"%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S"),
            'address_in_directory': lambda address: f"{address}",
            'last_modification': lambda last_mod : datetime.strptime(last_mod,"%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S"),
            'end_cluster': lambda end_cluster: f"#{end_cluster}"
        }
    def getCluster(self, numCluster):
        if numCluster < 0:
            raise Exception('No se puede leer un cluster con un indice negativo')
        if numCluster > self.specifications['totalClusters']:
            raise Exception('No se puede leer un cluster con un indice mayor al total de clusters')
        position = self.specifications['sizeCluster'] * numCluster
        return self.disc.read(position, self.specifications['sizeCluster'])
    def getClusters(self, startCluster, numClusters):
        return  bytes(sum([list(self.getCluster(startCluster + i)) for i in range(numClusters)], []))
    def clean(self):
        if self.disc != None:
            self.disc.close()
    def getFiles(self):
        return Directory(self.getClusters(1,3)).files
    def findEmptyClusters(self):
        bitMap = self.specifications['bitMap']
        segments = []
        start = None
        length = 0
        for i, bit in enumerate(bitMap):
            if bit == 0 and start is None:
                start = i
                length = 1
            elif bit == 0 and start is not None:
                length += 1
            elif bit != 0 and start is not None:
                segments.append((start, length))
                start = None
        if start is not None:
            segments.append((start, length))
        return segments

    def copyInside(self, absPath):
        files = sorted(self.getFiles(),key= lambda file: file.getData()['address_in_directory'])
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        name = os.path.basename(absPath)
        if len(name) > 14:
            name = name[:15]
        name = name.ljust(15,' ')
        name = name[:-1] + '\x00'
        size = os.path.getsize(absPath)
        binaryContent = open(absPath,'rb').read()
        numClusters = ceil(size / self.specifications['sizeCluster'])
        i = 0
        while not files[i].empty():
            i += 1
            if i >= files.__len__():
                raise Exception('No hay espacio en el directorio')
        adreesToAllocateInDirectory = i * self.specifications['sizeFileData'] + (self.specifications['sizeCluster'] * self.specifications['cluster_directory'])
        emptyClusters = [segment for segment in self.findEmptyClusters() if segment[1] >= numClusters]
        if emptyClusters.__len__() == 0:
            return richPrint(Panel("[red]No hay suficiente espacio en el disco[/red]",title="Error",expand=False))
        cluster = emptyClusters[0][0]
        base = cluster * self.specifications['sizeCluster']
        b = b''.join([b'\x2d',name.encode(encoding='ascii'),pack('<I',size),pack('<I',cluster),date.encode(encoding='ascii'),date.encode(encoding='ascii'),b'\x00'*12])
        self.disc.write(adreesToAllocateInDirectory,b)
        self.disc.write(base,binaryContent)
        for i in range(cluster,cluster + numClusters):
            self.specifications['bitMap'][i] = 1
    def deleteFile(self, name):
        files = self.getFiles()
        for file in files:
            if file.empty():
                continue
            fileData = file.getData()
            if fileData['name'] == name:
                base =  fileData['address_in_directory'] + self.specifications['sizeCluster'] * self.specifications['cluster_directory']
                b = b''.join([b'\x2f',b'\x23'*15,b'\x00'*4,b'\x00'*4,b'\x30'*14,b'\x30'*14])
                self.disc.write(base,b)
                for i in range(fileData['cluster'],fileData['end_cluster'] + 1):
                    self.specifications['bitMap'][i] = 0
                return
        raise Exception('No se encontro el archivo')
    def ls(self):
        files = [file for file in self.getFiles() if file.empty() == False]
        if files.__len__() == 0:
            return richPrint(Panel("[yellow]No hay archivos para mostrar[/yellow]",title="Sin archivos",expand=False))
        table = Table(title="Directorio")
        aviableColumns = self.preprocessToShowFields.keys()
        for column in files[0].getData().keys():
            if column not in aviableColumns:
                continue
            table.add_column(column)
        for file in files:
            values = [self.preprocessToShowFields[pair[0]](pair[1]) for pair in list(file.getData().items()) if pair[0] in aviableColumns]
            table.add_row(*values)
        console = Console()
        console.print(table)



fileSystem = FileSystemFiUNAMFS(Disc('fiunamfs.img'))
class Menu:
    def __init__(self, fileSystem: FileSystemFiUNAMFS):
        self.fileSystem = fileSystem
        richPrint(Panel(renderable="[cyan bold italic]Alumno: [/cyan bold italic][cyan]Aguilar Martínez Erick Yair[/cyan]\n[cyan bold italic]Materia: [/cyan bold italic][cyan]Sistemas Operativos[/cyan]\n[cyan bold italic]Semestre: [/cyan bold italic][cyan]2024-2[/cyan]\n[cyan bold italic]Profesor: [/cyan bold italic][cyan]Ing. Gunnar Eyal Wolf Iszaevich[/cyan]",title="FileSystem [red]FIUNAMFS", expand=True))
        pprint(self.fileSystem.specifications,expand_all=False,max_length=20)
        input("Presiona cualquier ENTER para continuar...")
    def listFiles(self):
        return self.fileSystem.ls()
    def deleteFile(self):
        files = [file for file in self.fileSystem.getFiles() if not file.empty()]
        if files.__len__() == 0:
            return richPrint(Panel("[yellow]No hay archivos para eliminar[/yellow]",title="Sin archivos",expand=False))
        cleaned_files = [(i+1, file.getData()['name'].rstrip('\x00').strip()) for i, file in enumerate(files)]
        questions = [
            {
                'type': 'list',
                'name': 'file',
                'message': 'Choose a file to delete',
                'choices': [f"{i}){name}" for i, name in cleaned_files]
            }
        ]
        fileToDelete = prompt(questions)['file']
        index = int(fileToDelete[0]) - 1
        name = files[index].getData()['name']
        self.fileSystem.deleteFile(name)
    def copyFile(self):
        def getParentDirectory(filePath):
            return os.path.dirname(filePath)
        def formatPath(base,path):
            absolutePath = os.path.join(base,path)
            if absolutePath == None:
                raise Exception('No se puede formatear un path nulo')
            if os.path.isdir(absolutePath):
                return f"{path}/"
            if os.path.isfile(absolutePath):
                return f"{path}"
            return path
        base = getParentDirectory(os.path.abspath(__file__))
        selectedFile = ''
        while not os.path.isfile(os.path.join(base,selectedFile)):
            contentDir = os.listdir(base) + ['..']
            options = list(map(lambda item : formatPath(base,item), contentDir))
            question = [
                {
                    'type': 'list',
                    'name': 'file',
                    'message': 'Choose a file to copy',
                    'choices': options,
                }
            ]
            selectedFile = prompt(question)['file']
            index = options.index(selectedFile)
            absolutePaths = [os.path.join(base,x) for x in contentDir]
            absolutePath = absolutePaths[index]
            if absolutePath.endswith('..'):
                base = getParentDirectory(os.path.abspath(base))
                print('base:',base)
                selectedFile = ''
                continue
            if os.path.isdir(absolutePath):
                base = os.path.join(base,contentDir[index])
                print('base:',base)
                selectedFile = ''
                continue
        absPath = os.path.join(base,selectedFile)
        self.fileSystem.copyInside(absPath)
menu = Menu(fileSystem)
options = {
    "DELETE_FILE" : menu.deleteFile,
    "LIST_FILES" : menu.listFiles,
    "COPY_FILE" : menu.copyFile,
    "EXTRACT_FILE" : lambda: print('EXTRACT_FILE'),
    "EXIT" : lambda: sys.exit(0)
}
def main_menu():
    questions = [
        {
            'type': 'list',
            'name': 'main_menu',
            'message': 'What do you want to do?',
            'choices': options.keys()
        }
    ]
    answers = prompt(questions)
    return answers['main_menu']
while True:
    choice = main_menu()
    options[choice]()
