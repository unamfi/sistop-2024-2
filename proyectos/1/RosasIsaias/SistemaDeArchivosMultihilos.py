'''
    >> SEMESTRE: 2024-2
    >> ASIGNATURA: Sistemas Operativos
    >> GRUPO: 6
    >> AUTOR: Rosas Meza Isaías
    >> DESCRIPCIÓN: Este programa puede abrir, copiar y modificar archivos del disco "FiUnamFs.img". 
       El mismo puede operar con multihilos en la sección de copiar un archivo al sistema del usuario
    >> FECHA: 19/05/2024
'''

# BIBLIOTECAS
import struct, threading

# CLASE GLOBAL Y SUS FUNCIONES
class gestorArchivos:
    def __init__(self):
        self.sector = 512
        self.cluster = self.sector*4
        self.fs = open('fiunamfs.img','r+b')
        self.longitudNombre = 15
        self.longitudInicial = 4
        self.clusterInicial = 4


# OPCIÓN 1) Listar archivos del disco
    def listar(self):
        self.fs.seek(0)
        files = []
        # Se busca y se enlistan todos los registros. Donde no existan se escribe una cadena de numerales
        for i in range (0,64):
            self.fs.seek(self.cluster + (i*64))
            file_name = self.fs.read(self.longitudNombre)
            if file_name != b'###############':
                files.append(file_name)
        for fil in files:
            print(fil.decode())
        self.fs.seek(0)


# OPCIÓN 2) Copia y pega un archivo de FiUnamFS a el sistema del usuario
    def extraccion(self, nombre, destino):
        # Se busca en los 64 registros el archivo a copiar
        for i in range(0, 64):
            self.fs.seek(self.cluster + (i * 64))
            nombreArchivo = self.fs.read(self.longitudNombre)
            self.fs.read(1)
            if nombreArchivo.decode().strip() == nombre:
                # Una vez encontrado, se copian los datos a un nuevo archivo
                tam = struct.unpack('<L', self.fs.read(4)) [0]
                inicio = struct.unpack('<L', self.fs.read(4)) [0]
                self.fs.seek(self.cluster * inicio)
                data = self.fs.read(tam)
                escribeEnArchivo = open(destino + "/" + nombreArchivo.decode().strip(), "wb")
                escribeEnArchivo.write(data)
                escribeEnArchivo.close()
                break
                # Si no se encuentra el archivo se envía un mensaje
        if i == 63:
            print("\033[1;31m" + "ERROR: El archivo no existe")


# OPCIÓN 3) Copia y pega un archivo del sistema a FiUnamFS
    def exportacion(self, nombre):
        print("No fue posible implementar esta función. Se implementará proximamente en una atualización")


# OPCIÓN 4) Borrar un archivo de FiUnamFS
    def borrar(self, borrado):
        # Se busca en cada registro para ver si hay coincidencias con el archivo que se quiere eliminar
        for i in range(0,64):
            self.fs.seek(self.cluster + (i*64))
            file_name = self.fs.read(self.longitudNombre)
            if file_name.decode().strip() == borrado:
                    self.fs.seek(self.cluster + (i*64))
                    # Si el archivo se encuentra, se reescribe con la cadena que indica que el espacio ya esta libre
                    self.fs.write(('###############').encode())
                    break
        if i == 63:
            print("\033[1;31m" + "ERROR: El archivo no existe")


# OPCIÓN 5) 'Cortar' y pegar un archivo de FiUnamFS al sistema [PENDIENTE]
    def corta(self, nombre, destino):
        print("PENDIENTE")


# VISTA AL USUARIO
    def menu(self):
        while True:
            print("\033[1;36m" + "========== BIENVENIDO AL SISTEMA DE ARCHIVOS ==========")
            print("\033[1;36m" + "         ========== VERSIÓN: 1.0 ==========           \n")

            print(" 1) Listar archivos del disco ==> enlista")
            print(" 2) Copiar un archivo de FiUnamFS a sistema ==> copia -<nombreArchivo> <rutaDestino>")
            print(" 3) Copiar un archivo del sistema a FiUnamFS ==> inserta -<nombreArchivo>")
            print(" 4) Borrar un archivo de FiUnamFS ==> elimina -<nombreArchivo>")
            print(" 5) 'Cortar' y pegar un archivo de FiUnamFS al sistema ==> corta -<nombreArchivo> <rutaDestino>")
            print(" 6) Salir del programa ==> salir \n")

            entradaComando = input("\033[1;33m" + "Ingrese el comando como se muestra en el menú de opciones: ")
            print("\n")
            entradaRecibida = entradaComando.split()
            opciones = ['enlista', 'copia', 'pega', 'elimina', 'corta', 'salir']

            if entradaRecibida[0] in opciones:

            # Para la OPCIÓN 1: Listar archivos del disco
                if entradaRecibida[0] == 'enlista':
                    if len(entradaRecibida)!=1:
                        print("\033[1;31m" + "ERROR: Se escribió una sentencia adicional \n")
                    else:
                        print("\033[1;32m" + "Lista de archivos: \n")
                        self.listar()
                        print("==================================================")
            
            # Para la OPCIÓN 2: Copiar un archivo de FiUnamFS a sistema
                elif entradaRecibida[0] == 'copia':
                    if len(entradaRecibida)!=3:
                        print("\033[1;31m" + "ERROR: Faltó escribir el nombre del archivo y/o la ruta de destino \n")
                    else:
                        print("\033[1;32m" + "PROCESO INICIADO: Copiando archivo de FiunamFS al sistema...\n")
                        self.extraccion(entradaRecibida[1],entradaRecibida[2])
                        print("==================================================")

            # Para la OPCIÓN 3: Copiar un archivo del sistema a FiUnamFS
                elif entradaRecibida[0] == 'inserta':
                    if len(entradaRecibida)!=2:
                        print("\033[1;31m" + "ERROR: Faltó escribir el nombre del archivo \n")
                    else:
                        self.exportacion(entradaRecibida[1])
                        print("==================================================")

            # Para la OPCIÓN 4: Eliminar un archivo de FiUnamFS
                elif entradaRecibida[0] == 'elimina':
                    if len(entradaRecibida)!=2:
                        print("\033[1;31m" + "ERROR: No se especificó el archivo a eliminar \n")
                    else:
                        print("\033[1;32m" + "PROCESO INICIADO: Eliminando archivo...\n")
                        self.borrar(entradaRecibida[1])
                        print("==================================================")

            # Para la OPCIÓN 5: 'Cortar' y pegar un archivo de FiUnamFS al sistema
                elif entradaRecibida[0] == 'corta':
                    print("PENDIENTE")

            # Para la OPCIÓN 6: Eliminar un archivo de FiUnamFS
                elif entradaRecibida[0] == 'salir':
                    break

            else:
                print("\033[1;31m" + "ERROR: Comando invalido. Intente nuevamente \n")

# INICIALIZACIÓN DEL PROGRAMA CON EL MENÚ
if __name__ == '__main__':
    INICIA = gestorArchivos()
    INICIA.menu()