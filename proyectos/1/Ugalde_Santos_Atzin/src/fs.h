/*
 * File: fs.h
 * Incluye funciones para administrar un sistema de archivos existente
 */

#ifndef FIUNAMFS_FS
#define FIUNAMFS_FS

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "error.h"
#include "misc.h"

typedef struct {
    char etiqueta[16]; /**< Etiqueta de la unidad */
    uint32_t tam_cluster; /**< Tamaño de un cluster en bytes */
    uint32_t clusters_directorio; /**< Tamaño del directorio en clusters */
    uint32_t clusters_unidad; /**< Tamaño de la unidad completa en clusters */
} fiunamfs_fs;

/*
 * Valida si el sistema de archivos está en buen estado
 * @param ruta Ruta de la imagen de disco a leer
 * @return Puntero al archivo, o NULL si falló
 */
FILE* fiunamfs_open_fs(const char* ruta);

/*
 * Devuelve una estructura con información sobre el sistema de archivos
 * @param imagen Puntero al sistema de archivos
 * @return un puntero con la estructura con los datos del sistema de archivos, o NULL si hubo un error
 */
fiunamfs_fs* fiunamfs_stat_fs(FILE* imagen);

#endif
