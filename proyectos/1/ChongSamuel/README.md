# Sistema de Archivos FIUnamFS
## Autor(es)
Chong Hernandez Samuel

## Descripción
Este programa implementa un sistema de archivos FIUnamFS con funcionalidades básicas como listar archivos, copiar archivos dentro y fuera del sistema de archivos, eliminar archivos.

## Estrategia
El programa utiliza concurrencia mediante la biblioteca threading de Python para ejecutar dos hilos de manera concurrente. 
Un hilo monitorea el estado del sistema de archivos y actualiza periódicamente la cola de mensajes con el mapa de almacenamiento. El otro hilo maneja las operaciones del usuario a través de un menú interactivo. Se utiliza un evento para sincronizar la terminación del hilo de monitoreo cuando el usuario decide salir del programa.

## Requisitos
Python (versión 3.6 o superior)
Instalación de los módulos threading y queue de Python, así como demás librerías (generalmente incluidos en la instalación estándar de Python)

## Uso

-Clona o descarga el repositorio en tu máquina local.

-Abre una terminal y navega al directorio donde se encuentra el código.

-Ejecuta el programa utilizando el siguiente comando:

python3 proyecto_1.py

Sigue las instrucciones proporcionadas en el menú interactivo para realizar las operaciones deseadas en el sistema de archivos FIUnamFS.

## Sincronización
Se utiliza un evento para sincronizar la terminación del hilo de monitoreo con la acción del usuario de salir del programa.
El hilo de monitoreo actualiza periódicamente la cola de mensajes con el mapa de almacenamiento del sistema de archivos, mientras que el hilo del menú maneja las operaciones del usuario.

## Ejemplos de uso

El usuario ejecuta el programa y se presenta un menú interactivo con varias opciones. 
Por ejemplo, puede seleccionar la opción para listar archivos, copiar un archivo del sistema de archivos a una ubicación externa, 
copiar un archivo de la computadora al sistema de archivos, eliminar un archivo del sistema de archivos, o salir del programa.


