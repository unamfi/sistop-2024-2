#include "fs.h"

FILE* fiunamfs_open_fs(const char* ruta){
    // Buffer para lecturas
    char buf[16];
    memset(buf, 0, 16);

    FILE* imagen = fopen(ruta, "rb+");
    if (imagen == NULL) return NULL;

    // Obtener tamaño de archivo
    fseek(imagen, 0L, SEEK_END);
    uint32_t tam_unidad_real = ftell(imagen);
    fseek(imagen, 0L, SEEK_SET);

    // Probar número mágico
    fread(buf, 9, 1, imagen);
    if (strncmp(buf, "FiUnamFS", 8) != 0){
        errno = ERR_NOFS;
        return NULL;
    }

    // Comprobar versión del sistema de archivos
    fseek(imagen, 1, SEEK_CUR);
    fread(buf, 5, 1, imagen);
    if (strncmp(buf, "24-2", 4) != 0){
        errno = ERR_NOFSVER;
        return NULL;
    }

    // Obtener tamaño de cluster en bytes
    fseek(imagen, 25, SEEK_CUR);
    fread(buf, 1, 4, imagen);
    uint32_t tam_cluster = fiunamfs_int32(buf);

    // Obtener tamaño de directorio informado
    fseek(imagen, 1, SEEK_CUR);
    fread(buf, 1, 4, imagen);
    uint32_t tam_dir = fiunamfs_int32(buf);

    // Obtener tamaño de unidad informado
    fseek(imagen, 1, SEEK_CUR);
    fread(buf, 1, 4, imagen);
    uint32_t tam_unidad = fiunamfs_int32(buf);

    // Comprobar tamaño de unidad
    if (tam_unidad_real != tam_unidad*tam_cluster){
        errno = ERR_BADDRVSZ;
        return NULL;
    }

    // Crear un índice
    char* clusters = (char*) calloc(fiunamfs_bools_tam(tam_unidad), 1);
    for (size_t i=0; i<=(tam_dir); i++)
        fiunamfs_bools_set(clusters, i, true);

    // Comprobar entradas del directorio
    fseek(imagen, tam_cluster, SEEK_SET);
    for (size_t i=0; i<((tam_dir*tam_cluster)>>6); i++){
        char arc_tipo = fgetc(imagen);
        if (arc_tipo == 0x2d){
            // Archivo regular
            fseek(imagen, 15, SEEK_CUR);
            fread(buf, 1, 4, imagen);
            uint32_t arc_tam = fiunamfs_int32(buf);
            fread(buf, 1, 4, imagen);
            uint32_t arc_cluster = fiunamfs_int32(buf);
            for (size_t j=0; j<(arc_tam/tam_cluster+1); j++){
                bool val_cluster = fiunamfs_bools_get(clusters, arc_cluster+j);
                if (val_cluster){
                    errno = ERR_OVERCLUST;
                    free(clusters);
                    return NULL;
                } else fiunamfs_bools_set(clusters, arc_cluster+j, true);
            }
            fseek(imagen, 40, SEEK_CUR);
        } else if (arc_tipo == 0x2f){
            // Entrada vacía
            fseek(imagen, 63, SEEK_CUR);
            continue;
        } else {
            errno = ERR_BADDIRITEM;
            free(clusters);
            return NULL;
        }
    }
    free(clusters);
    return imagen;
}

fiunamfs_fs* fiunamfs_stat_fs(FILE* imagen){
    // Buffer para lecturas
    char buf[16];
    memset(buf, 0, 16);

    // Estructura para los datos
    fiunamfs_fs* str_datos = (fiunamfs_fs*) calloc(1, sizeof(fiunamfs_fs));
    if (str_datos == NULL){
        errno = ERR_MEMORY;
        return NULL;
    }

    // Obtener etiqueta
    fseek(imagen, 20, SEEK_SET);
    fread(buf, 1, 16, imagen);
    strcpy(str_datos->etiqueta, buf);

    // Obtener tamaño de cluster en bytes
    //clusters_directorio,clusters_unidad
    fseek(imagen, 40, SEEK_SET);
    fread(buf, 1, 4, imagen);
    str_datos->tam_cluster = fiunamfs_int32(buf);

    // Obtener tamaño de directorio
    fseek(imagen, 45, SEEK_SET);
    fread(buf, 1, 4, imagen);
    str_datos->clusters_directorio = fiunamfs_int32(buf);

    // Obtener tamaño de unidad
    fseek(imagen, 50, SEEK_SET);
    fread(buf, 1, 4, imagen);
    str_datos->clusters_unidad = fiunamfs_int32(buf);

    return str_datos;
}
