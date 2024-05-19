def desplegar_menu():
    while True:
        print("\n-------------------------Menú de opciones--------------------------------")
        print("1. Listar los contenidos del directorio")
        print("2. Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema")
        print("3. Copiar un archivo de tu computadora hacia tu FiUnamFS")
        print("4. Eliminar un archivo del FiUnamFS")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            print("1")
        elif opcion == '2':
            print("2")
        elif opcion == '3':
            print("3")
        elif opcion == '4':
            print("4")
        elif opcion == '5':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")
desplegar_menu()
