#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  int res;
  printf("¡Hola Mundo!\n");
  res = sleep(2);
  printf("La respuesta fue %d. ¿Listo para seguir?\n", res);
  scanf("%s");
  exit(0);
}
