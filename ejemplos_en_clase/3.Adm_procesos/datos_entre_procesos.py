#!/usr/bin/python3
import os
import time
datos = 0

def muestra_datos():
    global datos
    while True:
        print(datos)
        time.sleep(1)

def incrementa():
    global datos
    while True:
        datos = datos + 1
        time.sleep(1)

pid = os.fork()
if (pid > 0):
    # Proceso padre
    incrementa()
else:
    # Proceso hijo
    muestra_datos()
