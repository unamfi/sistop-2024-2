#!/usr/bin/python3
fuente = '/home/gwolf/vcs/sistemas_operativos/laminas/03-relacion-con-el-hardware.org'
dest = '/tmp/laminas.org'

fh_fuente = open(fuente, 'r')
fh_dest = open(dest, 'w')

terminado = False
while not terminado:
    print('.', end='')
    data = fh_fuente.read(16)
    if len(data) == 0:
        break
    fh_dest.write(data)
