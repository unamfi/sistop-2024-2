import random
import os

MAX_MEMORY = 30

def create_initial_memory():

    memory = []
    processes = ['A', 'B', 'C', 'D', 'E', 'F', 
                 'G', 'H', 'I', 'J', 'K', 'L', 
                 'M', 'N', 'O', 'P', 'Q', 'R', 
                 'S', 'T', 'U', 'V', 'W', 'X', 
                 'Y', 'Z']

    while len(memory) < 30:
        indexProcess = random.randint(0, 25)
        numProcesses = random.randint(2,15)
        numFreeSpaces = random.randint(2,6)

        if processes[indexProcess] in memory:
            indexProcess = random.randint(0, 25)
        else:
            if (len(memory) + numProcesses) > MAX_MEMORY:
                memory.extend([processes[indexProcess] for i in range(len(memory), MAX_MEMORY)])
                break
            
            memory.extend([processes[indexProcess] for i in range(numProcesses)])
            memory.extend(['-' for i in range(numFreeSpaces)])
        
            if len(memory) > 30:
                for i in range(len(memory)-MAX_MEMORY):
                    memory.pop()
    
    return memory

def mejor_ajuste(memory:list, numProcesses:int, process:str) -> list:
    
    auxCount = 0
    numFreeSpaces = memory.count('-')
    firstSpace = memory.index('-')      
    
    if numFreeSpaces < numProcesses:
        for i in range(numFreeSpaces):
            memory.remove('-')
            memory.append(process)
        print('\nSe aplico una compactación.\n')

    elif numFreeSpaces >= numProcesses:
        
        for i in range(firstSpace, MAX_MEMORY):
            if memory[i] == '-':
                auxCount += 1
                
                if auxCount == numProcesses:
                    memory[firstSpace:(firstSpace + numProcesses)] = [process for i in range(numProcesses)]
                    break
            else:
                if auxCount < numProcesses:
                    auxCount = 0
                    firstSpace = i + 1
        
        if auxCount < numProcesses:
            for i in range(numProcesses):
                memory.remove('-')
                memory.append(process)
            print('\nSe aplico una compactación.\n')



    return memory

def primer_ajuste(memory:list, numProcesses:int, process:str) -> list:
    
    numFreeSpaces = memory.count('-')

    if numFreeSpaces >= numProcesses:
        for i in range(numProcesses):
            aux = memory.index('-')
            memory.insert(aux, process)
            memory.remove('-')
    else:
        for i in range(numFreeSpaces):
            aux = memory.index('-')
            memory.insert(aux, process)
            memory.remove('-')

    return memory


def quitar_proceso(memory:list, process:str) -> None:

    while process in memory:
        aux = memory.index(process)
        memory.insert(aux, '-')
        memory.remove(process)


if __name__ == '__main__':

    initial_map = create_initial_memory()
    while True:
        print(f'\nMapa de Memoria Inicial: {''.join(initial_map)}')
        print('1. Asignar Proceso')
        print('2. Liberar Proceso')
        print('3. Salir')
        option = input('Opcion: ')

        if option == '1':
            os.system('cls')
            process = input('Incgresa Proceso (A - Z): ')
            numProcesses = input('Incgresa Numero de Procesos: ')
            print(f"Mapa de Memoria Anterior: {''.join(initial_map)}")
            new_map = mejor_ajuste(initial_map, int(numProcesses), process)
            print(f"Mapa de Memoria Actualizado (Mejor Ajuste): {''.join(new_map)}")
            print('________________________________________________________________')
        
        if option == '2':
            os.system('cls')
            process = input('Incgresa Proceso (A - Z): ')
            print(f"Mapa de Memoria Anterior: {''.join(initial_map)}")
            new_map = quitar_proceso(initial_map,process)
            print(f"Mapa de Memoria Actualizado: {''.join(initial_map)}")
            print('________________________________________________________________')
            
        if option == '3':
            break