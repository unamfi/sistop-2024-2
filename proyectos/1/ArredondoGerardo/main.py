if __name__ == "__main__":
    while True:
        print("\nSeleccione una opción:")
        print("1. Ver contenidos")
        print("2. Copiar de FiUnamFS al sistema operativo")
        print("3. Copiar del sistema operativo a FiUnamFS")
        print("4. Eliminar archivo")
        print("5. Salir")

        opcion = input("\n\nQué opción desea -----> ")
        if verificar_superbloque(ruta_imagen):
            if opcion == "1":
                listar_archivos(ruta_imagen)
            elif opcion == "2":
                nombre_archivo = input("Archivo en FiUnamFS a copiar al sistema:")
                copiar_desde_fiunamfs(nombre_archivo, ruta_imagen)
            elif opcion == "3":
                nombre_archivo = input("Archivo en el sistema a copiar a FiUnamFS:")
                copiar_a_fiunamfs(nombre_archivo, ruta_imagen)
            elif opcion == "4":
                nombre_archivo = input("Archivo a eliminar:")
                eliminar_archivo(nombre_archivo, ruta_imagen)
            elif opcion == "5":
                print("Gracias por usar :D")
                break
            else:
                print("Ingrese una opción válida.")
        else:
            print("Sistema no válido.")

