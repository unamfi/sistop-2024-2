#!/usr/bin/python3
from threading import Thread, Semaphore
from time import sleep

def controlador():
    while True:
        print("¡Abrir las puertas!")
        torniq.release()
        sleep(2)
        print("¡Cerrar las puertas!")
        torniq.acquire()
        sleep(2)

def fulano(id):
    while True:
        torniq.acquire()
        torniq.release()
        print(id)
        sleep(0.3)

torniq = Semaphore(0)
Thread(target=controlador).start()
for i in range(4):
    Thread(target=fulano,args=[i]).start()
