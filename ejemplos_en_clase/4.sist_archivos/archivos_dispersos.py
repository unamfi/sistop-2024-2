#!/usr/bin/python3

fh = open('archivote', 'w')

fh.seek(1024 * 1024 * 1024 * 1024 * 1024 - 1)
fh.write('!')
