#!/usr/bin/python3
import threading
import time
from random import random, randint
canal = []
mutex = threading.Semaphore(1)
señal = threading.Semaphore(0)
capacidad = threading.Semaphore(5)

def productor(id):
    print('  P%d: Iniciando' % id)
    while True:
        cosa = produce_objeto(id)
        print('  P%d: Objeto producido: %d' % (id, cosa))
        print('  P%d: Por agregar objeto; hay %d' % (id, len(canal)))
        capacidad.acquire()
        mutex.acquire()
        canal.append(cosa)
        print('  P%d: %d objetos en el canal' % (id, len(canal)))
        mutex.release()
        señal.release()
        time.sleep(random())

def consumidor(id):
    print('C%d: Iniciando' % id)
    while True:
        señal.acquire()
        mutex.acquire()
        cosa = canal.pop()
        print('C%d: %d objetos en el canal' % (id, len(canal)))
        capacidad.release()
        mutex.release()
        procesa(id, cosa)
        time.sleep(random())
        print('C%d: Siguiente...' % id)

def produce_objeto(quien):
    res = randint(1,10)
    print('  P%d: Produciendo %d' % (quien, res))
    return res

def procesa(quien, que):
    print('C%d procesando %d' % (quien, que))

for i in range(5):
    threading.Thread(target=productor, args=[i]).start()
for i in range(3):
    threading.Thread(target=consumidor, args=[i]).start()
