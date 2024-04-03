#!/usr/bin/python3
import os
import time
import threading
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

threading.Thread(target=incrementa).start()
threading.Thread(target=muestra_datos).start()
while True:
    time.sleep(1)
    pass
