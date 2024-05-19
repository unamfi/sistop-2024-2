#include <stdio.h>
#include <omp.h>//para multihilo
#include <unistd.h>//para verificar existencia de ficheros
#include <dirent.h>//para leer directorio
#include <time.h>//para obtener la hora
#include <string.h>//para comparar cadenas
#include <math.h>
#define LITTLE_ENDIAN 0
#define BIG_ENDIAN    1
#define TERMINAR_PROGRAMA 't'
int tipo_maquina;
char seleccion = 'a';
int littleEndian(int);
int endian();
void PmensajeInicial();
void listarContenido(char *nd, int tipo_maquina);
void mostrarDirectorioExterno();
void printHora(char *h);
int escribirEnDirectorio(char nd[], int tipo_maquina, char nA[], int bytes,int clusterInicial);

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
    FILE * arch = fopen(nA,"rb");
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
    FILE *f = fopen(nd,"rb");
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
    int i, bArchivo, id, cluster;
    char nombreArchivo[16];
    FILE *fp;
    #pragma omp parallel private(fp,i,bArchivo,nombreArchivo, id, cluster)
    {
        fp = fopen(nd,"rb");
        
        nombreArchivo[15] = '\0';
        id = omp_get_thread_num();
        i = id;
        while(i < 128)
        {
            fseek(fp,2048 + 64 * i + 1,SEEK_SET);
            fread(nombreArchivo,sizeof(char),15,fp);
            fread(&bArchivo,sizeof(int),1,fp);
            fread(&cluster,sizeof(int),1,fp);

            if(tipo_maquina == BIG_ENDIAN)
            {
                bArchivo = littleEndian(bArchivo);
                cluster = littleEndian(cluster);
            }
                
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

void copiaDePCaFI(char nd[], int tipo_maquina)
{
    mostrarDirectorioExterno();
    int i = 0,j = 0,k = 0,bArchivo, bytes,cluster,uc, memoria,e,bandera1 = 0 ,bandera2;
    char nombreArchivo[16],nA[16];
    printf("QUE ARCHIVO QUIERE PASAR A FIUNAMFS?\n");
    scanf(" %s",nA);
    if(access(nA,F_OK) != 0)
    {
        printf("NO EXISTE ESE FICHERO\n");
        return;
    }
    FILE *f = fopen(nA,"rb");
    fseek(f,0,SEEK_END);
    bArchivo = ftell(f);
    bytes = bArchivo;
    fclose(f);
    memoria = bArchivo / 2048;
    FILE *fp = fopen(nd,"rb");
    nombreArchivo[15] = '\0';
    nA[15] = '\0';

    int intervalos[128][2],libres[128][2];

    while(i < 128)
    {
        fseek(fp,2048 + 64 * i + 1,SEEK_SET);
        fread(nombreArchivo,sizeof(char),15,fp);
        fread(&bArchivo,sizeof(int),1,fp);
        fread(&cluster,sizeof(int),1,fp);

        if(tipo_maquina == BIG_ENDIAN)
        {
            bArchivo = littleEndian(bArchivo);
            cluster = littleEndian(cluster);
        }
        if(bArchivo > 0)
        {
            printf("%i \n",bArchivo);
            uc = cluster + (bArchivo / 2048);
            intervalos[j][0] = cluster;
            intervalos[j][1] = uc;   
            j += 1;
        }
        i += 1;
    }
    fclose(fp);

    if(j > 0)
    {
        i = 5;
        j = 0;
        libres[k][0] = i;
        while(i < 720)
        {
            if(i == intervalos[j][0])
            {
                if( ( i - 1) - libres[k][0] < 0)
                {
                    i = intervalos[j][1] + 1;
                    libres[k][0] = i;
                }

                else
                {
                    libres[k][1] = i - 1;
                    if(intervalos[j][1] + 1 < 720)
                    {  
                        k += 1;
                        i = intervalos[j][1] + 1;
                    }
                }
                j++;
            }

            else
            {
                i++;
                if(i == 720)
                    libres[k][1] = i - 1;
            }
                
        } 
        for (i = 0; i <= k; i++)
        {
            e = libres[i][1] - libres[i][0];
            if(e >= memoria)
            {
                bandera1 = 1;
                break;
            }
            
        }
    }
    
    if(bandera1 != 1)
    {
        printf("NO ES POSIBLE GUARDAR EN FIUNAMFS\n");
        return;
    }
    printf("%i \n",bytes);
    if(escribirEnDirectorio(nd,tipo_maquina,nA, bytes, libres[i][0]) == 1)
    {
        char buffer[bytes];
        FILE *f = fopen(nA,"rb");
        fread(buffer,sizeof(char),bytes,f);
        fclose(f);
        fp = fopen(nd,"rb+");
        fseek(fp,2048 * libres[i][0],SEEK_SET);
        fwrite(buffer,sizeof(char),bytes,fp);
        fclose(fp);
        return;
    }
    
    printf("NO ES POSIBLE GUARDAR EN FIUNAMFS\n");
}
int escribirEnDirectorio(char nd[], int tipo_maquina, char nA[], int bytes,int clusterInicial)
{
    int i = 0;
    FILE *fp = fopen(nd,"rb+");
    char libre = 0;
    nA[15] = '\0';
    char fechaCreacion[15];
    char fechaMoficacion[15];
    printHora(fechaCreacion);
    printHora(fechaMoficacion);

    while(i < 128 && libre != '/')
    {
        fseek(fp,2048 + 64 * i,SEEK_SET);
        fread(&libre,sizeof(char),1,fp);
        i += 1;
    }

    if(i == 128)
        return 0;

    fseek(fp,2048 + 64 * (i - 1),SEEK_SET);
    libre = '-';
    fwrite(&libre,sizeof(char),1,fp);
    fwrite(nA,sizeof(char),15,fp);

    if(tipo_maquina == BIG_ENDIAN)
    {
        bytes = littleEndian(bytes);
        clusterInicial = littleEndian(clusterInicial);
    }

    fwrite(&bytes,sizeof(int),1,fp);
    fwrite(&clusterInicial,sizeof(int),1,fp);
    fwrite(fechaCreacion, sizeof(char),14,fp);
    fwrite(fechaMoficacion, sizeof(char),14,fp);
    fclose(fp);
    return 1;
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
        fp = fopen(nd,"rb");
        
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
    printf("        NOMBRE  |    NUM_BYTES\n");
    while ((archivo = readdir(dir)) != 0) 
    {
        if(*(archivo->d_name) != '.')
        {
            char name[16];
            name[15] = 0;
            strcpy(name, archivo->d_name);
            FILE *f = fopen(archivo->d_name, "rb");
            fseek(f,0,SEEK_END);

            printf("%15s | %10i\n", name, ftell(f));
            fclose(f);
        }
       
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