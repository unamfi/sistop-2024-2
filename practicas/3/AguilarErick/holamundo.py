import time

def hola_mundo_complicado(nombre):
    mensaje = "Hola"
    for letra in mensaje:
        print(letra, end='', flush=True)
        time.sleep(0.05)
    print(" ", end='', flush=True)
    for letra in nombre:
        print(letra, end='', flush=True)
        time.sleep(0.05)

def leer_datos(mensaje):
    datos = input(mensaje)
    if datos.__len__() == 0:
        raise ValueError("El nombre no puede estar vacío")
    return datos

nombre = leer_datos("Dame tu nombre: ")
hola_mundo_complicado(nombre=nombre)