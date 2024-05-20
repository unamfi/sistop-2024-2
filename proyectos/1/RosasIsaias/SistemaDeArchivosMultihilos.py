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



# OPCIÓN 1) Listar archivos del disco



# OPCIÓN 2) Copia y pega un archivo de FiUnamFS a el sistema del usuario


# OPCIÓN 3) Copia y pega un archivo del sistema a FiUnamFS


# OPCIÓN 4) Borrar un archivo de FiUnamFS


# OPCIÓN 5) 'Cortar' y pegar un archivo de FiUnamFS al sistema


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

            
            # Para la OPCIÓN 2: Copiar un archivo de FiUnamFS a sistema
                elif entradaRecibida[0] == 'copia':


            # Para la OPCIÓN 3: Copiar un archivo del sistema a FiUnamFS
                elif entradaRecibida[0] == 'inserta':


            # Para la OPCIÓN 4: Eliminar un archivo de FiUnamFS
                elif entradaRecibida[0] == 'elimina':


            # Para la OPCIÓN 5: 'Cortar' y pegar un archivo de FiUnamFS al sistema
                elif entradaRecibida[0] == 'corta':


            # Para la OPCIÓN 6: Eliminar un archivo de FiUnamFS
                elif entradaRecibida[0] == 'salir':
                    break

            else:
                print("\033[1;31m" + "ERROR: Comando invalido. Intente nuevamente \n")

# INICIALIZACIÓN DEL PROGRAMA CON EL MENÚ
if __name__ == '__main__':
    INICIA = gestorArchivos()
    INICIA.menu()