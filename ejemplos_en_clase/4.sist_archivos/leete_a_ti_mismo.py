#!/usr/bin/python3

fh = open('leete_a_ti_mismo.py', 'r')

# Muestra los primeros 20 caracteres
print(fh.read(20))

# muestra 5 veces los siguientes 5 caracteres
for i in range(5):
    fh.seek(30)
    print(fh.read(5))


