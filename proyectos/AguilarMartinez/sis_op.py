import struct

def showFile(bytes: bytes):
    if bytes.__len__() > 64:
        raise Exception('El archivo no puede ser mayor a 64 bytes')
    return {'type': bytes[0:1].decode(), 'name': bytes[1:16].decode(), 'size': struct.unpack('<I', bytes[16:20])[0], 'cluster': struct.unpack('<I', bytes[20:24])[0], 'date': bytes[24:38].decode(), 'last_modification': bytes[38:52].decode()}

disc = open('./fiunamfs.img', 'rb')
disc.seek(0)
identifySystem = disc.read(8).decode()
disc.seek(10)
versionSystem = disc.read(4).decode()
disc.seek(20)
labelVolume = disc.read(15).decode()
disc.seek(40)
sizeCluster = struct.unpack('<I', disc.read(4))[0]
disc.seek(45)
numClustersByDirectory = struct.unpack('<I', disc.read(4))[0]
disc.seek(50)
totalClusters = struct.unpack('<I', disc.read(4))[0]
print({'system' : identifySystem, 'version' : versionSystem, 'label' : labelVolume, 'sizeCluster' : sizeCluster, 'numClusters' : numClustersByDirectory, 'totalClusters' : totalClusters})


for i in range(sizeCluster*1, sizeCluster*numClustersByDirectory,64):
    disc.seek(i)
    file = showFile(disc.read(64))
    if file['type'] == '/':
        continue
    print(f"{file['name']} {file['size']} {file['date']} {file['last_modification']}")

disc.close()