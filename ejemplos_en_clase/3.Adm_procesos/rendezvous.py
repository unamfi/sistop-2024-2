#!/usr/bin/python3
from threading import Semaphore, Thread
from time import sleep
from random import randint

def interro_adm(pesos_listo, interrog_listo):
    interrog = randint(0,30)
    adm = randint(0,30)
    print("%d interrogaciones, %d admiraciones" % (interrog,adm))
    for i in range(interrog):
        print('?', end="")
        sleep(0.1)
    interrog_listo.release()
    pesos_listo.acquire()
    for i in range(adm):
        print('!', end="")
        sleep(0.1)


def pesos_numeral(pesos_listo, interrog_listo):
    pesos = randint(0,30)
    numeral = randint(0,30)
    print("%d pesos, %d numeral" % (pesos, numeral))
    for i in range(pesos):
        print('$', end="")
        sleep(0.1)
    pesos_listo.release()
    interrog_listo.acquire()
    for i in range(numeral):
        print('#', end="")
        sleep(0.1)

pesos_listo = Semaphore(0)
interrog_listo = Semaphore(0)
Thread(target = interro_adm, args = [pesos_listo, interrog_listo]).start()
Thread(target = pesos_numeral, args = [pesos_listo, interrog_listo]).start()
