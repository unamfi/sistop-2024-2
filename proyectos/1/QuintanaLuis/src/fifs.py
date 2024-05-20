"""
Proyecto 1

"""
from sistema_archivos import SistemaArchivos
import sys
import os
import platform
import excepciones

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
        try:
            comando = input("$ ")

            if comando == "":
                mostrar_manual()

            # Comando interactivo
            elif comando == "push":
                print("Copiando archivo del sistema a fi unam fs")
                archivo_externo = input("Ingrese el nombre de archivo de su sistema: ")
                nombre_por_defecto = os.path.basename(archivo_externo)
                archivo_interno = input(
                    f"Ingrese el nombre con el que se copiará a fi unam fs [Por defecto: {nombre_por_defecto}]: ")

                sistema_archivos.push(archivo_externo, archivo_interno)
                print(f"Se ha copiado {archivo_externo} a {archivo_interno}")

            elif comando == "pull":
                print("Copiando archivo de fi unam fs a su sistema")
                archivo_interno = input("Ingrese el nombre de archivo de fi unam fs: ")
                archivo_externo = input(
                    f"Ingrese el nombre con el que se copiará a fi unam fs [Por defecto: {archivo_interno}]: ")

                sistema_archivos.pull(archivo_interno, archivo_externo)
                print(f"Se ha copiado {archivo_interno} a {archivo_externo}")

            elif comando == "remove":
                print("Eliminando archivo de fi unam fs")
                archivo_interno = input("Ingrese el nombre de archivo de fi unam fs: ")
                aceptar = input(f"\t¿Está seguro de eliminar {archivo_interno}? [SI/no]: ")

                if aceptar == "SI":
                    sistema_archivos.remove(archivo_interno)
                    print(f"Se ha eliminado {archivo_interno}")


            elif comando in ("mostrar", "listar"):
                sistema_archivos.directorio.listar(detalles=False)

            elif comando in ("ls", "mostrar", "listar"):
                sistema_archivos.directorio.listar(detalles=False)

            elif comando in ("ls -l", "mostrar detalles", "listar detalles", "ll"):
                sistema_archivos.directorio.listar(detalles=True)

            elif comando in ("help", "ayuda", "man"):
                mostrar_manual()

            elif comando in ("clear", "limpiar"):
                limpiar_pantalla()

            # Comando directo
            elif len(comando.split()) > 1:
                comandos = comando.split()
                if comandos[0] == "push":
                    if len(comandos) == 3:
                        sistema_archivos.push(comandos[1], comandos[2])
                    else:
                        sistema_archivos.push(comandos[1])

                elif comandos[0] == "pull":
                    sistema_archivos.pull(comandos[1])
                    if len(comandos) == 3:
                        sistema_archivos.pull(comandos[1], comandos[2])
                    else:
                        sistema_archivos.pull(comandos[1])
                elif comandos[0] in ("remove", "rm") and comandos[1] in ("-f", "--force"):
                    sistema_archivos.remove(comandos[2])
                    print(f"Se ha eliminado {comandos[2]}")

                elif comandos[0] in ("remove", "rm"):
                    aceptar = input(f"\t¿Está seguro de eliminar {comandos[1]}? [SI/no]: ")

                    if aceptar == "SI":
                        sistema_archivos.remove(comandos[1])
                        print(f"Se ha eliminado {comandos[1]}")

            elif comando in ("salir", "exit", ":q"):
                exit(0)

            else:
                mostrar_manual()

        except excepciones.EntradaNoValidaException as ex:
            print(ex.message)

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
    try:
        cli()
    except excepciones.EntradaNoValidaException as ex:
        print(ex.message)
    except KeyboardInterrupt as ex:
        print("bye!")
