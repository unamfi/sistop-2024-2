#!/usr/bin/python3
import mmap
import os
import time

archivo = '/home/gwolf/gwolf_bosnia.jpg'


fh = open(archivo, 'r+')
print('El PID de este proceso es %d' % os.getpid() )

fileno = fh.fileno()
print('El fileno() de %s es %d' % (fh, fileno))
mapeado = mmap.mmap(fileno, 0)

time.sleep(10)
