#!/usr/bin/python3
from threading import Semaphore, Thread
from random import random
from time import sleep

def vamos(id):
    global mutex, cuenta, barrera
    # En vez de "inicializa", esperamos un tiempo aleatorio ≤3s
    sleep(random() * 3)

    mutex.acquire()
    # Sección crítica para el manejo de "cuenta"
    cuenta = cuenta + 1
    if cuenta == 10:
        print("%d: ¡Se abre la barrera!" % id)
        barrera.release()
    mutex.release()

    print("%d: Quiero entrar" % id)
    barrera.acquire()
    barrera.release()
    print("%d: ¡Dentro!" % id)

    sleep(random() * 3)

mutex = Semaphore(1)
barrera = Semaphore(0)
cuenta = 0

for i in range(15):
    Thread(target=vamos, args=[i]).start()
