"""
Trea 1 Sistemas Operativos

Created on Tue Mar 12 21:26:20 2024

@authors: Flores Melquiades Evelyn Jasmin
         Vera Garmendia Miriam Marisol
"""
#listas=l
def compactar(l):
    for elem in l:
        if elem == '-':
            l.remove(elem)
            l.append('-')
    
    l_act = ''.join(l)
    print("\nLista compactada:\n" + l_act)

    return l

def asignar(l, l_pr, esp):
    #Inicializar variables
    a = 0
    inc = 0
    warng = 0
    l_act = ''.join(l)
    
    letter = input("\nIngresa la letra que nombra al proceso: ")    
    
    while True:
       #Manejo de excepcion para numeros enteros
       try:
           cant = input("Ingresa uniidades de memoria que ocupara: ")
           cant = int(cant)
           
           if esp - cant < 0:
               print("\nNo hay suficiente memoria para almacenar dicho proceso\nMemoria disponible:", esp)
               return l, l_pr, esp
           
           esp = esp - cant

           if letter not in l_pr:
               l_pr.append(letter)

           for elem in l:
               if elem == '-' and a == cant:
                   for i in range(inc, inc + a):
                       l[i] = letter
                   warng = 1
                   break
               elif elem == '-':
                   a += 1
               elif elem != '-':
                   inc += 1
                   inc += a
                   a = 0     

           if warng == 0:
               print("\nNo hay suficiente memoria para almacenar el proceso, es necesario compactar memoria")
               l = compactar(l)
               l_act = ''.join(l)
               a = 0; inc = 0
               for elem in l:
                   if elem == '-' and a == cant:
                       for i in range(inc, inc + a):
                           l[i] = letter
                       break
                   elif elem == '-':
                       a += 1
                   elif elem != '-':
                       inc += 1
                       inc += a
                       a = 0     
               
               

           lista_formato = ''.join(l)
           print("\nMemoria actual:\n" + l_act + "\nNuevo proceso ("+ letter +"):", cant, "\nMemoria actual:\n" + lista_formato)
           
           return l, l_pr, esp
       except ValueError:
           print ("La entrada es incorrecta: escribe un numero entero")
    

def liberar(l, l_pr, esp):
    a = 0;
    l_act = ''.join(l)
    proc_form = ''.join(l_pr)
    quitar = input("\nIngresa el proceso que desea remover: ")

    if quitar not in l_pr:
        print("\nNo hay registro de dicho proceso")
        return l, l_pr, esp
    
    for elem in l:
        if quitar == elem:
            l[a] = '-'
        a += 1

    esp += a
    
    lista_formato = ''.join(l)
    print("\Memoria actual:\n", l_act, "\nProceso a liberar (" + proc_form + ")\nMemoria actual:\n" + lista_formato)
    l_pr.remove(quitar)

    return l, l_pr, esp

def mostrar (l, l_pr, esp):
    l_act = ''.join(l)
    print("\nMemoria actual:\n" + l_act + "\nMemoria disponible:", esp)
    return l, l_pr, esp

def main():
    l = ['-'] * 30
    l_pr= []
    op = 0 
    esp = 30;

    while op != 4:

        if op == 1:
            l, l_pr, esp = asignar(l, l_pr, esp)
        if op == 2:
            l, l_pr, esp = liberar(l, l_pr, esp)
        if op == 3:
            l, l_pr, esp = mostrar(l, l_pr, esp)
        if op == 4:
            print("\nVuelva pronto")
        try:
            op = int(input("\n\t\tAdministrador de procesos\n\n"
                               +"1. Asignar\n"
                               +"2. Liberar\n"
                               +"3. Mostrar\n"
                               +"4. Salir\n"
                               +"\nIngrese una opcion: "))
        except:
            print("Ingrese uan opcion valida\n")
            
    print ('\n---Ha salido del sistema---\n')
main()