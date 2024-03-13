#De la Merced Soriano Uriel Benjamin
#Hernandez Gutierrez Carlos Mario

#Tarea 1 realizada por el metodo de primer ajuste

def compactarMemoria(memoriaTotal):
    print("*Compactación requerida*")
    memoriaTotal_string = ''.join([unit for unit in memoriaTotal if unit != '-'])
    memoriaTotal[:len(memoriaTotal_string)] = memoriaTotal_string
    memoriaTotal[len(memoriaTotal_string):] = ['-'] * (30 - len(memoriaTotal_string))
    print("Nueva situación:")
    print(''.join(memoriaTotal))
    return memoriaTotal

def AsignarMemoria(memoriaTotal, procesoActual, memoriaDisponible, procesosOcupados, tamanioMemoria):
    if memoriaDisponible >= tamanioMemoria:
        asignandoEspacio = False
        varAux = 0
        for i in range(30):
            if memoriaTotal[i] == '-':
                varAux += 1
                if varAux == tamanioMemoria:
                    for j in range(i - tamanioMemoria + 1, i + 1):
                        memoriaTotal[j] = chr(procesoLetra + procesoActual)
                    procesosOcupados.append(chr(procesoLetra + procesoActual))
                    procesoActual += 1
                    memoriaDisponible -= tamanioMemoria
                    asignandoEspacio = True
                    break
            else:
                varAux = 0
        if not asignandoEspacio:
            compactarMemoria(memoriaTotal)
            procesoActual = AsignarMemoria(memoriaTotal, procesoActual, memoriaDisponible, procesosOcupados, tamanioMemoria)
        print("Asignación actual:")
        print(''.join(memoriaTotal))
    else:
        print("Memoria insuficiente")
    return procesoActual

def memoriaLibre(memoriaTotal, liberarProceso, memoriaDisponible, procesosOcupados):
    for i in range(30):
        if memoriaTotal[i] == liberarProceso:
            memoriaTotal[i] = '-'
            memoriaDisponible += 1
    procesosOcupados.remove(liberarProceso)
    print("Asignación actual:")
    print(''.join(memoriaTotal))

# Inicialización de variables
memoriaTotal = ['-'] * 30
procesoLetra = ord('A')
procesoActual = 0
memoriaDisponible = 30
procesosOcupados = []

print("Asignación actual:")
print(''.join(memoriaTotal))

opcion = None
while opcion != 'salir':
    opcion = input("Asignar (0), liberar (1) o salir (salir): ")
    
    if opcion == '0':
        tamanioMemoria = int(input("Tamaño del proceso (2-15): "))
        if 2 <= tamanioMemoria <= 15:
            procesoActual = AsignarMemoria(memoriaTotal, procesoActual, memoriaDisponible, procesosOcupados, tamanioMemoria)
        else:
            print("Tamaño inválido. El tamaño debe estar entre 2 y 15.")
    
    elif opcion == '1':
        if not procesosOcupados:
            print("No hay procesos en memoria para liberar.")
            continue
        liberarProceso = input("Proceso a liberar (" + ''.join(procesosOcupados) + "): ")
        if liberarProceso in procesosOcupados:
            memoriaLibre(memoriaTotal, liberarProceso, memoriaDisponible, procesosOcupados)
        else:
            print("Proceso no encontrado.")
    
    elif opcion != 'exit':
        print("Acción no válida.")
        break
