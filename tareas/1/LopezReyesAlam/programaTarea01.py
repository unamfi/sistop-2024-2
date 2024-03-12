
##Lopez Reyes Alam -- Tarea 01 utilizando primer ajuste
class AdministradorMemoria:
    def __init__(self, tamaño=30):
        self.tamaño = tamaño
        self.memoria = ['-'] * tamaño  # Representa la memoria vacía inicialmente

    def imprimir_memoria(self):
        print("\nAsignación actual:\n")
        print(''.join(self.memoria) + "\n")

    def asignar(self, id_proceso, unidades):
        if unidades < 2 or unidades > 15:
            print("El proceso debe requerir entre 2 y 15 unidades.\n")
            return False

        indice = self.encontrar_primer_ajuste(unidades)
        if indice == -1:
            print("No hay suficiente espacio contiguo disponible. *Compactación requerida*\n")
            self.compactar()
            indice = self.encontrar_primer_ajuste(unidades)
            if indice == -1:
                print("Aún no hay suficiente espacio disponible después de la compactación.\n")
                return False

        for i in range(indice, indice + unidades):
            self.memoria[i] = id_proceso
        return True

    def liberar(self, id_proceso):
        liberado = False
        for i in range(len(self.memoria)):
            if self.memoria[i] == id_proceso:
                self.memoria[i] = '-'
                liberado = True
        return liberado

    def encontrar_primer_ajuste(self, unidades):
        cuenta_libre = 0
        for i in range(len(self.memoria)):
            if self.memoria[i] == '-':
                cuenta_libre += 1
                if cuenta_libre == unidades:
                    return i - unidades + 1
            else:
                cuenta_libre = 0
        return -1

    def compactar(self):
        self.memoria = [x for x in self.memoria if x != '-'] + ['-'] * self.memoria.count('-')
        print("Memoria compactada.\n")

def interfaz_usuario():
    admin_memoria = AdministradorMemoria()
    admin_memoria.imprimir_memoria()

    while True:
        acción = input("Asignar (0), Liberar (1), Salir (cualquier otra tecla): ")
        if acción == '0':  # Asignar
            id_proceso = input("Nuevo proceso (una letra): ")
            unidades = int(input("Unidades de memoria requeridas (2-15): "))
            if admin_memoria.asignar(id_proceso, unidades):
                print("Nueva asignación:")
            else:
                print("Asignación fallida.")
            admin_memoria.imprimir_memoria()
        elif acción == '1':  # Liberar
            id_proceso = input("Proceso a liberar (una letra): ")
            if admin_memoria.liberar(id_proceso):
                print(f"Memoria liberada para el proceso {id_proceso}:")
            else:
                print(f"Proceso {id_proceso} no encontrado o ya liberado.")
            admin_memoria.imprimir_memoria()
        else:
            print("Saliendo del programa...")
            break

if __name__ == "__main__":
    interfaz_usuario()
