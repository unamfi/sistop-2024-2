/*
 * File: misc.h
 * Incluye funciones para manejar bits y estructuras
 */

#ifndef FIUNAMFS_MISC
#define FIUNAMFS_MISC

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Indica de qué tamaño debe ser un array de bits para almacenarse
 * @param n el número de bits a almacenar
 * @return el tamaño en bytes requerido
 */
size_t fiunamfs_bools_tam(size_t n);

/*
 * Establece un bit a un valor
 * @param a Array de bits
 * @param p Posición de bit a editar
 * @param v valor a establecer
 */
void fiunamfs_bools_set(char* a, size_t p, bool v);

/*
 * Devuelve el valor de un bit
 * @param a Array de bits
 * @param p Posición del bit a devolver
 * @return valor del bit
 */
bool fiunamfs_bools_get(char* a, size_t p);

/*
 * Lee un buffer little-endian y extrae un entero sin signo de 32 bits
 * @param a Buffer de caracteres
 * @return el valor
 */
uint32_t fiunamfs_int32(char* a);

/*
 * Lee un entero sin signo de 32 bits, y escribe en un buffer su representación little-endian
 * @param val Entero sin signo de 32 bits
 * @param buf Buffer al cual escribir
 */
void fiunamfs_int32_dump(uint32_t val, unsigned char* buf);

#endif
