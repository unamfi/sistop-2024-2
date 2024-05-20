/*
 * File: cp.h
 * Incluye las funciones para copiar archivos, desde y hacia el sistema de archivos
 */

#ifndef FIUNAMFS_CP
#define FIUNAMFS_CP

#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include "error.h"
#include "fs.h"
#include "misc.h"

/*
 * Copia un archivo dentro del sistema de archivos hacia otro sistema de archivos
 * @param imagen Puntero al sistema de archivos
 * @param ruta_dentro Nombre del archivo dentro del sistema de archivos a copiar
 * @param ruta_fuera Ruta a dónde escribir la copia
 * @return 0 si la tarea tuvo éxito, 1 si no
 */
int fiunamfs_cp_fuera(FILE* imagen, const char* ruta_dentro, const char* ruta_fuera);

/*
 * Copia un archivo de otro sistema de archivos hacia el sistema de archivos
 * @param imagen Puntero al sistema de archivos
 * @param ruta_dentro Nombre que recibirá el archivo copiado dentro del sistema de archivos
 * @param ruta_fuera Ruta al archivo a copiar
 * @return 0 si la tarea tuvo éxito, 1 si no
 */
int fiunamfs_cp_dentro(FILE* imagen, const char* ruta_dentro, const char* ruta_fuera);

/*
 * Copia un archivo dentro del sistema de archivos
 * @param imagen Puntero al sistema de archivos
 * @param origen Nombre del archivo a copiar
 * @param destino Nombre de la copia
 * @return 0 si la tarea tuvo éxito, 1 si no
 */
int fiunamfs_cp_interno(FILE* imagen, const char* origen, const char* destino);

#endif
