#include "rm.h"

int fiunamfs_rm(FILE* imagen, const char* ruta){
    // Buffer para lecturas
    char buf[16];
    memset(buf, 0, 16);

    // Obtener datos del sistema de archivos
    fiunamfs_fs* str_datos = fiunamfs_stat_fs(imagen);

    fseek(imagen, str_datos->tam_cluster, SEEK_SET);
    for (size_t i=0; i<((str_datos->clusters_directorio*str_datos->tam_cluster)>>6); i++){
        char arc_tipo = fgetc(imagen);
        if (arc_tipo == 0x2d){
            // Leer nombre de archivo
            memset(buf, 0, 16);
            fread(buf, 1, 15, imagen);

            // Normalizar espacios al final y comparar
            for (int j=15; j>=0 && (buf[j] == ' ' || buf[j] == 0); j--) buf[j] = 0;
            if (!strcmp(buf, ruta)){
                // Borrar entrada del directorio
                fseek(imagen, -16, SEEK_CUR);
                fwrite("/###############", 1, 16, imagen);
                return 0;
            }

            fseek(imagen, 47, SEEK_CUR);
        } else if (arc_tipo == 0x2f){
            // Entrada vacía
            fseek(imagen, 63, SEEK_CUR);
            continue;
        }
    }
    errno = ERR_NOFILE;
    return 1;
}
