package main

import (
	"math/rand"
	"fmt"
)

var (
	procesos map[string]int = make(map[string]int)
	memoria [30]string
	libres = 30
)


func main() {
	for i := range memoria {
		memoria[i] = "-"
	}

	letras := []string{"A", "B", "C", "D", "E", "F", "G", "H", "I", "J"}

	verMemoria()
	for _, v := range letras {
		tam := rand.Intn(14) + 2 // [2, 15]

		fmt.Printf("Se intenta crear al proceso %v de tamaño %v.\n", v, tam)

		if tam > libres {
			fmt.Println("No hay memoria suficiente :(")
			continue
		}
		crearProceso(v, tam)
		pos := posPrimerAjuste(tam)
		if pos == -1 {
			fmt.Println("No hay un bloque contiguo lo suficientemente grande, se hará compactación")
			compactacion()
			pos = posPrimerAjuste(tam)
		}

		llenarMemoria(v, pos)
		verMemoria()
		fmt.Println()

		if rand.Float64() > 0.5 {
			letra := pick()

			fmt.Printf("Ha terminado el proceso %v\n", letra)
			matarProceso(letra)
			verMemoria()
		}
	}

	fmt.Println("Memoria en su estado final: ")
	verMemoria()
}

func pick() string {
	n := rand.Intn(len(procesos))
	for key := range procesos {
		if n == 0 {
			return key
		}
		n--
	}
	return ""
}

func crearProceso(nombre string, tam int) {
	if procesos[nombre] == 0 {
		procesos[nombre] = tam
	}
}

func posPrimerAjuste(tam int) int {
	for i, v := range memoria {
		if v == "-" {
			libres := 1
			for j := i+1; j < len(memoria) && j < i + 1 + tam; j++ {
				if (memoria[j] == "-") {
					libres++
				}
			}
			if libres >= tam {
				return i
			}
		}
	}

	return -1
}

func llenarMemoria(nombre string, pos int) {
	tam := procesos[nombre]
	for i := pos; i < pos + tam; i++ {
		memoria[i] = nombre
		libres--
	}
}

func matarProceso(nombre string) {
	for i, v := range memoria {
		if v == nombre {
			memoria[i] = "-"
		}
	}
	libres += procesos[nombre]
	delete(procesos, nombre)
}

func compactacion() {
	distancia := 0
	moviendo := false
	contando := false
	movioAnterior := false
	for i, v := range memoria {
		if !moviendo && !contando && v == "-" {
			contando = true
			distancia = 1
		} else if contando && v == "-" {
			distancia ++
		} else if contando && v != "-" {
			memoria[i - distancia] = v
			memoria[i] = "-"
			movioAnterior = true
			contando = false
			moviendo = true
		} else if moviendo && movioAnterior && v == "-" {
			moviendo = false
			contando = true
			movioAnterior = false
			distancia++
		} else if moviendo && v != "-" {
			memoria[i - distancia] = v
			memoria[i] = "-"
			movioAnterior = true
		}
	}
}

func verMemoria() {
	for _, v := range memoria {
		fmt.Print(v)
	}
	fmt.Println()
}
