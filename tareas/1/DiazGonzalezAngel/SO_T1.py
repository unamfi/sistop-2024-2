total_memoria = 30
memoria = {}

def imprimir_mapa_memoria():
    global memoria
    memoria_actual = ['-' for _ in range(total_memoria)]
    for process_id, info in memoria.items():
        start_index = info['start_index']
        size = info['size']
        if start_index + size > total_memoria:
            print(f"Error: el proceso {process_id} excede los límites de la memoria.")
            return
        for i in range(size):
            memoria_actual[start_index + i] = process_id
    print("Asignación actual:")
    print(''.join(memoria_actual))


def asignar_memoria(process_id, size, ajuste):
    global total_memoria
    global memoria

    if process_id in memoria:
        print(f"El proceso {process_id} ya está en memoria.")
        return

    if size < 2 or size > 15:
        print("Tamaño de proceso no válido. Debe estar entre 2 y 15 unidades.")
        return

    espacio_disponible = total_memoria - sum([info['size'] for info in memoria.values()])
    if espacio_disponible < size:
        print("No hay suficiente espacio en la memoria para asignar este proceso.")
        return

    # Determinar la posición de inicio para el nuevo proceso según el tipo de ajuste
    if ajuste == 0:
        start_index = encontrar_peor_ajuste(size)
    elif ajuste == 1:
        start_index = encontrar_mejor_ajuste(size)
    else:  # ajuste == "primer_ajuste"
        start_index = encontrar_primer_ajuste(size)

    memoria[process_id] = {'start_index': start_index, 'size': size}
    print(f"Proceso {process_id} asignado con éxito a la memoria.")
    imprimir_mapa_memoria()

def liberar_memoria(process_id):
    global memoria

    if process_id not in memoria:
        print(f"El proceso {process_id} no se encuentra en memoria.")
        return

    del memoria[process_id]
    print(f"Proceso {process_id} liberado de la memoria.")
    imprimir_mapa_memoria()

def encontrar_primer_ajuste(size):
    global memoria
    start_index = 0
    for _, info in memoria.items():
        start_index = info['start_index'] + info['size']
    return start_index

def encontrar_peor_ajuste(size):
    global memoria
    start_index = -1
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
                start_index = i
    return start_index

def encontrar_mejor_ajuste(size):
    global memoria
    start_index = -1
    min_hueco = total_memoria
    memoria_actual = ['-' for _ in range(total_memoria)]
    for i in range(total_memoria):
        if memoria_actual[i] == '-':
            j = i
            while j < total_memoria and memoria_actual[j] == '-':
                j += 1
            hueco_actual = j - i
            if hueco_actual >= size and hueco_actual < min_hueco:
                min_hueco = hueco_actual
                start_index = i
    return start_index

while True:
    print("\nOperaciones disponibles:")
    print("0. Asignar memoria a un proceso")
    print("1. Liberar memoria de un proceso")
    print("2. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "0":
        process_id = input("Ingrese nuevo proceso: ")
        size = int(input("Ingrese el tamaño del proceso (entre 2 y 15 unidades): "))
        ajuste = input("Seleccione el tipo de ajuste (peor_ajuste (0), mejor_ajuste (1), primer_ajuste (2): ")
        asignar_memoria(process_id, size, ajuste)
    elif opcion == "1":
        process_id = input("Proceso a liberar ")
        liberar_memoria(process_id)
    elif opcion == "2":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
