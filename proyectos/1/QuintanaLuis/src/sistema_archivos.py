import os.path

import struct
from entrada import Entrada
from directorio import Directorio
from super_bloque import SuperBloque
from pathlib import Path
import constantes
from excepciones import *
import helper
import datetime


class SistemaArchivos:

    def __init__(self, ruta_sistema: str):
        self.ruta_sistema = ruta_sistema
        self.sistema = bytes()
        self.__cargar_sistema()
        self.super_bloque = SuperBloque(
            nombre=self.sistema[:8].decode('ascii'),
            version=self.sistema[10:14].decode('ascii'),
            etiqueta_volumen=self.sistema[20:35].decode('ascii'),
            tamano_cluster_bytes=struct.unpack('i', self.sistema[40:44])[0],
            tamano_cluster_directorio=struct.unpack('i', self.sistema[45:49])[0],
            tamano_cluster_unidad=struct.unpack('i', self.sistema[50:54])[0]
        )
        self.directorio = Directorio(self.super_bloque)
        # Si es la primera vez se cargará el directorio
        self.actualizar_directorio()

    def recargar_sistema(self):
        """
        Recargar para poder actualizar el directorio una vez se realice alguna
        modificación
        """
        self.__cargar_sistema()
        # Refrescar el directorio
        # Si es la primera vez se cargará el directorio
        self.actualizar_directorio()

    def __cargar_sistema(self):
        """
        Obtener el sistema en un grupo de bytes, en un futuro puede ser mejorado
        para cargar ciertos cluster o áreas más limitadas y no saturar memoria
        """
        self.sistema = Path(self.ruta_sistema).read_bytes()

    # Si es la primera vez se cargará el directorio
    def actualizar_directorio(self):
        self.directorio.entradas_ocupadas = []
        self.directorio.entradas_desocupadas = []

        i = self.directorio.byte_inicio

        # Se llegará hasta el tamaño en clusters del directorio.py por
        # 4 sectores por 512 bytes
        while i < self.directorio.byte_fin:
            tipo_archivo = self.sistema[i:i + 1].decode('ascii')

            # En caso de tener una entrada vacia se omite
            if tipo_archivo == '/':
                # agregar el byte inicial donde hay una entrada desocupada
                self.directorio.entradas_desocupadas.append(i)
                i += 64
                continue

            i += 1
            nombre_archivo = self.sistema[i:i + 14].decode('ascii')
            i += 15
            tamano_bytes_archivo = struct.unpack('i', self.sistema[i:i + 4])[0]
            i += 4
            cluster_inicial_archivo = struct.unpack('i', self.sistema[i:i + 4])[0]
            i += 4
            fecha_creacion_archivo = self.sistema[i:i + 14].decode('ascii')
            i += 14
            fecha_ultima_modificacion_archivo = self.sistema[i:i + 14].decode('ascii')
            i += 14
            espacio_no_utilizado = struct.unpack('iii', self.sistema[i:i + 12])[0]
            i += 12

            self.directorio.entradas_ocupadas.append(Entrada(
                tipo=tipo_archivo,
                nombre=nombre_archivo,
                tamano_bytes=tamano_bytes_archivo,
                cluster_inicial=cluster_inicial_archivo,
                fecha_creacion=fecha_creacion_archivo,
                fecha_ultima_modificacion=fecha_ultima_modificacion_archivo,
            ))

    def es_archivo_valido_interno(self, nombre: str) -> bool:
        """
        Validará si el archivo se encuentra en el directorio unico del
        sistema de archivos
        """
        for entrada in self.directorio.entradas_ocupadas:
            print(entrada.nombre)
            if entrada.nombre == nombre:
                return True

        return False

    def pull(self, nombre: str, destino: str):
        """
        Encargado de llevar un archivo del sistema FiUnamFs a nuestro sistema
        como funciona en android-tools, por medio de adb pull | push
        """
        if not self.es_archivo_valido_interno(nombre):
            raise EntradaNoValidaException(f"{nombre} no existe en {constantes.NOMBRE_SISTEMA_ARCHIVOS}")

        # buscamos en las entradas ocupadas el cluster inicial y tamaño
        cluster_inicial = 0
        tamano_bytes = 0
        for entrada in self.directorio.entradas_ocupadas:
            if entrada.nombre == nombre:
                cluster_inicial = entrada.cluster_inicial
                tamano_bytes = entrada.tamano_bytes

        self.__pull_con_cluster(cluster_inicial, tamano_bytes, destino)

    def __pull_con_cluster(self, cluster_inicial: int, tamano_bytes: int, destino: str) -> bool:
        # hay 2048 bytes por cluster
        byte_inicial = cluster_inicial * constantes.TAMANO_CLUSTER_BYTES
        byte_final = byte_inicial + tamano_bytes
        contenido_bytes = self.sistema[byte_inicial: byte_final]

        with open(destino, "wb") as archivo:
            archivo.write(contenido_bytes)
            return True

    def push(self, ruta: str, nombre: str = ''):
        """
        Ruta puede ser directorio o nombre de archivo
        """

        # validar si lo que se va a copiar es un archivo
        if not Path(ruta).is_file():
            raise EntradaNoValidaException(f"{ruta} no existe en su sistema de archivos o es un directorio")

        # se asignara el nombre que tiene en nuestro fs al archivo para fiunamfs
        if nombre == '':
            nombre = os.path.basename(ruta)

        tamano_bytes = Path(ruta).stat().st_size

        # buscamos en las entradas ocupadas el cluster inicial y tamaño
        cluster_inicial = helper.buscar_cluster_contiguo_desocupado(
            tamano_bytes=tamano_bytes,
            directorio=self.directorio,
            cluster_archivos_inicio=self.super_bloque.tamano_cluster_directorio + 1,
            cluster_archivos_fin=self.super_bloque.tamano_cluster_unidad
        )

        entrada_vacia_byte = self.directorio.pop_entrada_vacia()

        # agregar como archivo
        archivo_creado = self.__push_con_cluster(ruta, cluster_inicial)

        fecha_creacion = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # agregar entrada
        if archivo_creado:
            self.escribir_entrada(Entrada(
                tipo='-',
                nombre=nombre,
                tamano_bytes=tamano_bytes,
                cluster_inicial=cluster_inicial,
                fecha_creacion=fecha_creacion,
                fecha_ultima_modificacion=fecha_creacion
            ), entrada_vacia_byte)

        self.recargar_sistema()

    def __push_con_cluster(self, ruta: str, cluster_inicial: int) -> bool:
        """
        Copiará archivos de nuestro sistema de archivos al sistema
        FiUnamFs
        """

        # 512 * 4 * cluster_inicial
        byte_inicial = cluster_inicial * constantes.TAMANO_CLUSTER_BYTES

        # cargar archivo a bytes para transferir
        contenido = Path(ruta).read_bytes()

        with open(self.ruta_sistema, "r+b") as archivo:
            archivo.seek(byte_inicial)
            archivo.write(contenido)
            return True

    def formatear_string_a_ascii_7_bits(self, string: str) -> bytes:
        # se deben tener 14 caracteres fijos
        return string.ljust(15).encode('ascii')

    def escribir_entrada(self, entrada: Entrada, entrada_vacia_byte: int):

        tipo = entrada.tipo.encode('ascii')
        nombre = self.formatear_string_a_ascii_7_bits(entrada.nombre)
        tamano_bytes_archivo = struct.pack('i', entrada.tamano_bytes)
        cluster_inicial_archivo = struct.pack('i', entrada.cluster_inicial)
        fecha_creacion_archivo = entrada.fecha_creacion.encode('ascii')
        fecha_ultima_modificacion_archivo = entrada.fecha_ultima_modificacion.encode('ascii')
        espacio_no_utilizado = struct.pack('iii', 0, 0, 0)

        contenido = tipo + nombre + tamano_bytes_archivo + cluster_inicial_archivo + fecha_creacion_archivo + fecha_ultima_modificacion_archivo + espacio_no_utilizado

        with open(self.ruta_sistema, "r+b") as archivo:
            archivo.seek(entrada_vacia_byte)
            archivo.write(contenido)
            return True
