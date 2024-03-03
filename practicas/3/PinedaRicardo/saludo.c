#include <stdio.h>

char nombre[50];

int main() {
    printf("Hola mundo!!\n");
    printf("Ingrese su nombre: ");
    scanf("%[^\n]",&nombre);
    printf("\nHola %s",nombre);
    return (0);
}
