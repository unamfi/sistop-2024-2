#include <stdio.h>
#include <string.h>

struct Libro {
    char autor[100];
    char titulo[100];
    int anio;
};

int main() {
    int i, j, n = 3;
    struct Libro libros[n], temp;

    for (i = 0; i < n; i++) {
        printf("Ingrese los detalles del libro #%d:\n", i + 1);
        printf("Titulo: ");
        scanf(" %[^\n]s", libros[i].titulo);
        printf("Autor: ");
        scanf(" %[^\n]s", libros[i].autor);
        printf("Anio: ");
        scanf("%d", &libros[i].anio);
    }

    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - i - 1; j++) {
            if (strcmp(libros[j].titulo, libros[j + 1].titulo) > 0) {
                temp = libros[j];
                libros[j] = libros[j + 1];
                libros[j + 1] = temp;
            }
        }
    }

    printf("\nLibros ordenados por titulo:\n");
    for (i = 0; i < n; i++) {
        printf("Libro #%d\n", i + 1);
        printf("Titulo: %s\n", libros[i].titulo);
        printf("Autor: %s\n", libros[i].autor);
        printf("Anio: %d\n", libros[i].anio);
        printf("\n");
    }

    return 0;
}
