#!/usr/bin/python3
from threading import Semaphore, Thread
from time import sleep

def trabajador(id):
    caracteres = 0
    while True:
        mutex.acquire()
        for i in range(5):
            caracteres += 1
            print(id, end="")
            sleep(0.01)
        mutex.release()
        sleep(0.1)
        if caracteres > 10:
            caracteres = 0
            print("...")

mutex = Semaphore(1)
for i in range(5):
    Thread(target=trabajador, args=[i]).start()
