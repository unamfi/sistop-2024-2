#!/usr/bin/python3
import threading
from random import random
import time

apagador = threading.Semaphore(1)
pizarron = 0
cuantos = 0
mutex = threading.Semaphore(1)
torniquete = threading.Semaphore(1)

def alumno(id):
    global cuantos
    print('  A%d: Iniciando' % id)
    time.sleep(random())
    while True:
        # ¿Puedo entrar al salón sin causar inanición?
        torniquete.acquire()
        torniquete.release()

        # El primero en entrar prende la luz
        mutex.acquire()
        if cuantos == 0:
            apagador.acquire()
        cuantos = cuantos + 1
        mutex.release()

        print('  A%d: En el salón. ¡Somos %d alumnos!' % (id, cuantos))
        time.sleep(random())
        print('  A%d: Hoy aprendí que %f' % (id, pizarron))

        # El último en salir apaga la luz
        mutex.acquire()
        cuantos = cuantos - 1
        if cuantos == 0:
            apagador.release()
        mutex.release()

def profesor(id):
    global pizarron
    print('P%d: Iniciando' % id)
    while True:
        torniquete.acquire()
        apagador.acquire()
        clase = random()
        print('P%d: Mi clase es %f' % (id, clase))
        pizarron = clase
        print('P%d: Ya m\'voy.' % id)
        apagador.release()
        torniquete.release()
        time.sleep(random())

for i in range(3):
    threading.Thread(target=profesor, args=[i]).start()

for i in range(10):
    threading.Thread(target=alumno, args=[i]).start()
