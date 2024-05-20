# Estrategia

Se decidió dividir el proyecto en 5 fases
1. Conocer el problema
2. Modularizar y optimización
3. Desarrollo de interfaz de usuario (cli y shell)
4. Solucionar problemas
5. Documentar

Solución inicial
---
Se opto por primero conocer al sistema de archivos con ayuda de las funciones de 
decode('ascii') y struct.unpack(), estas facilitaron la comprensión del problema,
el como estaba divido el super bloque.

Modularización
---
Una vez logrado hacer que el programa funcione con las operaciones de copiar, listar
y eliminar; se busco crear clases para un código más limpio, se generó los siguientes archivos

## Principales

### [FIFS](../src/fifs.py)
Contiene la interacción con el usuario, en un inicio se utilizó para realizar pruebas
de las funciones e instancias que componen al proyecto, posteriormente se procedió a
implementar [cli](cli.md) y [shell](shell.md)

### [Sistema de Archivos](../src/sistema_archivos.py)
Se consideró que se tenia que implementar el directorio y super bloque dentro de la clase
de sistema de archivos, al igual que las operaciones con las que se manipularán los archivos
como push (copiar de nuestro sistema operativo a fi unam fs), pull (copiar de fi unam fs a nuestro sistema operativo),
ls (mostrar el contenido del directorio principal) y remove (encargado de 'olvidar' donde se ubica el archivo)

### [Directorio](../src/directorio.py)
Para el directorio existen 2 partes caracteristicas de él, ambas entradas

- `Entradas ocupadas`: permite almacenar para poder listar y obtener información de los archivos existentes
- `Entradas desocupadas`: no contiene una lista de entradas, pero contiene una lista de los clusters desocupados,
                          esto permite calcular el byte en donde se puede escribir un nuevo archivo con ayuda
                          del número de cluster
### [SuperBloque](../src/super_bloque.py)
Contiene la información del super_bloque, es implementada en sistema de archivos para su uso
informativo


### [Entrada](../src/entrada.py)
Permite simplificar el acceso a los datos de cada entrada y listar la información de los archivos


## Extras

### [Excepciones](../src/excepciones.py)
Contiene 2 excepciones personalizadas
- `EntradaNoValidaException`: Permite identificar cuando una entrada no cumple con las características,
                              principalmente errores dentro de fi unam fs cuando se quieren hacer operaciones
                              sobre nombres de archivos que no existen
- `EspacioInsuficienteException`: En caso de no encontrar un conjunto de clusters contiguos desocupados, se levantará
 
### [Constantes](../src/constantes.py)
Permite reutilizar valores que se utilizaron constantemente como el número de bytes por cluster
y el número de bytes por sector.

### [Helper](../src/helper.py)
Contiene funciones para la búsqueda de espacio disponible, en este caso de clusters desocupados
`buscar_clusters_desocupados`: genera una lista con los clusters desocupados después del cluster de directorio
`buscar_cluster_contiguo_desocupado`: realiza una búsqueda iterando la lista obtenida para encontrar
números consecutivos que cumplan con el número de clusters calculados para albergar el archivo deseado.

Interfaz de usuario cli y shell:
---
Evitando el uso de bibliotecas externas se opto por un sistema básico de cli y shell
ambos responde a usos 'reales' para la manipulación de un sistema de archivos como 
fi unam fs, mientras cli permite ejecutar comandos sin salir de la terminal común,
shell permite la ejecución de comandos continua y con ayuda de los menus interactivos
para las operaciones de copiar y eliminar.

Solución de problemas
---
Se aplicó testing manual, esto permitió identificar problemas y algunas fallas en la experiencia de uso