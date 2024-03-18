def make_consecutive(string):
    new_string = ''
    consecutive_count = 0
    print("\nLa cadena de prueba es --->" + string + "\n\n")

    for char in string:
        print("Estamos en el char " + char)

        if char == '-':
            consecutive_count += 1
        else:
            if consecutive_count > 0:
                new_string += '-'
                consecutive_count = 0
            new_string += char

    # Si hay '-' al final, los añadimos a la nueva cadena
    if consecutive_count > 0:
        new_string += '-' * consecutive_count

    return new_string


# Ejemplo de uso
cadena = "AAAAA--CDDDDD---GGGGGGG-------"
cadena_consecutiva = make_consecutive(cadena)
print(cadena_consecutiva)
