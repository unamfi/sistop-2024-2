#include <stdio.h>
#include <stdlib.h>
#include <time.h>


unsigned int strl(char* str);
void copy(char* destiny, char* origin, unsigned int size);
void newFile(char* destiny, unsigned int startpoint);


int main(int argc,char **argv)
{
    unsigned int size = strl(argv[0]);
    unsigned int i = size - 1;
    while (*(argv[0] + i) != '\\')
    {
        --i;
    }
    char *p;
    p = malloc( (i + 12) * sizeof(char));
    copy(p,argv[0],i);
    newFile(p,i);
    
    FILE *ff;
    ff  = fopen(p,"w+t");
    if ( ff == NULL)
    {
        printf("Error al abrir archivo nuevo!\n");
        exit(-1);
    }


    time_t t;
    time(&t);

    fprintf(ff, "Practica 4, Zurita Cámara Juan Pablo\n%s\n",ctime(&t));

    fclose(ff);
    free(p);

}


unsigned  strl(char* str)
{
    int i = 0;
    while(*(str++) != '\0')
    {
        ++i;
    }
    return i;
}


void copy(char* destiny, char* origin, unsigned int size)
{
    for(int i = 0; i <= size; i++)
    {
        destiny[i] = origin[i];
    }
}

void newFile(char* destiny, unsigned int startpoint)
{
    char origin[] = "newFile.txt";
    for(int i = 0; i <= 10; i++)
    {
        destiny[++startpoint] = origin[i];
    }
    destiny[++startpoint] = '\0';
}