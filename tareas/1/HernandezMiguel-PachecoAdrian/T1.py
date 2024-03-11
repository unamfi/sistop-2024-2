TAM_MEM = 30
memory = ['-'] * TAM_MEM

def imprimir_memoria(memoria):
    print(''.join(memoria))

def asignar_memoria(memoria, id, proceso):
    allocated = 0
    for i in range(TAM_MEM):
        if memory[i] == '-':
            memory[i] = id
            allocated += 1
            if allocated == proceso:
                break

    if allocated == proceso:
        print(f"Asignando a {id}:")
        imprimir_memoria(memoria)
    else:
        print(f"No hay suficiente espacio disponible para asignar {proceso} unidades.")

def limpiar_memoria(memoria, id):
    for i in range(TAM_MEM):
        if memoria[i] == id:
            memoria[i] = '-'
    print(f"Proceso {id} liberado:")
    imprimir_memoria(memoria)

def memoria_usada(memory):
    used_space = TAM_MEM - memory.count('-')
    print(f"Memoria ocupada: {used_space}/{TAM_MEM}")

print("Asignación actual:")
imprimir_memoria(memory)

while True:
    option = input("Selecciona una opción:\n0. Asignar espacio\n1. Liberar espacio\n2. Ver memoria ocupada\n3. Salir\nOpción: ")

    if option == '0':
        id = input("Nuevo proceso (ID): ")
        proceso = int(input("Tamaño del proceso (2-15): "))
        liberar = memory.count('-')
        if liberar >= proceso:
            asignar_memoria(memory, id, proceso)
        else:
            print(f"El tamaño del proceso excede el límite de memoria disponible ({liberar} unidades).")
    elif option == '1':
        id = input("Proceso a liberar: ")
        limpiar_memoria(memory, id)
    elif option == '2':
        memoria_usada(memory)
    elif option == '3':
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida.")