#!/usr/bin/python3
import os

print("Sólo hay un proceso.")
pid = os.fork()

if pid == 0:
    # Proceso hijo
    print("Saludos desde el proceso hijo")
    print("Resultado del fork: %d" % pid)
    print("Mi PID: %d" % os.getpid())
else:
    # Proceso padre
    print("Saludos desde el proceso padre")
    print("Resultado del fork: %d" % pid)
    print("Mi PID: %d" % os.getpid())
