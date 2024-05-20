"""
Proyecto 1

"""
from sistema_archivos import SistemaArchivos
import sys
import os
import platform

# Se encuentran los archivos de ayuda y se almacenan los extraidos
# del sistema de archivos
RESOURCES_DIR = '../resources'


def mostrar_manual():
    print("manual")

def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def shell():
    sistema_archivos = SistemaArchivos(ruta_sistema="../fiunamfs.img")

    print("Bienvenido a la shell del sistema fi unam fs, utilice ayuda o help para visualizar los comandos")

    shell_loop = True
    while shell_loop:
        comando = input("$ ")

        if len(comando.split()) > 1:
            comandos = comando.split()
            if comandos[0] == "push":
                sistema_archivos.push(comandos[1])
            elif comandos[0] == "pull":
                sistema_archivos.pull(comandos[1])
            elif comandos[0] == "remove":
                sistema_archivos.remove(comandos[1])

        if comando in ("mostrar", "listar"):
            sistema_archivos.directorio.listar(detalles=False)

        if comando in ("ls", "mostrar", "listar"):
            sistema_archivos.directorio.listar(detalles=False)

        if comando in ("ls -l", "mostrar detalles", "listar detalles"):
            sistema_archivos.directorio.listar(detalles=True)

        if comando in ("help", "ayuda", "man"):
            mostrar_manual()

        if comando in ("clear", "limpiar"):
            limpiar_pantalla()

        if comando in ("salir", "exit", ":q"):
            exit(0)

def cli():
    sistema_archivos = SistemaArchivos(ruta_sistema="../fiunamfs.img")

    args = sys.argv

    if args[1] == 'push':
        # si no es el numero de argumentos correcto se mostrara manual
        if len(args) not in (3, 4):
            mostrar_manual()
            exit(1)

        ruta_externa = args[2]
        nombre_interno = ''
        if len(args) == 4:
            nombre_interno = args[3]

        sistema_archivos.push(ruta_externa, nombre_interno)

    elif args[1] == 'pull':
        if len(args) not in (3, 4):
            mostrar_manual()
            exit(1)

        nombre_interno = args[2]
        if len(args) == 4:
            ruta_externa = args[3]
        else:
            ruta_externa = './'

        sistema_archivos.pull(nombre_interno, ruta_externa)


    elif args[1] == 'remove' or args[1] == 'rm':
        if len(args) != 3:
            mostrar_manual()
            exit(1)

        nombre_archivo = args[2]
        sistema_archivos.remove(nombre_archivo)

    elif args[1] == 'ls':
        if len(args) == 3 and args[2] == '-l':
            sistema_archivos.directorio.listar(detalles=True)
        else:
            sistema_archivos.directorio.listar(detalles=False)

    elif args[1] == 'shell':
        del sistema_archivos
        shell()
    else:
        mostrar_manual()

    exit(0)

if __name__ == "__main__":
    cli()