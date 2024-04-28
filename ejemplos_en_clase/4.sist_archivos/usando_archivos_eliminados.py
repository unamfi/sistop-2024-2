#!/usr/bin/python3
import os
print('PID del proceso: %d' % os.getpid())

file = open('archivo de datos', 'w+')
file.seek(1024*1024*1024-1)
file.write(".")
file.flush()
os.unlink('archivo de datos')

input()
