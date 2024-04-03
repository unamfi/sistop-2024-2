#include <stdio.h>
#include <time.h>

int main() {
    // Obtiene la fecha y hora actual
    time_t tiempoActual;
    struct tm *infoTiempo;
    time(&tiempoActual);
    infoTiempo = localtime(&tiempoActual);

    // Imprime la fecha y hora actual con segundos, minutos, horas, día, mes y año
    printf("Fecha y hora actual: %02d-%02d-%d %02d:%02d:%02d\n",
           infoTiempo->tm_mday, infoTiempo->tm_mon + 1, infoTiempo->tm_year + 1900,
           infoTiempo->tm_hour, infoTiempo->tm_min, infoTiempo->tm_sec);

    // Determina el saludo según la hora del día
    int hora = infoTiempo->tm_hour;
    if (hora >= 0 && hora < 6) {
        printf("¡Bonita madrugada!\n");
    } else if (hora >= 6 && hora < 12) {
        printf("¡Buenos días!\n");
    } else if (hora >= 12 && hora < 19) {
        printf("¡Buenas tardes!\n");
    } else {
        printf("¡Buenas noches!\n");
    }

    return 0;
}

