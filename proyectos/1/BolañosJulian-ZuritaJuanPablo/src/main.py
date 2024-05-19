from models import FiUnamFS, system_validation
import os, threading

option = 0
fiunamfs = None

'''Funcion que es ejecutada por un hilo distinto al resto. Su trabajo es
   mostrar en pantalla los archivos existentes en FiUnamFS, los archivos 
   se obtienen del obejto 'fiunamfs'. '''
def _listarContenido(semaphore1, semaphore2):
    global option, fiunamfs

    while True:
        # Bloquea la ejecucion de esta funcion, hasta recibir una notificacion.
        semaphore2.acquire()

        if option == '5' : break

        files_in_directory = fiunamfs.divideGetFile()
        print('\n\t\t|Archivos en FiUnamFS|\n')
        i = 1
        for file in files_in_directory:
            print(f'{i}. {file.name}   {file.size} Bytes    {file.creation_date}')
            i = i + 1

        # Libera el bloqueo de la función '_menu'
        semaphore1.release()


'''Funcion que es ejecutada por un hilo distinto al resto. Su trabajo es
   mostrar en pantalla si hubo exito o no, al copiar un archivo de FiUnamFS
   a la computadora local. El proceso se realiza en el método 'copyToSystem'
   del objeto de tipo File.'''
def _copiarACompuLocal(semaphore1, semaphore2):
    global option, fiunamfs

    while True:
        semaphore2.acquire()

        if option == '5' : break

        print('\n\t\t|Copiar archivo a mi Computadora|\n')
        file_name = input('Nombre de archivo a copiar: ')
        path = input('Ingresa la dirección destino: ')

        files_in_directory = fiunamfs.divideGetFile()
        for i in range(len(files_in_directory)):
            if file_name == files_in_directory[i].name:
                if files_in_directory[i].copyToSystem(path):
                    print(f'\nSe copió "{file_name}" en "{path}"')
                    break
                else:
                    print(f'\nError al copiar "{file_name}", el archivo ya existe\no la direccion no existe.')
                    break
            else:
                if i == len(files_in_directory) - 1:
                    print(f'\nEl archivo "{file_name}" no existe en FiUnamFS.')
        semaphore1.release()
    

'''Funcion que es ejecutada por un hilo distinto al resto. Su trabajo es
   mostrar en pantalla si hubo exito o no, al copiar un archivo de nuestra
   computadora local a FiUnamFS. El proceso se realiza en el método 'copyFromSystem'
   del objeto instanciado 'fiunamfs'.'''
def _copiarASistema(semaphore1, semaphore2):
    global option, fiunamfs

    while True: 
        semaphore2.acquire()

        if option == '5' : break

        print('\n\t\t|Copiar archivo de mi Computadora a FiUnamFS|\n')
        print('Ingresa la ubcicacion del archivo a copiar, por ejemplo: D:/my_files/archivo_a_copiar.jpg\n')
        print('|* NOTA: Si no encuentra el archivo posiblemente es por que falta su extensión *|\n')
        path = input('Ubicacion: ')

        if os.path.exists(path):
            result = fiunamfs.copyFromSystem(path = path)
            name = os.path.basename(path)

            if result == 1: 
                print(f'\nNo se puede almacenar el nombre "{name}" ya que supera los 14 caracteres.')
            elif result == 2:
                print(f'No se puede almacenar el nombre "{name}" ya que no contiene unicamente caracteres ascii') 
            elif result == 3:
                print("\nSe copió el archivo de manera satisfactoria")
            elif result == 4:
                print("\nEspacios de directorio no disponibles.")
            elif result == 5:
                print("\nNo se logró hacer la copia. Error al realizar la copia.")
            elif result == 6:
                print("\nNo hay espacio para almacenar el archivo en FiUnamFS.")
            elif result == 7: 
                print("\nEl nombre de archivo ya está ocupado por otro en FiUnamFS.")
        else: 
            print("\nEl archivo no existe")

        semaphore1.release()


'''Funcion que es ejecutada por un hilo distinto al resto. Su trabajo es
   mostrar en pantalla si hubo exito o no, al eliminar un archivo de FiUnamFS. 
   El proceso se realiza en el método 'deleteFile' del objeto instanciado 'fiunamfs'.'''
def _eliminarArchivo(semaphore1, semaphore2):
    global option, fiunamfs

    while True: 
        semaphore2.acquire()

        if option == '5' : break

        print('\n\t\t|Eliminar archivo de FiUnamFS|\n')
        file_name = input('Ingresa el nombre de archivo a eliminar: ')
        fiunamfs.deleteFile(file_name)

        semaphore1.release()


'''La función _menu es ejecutada por un hilo que podemos verlo como 'hilo principal'
   porque señaliza cuando uno de los otros hilos debe ejecutarce.'''
def _menu(sem1,sem2,sem3,sem4, sem5):
    global option, fiunamfs

    directory_path = 'C:/Users/juanz/Downloads/Proyecto/fiunamfs.img'
    if system_validation(directory_path):
        fiunamfs = FiUnamFS(path = directory_path, directory_entry_size = 64)

        while True:
            sem1.acquire()
            print('\n\t\tBienvenido a FiUnamFS\n')
            print('(1) - Listar los contenidos del directorio.')
            print('(2) - Copiar uno de los archivo dentro de FiUnamFS hacia tu sistema.')
            print('(3) - Copiar un archivo de tu computadora hacia FiUnamFS.')
            print('(4) - Eliminar un archivo del FiUnamFS.')
            print('(5) - Salir.')
            option = input('Opcion -> ')

            if option == '1':
                sem2.release()
            elif option == '2':
                sem3.release()
            elif option == '3':
                sem4.release()
            elif option == '4':
                sem5.release()              
            elif option == '5':
                sem2.release()
                sem3.release()
                sem4.release()
                sem5.release()
                break
            else: 
                sem1.release()


'''Los siguientes semáforos van a servir de señales para que los hilos realicen 
   su ejecución. Cada hilo le corresponde una función que señalizar (listarContenido, 
   copiarACompuLocal, etc).'''

menu = threading.Semaphore(1)
listarContenido = threading.Semaphore(0)
copiarACompuLocal = threading.Semaphore(0)
copiarASistema = threading.Semaphore(0)
eliminarArchivo = threading.Semaphore(0)

threading.Thread(target = _menu, args = [menu,listarContenido,copiarACompuLocal,copiarASistema, eliminarArchivo]).start()
threading.Thread(target = _listarContenido, args = [menu,listarContenido]).start()
threading.Thread(target = _copiarACompuLocal, args = [menu,copiarACompuLocal]).start()
threading.Thread(target = _copiarASistema, args = [menu, copiarASistema]).start()
threading.Thread(target = _eliminarArchivo, args = [menu, eliminarArchivo]).start()