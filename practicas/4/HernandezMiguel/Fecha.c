#include <stdio.h>
#include <time.h>

int main() {
    time_t tiempo_actual;
    struct tm *info_tiempo;
    char fecha_actual[100];

    time(&tiempo_actual);
    info_tiempo = localtime(&tiempo_actual);

    strftime(fecha_actual, sizeof(fecha_actual), "%Y-%m-%d", info_tiempo);

    printf("La fecha actual es: %s\n", fecha_actual);

    return 0;
}
