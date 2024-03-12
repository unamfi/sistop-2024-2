from random import randint as aleatorio
import os 

ProcesosEnMemoria = []
abecedario = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
numero = ['1','2','3','4','5','6','7','8','9'] 
indice=0 #Es un indice para decirle a una función que letra asignarle como nombre a un nuevo proceso
opcion = 0 #Se puede anañir un proceso, liberar un proceso o finalizar el programa
total = 0 #Indica el espacio ya ocupado en memoria
numProcesos = 0  #Indica cuantos procesos se encuentran activos
indiceNum = -1 #Indica el numero que se va a concatenar con la letra para ponerle un nombre al proceso
op = 0 #Indica la forma de procesar solicitudes
contador = 3 #Sirve para controlar la cantidad de veces que se utiliza la forma de procesar una solicitud
class Proceso:
    def __init__(self,name = '-',lenght = 1):
        self.name = name
        self.lenght = lenght
    
    def setName(self,nombre):
        self.name = nombre

    def getName(self):
        return self.name

    def setLenght(self,tam):
        self.lenght = tam

    def getLenght(self):
        return self.lenght

def limpiarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

def imprimirMemoria(numP):
    print("Asignación de memoria actual (",numP,end=' ')
    if numP == 1: print("proceso activo)\n")
    else: print("procesos activos)\n")
    for elemento in ProcesosEnMemoria:
        print(elemento.getName(),end= " ")
    print("\n")

def revisarEspacio(tam, bandera,total,nump,operacion,cantVeces):
    tamProceso = tam
    indexMin = 0 #Indica el indice a partir del cual se va a insertar el proceso
    indexMax = 0 #Indica el indice hasta donde se va a insertar el proceso
    encontrado = 0 #Indica si se encontró espacio suficiente en memoria para insertar el proceso
    tam_min = 0 #Se utiliza para el mejor y peor ajuste, sirve para comparar en donde hay el mayor o menor espacio donde cabe el proceso
    temp = 40 #Se utiliza para el mejor y peor ajuste, sirve para comparar
    j = 0
    k = 0
    if cantVeces == 0: #Indica la cantidad de veces que se va a procesar una solicitud de x forma
        cantVeces = 3
        operacion = 0
    while operacion != 1:
        if operacion == 0:
            operacion = int(input("Procesamiento de las siguientes 3 solicitudes:\n *Escriba 1 si quiere el primer ajuste, 2 para el mejor ajuste o 3 para el peor ajuste: "))
            limpiarPantalla()
            imprimirMemoria(nump)
        if operacion == 2: #Procesar con mejor  ajuste, buscar el espacio minimo con el que cumple la condición
            while j < len(ProcesosEnMemoria):
                if ProcesosEnMemoria[j].getName() == '-': #Si hay un espacio vacio en memoria, empieza a contarse
                    tam_min += 1
                    k = j + 1
                    while k < len(ProcesosEnMemoria) and ProcesosEnMemoria[k].getName() == '-': #Mientras haya espacios vacios se va a contar todo el espacio libre
                        tam_min += 1
                        k += 1
                    if tam_min >= tamProceso and tam_min < temp:#Si en el bloque actual cabe el proceso y el bloque es más pequeño que otro bloque libre
                        indexMin = j #Se guardan los indices y se actualiza la variable temporal
                        indexMax = j + tamProceso
                        temp = tam_min
                tam_min = 0 #Se reestablece el contador para seguir revisando la memoria
                if ProcesosEnMemoria[j].getName() != '-': #Si el espacio ya está ocupado entonces se salta todo ese proceso para revisar si hay más espacio libre
                    j += ProcesosEnMemoria[j].getLenght()
                else:
                    j += temp
            if indexMax-indexMin != tamProceso: #Si no se encontró espacio en memoria 
                if total + tam >= len(ProcesosEnMemoria) + 1: return -1,-1,cantVeces,operacion #Si toda la memoria está ocupada entonces se manda un mensaje a terminal
                if total + tam < len(ProcesosEnMemoria) + 1: #Si aun hay espacio pero no cabe el proceso
                    if bandera == 0:  #Si aun no se ha realizado la compactación
                        bandera = compactacion() #Después de compactación se revisa nuevamente si cabe el proceso en memoria
                        indexMin,indexMax,cantVeces,operacion = revisarEspacio(tam,bandera,total,nump,operacion,cantVeces)
                        return indexMin,indexMax,cantVeces,operacion 
                    if bandera == 1: #Si ya se realizó la compactación y el proceso no cabe, entonces se mandan ciertos valores para indicar que no cabe
                        return -1,-1,cantVeces,operacion
            print("\nResolviendo solicitud por mejor ajuste...\n")
            return indexMin,indexMax,cantVeces,operacion
        if operacion == 3: #Procesa con peor ajuste, busca el lugar donde se desperdicie más espacio
            temp = 0 #Se ejecuta casi de la misma forma que el mejor ajuste
            while j < len(ProcesosEnMemoria):
                if ProcesosEnMemoria[j].getName() == '-':
                    tam_min += 1
                    k = j + 1
                    while k < len(ProcesosEnMemoria) and ProcesosEnMemoria[k].getName() == '-':
                        tam_min += 1
                        k += 1
                    if tam_min >= tamProceso and tam_min > temp: #La diferencia es que revisa si ahora el bloque actual es más grande que otro bloque
                        indexMin = j
                        indexMax = j + tamProceso
                        temp = tam_min
                tam_min = 0
                if ProcesosEnMemoria[j].getName() != '-':
                    j += ProcesosEnMemoria[j].getLenght()
                else:
                    if temp != 0: j += temp
                    else: j += 1
            if indexMax-indexMin != tamProceso: #Si no se encontró hueco en memoria 
                if total + tam >= len(ProcesosEnMemoria) + 1: return -1,-1,cantVeces,operacion #Si ya no hay espacio entonces manda mensaje
                if total + tam < len(ProcesosEnMemoria) + 1: #Si aun hay espacio pero no cabe el proceso
                    if bandera == 0:  #Si aun no se ha realizado la compactación
                        bandera = compactacion()
                        indexMin,indexMax,cantVeces,operacion = revisarEspacio(tam,bandera,total,nump,operacion,cantVeces)
                        return indexMin,indexMax,cantVeces,operacion
                    if bandera == 1: #Si ya se realizó la compactación y el proceso no cabe, entonces se mandan ciertos valores para indicar que no cabe
                        return -1,-1,cantVeces,operacion
            print("\nResolviendo solicitud por peor ajuste...\n")
            return indexMin,indexMax,cantVeces,operacion

    for i in range(len(ProcesosEnMemoria)): #Procesa con el primer ajuste, encuentra el primer lugar donde quepa el proceso
        if ProcesosEnMemoria[i].getName() == '-':  #Si el espacio está vacío, puede seguir revisando si cabe todo el proceso
            tamProceso-=1
            if tamProceso == 0: 
                indexMax = i+1
                indexMin = i-(tam-1)
                encontrado = 1
                break
        else:
            tamProceso = tam #Si no hay espacio, se reestablece el contador y sigue buscando en la memoria
    if encontrado != 1:
        if total + tam >= len(ProcesosEnMemoria) + 1: return -1,-1,cantVeces,operacion #Si el proceso no cupo en memoria y ya está llena, se lanza un mensaje
        if total + tam < len(ProcesosEnMemoria) + 1: #Si la memoria aun no está llena entonces se indica que se debe liberar un proceso
            if bandera == 0:  #Si aun no se ha realizado la compactación
                bandera = compactacion()
                indexMin,indexMax,cantVeces,operacion = revisarEspacio(tam,bandera,total,nump,operacion,cantVeces)
                return indexMin,indexMax,cantVeces,operacion
            if bandera == 1: #Si ya se realizó la compactación y el proceso no cabe, entonces se mandan ciertos valores para indicar que no cabe
                return -1,-1,cantVeces,operacion
    print("\nResolviendo solicitud por primer ajuste...\n")
    return indexMin,indexMax,cantVeces,operacion 

def compactacion():
    print("\nREALIZANDO COMPACTACIÓN...")
    for i in range(len(ProcesosEnMemoria)):
        for j in range(len(ProcesosEnMemoria)):#Se utiliza bubbleSort para desplazar los espacios libres hacia la derecha
            if j < len(ProcesosEnMemoria)-1:
                if ProcesosEnMemoria[j].getName() == '-' and ProcesosEnMemoria[j+1].getName() != '-': 
                    temp = ProcesosEnMemoria[j]
                    ProcesosEnMemoria[j] = ProcesosEnMemoria[j+1]
                    ProcesosEnMemoria[j+1] = temp
    return 1 #Sirve para indicar que ya se realizó 1 vez este procedimiento
   
def crearProceso(indice,total,cantidad,idxNum,operacion,numVeces):
    compactacionFlag = 0
    tam = aleatorio(2,15)
    min,max,numVeces,operacion = revisarEspacio(tam,compactacionFlag,total,cantidad,operacion,numVeces)
    if min == -1 and max == -1: #Dependiendo de si cupo o no un proceso entonces se lanza el siguiente mensaj
        print("\nEl proceso asignado es muy grande y no cabe en memoria, se recomienda liberar algún proceso")
        return indice,total,cantidad,idxNum,numVeces,operacion
    if indice < 26 and idxNum == -1: #Sirve para asignarle un nombre al proceso
        nombre = abecedario[indice]
        indice += 1
    else:
        if indice == 26: #Si ya se ocuparon todas las letras del alfabeto entoncs ahora se van a combinar con los números del 1 al 9
            indice = 0
            idxNum += 1
        nombre = abecedario[indice] + numero[idxNum]
        indice += 1
    total += tam
    cantidad += 1
    for i in range(min,max): #Aquí se configura el nombre y tamaño de los procesos
        ProcesosEnMemoria[i].setName(nombre)
        ProcesosEnMemoria[i].setLenght(tam)
    print("\nEl proceso " + nombre + " requiere " + str(tam) + " unidades de memoria\n\n")
    numVeces -= 1
    return indice,total,cantidad,idxNum,numVeces,operacion
 
def liberarProceso(numP,total):
    limpiarPantalla()
    imprimirMemoria(numP)
    print("¿Qué proceso deseas liberar?",end='(')
    i = 0
    while i < 30:
        if ProcesosEnMemoria[i].getName() != '-':
            print(ProcesosEnMemoria[i].getName(), end='/')
        i += ProcesosEnMemoria[i].getLenght()
    print(')',end=': ')
    nombre = input() #Después de seleccionar el proceso hay que buscar que exista
    nombre = nombre.upper()
    i = 0   
    encontrado = 0
    while i < 30: #básicamente busca la posición del proceso y le cambia el nombre y tamaño
        if  ProcesosEnMemoria[i].getName() != '-' and ProcesosEnMemoria[i].getName() == nombre:
            encontrado = 1
            break
        i+= ProcesosEnMemoria[i].getLenght()
    if encontrado == 1:
        min = i 
        max = i + ProcesosEnMemoria[i].getLenght()
        total -= ProcesosEnMemoria[i].getLenght()
        numP -= 1
        for j in range(min,max):
            ProcesosEnMemoria[j].setName('-')
            ProcesosEnMemoria[j].setLenght(1)
    else:
        print("Proceso no encontrado!")
        input("\nPresione enter para continuar...\n")
    return numP,total

for i in range(30): #Se crea inicialmente la lista con los 30 espacios libres en memoria para los procesos
    ProcesosEnMemoria.append(Proceso())
while opcion != 2:
    imprimirMemoria(numProcesos)
    opcion = int(input("Escribe 0 para ASIGNAR un proceso, 1 para LIBERAR un proceso o 2 para finalizar el programa: "))
    if opcion == 0:
        indice,total,numProcesos,indiceNum,contador,op = crearProceso(indice,total,numProcesos, indiceNum,op,contador)
        input("Presione enter para continuar...\n")
    if opcion == 1:
        numProcesos,total = liberarProceso(numProcesos,total)
    limpiarPantalla()