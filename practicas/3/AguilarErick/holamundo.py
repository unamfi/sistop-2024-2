import time

def hola_mundo_complicado():
    mensaje = "¡Hola Mundo!"
    for letra in mensaje:
        print(letra, end='', flush=True)
        time.sleep(0.05)

hola_mundo_complicado()