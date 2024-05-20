#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <unistd.h>
#include <sys/stat.h>

#define SUPERBLOQUE_TAMANO 1024
#define ENTRADA_DIRECTORIO_TAMANO 64

typedef struct
{
    char nombre_fs[9];
    char version[6];
    uint32_t tamano_cluster;
    uint32_t numero_clusters_directorio;
    uint32_t numero_maximo_clusters;
    uint32_t directorio_inicio;
    uint32_t directorio_tamano;
    uint32_t entrada_directorio_tamano;
} Superbloque;
