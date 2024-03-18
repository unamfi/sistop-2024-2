#include <stdio.h>
#include <stdlib.h>

#define MEM_SIZE 30

typedef struct {
    char id;
    int size;
} MemoryBlock;

void printMemoryMap(MemoryBlock memory[], char *adjustment) {
    printf("Asignacion actual (Metodo de ajuste: %s):\n", adjustment);
    for (int i = 0; i < MEM_SIZE; i++) {
        if (memory[i].id == '\0') {
            printf("-");
        } else {
            for (int j = 0; j < memory[i].size; j++) {
                printf("%c", memory[i].id);
            }
            i += memory[i].size - 1;
        }
    }
    printf("\n");
}

int main() {
    MemoryBlock memory[MEM_SIZE] = {0};
    char *adjustment_method = "Primer ajuste";

    while (1) {
        printMemoryMap(memory, adjustment_method);

        printf("Asignar (0) o liberar (1): ");
        int action;
        scanf("%d", &action);

        if (action == 0) {
            printf("Nuevo proceso (A-Z): ");
            char id;
            int size;
            scanf(" %c", &id);
            printf("Tamano del proceso (%d-%d): ", 2, 15);
            scanf("%d", &size);

            int start = -1;
            for (int i = 0; i < MEM_SIZE; i++) {
                int count = 0;
                while (i < MEM_SIZE && memory[i].id == '\0') {
                    count++;
                    i++;
                }
                if (count >= size) {
                    start = i - count;
                    break;
                }
            }

            if (start != -1) {
                for (int i = start; i < start + size; i++) {
                    memory[i].id = id;
                    memory[i].size = size;
                }
                printf("Nueva asignacion:\n");
            } else {
                printf("No hay espacio suficiente para asignar el proceso.\n");
            }
        } else if (action == 1) {
            printf("Proceso a liberar (A-Z): ");
            char id;
            scanf(" %c", &id);

            for (int i = 0; i < MEM_SIZE; i++) {
                if (memory[i].id == id) {
                    memory[i].id = '\0';
                    memory[i].size = 0;
                }
            }

            printf("Asignacion actual:\n");
        } else {
            printf("Opcion no valida. Por favor, introduce 0 para asignar o 1 para liberar.\n");
        }

        while (getchar() != '\n');
    }

    return 0;
}
