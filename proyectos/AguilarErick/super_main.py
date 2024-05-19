from math import ceil
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
        # name = ''.join([chr(b) for b in bytes[1:16] if chr(b) not in whitespace and b > 0])
        self.data = {
            'type': bytes[0:1].decode(encoding='ascii'),
            'name': bytes[1:16].decode(encoding='ascii'),
            'size': int(unpack('<I', bytes[16:20])[0]),
            'cluster': int(unpack('<I', bytes[20:24])[0]),
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

class FileSystem:
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
            'sizeFileData': 64
        }
        spec = self.specifications
        if spec['version'] != '24-2':
            raise Exception('La versión del sistema de archivos no es compatible')
        if spec['system'] != 'FiUnamFS':
            raise Exception('El sistema de archivos no es compatible')
        
        self.preprocessToShowFields = {
            'name': lambda name : name.rstrip().rstrip('\x00').strip() if name != None else '',
            'size': lambda size: f"{str(ceil(size//1024))}(kB)" if size > 1024 else f"{size}[B]",
            'cluster': lambda cluster:f"#{cluster}" if cluster != None else '',
            'date': lambda date: datetime.strptime(date,"%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S"),
            'address_in_directory': lambda address: f"{address}",
            'last_modification': lambda last_mod : datetime.strptime(last_mod,"%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        }
    def showSpecifications(self):
        richPrint(Panel(renderable="[cyan bold italic]Alumno: [/cyan bold italic][cyan]Aguilar Martínez Erick Yair[/cyan]\n[cyan bold italic]Materia: [/cyan bold italic][cyan]Sistemas Operativos[/cyan]\n[cyan bold italic]Semestre: [/cyan bold italic][cyan]2024-2[/cyan]\n[cyan bold italic]Profesor: [/cyan bold italic][cyan]Ing. Gunnar Eyal Wolf Iszaevich[/cyan]",title="FileSystem [red]FIUNAMFS", expand=True))
        pprint(self.specifications,expand_all=True)
    def getSpecifications(self):
        return deepcopy(self.specifications)
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
                return
        raise Exception('No se encontro el archivo')
    def ls(self):
        files = self.getFiles()
        table = Table(title="Directorio")
        aviableColumns = self.preprocessToShowFields.keys()
        for column in files[0].getData().keys():
            if column not in aviableColumns:
                continue
            table.add_column(column)
        for file in files:
            if file.empty():
                continue
            values = [self.preprocessToShowFields[pair[0]](pair[1]) for pair in list(file.getData().items()) if pair[0] in aviableColumns]
            table.add_row(*values)
        console = Console()
        console.print(table)



fileSystem = FileSystem(Disc('fiunamfs.img'))
class Menu:
    def __init__(self, fileSystem: FileSystem):
        self.fileSystem = fileSystem
    def deleteFile(self):
        files = [file for file in self.fileSystem.getFiles() if not file.empty()]
        if files.__len__() == 0:
            return richPrint(Panel("No hay archivos para eliminar",title="Sin archivos",expand=False))
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
    
menu = Menu(fileSystem)
options = {
    "DELETE_FILE" : menu.deleteFile,
    "LIST_FILES" : lambda: fileSystem.ls(),
    "COPY_FILE" : lambda: print('COPY_FILE'),
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
