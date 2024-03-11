#include <stdio.h>
#include <stdlib.h>

int main(void) {
	char *nombre;
	nombre = malloc(BUFSIZ * sizeof(*nombre));

	printf("¿Cuál es tu nombre?: ");
	fgets(nombre, BUFSIZ, stdin);

	printf("Hola, %s", nombre);

	return 0;
}
