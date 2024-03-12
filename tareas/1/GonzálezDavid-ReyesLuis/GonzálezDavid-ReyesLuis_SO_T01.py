#Realizado por 
#-González López David
#-Reyes Romero Luis Fernando
#Sistemas Operativos 2024-2

import random
#Función para generar de forma aleatoria nuestra cadena que simulará a nuestra memoria. 
def generar_cadena_aleatoria():
    letras = "ABCDEFGHI" #Lista de caracteres que se utilizara para crear nuestra cadena. 
    cadena = ''.join(random.choice(letras) for i in range(30)) #Se crea nuestra cadena de forma aleatoria con un rango de 30 caracteres.
    return ''.join(sorted(cadena)) #La funcion sorted devuelve la cadena en orden alfabetico para facilitar el entendimiento visual de la cadena.

#Función para compactar la memoria en caso de que se busque hacer una asignación
def compactar(cadena):
    letras = [c for c in cadena if c.isalpha()] #El ciclo interno analiza caracter a caracter la pertenencia del mismo al alfabeto
    #esto por medio de la macro isalpha()
    guiones = '-' * (len(cadena) - len(letras)) #Los guines representan los espacios libres en memoria
    return ''.join(letras) + guiones

#Función para asignar unidades de memoria    
def asignar(cadena, letra, cantidad):
    indice = cadena.find('-' * cantidad) #El metodo find encuentra la primera aparición de '-' tantas veces se indique por la variable cantidad. 
    if indice != -1: #Como el metodo find devuelve -1 si no se ha encontrado el valor. Entonces, nuestra condición es si indice es 
        #diferente a -1 se ejecuta lo que viene dentro de nuestro if
        cadena_modificada = cadena[:indice] + letra * cantidad + cadena[indice + cantidad:]
        if cadena_modificada.count(letra) < 2: #Verifica que al menos existan dos unidades de un proceso.
            print("El proceso {} tiene menos de dos unidades dentro de la memoria".format(letra))
            return cadena #Si existe un proceso con menos de dos unidades se va a regresar la cadena sin modificar.
        if cadena_modificada.count(letra) > 15: #Verifica que no se exceda la maxima cantidad de unidades que puede tener un proceso.
            print("El proceso {} excede las unidades que puede tener un proceso dentro de la memoria".format(letra))
            return cadena #Si existe un proceso con mas de quince unidades se va a regresar la cadena sin modificar.
        else: #Si existe al menos dos y menos de quince unidades de memoria de un proceso se regresa la cadena_modificada 
            return cadena_modificada
    else: #Si no se ha encontrado el valor necesario para asignar las unidades de memoria se compacta la memoria.
        print("No hay suficiente espacio en la memoria para asignar {} unidades.".format(cantidad))
        cadena = compactar(cadena) #Se llama a la función compactar
        print("Compactando...\nNueva situación:\n{}".format(cadena))
        indice = cadena.find('-' * cantidad) #Una vez compactada la memoria se hace nuevamente el mismo metodo para la asignacion de unidades, para la memoria ya compactada.
        if indice != -1:
            cadena = cadena[:indice] + letra * cantidad + cadena[indice + cantidad:]
            return cadena
        else: #Si incluso con la memoria compactada no hay suficiente espacio en la memoria se mandara un mensaje.
            print("No hay suficiente espacio en la memoria incluso después de compactar.")
    return cadena

#Función para liberar procesos de la memoria
def liberar(cadena, letras): 
    for letra in letras: #Este bucle lo que hace es recorrer cada letra en la lista letras.
        if letra not in cadena: #Esta condición es para verificar si un proceso que se requiera liberar exista dentro de nuestra memoria.
            print(f"Error: El proceso {letra} no está presente dentro de nuestra memoria.")
            continue
        cadena = cadena.replace(letra, '-') #El metodo replace reemplaza un caracter específico por otro caracter específico. Entonces, 
        #esta parte del código remplaza una letra dentro de nuestra memoria por '-'. 
    return cadena #Se regresa la cadena modificada

#Función main
def main():
    asignacion_actual = generar_cadena_aleatoria() #Se genera la cadena.
    print("Asignación actual:\n",asignacion_actual)
    #Se inicia un bucle para ir ejecutando el programa de forma continua.
    while True:
        #Se hace uso de try and except para manejar un error el cual consta de que el usuario de una accion diferente a lo que se pide.
        try:
            accion = int(input("Asignar (0) o Liberar (1) o Salir (2): ")) #Es un pequeño menú para indicar la accion que se quiere realizar.
        except ValueError: #Se ejecuta este bloque cuando el usuario no de un numero entero.
            print("Acción invalida se debe ingresar 0 para Asignar, 1 para Liberar o 2 para Salir.")
            continue
        if accion == 1: #Si se escoge la opcion 1 se pide el nombre del proceso que se desea liberar para después llamar a la función correspondiente. 
            procesos_a_liberar = input("Proceso a liberar: ").upper()
            asignacion_actual = liberar(asignacion_actual, procesos_a_liberar)
        elif accion == 0: #Si se escogela opcion 0 es para la asignacion de procesos.
            if asignacion_actual.count('-') == 0 : #Si se desea asignar unidades de procesos a la memoria, pero esta misma ya se encuentra llena se mandara un error.
                print("No se puede Asignar ningun proceso debido a que la memoria se encuentra llena.\nSe recomienda Liberar un proceso para despues asignar el proceso que se quiera asignar a la memoria.")
                continue
            else: #Si hay espacio en la memoria se pedira el nombre del nuevo proceso y el numero de unidades que se quiere asignar a la memoria.
                nueva_letra = input("Nuevo proceso: ").upper()
                cantidad = int(input("Cuántas unidades quieres asignar: "))
                asignacion_actual = asignar(asignacion_actual, nueva_letra, cantidad)
        
        elif accion == 2: #La opcion 2 es para salir del programa.
            print("Saliendo del programa...")
            break
        else: #Si se coloca otro numero se mandara un error.
            print("Acción invalida se debe ingresar 0 para Asignar, 1 para Liberar o 2 para Salir")
        #Se hace la impresión de la cadena (memoria) cada vez que se haga una accion.
        print("Asignación actual:\n", asignacion_actual)

main()