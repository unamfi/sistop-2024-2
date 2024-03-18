#include <stdio.h>
#include <string.h>
#include <ctype.h>
//Resolviendo por primer ajuste
char memoria[30];
char procesos[30];
char anterior;
int i,j,t;

void imprimirmemoria() {
    memset(procesos, 0, sizeof(procesos));
    anterior = 0;
    for ( i = 0; i < 30; i++) {
        if (anterior != memoria[i] && memoria[i] != '-') {
            strncat(procesos, &memoria[i], 1);
            strncat(procesos, " ", 1);
            anterior = memoria[i];
        }
        printf("%c", memoria[i]);
    }
}

int hayProcesos() {
    for (i = 0; i < 30; i++) {
        if (memoria[i] != '-') {
            return 1;
        }
    }
    return 0;
}

void primerEspacio(int unidades, char proceso) {
    int espacio = 0;
    int flag = 0;
    int espacioTotal = 0;
    int maximoEspacio = 0;

    for ( i = 0; i < 30; i++) {
        if (memoria[i] == '-') {
            espacio++;
            espacioTotal++;
        }

        if (espacio >= unidades) {
            for ( j = i - espacio + 1; j < i - espacio + unidades + 1; j++) {
                memoria[j] = proceso;
            }
            flag = 1;
            break;
        }

        if (memoria[i] != '-' || i == 29) {
            if (maximoEspacio < espacio) {
                maximoEspacio = espacio;
            }
            espacio = 0;
        }
    }

    if (espacioTotal < unidades) {
        printf("No hay espacio suficiente para agregar el proceso solicitado\n");
    } else if (flag == 0) {
        printf("\nSe necesitan %d unidades, solo se tienen %d unidades consecutivas\n", unidades, maximoEspacio);
        printf("Es necesaria compactacion \n");
        int t = 0;
        for ( i = 0; i < 30; i++) {
            if (memoria[i] != '-') {
                memoria[t++] = memoria[i];
            }
        }
        for (; t < 30; t++) {
            memoria[t] = '-';
        }
        printf("\nMemoria nueva:\n");
        imprimirmemoria();
        printf("\nAgregando el proceso: %c\n", proceso);
        for ( t = 30 - espacioTotal; t < 30 - espacioTotal + unidades; t++) {
            memoria[t] = proceso;
        }
    }
}

int main() {
    printf("Simulacion de asignacion de memoria\n");
    for(i=0;i<30;i++){
		memoria[i]='-';
	}
	char continuar = 'S';
    while (continuar != 'N') {
        printf("Memoria actual:\n");
        imprimirmemoria();
        printf("\nAsignar (0), Liberar (1), Salir(2): \n");
        char accion;
        scanf(" %c", &accion);

        if (accion == '1') {
    if (hayProcesos()) {
        imprimirmemoria();
        printf("\nIndique el proceso que desea liberar : %s\n", procesos);
        char proceso;
        do {
            scanf(" %c", &proceso);
            if (!isupper(proceso)) {
                printf("El proceso debe ser un caracter en mayusculas (A - Z)\n");
            } else {
                int procesoExiste = 0;
                for ( i = 0; i < 30; i++) {
                    if (memoria[i] == proceso) {
                        procesoExiste = 1;
                        break;
                    }
                }
                if (!procesoExiste) {
                    printf("El proceso %c no existe. Intente nuevamente.", proceso);
                    char continuar;
                }
            }
        } while (!isupper(proceso));
        for ( i = 0; i < 30; i++) {
            if (memoria[i] == proceso) {
                memoria[i] = '-';
            }
        }
    } else {
        printf("No hay procesos para liberar.\n");
    }
        } else if (accion == '0') {
            printf("Ingrese el nuevo proceso desee asignar, este debe ser un caracter en mayusculas (A-Z): \n");
            char newProceso;
            do {
                scanf(" %c", &newProceso);
                if (!isupper(newProceso)) {
                    printf("Proceso invalido, el proceso debe ser un caracter en mayusculas (A-Z), intente nuevamente: \n");
                }
            } while (!isupper(newProceso));
            printf("Indique cuantas unidades necesita el nuevo proceso:\n");
            int unidades;
            do {
                scanf("%d", &unidades);
                if (!(unidades > 1 && unidades <= 15)) {
                    printf("Valor invalido, las unidades deben tener un valor entre 2 y 15, intente nuevamente: \n");
                    }
            } while (!(unidades > 1 && unidades <= 15));
            primerEspacio(unidades, newProceso);
            
        } else if (accion == '2'){
            return 0;
        }
            else {
            printf("Accion no reconocida. Por favor, ingrese 0 para asignar, 1 para liberar o 2 para salir del programa.\n");
            char continuar;
        }

        printf("Quieres continuar: (S), (N)\n");
        scanf(" %c", &continuar);
    }

    return 0;
}
