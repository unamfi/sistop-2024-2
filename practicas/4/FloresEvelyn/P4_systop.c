#include <stdio.h>
#include <stdlib.h>

#define MAX 8
int cont =0;

enum booleano{false, true };

struct node {
    int num;
    struct node *nxt; //apuntador tipo nodo
};

struct node *tope = NULL;
//PUSH
enum booleano push (struct node **tope){
    printf ("\tPUSH\n");
    if (cont < MAX)
    {
            struct node *tmp= (struct node*)malloc (sizeof (struct node));
            tmp->num=cont;
            tmp->nxt = *tope; 
            *tope = tmp;
            cont +=1;
            return true;
    }
    else {
    printf ("\tNo hay mas que apilar\n");    
        return false;
    }
}
//POP
struct node *pop(struct node **tope){
    printf ("\tPOP\n");
    if (*tope == NULL)
    {
        printf ("NO HAY NADA\n");
        return NULL;
    }
    else
    {
        struct node *tmp= *tope;
        *tope = tmp -> nxt ;// tmp o tpe puede usar
        tmp ->nxt = NULL;
        cont--; //-- decrementa de uno en uno 
        return tmp;
    }
}
//MOSTRAR
void show(struct node *tope)
{
    struct node*tmp= tope;
    printf ("\n\tSHOW STACK\n\n");
    int i;
    
        while(tmp != NULL)
        {
            printf ("%d: %p\n",tmp->num,tmp);
            tmp = tmp ->nxt;
        }
}
//MENU
void menu (){
    struct node *tope = NULL;
    int op;

    while (1){
        show(tope);

        printf ("\nQue deseas hacer?\n");
        printf ("1) Push\n");
        printf ("2) Pop\n");
        printf ("3) Salir\n");
        scanf ("%d", &op);
        switch (op)
        {
        case 1:
            push (&tope);
            break;
        case 2:
            pop (&tope);
            break;
        case 3:
            return;
        default:
            printf ("Opcion Invalida");
        }
    }
}
int main(){
    menu ();
    return 0;
} 