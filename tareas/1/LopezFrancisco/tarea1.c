/* 
	Código que realiza el ejemplo de administración de memoria a través de segmentación.
    No se incluye manejo de excepciones. Por favor introducir el tipo de dato correcto en cada solicitud durante la ejecución.
*/

#include <stdio.h>
#include <stdlib.h>

void inicializarArreglo(char *memoria);
void imprimirArreglo(char memoria[30]);
void liberarProceso(char *memoria, char ent);
void asignarProceso(char *memoria, int tam, char process);
int conteoParticular(char *memoria,int required);
int conteoGeneral(char *memoria);
int validacion(int contador,int required);
void compactar(char *memoria);


int main(){
    char memoria[30];
    int sel=0;
    char ent;
    int tam=0;
    int valid=0;
    int fit=0;
    inicializarArreglo(memoria);
    imprimirArreglo(memoria);
    printf("Aisgnar (0)\tLiberar (1)\t Salir (2)\n");
    printf("¿Qué operación desea realizar?:\t");
    fflush(stdin);
    scanf("%d",&sel); //Se solicita al usuario la operación que desea realizar.
    while(sel==1||sel==0){
		switch (sel){
			case 0: //Asignación de un proceso.
                printf("Tamaño del proceso: ");
                fflush(stdin);
                scanf("%d",&tam);                   //Se solicita el tamaño del proceso que desea aisngar.
                valid = conteoGeneral(memoria);     //Se realiza el conteo del espacio libre total.
                fit=validacion(valid,tam);          //Se verifica que la totalidad del espacio libre sea suficiente.
                if (fit==1){                        //El espacio libre total es suficiente.
                    printf("Nombre del proceso a agregar (1 letra mayúscula): ");
                    fflush(stdin);
                    scanf(" %c",&ent);                          //Se solicita el nombre del proceso que desea aisngar.
                    valid = conteoParticular(memoria,tam);      //Se busca el tamaño del espacio libre contiguo disponible para aisgnar el proceso.
                    fit=validacion(valid,tam);                  //Se valida que exista dicho espacio libre contiguo.
                    if (fit==1){                    //Se encontró un espacio libre contiguo disponible.
                        asignarProceso(memoria,tam,ent);        //Se asigna el proceso en el primer espacio disponible.
                        imprimirArreglo(memoria);
                    }
                    else {                          //No se encontró un espacio libre contiguo disponible.
                        printf("Se necesita compactación.\n");
                        compactar(memoria);                     //Se realiza el proceso de compactación en toda la memoria.
                        asignarProceso(memoria,tam,ent);        //Se asigna el proceso en el primer espacio disponible.
                        imprimirArreglo(memoria);
                        break;
                    }
                }
                else {                              //El espacio libre total no es suficiente.
                    printf("Error: no existe suficiente espacio total.\n");
                    imprimirArreglo(memoria);
                    break;
                }
			break;
			
			case 1:
                printf("Proceso a liberar: ");
                fflush(stdin);
                scanf(" %c",&ent);              //Se solicita el nombre del proceso que el usuario desea liberar.

				liberarProceso(memoria,ent);    //Se libera el espacio que ocupa el proceso solicitado.
                imprimirArreglo(memoria);
			break;
		}
		printf("Aisgnar (0)\tLiberar (1)\t Salir (2)\n");
        printf("¿Qué operación desea realizar?:\t");
        fflush(stdin);
        scanf("%d",&sel);
	}
    return 0;
}

/*Función que coloca el símbolo que representa al espacio libre.*/
void inicializarArreglo(char *memoria){
    char nulo;
    nulo = '-';
    int i=0;
    for (i=0;i<30;i++){
        memoria[i]=nulo;
    }
}

/*Función que imprime al arreglo que representa a la memoria disponible en este ejercicio.*/
void imprimirArreglo(char memoria[30]){
    printf("\n");
    int i=0;
    printf("Asignación actual:\n");
    for (i=0;i<30;i++){
        printf("%c",memoria[i]);
    }
    printf("\n");
}

/*Función que libera el proceso solicitado por el usuario.*/
void liberarProceso(char *memoria, char ent){
    int i=0;
    for (i=0;i<30;i++){
        if(memoria[i]==ent){
            while(memoria[i]==ent && i<30){
                memoria[i]='-';
                i++;
            }
            break;
        }
    }
    printf("\n");
}

/*Función que verifica que el espacio libre y contiguo entre procesos sea suficiente para la asignación.*/
int conteoParticular(char *memoria,int required){
    char nulo;
    nulo = '-';
    int i=0;
    int contador=0;
    for (i=0;i<30;i++){
        if(memoria[i]==nulo){
            while(memoria[i]==nulo && i<30){
                contador++;
                i++;
            }
            if(contador>=required)          //Si se encuentra el espacio disponible continuo, se retorna su tamaño.
                return contador;
            else
                contador=0;      
        }
    }
    return contador;
}

/*Función que verifica que el espacio total libre (aunque esté separado) sea suficiente para el tamaño solicitado.*/
int conteoGeneral(char *memoria){
    char nulo;
    nulo = '-';
    int i=0;
    int contador=0;
    for (i=0;i<30;i++){
        if (memoria[i] == nulo)
        contador++;
    }
    return contador;
}

/*Función que retorna un booleano para validar si el espacio disponible es suficiente para asignar el espacio requerido.*/
int validacion(int contador,int required){
    if (required<=contador){
        return 1;
    }
    else{
        return 0;
    }
}

/*Función que asigna el proceso solicitado en el primer espacio disponible.
Por esta razón se emplea el concepto teórico del PRIMER AJUSTE.*/
void asignarProceso(char *memoria, int tam, char process){
    char nulo;
    nulo = '-';
    int i=1;
    int tamDisp=0;              //Auxiliar que representa al tamaño disponible.
    int fit=0;                  //Bandera que informa si el espacio disponible es suficiente.
    int base=0;                 //Auxiliar que almacena la posición inicial de un conjunto de espacios libres.
    int done=0;                 //Bandera que indicará que el proceso ya se ha asignado.
    for (i=0;i<30;i++){
        tamDisp=0;
        if(memoria[i]==nulo){
            base=i;
            while(memoria[i]==nulo && i<30){
                tamDisp++;
                i++;
            }
            fit = validacion(tamDisp,tam);
            if (fit==1){
                int aux=0;
                for(aux=base;aux<(base+tam);aux++){
                    memoria[aux]=process;
                }
                done=1; 
            }
            else{
                tamDisp=0;              //En caso de que el espacio libre no sea suficiente para asignar el proceso, se reinicia este auxiliar.
            }
        }
        if (done==1)
            break;
    }
}

/*Función que realiza el proceso de compactación cuando es requerido
La complejidad del algoritmo es muy alta, por lo que se observa las dificultades
que presenta la segmentación.*/
void compactar(char *memoria){
    char nulo;
    nulo = '-';                 // Caracter que representa al segmento vacío
    int i=0;
    char aux;
    int k=0;
    int j=0;
    for (j=0;j<30;j++){
        for (i=0;i<30;i++){
            if (memoria[i]==nulo){              //Cuando se encuentra un segmento libre se inicia el ciclo interno.
                k=i;
                for(k=i;k<29;k++){
                    memoria[k]=memoria[k+1];    //Se recorre a la izquierda el valor próximo al nulo encontrado.
                    memoria[k+1]=nulo;          //Se recorre el segmento vacío hacia la derecha.
                }
            }
        }
    }
}