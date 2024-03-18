def asignarAMemoria(proceso: str, procesoAMeter):
    if proceso.count("-") < procesoAMeter.__len__():
        print("El proceso ya no cabe en la memoria")
        return
    procesoAMeter = procesoAMeter.upper()
    cadenaAreemplazar = ""
    for i in range(procesoAMeter.__len__()):
        cadenaAreemplazar += "-"

    proceso = proceso.replace(cadenaAreemplazar, procesoAMeter, 1)
    print("La memoria queda de la siguiente manera: "+proceso)
    return proceso


def liberarEspacio(proceso: str, letraALiberar):
    proceso = proceso.replace(letraALiberar, '-')
    print("La memoria queda de la siguiente manera: " + proceso)
    return proceso


asignacionOriginal = input(
    "Ingresa lo que hay dentro de memoria actualmente (tenemos 30 unidades de memoria)\n --> ")
# print(asignacionOriginal)
asignacionOriginal = asignacionOriginal.replace(" ", "")
asignacionOriginal = asignacionOriginal.upper()

longitudInicial = len(asignacionOriginal)
longitudASumar = 30 - longitudInicial

proceso = ""

for i in range(longitudASumar):
    proceso += "-"

asignacionOriginal += proceso
proceso = asignacionOriginal

print(proceso)
flag = True
while flag == True:
    print("\n\n¿Qué es lo que quieres hacer?")
    print("1.-Asignar a la memoria\n2.-Liberar espacio en la memoria\n3.-Salir")
    option = input("Quiero --> ")

    if option == "1":
        procesoAMeter = input("¿Qué es lo que quieres ingresar?")
        if procesoAMeter.__len__() < 2 or procesoAMeter.__len__() > 15:
            print("El proceso es muy grande o muy pequeño, intenta otro diferente")
        else:
            proceso = asignarAMemoria(proceso, procesoAMeter)

    elif option == "2":
        queLetrasTenemos = set(proceso)
        queLetrasTenemos.remove("-")
        print("Que quieres liberar en la memoria, tenemos: ")
        print(queLetrasTenemos)
        letraALiberar = input("--> ")
        letraALiberar = letraALiberar.upper()
        proceso = liberarEspacio(proceso, letraALiberar)
    elif option == "3":
        flag = False
    else:
        print("Por favor ingresa una opción correcta")
