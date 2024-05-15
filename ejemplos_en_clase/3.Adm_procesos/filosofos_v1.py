#!/usr/bin/python3
import threading
num = 5
palillos = [threading.Semaphore(1) for i in range(num)]
comido = 0
mut_comido = threading.Semaphore(1)

def filosofo(id):
    while True:
        piensa(id)
        levanta_palillos(id)
        come(id)
        suelta_palillos(id)

def piensa(id):
    print("%d - Pensando..." % id)
    print("%d - Tengo hambre..." % id)

def levanta_palillos(id):
    if (id % 3 == 0):
        palillos[(id + 1) % num].acquire()
        print("%d - Tengo el palillo derecho" % id)
        palillos[id].acquire()
        print("%d - Tengo ambos palillos" % id)
    else:
        palillos[id].acquire()
        print("%d - Tengo el palillo izquierdo" % id)
        palillos[(id + 1) % num].acquire()
        print("%d - Tengo ambos palillos" % id)

def suelta_palillos(id):
    palillos[(id + 1) % num].release()
    palillos[id].release()
    print("%d - Sigamos pensando..." % id)

def come(id):
    global comido
    with mut_comido:
        comido += 1
    print("%d - ¡A comer! (%d)" % (id, comido))
    print("%d - ¡Satisfecho!" % id)

filosofos = []
for i in range(num):
    fil = threading.Thread(target=filosofo, args=[i])
    filosofos.append(fil)
    fil.start()
