#include <stdio.h>

int main() {
    FILE *archivo;
    archivo = fopen("resultado.txt", "w");
    if (archivo != NULL) {
        fprintf(archivo, "Este es el resultado generado por el programa.\n");
        fclose(archivo);
    } else {
        printf("Error al abrir el archivo.\n");
    }
    return 0;
}
