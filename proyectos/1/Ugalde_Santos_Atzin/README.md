# fiunamfs
Este es el proyecto 1 de la materia Sistemas Operativos, impartida por el profesor Gunnar Wolf.

## Compilar
Solo necesitas un compilador de C, como gcc; y make. Con escribir `make`, bastará.

## Ejecución
Puedes hacer 4 operaciones:
- Listar archivos: `./fiunamfs ls [sistema]`
- Borrar archivos del sistema de archivos: `./fiunamfs rm [sistema]`
- Copiar archivos del sistema de archivos a otro punto: `./fiunamfs cpi [sistema] [origen] [destino]`
- Copiar archivos al sistema de archivos desde otro punto: `./fiunamfs cpo [sistema] [origen] [destino]`

`[sistema]` será la ruta donde se encuentre la imagen del sistema de archivos. `[origen]` y `[destino]` pueden ser una ruta, cuando se refiera al archivo externo (`[destino]` con el comando `cpi`, y `[origen]` con el comando `cpo`), y un nombre de archivo de máximo 14 caracteres cuando se refiera a un nombre de archivo dentro del sistema de archivos fiunamfs (`[origen]` con el comando `cpi`, y `[destino]` con el comando `cpo`).

## Ejemplo de uso
```
$ ./fiunamfs ls fiunamfs.img 
README.org            30K    6     2024-05-08 13:17:56    2024-05-08 13:17:56
logo.png             123K    22    2024-05-08 13:17:56    2024-05-08 13:17:56
mensaje.jpg          248K    84    2024-05-08 13:17:56    2024-05-08 13:17:56
$ ./fiunamfs rm fiunamfs.img README.org
$ ./fiunamfs ls fiunamfs.img 
logo.png             123K    22    2024-05-08 13:17:56    2024-05-08 13:17:56
mensaje.jpg          248K    84    2024-05-08 13:17:56    2024-05-08 13:17:56
$ ./fiunamfs cpi fiunamfs.img /tmp/apps.py lily
$ ./fiunamfs ls fiunamfs.img 
logo.png             123K    22    2024-05-08 13:17:56    2024-05-08 13:17:56
mensaje.jpg          248K    84    2024-05-08 13:17:56    2024-05-08 13:17:56
lily                  96B    5     2024-05-20 07:29:09    2024-05-20 07:29:09
$ ./fiunamfs cpo fiunamfs.img  logo.png /tmp/logo.png
```

