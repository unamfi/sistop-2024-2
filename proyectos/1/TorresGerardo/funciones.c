#include <stdio.h>
#include <omp.h>//para multihilo
#include <unistd.h>//para verificar existencia de ficheros
#include <dirent.h>//para leer directorio
#include <time.h>//para obtener la hora
#include <string.h>//para comparar cadenas
#define LITTLE_ENDIAN 0
#define BIG_ENDIAN    1
#define TERMINAR_PROGRAMA 't'
int tipo_maquina;
char seleccion = 'a';
int littleEndian(int);
int endian();
void PmensajeInicial();

int moverACluster(int s, FILE *fp)
{
    int r = 0;

    if(s >= 5 && s <= 719)
    {
        fseek(fp, 2048 * s, SEEK_SET);
        r = 1;
    }

    else
        printf("ERROR\n");

    return r;
}

int verificaSistema(char nd[], int tipo_maquina)
{  
    int i;
    char s[9],v[5],n[17];
    n[16] = '\0';
    FILE *f = fopen(nd,"r");

    fread(s,sizeof(char),9,f);
    
    if(strcmp(s,"FiUnamFS\0") == 0)
        printf("SISTEMA: %s\n",s);

    else
        return 0;

    fseek(f,1,SEEK_CUR);

    fread(v,sizeof(char),5,f);
    
    printf("VERSION: %s\n",v);

    if(strcmp(v,"24-2\0") != 0)
    {
        printf("VERSION INCORRECTA\n");
        return 0;
    }

    fseek(f,5,SEEK_CUR);
        
    fread(n,sizeof(char),16,f);
    printf("ETIQUETA: %s\n",n);

    fseek(f,4,SEEK_CUR);
    fread(&i,sizeof(int),1,f);

    if(tipo_maquina == BIG_ENDIAN)
        i = littleEndian(i);

    printf("ESPACIO DEL CLUSTER: %i [B]\n",i);

    fseek(f,1,SEEK_CUR);
    fread(&i,sizeof(int),1,f);

    if(tipo_maquina == BIG_ENDIAN)
        i = littleEndian(i);

    printf("ESPACIO DEL DIRECTORIO: %i [CLUSTER]\n",i);

    fseek(f,1,SEEK_CUR);
    fread(&i,sizeof(int),1,f);

    if(tipo_maquina == BIG_ENDIAN)
        i = littleEndian(i);

    printf("ESPACIO TOTAL DE LA UNIDAD: %i [CLUSTER]\n",i);
    fclose(f);
    return 1;
}

void leerSeleccion(char *s)
{
    while(1 == 1)
    {
        PmensajeInicial();
        printf("TECLEE EL NUMERO DE SELECCION Y DE ENTER O TECLEE t PARA TERMINAR\n");
        printf("->$ ");
        scanf(" %c", s);

        if(*s > '0' && *s < '5' || *s == 't')
            return;
            
        else
        {
            printf("TECLEE UNA OPCION VALIDA\n");
            printf("PRESIONE CARACTER Y ENTER PARA CONTINUAR O t PARA TERMINAR\n");
            scanf(" %c", s);
        }
    }   
}


int endian() 
{
    int i = 1;
    char *p = (char *)&i;

    if (p[0] == 1)
        return LITTLE_ENDIAN;
        
    else
        return BIG_ENDIAN;
}

void PmensajeInicial()
{
    printf("\nBIENVENIDO A UNAMFS:\n\nQUE DESEA REALIZAR?\n");
    printf("a.Listar los contenidos del directorio\n");
    printf("b.Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema\n");
    printf("c.Copiar un archivo de tu computadora hacia tu FiUnamFS\n");
    printf("d.Eliminar un archivo del FiUnamFS\n");
}

int littleEndian(int n)
{
    int b[4],r = 0, i = 1;

    for (;i<5;i++)
    {
        b[i - 1] = n;
        b[i - 1] = b[i - 1] << 32 - 8 * i;
    }

    r = b[0];

    for (i=2;i<5;i++)
    {
        b[i - 1] = b[i - 1] >> 24;
        b[i - 1] = b[i - 1] << 32 - 8 * i;
        r += b[i - 1];
    }

    return r;
}

void mostrarDirectorioExterno(void)
{
    struct dirent *archivo;
    DIR *dir;
    
    printf("CONTENIDO DE sistop-2024-2|proyectos|1|TorresGerardo:\n");
    dir = opendir(".");

    while ((archivo = readdir(dir)) != 0) 
    {
        if(*(archivo->d_name) != '.')
            printf("\n%s\n", archivo->d_name);
    }

    closedir(dir);
}

void printHora(char nh[15])
{
    struct tm *newTime;
    time_t szClock;
    time( &szClock );
    newTime = localtime( &szClock );
    char *h,cmp[4];
    h = asctime( newTime );
    cmp[0] = h[4];
    cmp[1] = h[5];
    cmp[2] = h[6];
    cmp[3] = '\0';
    nh[14] = '\0';
    nh[0] = h[20];
    nh[1] = h[21];
    nh[2] = h[22];
    nh[3] = h[23];
    nh[6] = h[8];
    nh[7] = h[9];
    nh[8] = h[11];
    nh[9] = h[12];
    nh[10] = h[14];
    nh[11] = h[15];
    nh[12] = h[17];
    nh[13] = h[18];

    if (strcmp(cmp,"Jan\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '1';    
    }

    if (strcmp(cmp,"Feb\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '2';    
    }
    
    if (strcmp(cmp,"Mar\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '3';    
    }
    
    if (strcmp(cmp,"Apr\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '4';    
    }

    if (strcmp(cmp,"May\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '5';    
    }

    if (strcmp(cmp,"Jun\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '6';    
    }

    if (strcmp(cmp,"Jul\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '7';    
    }

    if (strcmp(cmp,"Aug\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '8';    
    }

    if (strcmp(cmp,"Sep\0") == 0)
    {
        nh[4] = '0';    
        nh[5] = '9';    
    }

    if (strcmp(cmp,"Oct\0") == 0)
    {
        nh[4] = '1';    
        nh[5] = '0';    
    }

    if (strcmp(cmp,"Nov\0") == 0)
    {
        nh[4] = '1';    
        nh[5] = '1';    
    }

    if (strcmp(cmp,"Dec\0") == 0)
    {
        nh[4] = '1';    
        nh[5] = '2';    
    }
}