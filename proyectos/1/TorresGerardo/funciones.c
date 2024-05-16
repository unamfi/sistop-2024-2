#include <stdio.h>
#include <omp.h>//para multihilo
#include <unistd.h>//para vrificar existencia de ficheros
#include <dirent.h>//para leer directorio
#include <time.h>//para obtener la hora
#include <string.h>//para comparar cadenas


void PmensajeInicial()
{
    printf("\n\nBIENVENIDO A UNAMFS:\n\nQUE DESEA REALIZAR?\n\n");
    printf("1.Listar los contenidos del directorio\n\n");
    printf("2.Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema\n\n");
    printf("3.Copiar un archivo de tu computadora hacia tu FiUnamFS\n\n");
    printf("4.Eliminar un archivo del FiUnamFS\n\n");
}

void moverAsector(int s)
{
}

void printHora(char nh[15])
{
    struct tm *newTime;
    time_t szClock;
    time( &szClock );
    newTime = localtime( &szClock );
    char *h,cmp[4];
    h = asctime( newTime );
    cmp[0] = h[4];
    cmp[1] = h[5];
    cmp[2] = h[6];
    cmp[3] = '\0';
    nh[14] = '\0';
    nh[0] = h[20];
    nh[1] = h[21];
    nh[2] = h[22];
    nh[3] = h[23];
    nh[6] = h[8];
    nh[7] = h[9];
    nh[8] = h[11];
    nh[9] = h[12];
    nh[10] = h[14];
    nh[11] = h[15];
    nh[12] = h[17];
    nh[13] = h[18];

    if (strcmp(cmp,"Jan\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '1';    
    }

    if (strcmp(cmp,"Feb\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '2';    
    }
    
    if (strcmp(cmp,"Mar\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '3';    
    }
    
    if (strcmp(cmp,"Apr\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '4';    
    }

    if (strcmp(cmp,"May\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '5';    
    }

    if (strcmp(cmp,"Jun\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '6';    
    }

    if (strcmp(cmp,"Jul\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '7';    
    }

    if (strcmp(cmp,"Aug\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '8';    
    }

    if (strcmp(cmp,"Sep\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '9';    
    }

    if (strcmp(cmp,"Oct\0") == 0)
    {
        nh[4] = '1';    
        nh[5] = '0';    
    }

    if (strcmp(cmp,"Nov\0") == 0)
    {
        nh[4] = '1';    
        nh[5] = '1';    
    }

    if (strcmp(cmp,"Dec\0") == 0)
    {
        nh[4] = '1';    
        nh[5] = '2';    
    }
}


int littleEndian(int n)
{
    int b[4],r = 0, i = 1;

    for (;i<5;i++)
    {
        b[i - 1] = n;
        b[i - 1] = b[i - 1] << 32 - 8 * i;
    }

    r = b[0];

    for (i=2;i<5;i++)
    {
        b[i - 1] = b[i - 1] >> 24;
        b[i - 1] = b[i - 1] << 32 - 8 * i;
        r += b[i - 1];
    }

    return r;
}

void mostrarDirectorioExterno(void)
{
    struct dirent *archivo;
    DIR *dir;
    
    printf("CONTENIDO DE sistop-2024-2|proyectos|1|TorresGerardo:\n");
    dir = opendir(".");

    while ((archivo = readdir(dir)) != 0) 
    {
        if(*(archivo->d_name) != '.')
            printf("\n%s\n", archivo->d_name);
    }

    closedir(dir);
}