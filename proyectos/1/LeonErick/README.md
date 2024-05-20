# Proyecto 1

Autor: León Gómez Erick

## Entorno
- Linux o Windows
- Python 3.10.11
- Modulos:
  - os
  - struct
  - datetime
  - threading
- Biblioteca
  - [prettytable 3.10.0](https://pypi.org/project/prettytable/)

## Uso

Para utilizar el programa, solo es necesario ejecutar el archivo main.py con la versión de Python correspondiente. Todo el programa se maneja mediante rutas relativas y no admite rutas absolutas. Automáticamente trata de detectar el sistema de archivos en la misma ubicación que el programa. En caso de no encontrarlo, se deberá especificar la ubicación.

Si se logra encontrar y abrir el archivo para verificar la información, se desplegará un menú con las funcionalidades solicitadas. Para hacer uso de este, se debe indicar la instrucción deseada ingresando únicamente el número correspondiente a la opción.

## Sincronización empleada

Se utilizó una barrera para tener un rendezvous de tres hilos, donde dos verifican la posibilidad de ingresar un archivo al sistema de archivos local de FiUnamFs: uno verifica la cantidad de espacio disponible y el otro verifica que no exista ya un archivo con el nombre que se desea guardar. El tercer hilo sigue la ruta principal del programa y espera a que ambas verificaciones se realicen para poder continuar con su ejecución.