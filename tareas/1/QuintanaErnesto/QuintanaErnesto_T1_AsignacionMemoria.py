
class AdministradorMemoria:
    def __init__(self, tamanio=30):#Se determina el tamaño de unidades totales de memoria
        self.memoria = ['-'] * tamanio
        self.procesos = {}

    def primer_ajuste(self, id_proceso, tamanio): #Escoge el primer hueco libre de tamaño suficiente.
        for i, celda in enumerate(self.memoria):
            if celda == '-':
                for j in range(i, i + tamanio):
                    if j >= len(self.memoria) or self.memoria[j] != '-':
                        break
                else:
                    for j in range(i, i + tamanio):
                        self.memoria[j] = id_proceso
                    self.procesos[id_proceso] = (i, tamanio)
                    return True
        return False

    def mejor_ajuste(self, id_proceso, tamanio): # Hueco más pequeño con tamaño suficiente (requiere ver toda la lista si no está ordenada).
        mejores = []
        actual = []
        for i, celda in enumerate(self.memoria):
            if celda == '-':
                actual.append(i)
            else:
                if len(actual) >= tamanio:
                    mejores.append((len(actual), actual[0]))
                actual = []
        if len(actual) >= tamanio:
            mejores.append((len(actual), actual[0]))

        if mejores:
            mejor_tam, mejor_inicio = min(mejores, key=lambda x: x[0])
            for i in range(mejor_inicio, mejor_inicio + tamanio):
                self.memoria[i] = id_proceso
            self.procesos[id_proceso] = (mejor_inicio, tamanio)
            return True
        return False

    def peor_ajuste(self, id_proceso, tamanio):# Hueco más grande: Pretende conseguir que los huecos que queden sean grandes (requiere ver toda la lista si no ordenada)
        huecos = []
        actual = []
        for i, celda in enumerate(self.memoria):
            if celda == '-':
                actual.append(i)
            else:
                if actual:
                    huecos.append((len(actual), actual[0]))
                actual = []
        if actual:
            huecos.append((len(actual), actual[0]))

        if huecos:
            peor_tam, peor_inicio = max(huecos, key=lambda x: x[0])
            for i in range(peor_inicio, peor_inicio + tamanio):
                self.memoria[i] = id_proceso
            self.procesos[id_proceso] = (peor_inicio, tamanio)
            return True
        return False

    def asignar_memoria(self, id_proceso, tamanio, estrategia):
        if estrategia == '1':
            return self.primer_ajuste(id_proceso, tamanio)
        elif estrategia == '2':
            return self.mejor_ajuste(id_proceso, tamanio)
        elif estrategia == '3':
            return self.peor_ajuste(id_proceso, tamanio)
        else:
            return False

    def liberar_memoria(self, id_proceso):
        if id_proceso in self.procesos:
            inicio, tamanio = self.procesos[id_proceso]
            for i in range(inicio, inicio + tamanio):
                self.memoria[i] = '-'
            del self.procesos[id_proceso]
            return True
        else:
            return False

    def compactar_memoria(self): #Recorre los procesos a los espacios disponibles para que se puedan almacenar mas procesos en memoria
        memoria_compacta = [celda for celda in self.memoria if celda != '-']
        memoria_compacta += ['-'] * (len(self.memoria) - len(memoria_compacta))
        self.memoria = memoria_compacta

    def imprimir_memoria(self):
        print('\n')
        print(''.join(self.memoria))

    def menu(self):
        while True:
            print("\n\t--MENU--")
            print("[1] Asignar memoria \n[2] Liberar memoria\n[3] Salir")

            opcion = input("Seleccione una opcion: ")

            if opcion == '1':
                id_proceso = input("Ingrese el IDENTIFICADOR del proceso: ")
                tamanio = int(input("Ingrese el tamaño del proceso: "))

                if tamanio >= 2 and tamanio <=15 :
                    estrategia = input("[1] Primer ajuste\n[2] Mejor ajuste\n[3] Peor ajuste\nIngrese la estrategia: ")
                    if estrategia not in ['1', '2', '3']:
                        print("Opcion no valida.")
                        continue
                    if self.asignar_memoria(id_proceso, tamanio, estrategia):
                        print(f"Proceso {id_proceso} asignado {tamanio} unidades.")
                    else:
                        print("Memoria insuficiente, se requiere compactación.")
                        self.compactar_memoria()
                        if self.asignar_memoria(id_proceso, tamanio, estrategia):
                            print(f"Proceso {id_proceso} asignado {tamanio} unidades después de la compactación.")
                        else:
                            print("No se pudo asignar memoria después de la compactación.")
                else:
                    print('El tamaño de memoria solo puede ser de 2 a 15 unidades por PROCESO')
                
                self.imprimir_memoria()
                     
                
            elif opcion == '2':
                id_proceso = input("Ingrese el IDENTIFICADOR del proceso a liberar: ")
                if self.liberar_memoria(id_proceso):
                    print(f"Proceso {id_proceso} liberado.")
                    self.imprimir_memoria()
                else:
                    print(f"Proceso {id_proceso} no encontrado.")


            elif opcion == '3':
                print("Adios!")
                break
                
            else:
                print("Opción no valida,seleccione alguna opcion del menu.")

# Inicializador
print('\n\t\t~{ASIGNACION DE MEMORIA}~')
administrador = AdministradorMemoria()
administrador.menu()
