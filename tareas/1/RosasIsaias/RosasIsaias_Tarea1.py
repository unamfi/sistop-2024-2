# ASIGNATURA: Sistemas Operativos
# GRUPO: 6
# ALUMNO: Rosas Meza Isaías
# SEMESTRE: 2024-2

#BIBLIOTECAS
import os

# VARIABLES GLOBALES
memoria = []

# VISTA AL USUARIO
def menu():
	while True:
		print("TAREA 1: Asignación de memoria --> MÉTODO: Primer Ajuste \n")
		print("1) Agregar un proceso")
		print("2) Quitar un proceso")
		print("3) Salir del programa \n")
		op = input("Escoja una de las opciones anteriores: ")
		if op == '3':
			break
		opcion(op)


def opcion(op):
	global memoria
	if op == '1':
		proceso = input("Ingrese el proceso que desea almacenar [Valores alfanuméricos]: ")
		existe = proceso in memoria
		if existe:
			print("\n <ERROR>: El proceso ya existe en memoria. \n")
		else:
			tamaño = int(input("Ingrese el tamaño del proceso [Sólo de 2 a 15]: "))
			if tamaño < 2 or tamaño > 15:
				print("\n <ERROR>: Este tamaño no es válido. \n")
			else:
				agregarProceso(proceso, tamaño)
	elif op == '2':
		proceso = input("Ingrese el nombre del proceso que desea eliminar [Valores alfanuméricos]: ")
		existe = proceso in memoria
		if existe:
			tamaño = memoria.count(proceso)
			borraMemoria(proceso, tamaño)
		else:
			print("\n <ERROR>: No existe el proceso. \n")
	else:
		print("\n <ERROR>: Opción inválida. \n")


# FUNCIONES INTERNAS
def agregarProceso(proceso,tamaño):
    global memoria
    numElementos = len(memoria)
    limiteMemoria = numElementos+tamaño
    if limiteMemoria > 30:
        compacta(proceso,tamaño)
    else:
        i=0
        while i < tamaño:
            memoria.append(proceso)
            i+=1
        os.system("cls")
        imprimeMapa()
        print("\n")


def borraMemoria(proceso,tamaño):
	global memoria
	i = tamaño
	while i > 0:
		indice = memoria.index(proceso)
		memoria.remove(proceso)
		memoria.insert(indice, '-')
		i-=1
	os.system("cls")
	imprimeMapa()
	print("\n")


def compacta(proceso,tamaño):
	global memoria
	espacio = '-' in memoria[0:30]
	if espacio:
		print("\n <AVISO>: Se requiere compactación de memoria. \n")
		espacio = memoria.count('-')
		if espacio >= tamaño:
			i = tamaño
			while i > 0:
				indice = memoria.index('-')
				memoria.remove('-')
				memoria.insert(indice, proceso)
				i-=1
			os.system("cls")
			imprimeMapa()
			print("\n")
		else:
			os.system("cls")
			print("\n <ERROR>: Memoria insuficiente. \n")
	else:
		os.system("cls")
		print("\n <ERROR>: No hay memoria disponible. \n")


def imprimeMapa():
	global memoria
	print("\n === Mapa de la memoria === \n")
	for x in memoria[0:30]:
		print('' + x + '',end =" ")
menu()