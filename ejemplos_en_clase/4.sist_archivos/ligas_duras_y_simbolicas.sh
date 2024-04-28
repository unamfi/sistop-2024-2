#!/bin/bash

# Limpieza antes que nada...
rm -f fecha.txt aquitambien simbólico

# Creamos un archivo con la fecha actual
date > fecha.txt

# Generamos una liga dura a fecha.txt
ln fecha.txt aquitambien

echo "Acá tenemos un mismo archivo con dos nombres:"
ls -li fecha.txt aquitambien

echo "Si le hago una modificación... El contenido del _otro_ es:"
pwd > aquitambien
cat fecha.txt

echo "Es más... Puedo borrar a fecha.txt y todo sigue en su lugar:"
rm fecha.txt
ls -li aquitambien
cat aquitambien

echo '---------------'
echo 'Generemos una liga simbólica:'
ln -s aquitambien simbólico
ls -li aquitambien simbólico

echo '¿y si borramos el archivo?'
rm aquitambien
ls -li aquitambien simbólico
cat simbólico
