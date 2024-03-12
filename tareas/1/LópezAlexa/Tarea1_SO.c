//López Tavera Alexa Fernanda_Tarea 1 de Sistemas operativos
//Programa que simula la administración de memoria donde los # representan los espacios vacios (30 unidades) y se puede asignar o liberar la memoria
//Se resuelven las solicitudes por primer ajuste
#include <stdio.h>
#include <stdlib.h>

#define TAM_MEM 30//Constante que representa el tamaño total de la memoria(30 unidades)

// Estructura que se declara para representar un bloque de memoria
struct BloqueMemoria {
    char id;  // Caracter que representa el dentificador del proceso que se encuentra en el bloque de memoria
    int tam; // Tamaño del bloque de memoria
};

// Arreglo que representa la memoria
struct BloqueMemoria memoria[TAM_MEM]; 
int total_bloques = 0; // Contador de bloques de memoria que ya han sido asignados

//Función para inicializar la memoria con bloques vacíos
void inicializarMemoria() {
    int i = 0;
    while (i < TAM_MEM) {
        memoria[i] = (struct BloqueMemoria){'#', 1};
        i++;
    }
}

//Función que imprime el mapa de memoria
void imprimirMapaMemoria() {
    int i = 0;
    while (i < TAM_MEM) { //Inicia un ciclo que imprime los elementos en el bloque de memoria
        printf("%c", memoria[i].id);
        i++;
    }
    printf("\n");
}

// Función que ayuda a asignar memoria a un proceso
void asignarMemoria(char proceso, int unidades) {//Recibe la letra del proceso y el tamaño del proceso que se asigna a memoria
    printf("Asignando %d unidades para el proceso %c:\n", unidades, proceso);

    int i, j;
    for (i = 0; i < TAM_MEM - unidades + 1; i++) {
        int coincide = 1;
        // Verifica si hay suficientes unidades consecutivas disponibles para asignar al proceso
        for (j = 0; j < unidades; j++) {
            if (memoria[i + j].id != '#') {
                coincide = 0;
                break;
            }
        }
        // Si se encuentran unidades consecutivas disponibles, se asignan al proceso
        if (coincide) {
            for (j = 0; j < unidades; j++) {
                memoria[total_bloques + j].id = proceso;
                memoria[total_bloques + j].tam = 1;
            }
            total_bloques += unidades; // Se actualiza el contador de bloques ocupados
            imprimirMapaMemoria();//Imprime el mapa de memoria una vez que se asigno el proceso correctamente
            return;
        }
    }

    printf("No hay suficiente espacio para asignar %d unidades al proceso %c.\n", unidades, proceso);//Si no hay espacio consecutivo suficiente se imprime el mensaje
}

// Función para liberar memoria de un proceso
void liberarMemoria(char proceso) {//Recibe la letra que se quiere "liberar" de la memoria
    printf("Liberando memoria del proceso %c:\n", proceso);

    int i, j;
    for (i = 0; i < total_bloques; i++) {
        if (memoria[i].id == proceso) {
            // Cuenta la cantidad de bloques adyacentes ocupados por el proceso
            int bloques_ocupados = 0;
            for (j = i; j < total_bloques && memoria[j].id == proceso; j++) {
                bloques_ocupados++;
            }
            //Marca los bloques adyacentes ocupados como libres
            for (j = i; j < i + bloques_ocupados; j++) {
                memoria[j].id = '#';
                memoria[j].tam = 1;
            }
            // Actualiza el total de bloques y limpiar el resto de la memoria
            total_bloques -= bloques_ocupados;
            for (j = total_bloques; j < TAM_MEM; j++) {
                memoria[j].id = '#';
                memoria[j].tam = 1;
            }
            imprimirMapaMemoria();//Imprime el mapa sin el proceso 
            return;
        }
    }

    printf("El proceso %c no esta en memoria.\n", proceso);
}

int main() {
    inicializarMemoria();  // Inicializa la memoria con bloques vacíos
    int continuar_liberando = 1; // Variable que controla si se debe continuar liberando memoria
	int continuar_asignando = 1; // Variable que controla si se debe continuar asignando memoria


    printf("Mapa de memoria inicial (30 Unidades):\n");
    imprimirMapaMemoria();  // Imprime el mapa de memoria inicial con las 30 'O' que representan los espacios vacios

    // Lo primero que se puede hacer en nuestro programa es asignar memoria
    printf("1r.Proceso_Asignar memoria:\n");
    char proceso;
    int unidades;
    do {
        printf("Nombre del nuevo proceso (da una letra mayuscula de preferencia): ");
        scanf(" %c", &proceso);

        printf("Escoja las unidades que quiere asignar al ese proceso (entre 2 y 15 unidades posibles): ");
        scanf("%d", &unidades);

        if (unidades < 2 || unidades > 15) {//Se verifica que no se salga del rango permitido la cantidad de unidades a asignar del proceso
            printf("El numero de unidades no es valido. Por favor, ingrese un valor entre 2 y 15.\n");
            continue;
        }

        asignarMemoria(proceso, unidades);//Se llama a la función asignar memoria

        printf("Desea asignar memoria a otro proceso? (1: Si / 0: No): ");
        scanf("%d", &continuar_asignando);
    } while (continuar_asignando);//Mientras se quiera asignar y se pueda asignar se repite esta parte del código

    // Si ya no se quiere o puede asignar, continua la opción de liberar la memoria
    printf("2do.Proceso_Liberar memoria:\n");
    do {
        printf("Proceso a liberar: (Ingrese la letra que se quiere liberar)");
        scanf(" %c", &proceso);//Se pide la letra a liberar al usuario

        liberarMemoria(proceso);//Se llama a la función liberar memoria

        printf("Desea liberar memoria de otro proceso? (1: Si/ 0: No): ");
        scanf("%d", &continuar_liberando);
    } while (continuar_liberando);//Mientras se quiera y pueda seguir liberando continua la función, si no, termina el programa

    return 0;
}

