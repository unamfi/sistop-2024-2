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
void listarContenido(char *nd, int tipo_maquina);

int determinarCaracteresImprimibles(char str[])
{
    int u = 0;
    char p;
    p = *(str + u);
    while (p > 32 && p < 123)
    {
        u += 1;
        p = *(str + u);
    }
    return u;

}

int determinaEspacioArchivo(char nA[])
{
    int t;
    FILE * arch = fopen(nA,"r");
    fseek(arch,0,SEEK_END);
    t = ftell(arch);
    fclose(arch);
    return t;
}

void moverACluster(int s, FILE *fp)
{
    fseek(fp, 2048 * s, SEEK_SET);
}

int verificaSistema(char nd[], int tipo_maquina)
{  
    if(access(nd,F_OK) != 0)
        return 0;
    
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
            if(*s == 't')
                return;
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
    printf("1.Listar los contenidos del directorio\n");
    printf("2.Copiar uno de los archivos de dentro del FiUnamFS hacia tu sistema\n");
    printf("3.Copiar un archivo de tu computadora hacia tu FiUnamFS\n");
    printf("4.Eliminar un archivo del FiUnamFS\n");
}

void copiaDeFiApc(char nd[], int tipo_maquina)
{
    char nA[30];
    listarContenido(nd,tipo_maquina);
    printf("QUE ARCHIVO DESEA COPIAR A SU SISTEMA?\n");
    scanf(" %s",nA);
    int numThreads = 3, bandera = 0;
    omp_set_num_threads(numThreads);
    int i, j = 0, bArchivo, id, cluster;
    char nombreArchivo[16];
    FILE *fp;
    #pragma omp parallel private(fp,i,bArchivo,nombreArchivo, id, cluster)
    {
        fp = fopen(nd,"r");
        
        nombreArchivo[15] = '\0';
        id = omp_get_thread_num();
        i = id;
        while(i < 128)
        {
            fseek(fp,2048 + 64 * i + 1,SEEK_SET);
            fread(nombreArchivo,sizeof(char),15,fp);
            fread(&bArchivo,sizeof(int),1,fp);
            fread(&cluster,sizeof(int),1,fp);
            if(strncmp(nA,nombreArchivo,determinarCaracteresImprimibles(nombreArchivo)) == 0)
            {
                printf("EXISTE\n");
                printf("COPIANDO A TU SISTEMA...\n");
                    
                fseek(fp,cluster * 2048,SEEK_SET);
                char buffer[bArchivo];
                fread(buffer,sizeof(char),bArchivo,fp);
                FILE *nf = fopen(nombreArchivo,"wb+");
                fwrite(buffer,sizeof(char),bArchivo,nf);
                fclose(nf);
                i = 1000;
                bandera = 1;
            }
            i += numThreads;
        }
        fclose(fp);
    }
    if(bandera == 0)
        printf("NO EXISTE ESE FICHERO\n");
}

void listarContenido(char nd[], int tipo_maquina)
{
    int numThreads = 3;
    omp_set_num_threads(numThreads);
    int i, j = 0, bArchivo, id;
    char nombreArchivo[16], fechaCreacion[15], fechaMoficacion[15];
    FILE *fp;
    printf("|  NOMBRE_ARCHIVO |   NUM_BYTES   |  FECHA DE CREACION   |   FECHA ULTIMA MODIFICACION\n");
    #pragma omp parallel private(fp,i,bArchivo,nombreArchivo, fechaCreacion, fechaMoficacion,id)
    {
        fp = fopen(nd,"r");
        
        nombreArchivo[15] = '\0';
        fechaCreacion[14] = '\0';
        fechaMoficacion[14] = '\0';
        id = omp_get_thread_num();
        i = id;
        while(i < 128)
        {
            fseek(fp,2048 + 64 * i + 1,SEEK_SET);
            fread(nombreArchivo,sizeof(char),15,fp);
            fread(&bArchivo,sizeof(int),1,fp);
            fseek(fp, 4,SEEK_CUR);
            fread(fechaCreacion, sizeof(char),14,fp);
            fread(fechaMoficacion, sizeof(char),14,fp);

            if(tipo_maquina == BIG_ENDIAN)
                bArchivo = littleEndian(bArchivo);

            if(strcmp("##############\0",nombreArchivo) != 0)
                printf("|  %s | %10i    |   %s     |    %s\n",nombreArchivo, bArchivo, fechaCreacion, fechaMoficacion);
            i += numThreads;
        }
        fclose(fp);
    }
     /*FILE *fp = fopen(nd,"r");
    moverACluster(1,fp);
    char nombreArchivo[16], fechaCreacion[15], fechaMoficacion[15];
    nombreArchivo[15] = '\0';
    fechaCreacion[14] = '\0';
    fechaMoficacion[14] = '\0';


    printf("  # |  NOMBRE_ARCHIVO |   NUM_BYTES   |  FECHA DE CREACION   |   FECHA ULTIMA MODIFICACION\n");
   
    for (i = 0; i < 128; i++)
    {
        fseek(fp, 1,SEEK_CUR);
        fread(nombreArchivo,sizeof(char),15,fp);
        fread(&bArchivo,sizeof(int),1,fp);
        fseek(fp, 4,SEEK_CUR);
        fread(fechaCreacion, sizeof(char),14,fp);
        fread(fechaMoficacion, sizeof(char),14,fp);
        
        if(tipo_maquina == BIG_ENDIAN)
            bArchivo = littleEndian(bArchivo);

        fseek(fp,12,SEEK_CUR);
        if(strcmp("##############\0",nombreArchivo) != 0)
        {
            j += 1;

            if( j < 10 )
                printf("00%i.|  %s | %10i    |   %s     |    %s\n", j,nombreArchivo, bArchivo, fechaCreacion, fechaMoficacion);
            
            else
            {  
                if( j >= 10 && j < 100 )
                    printf("0%i.|  %s | %10i    |   %s     |    %s\n", j,nombreArchivo, bArchivo, fechaCreacion, fechaMoficacion);
                
                else
                    printf("%i.|  %s | %10i    |   %s     |    %s\n", j,nombreArchivo, bArchivo, fechaCreacion, fechaMoficacion);
            }
        }

    }
    fclose(fp);*/
}

int existeArchivo(char *fn)
{
    if(access(fn,F_OK) == 0)
        return 1;
    
    else
        return 0;
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