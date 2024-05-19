from struct import pack, unpack
import time
from rich import print as richPrint
from copy import deepcopy
from rich.console import Console
from rich.table import Table
from rich.pretty import pprint
from rich.panel import Panel



class Disc:
    def __init__(self,filePath):
        try:
            self.file = open(filePath, 'rb')
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
    def __init__(self, bytes: bytes):
        if bytes.__len__() > 64:
            raise Exception('La información del archivo no puede ser mayor a 64 bytes')
        self.data = {
            'type': bytes[0:1].decode(),
            'name': bytes[1:16].decode(),
            'size': int(unpack('<I', bytes[16:20])[0]),
            'cluster': int(unpack('<I', bytes[20:24])[0]),
            'date': bytes[24:38].decode(),
            'last_modification': bytes[38:52].decode()
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
        self.files = [FileData(bytes[i:i+sizeFileData]) for i in range(0, bytes.__len__(), 64)]

class FileSystem:
    def __init__(self,disc:Disc):
        self.disc = disc
        self.specifications = {
            'system': self.disc.read(0,8).decode(),
            'version': self.disc.read(10,4).decode(),
            'volumen_label': self.disc.read(20,15).decode(),
            'sizeCluster': int(unpack('<I', self.disc.read(40,4))[0]),
            'numClusters': int(unpack('<I', self.disc.read(45,4))[0]),
            'totalClusters': int(unpack('<I', self.disc.read(50,4))[0]),
            'sizeFileData': 64
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
    def ls(self):
        directory = Directory(self.getClusters(1,3))
        table = Table(title="Directorio")
        for column in directory.files[0].getData().keys():
            if column == 'type':
                continue
            table.add_column(column)
        for file in directory.files:
            if file.empty():
                continue
            values = [str(v) for v in list(file.getData().values())[1:]]
            table.add_row(*values)
        console = Console()
        console.print(table)
fileSystem = FileSystem(Disc('fiunamfs.img'))
fileSystem.showSpecifications()
fileSystem.ls()
fileSystem.clean()














# import struct

# def showFile(bytes: bytes):
#     if bytes.__len__() > 64:
#         raise Exception('El archivo no puede ser mayor a 64 bytes')
#     return {'type': bytes[0:1].decode(), 'name': bytes[1:16].decode(), 'size': struct.unpack('<I', bytes[16:20])[0], 'cluster': struct.unpack('<I', bytes[20:24])[0], 'date': bytes[24:38].decode(), 'last_modification': bytes[38:52].decode()}

# disc = open('fiunamfs.img', 'rb')
# print(disc.seek(0, 2))
# # disc.seek(0)
# # identifySystem = disc.read(8).decode()
# # disc.seek(10)
# # versionSystem = disc.read(4).decode()
# # disc.seek(20)
# # labelVolume = disc.read(15).decode()
# # disc.seek(40)
# # sizeCluster = struct.unpack('<I', disc.read(4))[0]
# # disc.seek(45)
# # numClustersByDirectory = struct.unpack('<I', disc.read(4))[0]
# # disc.seek(50)
# # totalClusters = struct.unpack('<I', disc.read(4))[0]
# # print({'system' : identifySystem, 'version' : versionSystem, 'label' : labelVolume, 'sizeCluster' : sizeCluster, 'numClusters' : numClustersByDirectory, 'totalClusters' : totalClusters})


# # for i in range(sizeCluster*1, sizeCluster*numClustersByDirectory,64):
# #     disc.seek(i)
# #     file = showFile(disc.read(64))
# #     if file['type'] == '/':
# #         continue
# #     print(f"{file['name']} {file['size']} {file['date']} {file['last_modification']}")

# # disc.close()