#include <stdio.h>

void main() {
  int w, x, y, z;

  w = 5;
  x = 7;
  y = 3;
  z = 8;

  printf("Va una operación no atómica: La suma de %d, %d, %d, %d: %d\n",
	 w, x, y, z, w+x+y+z);

  printf("Es más: ¡Ni siquiera el post-incremento es (siempre) atómico!\n");
  w++;
}
