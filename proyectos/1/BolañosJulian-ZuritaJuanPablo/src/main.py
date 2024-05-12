import struct

''' 'readDirectory' retorna un dato de tipo <str> o bien <int> decimal según 
    lo que encuentre en el directorio mediante una lectura en modo binario a 
    partir una posición y desplazamiento definidos. '''
def readDirectory(name:str, start:int, size:int):

    with open(name, 'rb') as FiUnamFS:
        FiUnamFS.seek(start)
        content = FiUnamFS.read(size)

    try:
        c, = struct.unpack('<I', content)
        return c
    
    except:
        return content.decode('ascii')
