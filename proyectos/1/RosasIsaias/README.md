# Entrega de proyecto final

## Nombre del proyecto: (Micro) sistema de archivos multihilos

### @Autor: Rosas Meza Isaías

### Lenguaje y entorno

- Lenguaje: Python
- Versión empleada: 3.9.9
- Entorno: Visual Studio Code
- Librerías externas: N/A

### Estrategia

- Se inicializan las propiedades más importantes del disco de FiUnamFS y se abre el mismo desde el inicio del programa. El menú de opciones ejecuta una función depenediendo de lo que se busque hacer, exceptuando la operación de "cortar y pegar" un archivo, siendo esa acción por medio de unos elementos de los semáforos para hilos.

### Funcionamiento

* Para que el sistema funcione correctamente, el disco debe encontrarse en la misma carpeta donde se encuentre el programa.

* Cuando se ejecuta el programa se muestra un menú de opciones para operar directamente con el disco de FiUnamFS. Las opciones son las siguientes:
- 1) Listar archivos del disco
- 2) Copiar un archivo de FiUnamFS a sistema
- 3) Copiar un archivo del sistema a FiUnamFS
- 4) Borrar un archivo de FiUnamFS 
- 5) 'Cortar' y pegar un archivo de FiUnamFS al sistema
- 6) Salir del programa

En cada opción se indica por medio de una flecha una sintaxis de lo que se debe escribir en la sección de comandos. Debe tenerse en cuenta que las ordenes van en mínusculas, con espacios hechos con la tecla SCAPE y el nombre de los archivos debe incluir su extensión.

### Ejemplos de uso

* OPCIÓN 1:
		Ingrese el comando como se muestra en el menú de opciones:
		enlista
* OPCIÓN 2
		Ingrese el comando como se muestra en el menú de opciones: 
		copia  -logo.png   .

###### NOTA: El punto en el apartado de "rutaDestino" es para copiar el archivo en la misma carpeta donde se encuentre el programa y el disco.

### Sobre esta versión
- La versión 1.0 todavía no cuenta con la implementación de la opción 3, por lo que su ejecución termina mostrando el error de comando. Se plantea implementarla en una futura versión si se presenta la oportunidad.

### Notas finales
Debo ser honesto con la forma del código: Se trata de una versión modificada del programa presentado por el compañero Diego Armenta del semestre 2021-1. Si bien traté de ajustarlo para implementar la opción faltante, la cual incluía más opciones como el análisis de cada bloque del disco, no pude completarla a tiempo.
Acepto una sanción correspondiente y me disculpo por recurrir a esta práctica.
