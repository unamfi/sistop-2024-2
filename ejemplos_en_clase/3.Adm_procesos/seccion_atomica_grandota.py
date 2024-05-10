#!/usr/bin/python3
import threading
import time
import random

valores = [1,3,5,7,9]
acumulado = 0
mutex = threading.Lock()

def trabajemos_con(num):
    global acumulado, valores
    print('   Hilo %d iniciando' % num)
    for i in range(10):
        print('%d → comienza su avance...' % num)
        local = valores[0] + valores[1] + valores[4]
        time.sleep(random.random())
        print('%d → busca entrar a su sección crítica' % num)
        mutex.acquire()
        print('%d → entró a su sección crítica' % num)
        for val in valores:
            acumulado = acumulado + val*num
        time.sleep(random.random())
        print('%d → sale de su sección crítica' % num)
        mutex.release()

print('** Por lanzar 5 hilos')
for i in range(5):
    threading.Thread(target = trabajemos_con, args = [i]).start()

