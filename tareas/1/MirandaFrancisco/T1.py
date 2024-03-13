
# Miranda González José Francisco

from colorama import Fore, Style # Para cambiar el color

print(Fore.YELLOW) # Color amarillo
print('\nAsignación actual:\n\n') # Mensaje inicial
print(Style.RESET_ALL) # Regresar a color normal
asignacion = 'AABBBBCCCCDDDDDDEEEE---HHHII--' # La indicada en las instrucciones (no especifica que un usuario pueda introducir una por teclado, asi que trabajare con esta)
print(asignacion) # La imprimimos

procesos = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # Esto me va a servir para saber que letras de 'asignación' estan en 'procesos' (para imprimir en el mensaje que procesos tengo)

impProcesos = [] # Guardamos a todas las letras 
impProcesosNoRepetidos = [] # Guardamos a las letras sin repetir

while True: 

    aOl = int(input('Asignar (0) o liberar (1) o salir (3): ')) # Elegir una opción

    if aOl == 0: # Si elegimos Asignar
        
        for i in asignacion:
            if i in procesos:
                impProcesos.append(i) # Guardamos las de 'asignacion' que estan en 'procesos'

        for i in impProcesos:
            if i not in impProcesosNoRepetidos:
                impProcesosNoRepetidos.append(i) # Para guardar las letras no repetidas

        ordenado = sorted(impProcesosNoRepetidos) # Orden alfabetico

        ultimaLetra = ordenado[-1] # Obtenemos la ultima letra del arreglo
        indice = procesos.index(ultimaLetra) # Obtenemos el indice de la ultima letra del arreglo en 'procesos'

        if indice == 25:
            print('Se terminaron los procesos')
            break

        ordenado.append(procesos[indice+1]) # Agregamos al arreglo la siguiente letra a la ultima encontrada
        
        arregloAstring = ''.join(ordenado) # Pasamos de arreglo a string

        # Esto es para imprimir el proceso correcto

        # Escoger el numero a asignar
        while True:
            asignar = int(input(f'Nuevo proceso ({arregloAstring[-1]}): '))

            if asignar < 2 or asignar > 15:
                print('Se requiere entre 2 y 15 unidades')
            else:
                break
        
        contador = 0 # Número de '-' seguidos
        segundoContador = 0 # Para saber el número total de '-'

        arregloMaximo = [] # Guardar los numeros de '-' seguidos
        asignacionProvisional = [] # Para ordenar los '-' al final 

        x = asignacion

        for i, caracter in enumerate(asignacion): # Ocupamos el caracter y su indice
            if caracter == '-':
                # Si encontramos un '-' incrementamos el contador 
                contador += 1
                segundoContador += 1
                if asignar == contador: # Si asignar es igual a contador, significa que si hay espacio disponible 
                    asignacionLista = list(asignacion)
                    asignacionLista[i-asignar+1:i+1] = [arregloAstring[-1]] * asignar # Los indices por reemplazar 
                    asignacionNueva = ''.join(asignacionLista)
                    break

                else:
                    asignacionNueva = x # En caso de necesitar compactación
        
            else:
                # Si encontramos un elemento diferente de '-' reiniciamos el contador
                if contador > 0:
                    arregloMaximo.append(contador) # Es para agregar el numero de '-' seguidos
                    contador = 0
        
        if contador > 0:
            arregloMaximo.append(contador) # Igual es para agregar el numero de '-' seguidos (pero estos son los que aparezcan al final)

        maximo = sorted(arregloMaximo)

        if asignar > segundoContador:
            print(f'Requiero asignar {asignar} unidades, máximo tengo {segundoContador}. No puedo asignar esa cantidad') # Terminar el programa en caso de que no tener suficientes unidades
            break
        
        if asignacionNueva == x:

            print(f'Requiero asignar {asignar} unidades, sólo tengo {maximo[-1]} consecutivas.')

            print('*Compactación requerida*')

            print('Nueva situación: ')

            arregloProvisional = asignacionNueva.replace('-','') ########

            for i in arregloProvisional:
                asignacionProvisional.append(i)

            for i in range(segundoContador):
                asignacionProvisional.append('-')

            variableProvicional = ''.join(asignacionProvisional)

            print(variableProvicional)

            print(f'Asignando a {arregloAstring[-1]}')

            contador = 0

            # Hacemos lo mismo de arriba
            for i, caracter in enumerate(variableProvicional): # Ocupamos el caracter y su indice
                if caracter == '-':
                    # Si encontramos un '-' incrementamos el contador 
                    contador += 1
                    segundoContador += 1
                    if asignar == contador: # Si asignar es igual a contador, significa que si hay espacio disponible 
                        asignacionLista = list(variableProvicional)
                        asignacionLista[i-asignar+1:i+1] = [arregloAstring[-1]] * asignar # Los indices por reemplazar 
                        asignacionNueva = ''.join(asignacionLista)
                        break
        
            else:
                # Si encontramos un elemento diferente de '-' reiniciamos el contador
                if contador > 0:
                    contador = 0
            

        print(Fore.YELLOW) # Color amarillo
        print('\nNueva asignación:\n\n') # Mensaje inicial
        print(Style.RESET_ALL) # Regresar a color normal

        print(asignacionNueva)

        asignacion = asignacionNueva # Actualizar el valor
        # Limpiar arreglos
        impProcesos = []
        impProcesosNoRepetidos = []
        arregloMaximo = [] 
        asignacionProvisional = [] 

    elif aOl == 1: # Si elegimos liberar

        for i in asignacion:
            if i in procesos:
                impProcesos.append(i) # Guardamos las de 'asignacion' que estan en 'procesos'
        
        if impProcesos == []:
            print('No hay más procesos por liberar\n')
            break

        for i in impProcesos:
            if i not in impProcesosNoRepetidos:
                impProcesosNoRepetidos.append(i) # Para guardar las letras no repetidas
        
        arregloAstring = ''.join(impProcesosNoRepetidos) # Pasamos de arreglo a string
        # Practicamente todo esto fue para que al solicitar el proceso a liberar nos enseñe que procesos tenemos
        # Por ejemplo liberamos a C, entonces al otra vez querer liberar otro proceso en el mensaje ya no nos va a mostar a C
        
        # Escoger el proceso
        liberar = input(f'Proceso a liberar ({arregloAstring}): ') 

        print(Fore.YELLOW) # Color amarillo
        print('\nAsignación actual:\n\n') # Mensaje inicial
        print(Style.RESET_ALL) # Regresar a color normal

        asignacionNueva = asignacion.replace(liberar,'-') # Se reemplaza el proceso a liberar por '-'
        print(asignacionNueva) 

        asignacion = asignacionNueva # Actualizar el valor
        # Limpiar arreglos
        impProcesos = []
        impProcesosNoRepetidos = []
    
    elif aOl == 3:
        break
    
    else:
        print('Entrada no valida')


