/*
 * File: ls.h
 * Incluye la función para listar archivos
 */

#ifndef FIUNAMFS_LS
#define FIUNAMFS_LS

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

#include "error.h"
#include "fs.h"
#include "misc.h"

/*
 * Copia un archivo dentro del sistema de archivos hacia otro sistema de archivos
 * @param imagen Puntero al sistema de archivos
 * @return 0 si la tarea tuvo éxito, 1 si no
 */
int fiunamfs_ls(FILE* imagen);

#endif
