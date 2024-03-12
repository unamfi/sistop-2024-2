total_memoria = 30
memoria = {}

def imprimir_mapa_memoria():
    global memoria
    memoria_actual = ['-' for _ in range(total_memoria)]
    for proceso, info in memoria.items():
        indiceInicio = info['indiceInicio']
        tamProceso = info['tamaño proceso']
        if indiceInicio + tamProceso > total_memoria:
            print(f"Error: el proceso excede los límites de la memoria.")
            return
        for i in range(tamProceso):
            memoria_actual[indiceInicio + i] = proceso
    print("Asignación actual:")
    print(''.join(memoria_actual))


def asignar_memoria(proceso, tamProceso, ajuste):
    global total_memoria
    global memoria

    if proceso in memoria:
        print(f"El proceso ya está en memoria.")
        return

    if tamProceso < 2 or tamProceso > 15:
        print("Tamaño de proceso no válido. Debe estar entre 2 y 15 unidades.")
        return

    espacio_disponible = total_memoria - sum([info['tamaño proceso'] for info in memoria.values()])
    if espacio_disponible < tamProceso:
        print("No hay suficiente espacio en la memoria para asignar este proceso.")
        return

    if ajuste == 0:
        indiceInicio = encontrar_peor_ajuste(tamProceso)
    elif ajuste == 1:
        indiceInicio = encontrar_mejor_ajuste(tamProceso)
    else: 
        indiceInicio = encontrar_primer_ajuste(tamProceso)

    memoria[proceso] = {'indiceInicio': indiceInicio, 'tamaño proceso': tamProceso}
    print(f"El proceso se asignó con éxito a la memoria.")
    imprimir_mapa_memoria()

def liberar_memoria(proceso):
    global memoria

    if proceso not in memoria:
        print(f"El proceso no se encuentra en memoria.")
        return

    del memoria[proceso]
    print(f"El proceso se liberó de la memoria.")
    imprimir_mapa_memoria()

def encontrar_primer_ajuste(tamProceso):
    global memoria
    indiceInicio = 0
    for _, info in memoria.items():
        indiceInicio = info['indiceInicio'] + info['tamaño proceso']
    return indiceInicio

def encontrar_peor_ajuste(tamProceso):
    global memoria
    indiceInicio = -1
    max_hueco = 0
    memoria_actual = ['-' for _ in range(total_memoria)]
    for i in range(total_memoria):
        if memoria_actual[i] == '-':
            j = i
            while j < total_memoria and memoria_actual[j] == '-':
                j += 1
            hueco_actual = j - i
            if hueco_actual > max_hueco:
                max_hueco = hueco_actual
                indiceInicio = i
    return indiceInicio

def encontrar_mejor_ajuste(tamProceso):
    global memoria
    indiceInicio = -1
    min_hueco = total_memoria
    memoria_actual = ['-' for _ in range(total_memoria)]
    for i in range(total_memoria):
        if memoria_actual[i] == '-':
            j = i
            while j < total_memoria and memoria_actual[j] == '-':
                j += 1
            hueco_actual = j - i
            if hueco_actual >= tamProceso and hueco_actual < min_hueco:
                min_hueco = hueco_actual
                indiceInicio = i
    return indiceInicio

while True:
    print("1. Asignar memoria a un proceso")
    print("2. Liberar memoria de un proceso")
    print("0. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        proceso = input("Ingrese nuevo proceso: ")
        tamProceso = int(input("Ingrese el tamaño del proceso (entre 2 y 15 unidades): "))
        ajuste = input("Seleccione el tipo de ajuste: 1) Peor ajuste  2) Mejor ajuste  3) Primer_ajuste: ")
        asignar_memoria(proceso, tamProceso, ajuste)
    elif opcion == "2":
        proceso = input("Proceso por liberar ")
        liberar_memoria(proceso)
    elif opcion == "0":
        print("Programa finalizado")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")