#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_MEM 1024 // Tamaño máximo de la memoria simulada

// Estructura para simular un bloque de memoria
typedef struct {
    int id; // Identificador del bloque
    int size; // Tamaño del bloque
    int start; // Dirección de inicio del bloque
    int end; // Dirección de fin del bloque
    char *data; // Datos del bloque
} MemoryBlock;

// Simulación de la memoria
MemoryBlock memory[MAX_MEM];

// Función para inicializar la memoria
void initializeMemory() {
    for (int i = 0; i < MAX_MEM; i++) {
        memory[i].id = -1; // -1 indica que la memoria está libre
        memory[i].size = 0;
        memory[i].start = -1;
        memory[i].end = -1;
        memory[i].data = NULL;
    }
}

// Función para asignar memoria
int allocateMemory(int size, const char *data) {
    int start = -1;
    for (int i = 0; i < MAX_MEM - size; i++) {
        int free = 1;
        for (int j = i; j < i + size; j++) {
            if (memory[j].id != -1) {
                free = 0;
                break;
            }
        }

        if (free) {
            start = i;
            break;
        }
    }

    if (start != -1) {
        int id = rand() % 1000; // Asignar un ID aleatorio al bloque
        for (int i = start; i < start + size; i++) {
            memory[i].id = id;
            memory[i].size = size;
            memory[i].start = start;
            memory[i].end = start + size - 1;
            memory[i].data = strdup(data); // Duplicar los datos para el bloque
        }
        return id;
    }

    return -1;
}

// Función para liberar memoria
void freeMemory(int id) {
    for (int i = 0; i < MAX_MEM; i++) {
        if (memory[i].id == id) {
            free(memory[i].data);
            memory[i].id = -1;
            memory[i].size = 0;
            memory[i].start = -1;
            memory[i].end = -1;
            memory[i].data = NULL;
        }
    }
}

// Función para mostrar la memoria
void displayMemory() {
    for (int i = 0; i < MAX_MEM; i++) {
        if (memory[i].id != -1) {
            printf("[%d]", memory[i].id);
        } else {
            printf("[ ]");
        }
    }
    printf("\n");
}

int main() {
    initializeMemory(); // Inicializar la memoria

    // Simular la asignación de memoria
    int block1 = allocateMemory(100, "Datos del bloque 1");
    if (block1 != -1) {
        printf("Bloque asignado con ID %d\n", block1);
    } else {
        printf("No se pudo asignar memoria para el bloque 1\n");
    }

    displayMemory(); // Mostrar la memoria

    // Simular la liberación de memoria
    freeMemory(block1);
    printf("Memoria liberada para el bloque con ID %d\n", block1);

    displayMemory(); // Mostrar la memoria

    return 0;
}
