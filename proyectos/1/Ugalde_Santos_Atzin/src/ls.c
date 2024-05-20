#include "ls.h"

int fiunamfs_ls(FILE* imagen){
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
            fread(buf, 1, 15, imagen);
            printf("%-20s", buf);

            // Leer tamaño de archivo en bytes
            fread(buf, 1, 4, imagen);
            uint32_t tam_crudo = fiunamfs_int32(buf);
            printf("%4u%c    ",
                (tam_crudo>1048575?(tam_crudo/1048576):(tam_crudo>1023?(tam_crudo/1024):tam_crudo)),
                (tam_crudo>1048575?'M':(tam_crudo>1023?'K':'B'))
            );

            // Leer cluster de archivo
            fread(buf, 1, 4, imagen);
            printf("%-6u", fiunamfs_int32(buf));

            uint32_t fecha[6];
            // Leer fecha de creación de archivo
            fscanf(imagen, "%4u%2u%2u%2u%2u%2u", fecha, fecha+1, fecha+2, fecha+3, fecha+4, fecha+5);
            printf("%04u-%02u-%02u %02u:%02u:%02u    ", fecha[0], fecha[1], fecha[2], fecha[3], fecha[4], fecha[5]);

            // Leer fecha de última modificación de archivo
            fscanf(imagen, "%4u%2u%2u%2u%2u%2u", fecha, fecha+1, fecha+2, fecha+3, fecha+4, fecha+5);
            printf("%04u-%02u-%02u %02u:%02u:%02u\n", fecha[0], fecha[1], fecha[2], fecha[3], fecha[4], fecha[5]);

            fseek(imagen, 12, SEEK_CUR);
        } else if (arc_tipo == 0x2f){
            // Entrada vacía
            fseek(imagen, 63, SEEK_CUR);
            continue;
        }
    }
    return 0;
}
