#!/usr/bin/python3
from threading import Semaphore, Thread
from time import sleep

def treinta_interrogaciones(sem):
    for i in range(30):
        print('?', end="")
        sleep(0.1)
    sem.release()

def veinte_admiraciones(sem):
    sem.acquire()
    for i in range(20):
        print('!', end="")
        sleep(0.1)

s = Semaphore(0)
Thread(target = treinta_interrogaciones, args = [s]).start()
Thread(target = veinte_admiraciones, args = [s]).start()
