/* Programa: Hola mundo*/
#include <stdio.h>
#include <stdlib.h>
int main ()
{
    char *nombre = (char *)malloc(10);
    printf("¿Cuál es tu nombre?\t");
    scanf("%s",nombre);
    printf("Hola %s.\n",nombre);
    return 0;
}