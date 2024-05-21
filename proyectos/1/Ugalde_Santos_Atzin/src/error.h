/*
 * File: error.h
 * Incluye funciones y macros para tratar con errores
 */

#ifndef FIUNAMFS_DEFS
#define FIUNAMFS_DEFS

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

#define ERR_NOFS 201
#define ERR_NOFSVER 202
#define ERR_BADDRVSZ 203
#define ERR_BADDIRITEM 204
#define ERR_OVERCLUST 205
#define ERR_MEMORY 206
#define ERR_NOFILE 207 // Hay qué diferenciar errores del sistema de archivos host y el del archivo
#define ERR_FULLDIR 208

/*
 * Muestra y trata errores FiUnamFS
 * @param err Error devuelto por una función FiUnamFS
 */
void fiunamfs_check_err();

#endif
