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

void leer_superbloque(const char *fiunamfs_img_path, Superbloque *sb)
{

    FILE *file = fopen(fiunamfs_img_path, "rb");
    if (!file)
    {
        perror("No se pudo abrir el archivo");
        exit(EXIT_FAILURE);
    }

    fseek(file, 0, SEEK_SET);
    uint8_t superbloque[SUPERBLOQUE_TAMANO];
    fread(superbloque, 1, SUPERBLOQUE_TAMANO, file);

    memcpy(sb->nombre_fs, superbloque, 8);
    sb->nombre_fs[8] = '\0';
    memcpy(sb->version, superbloque + 10, 5);
    sb->version[5] = '\0';
    printf("\n\033[1m----------Microsistema de archivos----------\033[0m\n");

    printf("%-20s: %s\n", "Nombre FS", sb->nombre_fs);
    printf("%-20s: %s\n", "Version FS leida", sb->version);
    printf("\033[1m-------------------------------------------\033[0m\n");

    if (strcmp(sb->nombre_fs, "FiUnamFS") != 0)
    {
        fclose(file);
        fprintf(stderr, "El sistema de archivos no es FiUnamFS\n");
        exit(EXIT_FAILURE);
    }

    if (strcmp(sb->version, "24-2") != 0)
    {
        fclose(file);
        fprintf(stderr, "Versión del sistema de archivos no compatible\n");
        exit(EXIT_FAILURE);
    }

    sb->tamano_cluster = *(uint32_t *)(superbloque + 40);
    sb->numero_clusters_directorio = *(uint32_t *)(superbloque + 45);
    sb->numero_maximo_clusters = *(uint32_t *)(superbloque + 50);
    sb->directorio_inicio = sb->tamano_cluster;
    sb->directorio_tamano = sb->numero_clusters_directorio * sb->tamano_cluster;
    sb->entrada_directorio_tamano = ENTRADA_DIRECTORIO_TAMANO;

    fclose(file);
}

void imprimir_fecha(const char *fecha_raw, char *fecha_formateada) {
    struct tm tm_fecha;
    memset(&tm_fecha, 0, sizeof(struct tm));

    sscanf(fecha_raw, "%4d%2d%2d%2d%2d%2d",
           &tm_fecha.tm_year, &tm_fecha.tm_mon, &tm_fecha.tm_mday,
           &tm_fecha.tm_hour, &tm_fecha.tm_min, &tm_fecha.tm_sec);

    tm_fecha.tm_year -= 1900; 
    tm_fecha.tm_mon -= 1; 

    time_t tiempo = mktime(&tm_fecha);

    strftime(fecha_formateada, 20, "%Y-%m-%d %H:%M:%S", localtime(&tiempo));
}

void listar_archivos(const char *fiunamfs_img_path, uint32_t directorio_inicio, uint32_t directorio_tamano, uint32_t entrada_directorio_tamano) {
    FILE *file = fopen(fiunamfs_img_path, "rb");
    if (!file) {
        perror("No se pudo abrir el archivo");
        exit(EXIT_FAILURE);
    }

    fseek(file, directorio_inicio, SEEK_SET);
    uint8_t *directorio = malloc(directorio_tamano);
    fread(directorio, 1, directorio_tamano, file);

    for (uint32_t i = 0; i < directorio_tamano; i += entrada_directorio_tamano) {
        uint8_t *entrada = directorio + i;
        char nombre_archivo[15];
        memcpy(nombre_archivo, entrada + 1, 14);
        nombre_archivo[14] = '\0';
        for (int j = 0; j < 14; j++) {
            if (nombre_archivo[j] == '-') {
                nombre_archivo[j] = '\0';
                break;
            }
        }

        if (strlen(nombre_archivo) == 0 || nombre_archivo[0] == '.') {
            continue;
        }

        uint32_t tamano_archivo = *(uint32_t *)(entrada + 16);
        uint32_t cluster_inicial = *(uint32_t *)(entrada + 20);
        char fecha_creacion[15], fecha_modificacion[15];
        memcpy(fecha_creacion, entrada + 24, 14);
        fecha_creacion[14] = '\0';
        memcpy(fecha_modificacion, entrada + 38, 14);
        fecha_modificacion[14] = '\0';

        char fecha_creacion_formateada[20], fecha_modificacion_formateada[20];
        imprimir_fecha(fecha_creacion, fecha_creacion_formateada);
        imprimir_fecha(fecha_modificacion, fecha_modificacion_formateada);

        if (tamano_archivo > 0 && cluster_inicial > 0 && strlen(fecha_creacion) > 0 && strlen(fecha_modificacion) > 0) {
            printf("\033[1m---> Archivo:\033[0m %s\n", nombre_archivo);
            printf("Tama%co                  %u\n", 164, tamano_archivo);
            printf("Cluster Inicial         %u\n", cluster_inicial);
            printf("Fecha de Creaci%cn       %s\n", 162, fecha_creacion_formateada);
            printf("Fecha de Modificaci%cn   %s\n", 162, fecha_modificacion_formateada);

            printf("\n\n");
        }
    }

    free(directorio);
    fclose(file);
}
int main()
{
    const char *fiunamfs_img_path = "fiunamfs.img";
    Superbloque sb;
    leer_superbloque(fiunamfs_img_path, &sb);

    while (1)
    {
        printf("\n\t=== Menu principal ===\n");
        printf("1. Mostrar archivos\n");
        printf("0. Salir\n");

        char opcion[3];
        printf("\n\nSeleccione una opci%cn: ", 162);
        scanf("%s", opcion);
        limpiarPantallaS();

        if (strcmp(opcion, "1") == 0)
        {
            printf("\n------------------------------------Listado de archivos------------------------------------\n\n");

            listar_archivos(fiunamfs_img_path, sb.directorio_inicio, sb.directorio_tamano, sb.entrada_directorio_tamano);
            limpiarPantallaE();
        }
        else if (strcmp(opcion, "0") == 0)
        {
            printf("Terminando programa...\n");
            break;
        }
        else
        {
            printf("\n\nOpci%cn no v%clida. Por favor, intente de nuevo.\n", 162, 160);
        }
    }

    return 0;
}