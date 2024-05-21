#include "cp.h"

int fiunamfs_cp_fuera(FILE* imagen, const char* ruta_dentro, const char* ruta_fuera){
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
            if (!strcmp(buf, ruta_dentro)){
                // Leer tamaño de archivo en bytes
                fread(buf, 1, 4, imagen);
                uint32_t arc_tam = fiunamfs_int32(buf);

                // Leer cluster de archivo
                fread(buf, 1, 4, imagen);
                uint32_t arc_cluster = fiunamfs_int32(buf);

                // Copiar archivo hacia afuera
                FILE* destino = fopen(ruta_fuera, "wb+");
                if (destino == NULL) return 1;

                fseek(imagen, arc_cluster*str_datos->tam_cluster, SEEK_SET);
                for (size_t k=0; k<arc_tam; k++) fputc(fgetc(imagen), destino);

                fclose(destino);
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

int fiunamfs_cp_dentro(FILE* imagen, const char* ruta_dentro, const char* ruta_fuera){
    // Buffer para lecturas
    char buf[16];
    memset(buf, 0, 16);

    // Leer archivo origen
    FILE* origen = fopen(ruta_fuera, "rb");
    if (origen == NULL) return 1;

    // Obtener tamaño de archivo origen
    fseek(origen, 0L, SEEK_END);
    uint32_t origen_tam = ftell(origen);
    fseek(origen, 0L, SEEK_SET);

    // Obtener datos del sistema de archivos
    fiunamfs_fs* str_datos = fiunamfs_stat_fs(imagen);

    // Crear índice de clusters ocupados...
    char* clusters = (char*) calloc(fiunamfs_bools_tam(str_datos->clusters_unidad), 1);
    for (size_t i=0; i<=(str_datos->clusters_directorio); i++)
        fiunamfs_bools_set(clusters, i, true);

    // Bandera de disponibilidad en directorio
    int cluster_disponible = -1;

    fseek(imagen, str_datos->tam_cluster, SEEK_SET);
    // ...y rellenarlo
    for (size_t i=0; i<((str_datos->clusters_directorio*str_datos->tam_cluster)>>6); i++){
        char arc_tipo = fgetc(imagen);
        if (arc_tipo == 0x2d){
            fseek(imagen, 15, SEEK_CUR);
            fread(buf, 1, 4, imagen);
            uint32_t arc_tam = fiunamfs_int32(buf);
            fread(buf, 1, 4, imagen);
            uint32_t arc_cluster = fiunamfs_int32(buf);
            for (size_t j=0; j<(arc_tam/str_datos->tam_cluster+1); j++){
                bool val_cluster = fiunamfs_bools_get(clusters, arc_cluster+j);
                if (!val_cluster) fiunamfs_bools_set(clusters, arc_cluster+j, true);
            }
        } else if (arc_tipo == 0x2f){
            // Entrada vacía
            if (cluster_disponible == -1) cluster_disponible = i;
            fseek(imagen, 63, SEEK_CUR);
            continue;
        }
    }

    // Ver si hay espacio
    if (cluster_disponible == -1){
        errno = ERR_FULLDIR;
        return 1;
    }

    // Buscar un bloque de clusters libre
    size_t contador = 0;
    size_t cluster_tentativo = 0;
    size_t clusters_necesarios = (origen_tam/(str_datos->tam_cluster)) + 1;
    bool val_cluster;
    for (size_t i=0; str_datos->clusters_directorio; i++){
        if (contador < clusters_necesarios){
            val_cluster = fiunamfs_bools_get(clusters, i);
            if (val_cluster) contador = 0;
            else {
                if (contador == 0) cluster_tentativo = i;
                contador++;
            }
        } else {
            // Copia!
            fseek(imagen, cluster_tentativo*(str_datos->tam_cluster), SEEK_SET);
            for (size_t j=0; j<origen_tam; j++) fputc(fgetc(origen), imagen);

            // Escribir la entrada en el directorio
            fseek(imagen, (str_datos->tam_cluster) + (64*i), SEEK_SET);
            //char* nombre = strrchr(ruta_fuera, '/');
            /// Tipo de archivo
            fputc('-', imagen);
            /// Nombre
            bool tiempo_pad = false; // Bandera para saber si se debe escribir nombre o relleno
            for (size_t j=0; j<14; j++){
                if (!tiempo_pad) fputc(ruta_dentro[j], imagen);
                else fputc(0, imagen);
                if (ruta_dentro[j] == 0) tiempo_pad = true;
            }
            fputc(0, imagen);
            /// Tamaño del archivo
            unsigned char bufint[4];
            fiunamfs_int32_dump(origen_tam, bufint);
            fwrite(bufint, 1, 4, imagen);
            /// Cluster inicial
            fiunamfs_int32_dump((uint32_t) cluster_tentativo, bufint);
            fwrite(bufint, 1, 4, imagen);

            time_t timet_tm = time(NULL);
            struct tm* str_tm = gmtime(&timet_tm);
            /// Fecha y hora de creación
            fprintf(imagen, "%04u%02u%02u%02u%02u%02u", str_tm->tm_year+1900, str_tm->tm_mon+1, str_tm->tm_mday, str_tm->tm_hour, str_tm->tm_min, str_tm->tm_sec);
            /// Fecha y hora de modificación
            fprintf(imagen, "%04u%02u%02u%02u%02u%02u", str_tm->tm_year+1900, str_tm->tm_mon+1, str_tm->tm_mday, str_tm->tm_hour, str_tm->tm_min, str_tm->tm_sec);

            fclose(origen);
            return 0;
        }
    }
    return 1;
}
