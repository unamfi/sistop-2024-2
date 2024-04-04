// ASIGNATURA: Sistemas Operativos
// GRUPO: 6
// ALUMNO: Rosas Meza Isaías
// SEMESTRE: 2024-2

#include <stdio.h>
int main() {
	#pragma omp parallel
	{
	int i;
	printf("Hola Mundo\n");
	for(i=0;i<10;i++){
		printf("Iteracion:%d\n",i);
	}
	}
	printf("Adios \n");
	return 0;
}
