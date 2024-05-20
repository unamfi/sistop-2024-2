#include "error.h"

void fiunamfs_check_err(){
    switch (errno){
        case 0:
            return;
        case 2:
            fputs("El archivo no existe en el equipo\n", stderr);
            break;
        case 13:
            fputs("No tienes permisos para abrir ese archivo\n", stderr);
            break;
        case 21:
            fputs("Intentas abrir una carpeta\n", stderr);
            break;
        case ERR_NOFS:
            fputs("El archivo leído no es un sistema de archivos FiUnamFS\n", stderr);
            break;
        case ERR_NOFSVER:
            fputs("La versión del sistema de archivos del disco no es compatible con la versión implementada\n", stderr);
            break;
        case ERR_BADDRVSZ:
            fputs("El tamaño de unidad informado en el sistema de archivos no corresponde con la realidad\n", stderr);
            break;
        case ERR_BADDIRITEM:
            fputs("Una entrada del directorio tiene un tipo de inodo no reconocido\n", stderr);
            break;
        case ERR_OVERCLUST:
            fputs("Un cluster pertenece a más de una entrada de directorio\n", stderr);
            break;
        case ERR_MEMORY:
            fputs("Hubo un error al momento de pedir memoria\n", stderr);
            break;
        case ERR_NOFILE:
            fputs("El archivo no existe en el sistema de archivos\n", stderr);
            break;
        case ERR_FULLDIR:
            fputs("El directorio está lleno\n", stderr);
            break;
        default:
            fputs("Hubo un error al abrir el archivo\n", stderr);
    }
    exit(EXIT_FAILURE);
}
