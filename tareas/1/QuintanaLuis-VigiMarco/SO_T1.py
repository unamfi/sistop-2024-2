import os
import platform

asignacion = ['A','-','-','-','-','-','-','-','-','-',
              '-','-','-','-','-','C','C','C','-','-',
              '-','A','-','-','B','-','-','-','B','B']

caracteres = []
impresionCaracteres = ""

procesosPosibles = list(map(chr, range(68, 91)))

def imprimirAsignacion():
    print("Asignacion actual:")
    print("".join(map(str, asignacion)))

def caracteresLista():
    conjunto_unico = {elemento for elemento in asignacion if '-' not in elemento}
    caracteres = list(conjunto_unico)
    print("")
    print("("+"".join(map(str, caracteres))+")")

def compactar():
    numeroLibres = asignacion.count('-')

    for i in range(numeroLibres):
        asignacion.remove('-')


    for i in range(numeroLibres):
        asignacion.append('-')

def getNumeroUnidadesLibres():
    return asignacion.count('-')

def getIndexUnidadesLibres(unidadesRequeridas):
    registrarIndex = True
    i = 0
    libresConsecutivas = 0
    libres = 0
    index = 0

    if (unidadesRequeridas > getNumeroUnidadesLibres()):
        raise ValueError(f"No se tienen {unidadesRequeridas} localidades requeridas")

    # iterar hasta encontrar numero consecutivo de unidades libres
    while i != len(asignacion)-1:
        if (asignacion[i] == '-'):
            libres += 1
            libresConsecutivas += 1

            if (registrarIndex):
                index = i
                registrarIndex = False

            if (libresConsecutivas == unidadesRequeridas):
                return index

        else:
            libresConsecutivas = 0
            registrarIndex = True

        i+=1

    if (unidadesRequeridas <= asignacion.count('-')):
        compactar()
        return getIndexUnidadesLibres(unidadesRequeridas)

def asignarProceso(inicio, requeridas, proceso):
    for l in range(inicio, inicio+requeridas):
        asignacion[l] = proceso

def asignar(proceso):
    unidades = int(input(f"Nuevo proceso ({proceso}): "))

    if (unidades > 15):
        print(f"No se puede solicitar más de 15 unidades")
        input("Ingrese cualquier tecla para continuar...")
        return

    try:
        index = getIndexUnidadesLibres(unidades)
        asignarProceso(index, unidades, proceso)
    except ValueError as ex:
        print(getattr(ex, 'message', str(ex)))
        input("Ingrese cualquier tecla para continuar...")



def liberar():
    caracteresLista()
    liberar = input("Proceso a liberar: ")
    for i in range(len(asignacion)):
        if asignacion[i] == liberar:
            asignacion[i] = '-'
        else:
            continue
    input("Ingrese cualquier tecla para continuar...")

def limpiarPantalla():
    if platform.platform() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def ciclo():
    while True:
        limpiarPantalla()
        imprimirAsignacion()
        print("0 - Asignar")
        print("1 - Liberar")
        print("2 - Salir")
        opcion = int(input("Ingresa la opcion a elegir: "))
        if opcion == 0:
            asignar(procesosPosibles.pop(0))
        elif opcion == 1:
            liberar()
        elif opcion == 2:
            print("\nAdios...")
            break
        else:
            print("Opcion no válida, regresando a la asignación actual...")

ciclo()
