#include "funciones.c"

int main(int argc, char **argv)
{
    if(argc == 2)
    {
        //la funcion endian determina como se guardan los int en el sistema
        tipo_maquina = endian();// 0 para little endian, 1 para big endian
          
        if(verificaSistema(*(argv + 1),tipo_maquina) == 1)
        {
            while(seleccion != TERMINAR_PROGRAMA)
            {    
                leerSeleccion(&seleccion);
                switch (seleccion)
                {
                    case '1':
                        printf("HACE 1\n");
                    break;

                    case '2':
                        printf("HACE 2\n");
                    break;

                    case '3':
                        printf("HACE 3\n");
                    break;

                    case '4':
                        printf("HACE 4\n");
                    break;
                }
                /*char nh[15];
                printHora(nh);
                printf("%s",nh);*/
            }
        }

        else 
            printf("UNIDAD NO RECONOCIDA\n");

        return 0;
    }
        
    else 
        printf("Especifique el nombre de la unidad a revisar\n");

    return 0;
}