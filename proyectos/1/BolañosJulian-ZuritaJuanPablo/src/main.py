from models import FiUnamFS, system_validation


if system_validation():
    directory_path = 'D:/workspace/sistemasOp/sistop-2024-2/proyectos/1/FiUnamFS.img'
    fiunamfs = FiUnamFS(path = directory_path, directory_entry_size = 64)

    while True:
        print('\t\tBienvenido a FiUnamFS\n')
        print('(1) - Listar los contenidos del directorio.')
        print('(2) - Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema.')
        print('(3) - Copiar un archivo de tu computadora hacia tu FiUnamFS.')
        print('(4) - Eliminar un archivo del FiUnamFS.')
        print('(5) - Salir.')
        op = input('Opcion -> ')

        if op == '1':
            files_in_directory = fiunamfs.getFiles()
            print('\n\t\t|Archivos en FiUnamFS|')
            for file in files_in_directory:
                print(f'{file.name}   {file.size} Bytes    {file.creation_date}')
        
        if op == '2':
            print('\n\t\t|Copiar archivo a mi Computadora|')
            file_name = input('Nombre de archivo a copiar: ')
            path = input('Ingresa la dirección destino: ')

            # D:/workspace/Python/sistema_archivos_multihilos
            files_in_directory = fiunamfs.getFiles()
            for i in range(len(files_in_directory)):
                if file_name == files_in_directory[i].name:
                    if files_in_directory[i].copyToSystem(path):
                        print(f'\nSe copio {file_name} en {path}')
                        break
                    else:
                        print(f'\nError al copiar {file_name}, el archivo ya existe\no la direccion no existe.')
                        break
                else:
                    if i == len(files_in_directory) - 1:
                        print(f'\nEl archivo {file_name} no existe en FiUnamFS.')
        
        if op == '3':
            print('\n\t\t|Copiar archivo a de mi Computadora a FiUnamFS|')
            print('\nIngresa la ubcicacion del archivo a copiar, por ejemplo: D:/my_files/archivo_a_copiar.jpg')
            path = input('Ubicacion: ')

            if fiunamfs.copyFromSystem(path = path):
                print('\nArchivo copiado con exito.')
            else:
                print('\nError. Espacio insuficiente o el archivo no existe.')

        if op == '4':
            print('\n\t\t|Eliminar archivo de FiUnamFS|')
            file_name = input('Ingresa el nombre de archivo a eliminar: ')

            files_in_directory = fiunamfs.getFiles()
            for i in range(len(files_in_directory)):
                if file_name == files_in_directory[i].name:
                    if fiunamfs.deleteFile(file_name = file_name):
                        print(f'\nSe elimino {file_name} de FiUnamFS')
                        break
                    else:
                        print(f'\nError al eliminar {file_name}.')
                        break
                else:
                    if i == len(files_in_directory) - 1:
                        print(f'\nEl archivo {file_name} no existe en FiUnamFS.')
                               
        if op == '5':
            break
