#include <stdio.h>
#include <time.h>

int main() {
    time_t tiempoActual;
    struct tm *info;
    char buffer[50];
    time(&tiempoActual);
    info = localtime(&tiempoActual);
    strftime(buffer,sizeof(buffer), "%Y-%m-%d %H:%M:%S",info);
    FILE *archivo;
    archivo = fopen("extra.txt","w");
    fprintf(archivo,"La fecha y hora actual son: %s \n",buffer);
    fclose(archivo);
    return 0;
}
