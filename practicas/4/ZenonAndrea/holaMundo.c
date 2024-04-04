#include <stdio.h>
#include <string.h>

int main() {
    char nombre[15];

    printf("Ingresa tu nombre: ");
    scanf("%s", nombre);
    
    printf("Hola %s, bienvenid@ al programa!", nombre);
	return 0;
}