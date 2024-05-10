#!/usr/bin/python3
from threading import Semaphore, Thread
from time import sleep
from random import random, randint

def trabajador(id):
    while True:
        mutex.acquire()
        print("%d entrando" % id)
        for i in range(randint(10,15)):
            print(id, end="")
            sleep(0.1 * random())
        print("%d saliendo" % id)
        mutex.release()
        sleep(0.01)

mutex = Semaphore(3)
for i in range(9):
    Thread(target=trabajador, args=[i]).start()
