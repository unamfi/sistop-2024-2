#!/usr/bin/python3

fh = open('leete_a_ti_mismo.py', 'r')

caracter = fh.read(1)
while (caracter):
    print(caracter, end='')
    caracter = fh.read(1)
