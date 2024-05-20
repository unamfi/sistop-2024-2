#include <stdio.h>
#include <omp.h>
#include <dirent.h>
//#include <sys/types.h>
/*ESTE ARCHIVO ES PARA CREAR EL PSEUDODISPOSITIVO 
Y OTROS ARCHIVOS DE EJEMPLO*/
int main() 
{ 
    char xd[4] = {0,0,0x80,00};
    int i = 0x00008000;
    FILE * arch = fopen("a.txt","r");
    printf("%li",ftell(arch));
    fseek(arch,0,SEEK_END);
    printf("%li",ftell(arch));
    fclose(arch);
    return 0;
}