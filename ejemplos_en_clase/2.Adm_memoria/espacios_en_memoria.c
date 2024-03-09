#include <stdlib.h>
#include <stdio.h>

int datos = 10;
char* cadena = "¡Hola bola!";

void funcioncita(int veces) {
  int i;
  for (i=0; i<veces; i++) {
    printf("!");
  }
  printf("\n");
}

void main() {
  int otro_dato = 15;
  char* mas_texto = "blablablá";

  char* rollo;
  /* ... */

  /* Necesitamos una cadena de 120 caracteres */
  rollo = malloc(120 * sizeof(char));
  rollo[0] = 65;
  rollo[1] = 32;
  rollo[2] = 65;
  rollo[3] = 0;

  funcioncita(10);
  funcioncita(5);

  printf("%s\n", rollo);
  free(rollo);
}
