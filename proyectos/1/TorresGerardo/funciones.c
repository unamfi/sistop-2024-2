#include <stdio.h>
#include <omp.h>
#include <unistd.h>

void PmensajeInicial()
{
    printf("\n\nBIENVENIDO A UNAMFS:\n\nQUE DESEA REALIZAR?\n\n");
    printf("1.Listar los contenidos del directorio\n\n");
    printf("2.Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema\n\n");
    printf("3.Copiar un archivo de tu computadora hacia tu FiUnamFS\n\n");
    printf("4.Eliminar un archivo del FiUnamFS\n\n");
}