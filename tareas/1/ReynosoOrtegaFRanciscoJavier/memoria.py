import random

def asignar_memoria_variable(memoria, procesos, operacion, proceso_liberar=None, nuevo_proceso=None):
    """
    Asigna o libera memoria según la operación indicada.

    Args:
        memoria: Lista que representa la memoria del sistema.
        procesos: Lista que contiene las porciones de memoria asignadas a los procesos.
        operacion: 0 para asignar, 1 para liberar.
        proceso_liberar: Índice del proceso a liberar (si aplica).
        nuevo_proceso: Tamaño del nuevo proceso a asignar (si aplica).

    Returns:
        Lista con la nueva asignación de memoria.
        Booleano que indica si se requiere compactación.
    """

    if operacion == 0:
        # Asignar memoria
        if nuevo_proceso > max(memoria):
            # No hay suficiente espacio libre para el nuevo proceso
            return memoria, True
        else:
            index = memoria.index(max(memoria))
            procesos[index:index+nuevo_proceso] = [nuevo_proceso] * nuevo_proceso
            return procesos, False
    else:
        # Liberar memoria
        procesos[proceso_liberar:proceso_liberar+1] = [0]
        return procesos, False

def mostrar_asignacion(memoria, procesos):
    """
    Muestra la asignación actual de memoria.

    Args:
        memoria: Lista que representa la memoria del sistema.
        procesos: Lista que contiene las porciones de memoria asignadas a los procesos.
    """
    print("Asignación actual:")
    for proceso in procesos:
        print(proceso if proceso != 0 else "-", end="")
    print()

# Inicializar memoria y procesos
memoria_total = 30
memoria = [random.randint(2, 15) for _ in range(memoria_total)]
procesos = [0] * memoria_total

# Bucle de operaciones
while True:
    # Mostrar la asignación actual
    mostrar_asignacion(memoria, procesos)

    # Leer la operación
    operacion = int(input("Asignar (0) o liberar (1): "))

    # Leer el proceso a liberar (si aplica)
    proceso_liberar = None  # Inicialización aquí
    if operacion == 1:
        proceso_liberar = int(input("Índice de la porción de proceso a liberar: "))

    # Leer el nuevo proceso (si aplica)
    nuevo_proceso = None  # Inicialización aquí
    if operacion == 0:
        nuevo_proceso = int(input("Tamaño del proceso (entre 2 y 15): "))

    # Realizar la operación
    procesos, requiere_compactacion = asignar_memoria_variable(memoria, procesos, operacion, proceso_liberar, nuevo_proceso)

    # Si se requiere compactación, realizarla
    if requiere_compactacion:
        print("*Compactación requerida*")
