#!/usr/bin/python3
# -*- encoding: utf-8
from mmap import mmap
import os
from struct import pack, unpack

class dentry:
    def __init__(self, fsdata, size, base):
        self.fsdata = fsdata
        self.size = size
        self.base = base

    def gen(self, filetype, name, size, cluster, creat, modif):
        # Corrección de tipo de datos sobre name :-Þ
        if name.__class__ == ''.__class__:
            name = name.encode()
        if len(name) != 14:
            name = b'%-14s' % name

        self.fsdata[self.base:self.base+1] = filetype
        self.fsdata[self.base+1:self.base+15] = name
        self.fsdata[self.base+16:self.base+20] = pack('<I', size)
        self.fsdata[self.base+20:self.base+24] = pack('<I', cluster)
        self.fsdata[self.base+24:self.base+38] = creat
        self.fsdata[self.base+38:self.base+52] = modif

    def read(self):
        self.nam = self.fsdata[self.base+1:self.base+14].decode()
        self.size = unpack('<I', self.fsdata[self.base+16:self.base+20])[0]
        self.cluster = unpack('<I', self.fsdata[self.base+20:self.base+24])[0]

    def name(self):
        return self.fsdata[self.base+1:self.base+15]

    def as_readable(self):
        self.read()
        return "%s clust. %3s + %6sb \n" % (self.nam, self.cluster, self.size)

class fiunamfs:

    """Implementación del sistema de archivos para el proyecto de Sistemas
    de Archivos. Gunnar Wolf, clase de Sistemas Operativos, Facultad
    de Ingeniería, UNAM.

    """

    from datetime import datetime
    def __init__(self, filename, fsname='FiUnamFS', version=1.0,
                 label='No Label', sector_size=512, sect_per_clust=4,
                 dir_clusters=4, tot_clusters=720, empty_dir_mark='-'*14):
        """Inicialización de un objeto fiunamfs.

        El único parámetro obligatorio es el nombre del archivo en el
        cual se inicializará elsistema de archivos. Los demás
        parámetros, espero, serán suficientemente autodescriptivos.

        """
        self.filename = filename
        self.fsname = fsname
        self.version = version
        self.label = label
        self.sector_size = sector_size
        self.sect_per_clust = sect_per_clust
        self.dir_clusters = dir_clusters
        self.tot_clusters = tot_clusters
        self.empty_dir_mark = empty_dir_mark

        self.direntry_size = 64
        self.cluster_size = self.sector_size * self.sect_per_clust
        self.tot_direntries = int(self.cluster_size * self.dir_clusters /
                                  self.direntry_size)
        self.total_size = self.cluster_size * self.tot_clusters

        if not os.path.isfile(filename):
            # Para dimensionar al sistema del tamaño deseado, creamos
            # un archivo vacío, saltamos (seek()) hasta el punto
            # máximo menos un byte, y escribimos un byte (\0). Todo el
            # espacio restante se llena de \0.
            with open(filename, 'w') as out:
                out.seek(self.tot_clusters * self.cluster_size - 1)
                out.write("\0")

        filesize = os.stat(self.filename).st_size
        if filesize != self.total_size:
            raise RuntimeError(('El archivo %s existe, pero es de tamaño ' +
                                'incorrecto (%d != %d)') %
                               (self.filename, self.total_size, filesize))

        self.fh = open(self.filename, 'r+')
        self.data = mmap(self.fh.fileno(), 0)

    def params_as_readable(self):
        """Entrega una cadena con los parámetros del sistema, en un formato
        que se pueda desplegar al usuario humano"""
        ret_str =  "-------------------------------------------------------\n"
        ret_str += "   FiUNAMFS\n   Parámetros del objeto\n"
        ret_str += "-------------------------------------------------------\n"
        for i in sorted(['filename', 'fsname', 'version', 'label',
                         'sector_size', 'sect_per_clust', 'dir_clusters',
                         'tot_clusters', 'empty_dir_mark', 'direntry_size',
                         'cluster_size', 'tot_direntries', 'total_size']):
            ret_str += "%-14s: %s\n" % (i, self.__getattribute__(i))
        ret_str += "-------------------------------------------------------\n"
        return ret_str

    def __del__(self):
        """Destructor del objeto (llamado automáticamente)"""
        self.data = None
        if 'fh' in dir(self):
            self.fh.close()

    def format(self):
        """Formatea un volumen / archivo ejemplo como fiunamfs, con los
        parámetros especificados en __init__"""
        self.init_superblock()
        for i in range(self.tot_direntries):
            self.write_dentry(i, self.empty_dir_mark, 0, 0, b'0'*14, b'0'*14)

    def init_superblock(self):
        """Inicializa el "superbloque" (el primer sector) del sistema de
        archivos con los parámetros especificados en __init__"""
        print('Inicializando volumen %s versión %s, etiqueta «%s»' %
              (self.fsname, self.version, self.label))
        print('Tamaño de cluster: %d. Tamaño de directorio: %d clusters' %
              (self.cluster_size, self.direntry_size))
        print('Entradas de directorio: %d. Clusters totales: %d' %
              (self.tot_direntries, self.tot_clusters))

        # Para almacenar datos dentro de un archivo mmap()eado,
        # tenemos que codificar nuestras cadenas de texto de modo
        # que no haya caracteres de ancho diferente a 8 bits
        # (recuerden Unicode...) — encode() convierte un objeto
        # tipo 'str' (cadena Unicode) en bytes (arreglo de
        # caracteres de 8 bits)
        self.data[0:8] = ('%-8s' % self.fsname).encode()
        self.data[10:14] = ('%-4s' % self.version).encode()
        self.data[20:39] = ('%-19s' % self.label).encode()
        self.data[40:44] = pack('<I', self.cluster_size)
        self.data[45:49] = pack('<I', self.dir_clusters)
        self.data[50:54] = pack('<I', self.tot_clusters)

    def write_dentry(self, pos, name, size, cluster, creat, modif):
        """Escribe una entrada de directorio en la posición especificada"""
        # Calcula la posición del dentry en el disco
        pos = self.cluster_size + pos * self.direntry_size
        if name == self.empty_dir_mark:
            filetype = b'/'
        else:
            filetype = b'-'
        entry = dentry(self.data, self.direntry_size, pos)
        entry.gen(filetype, name, size, cluster, creat, modif)

    def directory_as_readable(self):
        """muestra los contenidos del directorio, para ser mostrados al
        usuario (como cadena "procesada")"""
        ret_str =  "Directorio de archivos\n"
        ret_str += "-------------------------------------------------------\n"
        for entry in range(self.tot_direntries):
            pos = self.cluster_size + (entry * self.direntry_size)
            entry = dentry(self.data, self.direntry_size, pos)
            if entry.name() == self.empty_dir_mark:
                pass
            else:
                ret_str += entry.as_readable()

        return ret_str

    # stuff debe ser un objeto bytes, no str
    def filedata(self, start, stuff):
        """Graba los datos correspondientes a un archivo. Ojo, esta función no
        verifica _nada_, sólo hace lo que le pedimos

        """
        print('  Escribiendo %d bytes a partir de %d' % (len(stuff), start))
        st_byte = start * self.cluster_size
        end_byte = st_byte + len(stuff)
        self.data[st_byte:end_byte] = stuff

    def write(self, filename, filedata, dentry=None, start_cluster=None,
              creat=datetime.now().strftime('%Y%m%d%H%M%S').encode(),
              modif=datetime.now().strftime('%Y%m%d%H%M%S').encode()
              ):
        """Escribe dentro del fiunamfs el nombre de archivo especificado como
        primer parámetro, registrando los datos de archivo
        especificados como segundo parámetro.

        Los parámetros opcionales dentry (lugar en el directorio donde
        debe escribirse) y start_cluster (primer cluster para el
        archivo) deben ser llenados (no hay "defaults sensatos").

        """
        self.write_dentry(dentry, filename, len(filedata),
                          start_cluster, creat, modif)
        self.filedata(start_cluster, filedata)

#     def first_empty_cluster():
#         clusters = ['' for c in range(self.tot_clusters)]

#         for c in range(self.dir_clusters):
#             clusters[c] = 'DIR'

#         for pos in range(self.direntry_size):
#             de = dentry(self.data, self.direntry_size, pos)
#             de.read()
# #            print(de.size)
# #            num_clust = int(de.size / self.cluster_size)
#             # if clusters[c] == '':
#             #     pass
#             # else:
#             #     print( 'Conflicto: %c (%s vs. %s)' % (c, 'DIR', clusters[c]))

if __name__  == '__main__':
    filename = 'fiunamfs.img'
    fs = fiunamfs(filename, fsname='FiUnamFS', version='24-2', label='Mi Sistema Favorito',
                  sector_size=512, sect_per_clust=4, dir_clusters=4,
                  tot_clusters=720, empty_dir_mark=b'#' * 14)
    fs.format()

    # Copiar tres archivos hacia el interior de FiUnamFS
    stuff = open('README.org', 'rb').read()
    skip = fs.dir_clusters + 2
    fs.write('README.org', stuff, dentry=0, start_cluster=skip)

    skip = skip + int(len(stuff) / (fs.sector_size * fs.sect_per_clust)) + 1

    stuff = open('logo.png', 'rb').read()
    fs.write('logo.png', stuff, dentry=2, start_cluster=skip)

    skip = skip + int(len(stuff) / (fs.sector_size * fs.sect_per_clust)) + 1

    stuff = open('mensaje.jpg', 'rb').read()
    fs.write('mensaje.jpg', stuff, dentry=5, start_cluster=skip)

    print('Fue creado un sistema de archivos')
    print('con las siguientes características:')
    print(fs.params_as_readable())
    print(fs.directory_as_readable())
