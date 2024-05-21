/*
 * File: rm.h
 * Incluye la función para eliminar archivos
 */

#ifndef FIUNAMFS_RM
#define FIUNAMFS_RM

#include <errno.h>
#include <stdio.h>
#include <string.h>

#include "fs.h"

/*
 * Elimina un archivo dentro del sistema de archivos
 * @param imagen Puntero al sistema de archivos
 * @param ruta Nombre del archivo a borrar
 * @return 0 si la tarea tuvo éxito, 1 si no
 */
int fiunamfs_rm(FILE* imagen, const char* ruta);

#endif
