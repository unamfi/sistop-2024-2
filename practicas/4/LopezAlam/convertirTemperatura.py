def convertir_temperatura(temperatura, unidad):
    if unidad.upper() == "C":
        return (temperatura * 9/5) + 32, "Fahrenheit"
    elif unidad.upper() == "F":
        return (temperatura - 32) * 5/9, "Celsius"
    else:
        return None, "Unidad no reconocida"

temperatura_ingresada = float(input("Ingrese la temperatura: "))
unidad_ingresada = input("Ingrese la unidad (C para Celsius, F para Fahrenheit): ")

temperatura_convertida, unidad_convertida = convertir_temperatura(temperatura_ingresada, unidad_ingresada)

if temperatura_convertida is not None:
    print(f"La temperatura convertida es: {temperatura_convertida:.2f} {unidad_convertida}")
else:
    print("Unidad no reconocida. Por favor, ingrese C para Celsius o F para Fahrenheit.")
