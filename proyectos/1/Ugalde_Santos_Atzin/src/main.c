#include <stdio.h>
#include <stdlib.h>

#include "cp.h"
#include "error.h"
#include "fs.h"
#include "ls.h"
#include "rm.h"

int main (int argc, char* argv[]){
    // Necesita pasar la ruta de archivo como parámetro
    if (argc < 2){
        fputs("Necesitas especificar un comando\n", stderr);
        exit(EXIT_FAILURE);
    } else if (!strcmp(argv[1], "ayuda")){
        printf("Uso: %s <comando> <imagen> [parámetros]\n", argv[0]);
        puts("Comandos disponibles:");
        puts("  ayuda - muestra esta ayuda");
        puts("  ls [sistema] - lista los archivos del sistema de archivos");
        puts("  cpo [sistema] [origen] [destino] - copia un archivo del sistema de archivos hacia tu equipo");
        puts("  cpi [sistema] [origen] [destino] - copia un archivo de tu equipo hacia el sistema de archivos");
        puts("  rm [sistema] [archivo] - elimina un archivo del sistema de archivos");
        exit(EXIT_SUCCESS);
    } else if (argc < 3){
        fputs("Necesitas especificar la ruta de la imagen\n", stderr);
        exit(EXIT_FAILURE);
    }

    // Comprobar imagen de disco
    FILE *imagen = fiunamfs_open_fs(argv[2]);
    if (imagen == NULL) fiunamfs_check_err();

    if (!strcmp(argv[1], "ls")){
        fiunamfs_ls(imagen);
    } else if (!strcmp(argv[1], "cpo")){
        if (argc < 4){
            fputs("Necesitas especificar el nombre del archivo a copiar y el destino\n", stderr);
            fclose(imagen);
            exit(EXIT_FAILURE);
        } else if (argc < 5){
            fputs("Necesitas especificar el destino del archivo a copiar\n", stderr);
            fclose(imagen);
            exit(EXIT_FAILURE);
        }
        if (fiunamfs_cp_fuera(imagen, argv[3], argv[4])) fiunamfs_check_err();
    } else if (!strcmp(argv[1], "cpi")){
        if (argc < 4){
            fputs("Necesitas especificar la ruta del archivo a copiar\n", stderr);
            fclose(imagen);
            exit(EXIT_FAILURE);
        } else if (argc < 5){
            fputs("Necesitas especificar el nombre del archivo a guardar", stderr);
            fclose(imagen);
            exit(EXIT_FAILURE);
        }
        if (fiunamfs_cp_dentro(imagen, argv[4], argv[3])) fiunamfs_check_err();
    } else if (!strcmp(argv[1], "rm")){
        if (argc < 4){
            fputs("Necesitas especificar el nombre del archivo a borrar\n", stderr);
            fclose(imagen);
            exit(EXIT_FAILURE);
        }
        if (fiunamfs_rm(imagen, argv[3])) fiunamfs_check_err();
    } else {
        fprintf(stderr, "No existe el comando %s\n", argv[1]);
    }

    fclose(imagen);
    exit(EXIT_SUCCESS);
}
