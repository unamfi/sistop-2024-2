#include <stdio.h>

// Definiciones de constantes
#define LONGITUD 1024
#define VECES 10

// Función para obtener el timestamp del CPU
unsigned long timestamp()
{
  long tsc;
  // La instrucción asm volatile permite introducir código ensamblador en C
  asm volatile("rdtscp; "         // Lectura serializada del TSC
               "shl $32, %%rdx; " // Recorre 32 bits bajos de RDX a izquierda
               "or %%rdx, %%rax"  // Combina RDX y RAX
               : "=a"(tsc)        // Obtiene el valor en la variable tsc
               :                  // No hay entradas adicionales
               : "%rcx", "%rdx"   // Registros que son afectados
  );
  return tsc;
}

// Función para llenar un arreglo bidimensional
void llena_arreglo(int modo)
{
  int data[LONGITUD][LONGITUD];
  int x, y;
  // Bucle para llenar el arreglo
  for (x = 0; x < LONGITUD; x++)
    for (y = 0; y < LONGITUD; y++)
      // Dependiendo del modo, se llena el arreglo en dirección horizontal o vertical
      if (modo)
        data[y][x] = 1; // Llenado vertical
      else
        data[x][y] = 1; // Llenado horizontal
}

// Función principal
int main()
{
  unsigned long inicio, fin, prom_h, prom_v;
  // Imprime el tamaño de memoria utilizado
  printf("Usando %lu bytes de memoria\n", LONGITUD * LONGITUD * sizeof(int));
  // Inicialización de variables
  prom_h = 0;
  prom_v = 0;
  int i;

  // Bucle para realizar el llenado horizontal VECES veces
  for (i = 0; i < VECES; i++)
  {
    inicio = timestamp();     // Marca de tiempo inicial
    llena_arreglo(0);         // Llenado horizontal
    fin = timestamp();        // Marca de tiempo final
    prom_h += (fin - inicio); // Suma de los tiempos de ejecución
    // Imprime el rango de tiempo y el tiempo de ejecución
    printf("De %lu a %lu: %lu\n", inicio, fin, fin - inicio);
  }
  // Imprime el promedio de tiempo de ejecución (horizontal)
  printf("Promedio (horizontal): %lu\n", prom_h / VECES);

  // Imprime una separación
  printf("=========\n");

  // Bucle para realizar el llenado vertical VECES veces
  for (i = 0; i < VECES; i++)
  {
    inicio = timestamp();     // Marca de tiempo inicial
    llena_arreglo(1);         // Llenado vertical
    fin = timestamp();        // Marca de tiempo final
    prom_v += (fin - inicio); // Suma de los tiempos de ejecución
    // Imprime el rango de tiempo y el tiempo de ejecución
    printf("De %lu a %lu: %lu\n", inicio, fin, fin - inicio);
  }
  // Imprime el promedio de tiempo de ejecución (vertical)
  printf("Promedio (vertical): %lu\n", prom_v / VECES);
  // Imprime la relación entre los tiempos de ejecución horizontal y vertical
  printf("\nRelación (horiz / vert): %f\n", (float)prom_h / prom_v);
  return (0);
}
