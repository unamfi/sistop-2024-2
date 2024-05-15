#include "funciones.c"

int main()
{
    PmensajeInicial();
    if(access("README.org",F_OK) == 0)
    {
        printf("EXISTE");
    }
    
    double a = omp_get_wtime(); 
    return 0;
}