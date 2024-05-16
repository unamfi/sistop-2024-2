package main

import (
	"bufio"
	"encoding/binary"
	"errors"
	"fmt"
	"io"
	"log"
	"os"
	"strings"
)

type FileSystem struct {
	nombre, version, etiqueta            string
	tamCluster, tamDirectorio, tamUnidad uint32
	file                                 *os.File
}

type archivo struct {
	nombre, creado, modificado string
	tam, cluster, offset       uint32
}

var miFS FileSystem = FileSystem{}
var archivos []archivo = make([]archivo, 0)

func main() {
	var err error
	miFS.file, err = os.Open("fiunamfs.img")

	if err != nil {
		log.Fatal("No pude abrir el archivo: ", err)
	}
	defer miFS.file.Close()

	r := bufio.NewReader(miFS.file)

	superBloque := make([]byte, 55)
	_, err = r.Read(superBloque)
	genErrCheck(err)
	leerSuperBloque(superBloque)

	_, err = miFS.file.Seek(int64(miFS.tamCluster), 0)
	genErrCheck(err)

	dirEntry := make([]byte, 64)
	for {
		offset, err := miFS.file.Seek(0, io.SeekCurrent)
		genErrCheck(err)
		if offset >= int64(miFS.tamCluster*(miFS.tamDirectorio+1)) {
			break
		}

		_, err = miFS.file.Read(dirEntry)
		genErrCheck(err)
		arch, err := leerEntradaDirectorio(dirEntry, uint32(offset))
		if err == nil {
			archivos = append(archivos, arch)
		}
	}

	fmt.Println("Nombre \t\tTamaño")
	for _, papu := range archivos {
		fmt.Printf("- %s: \t%7d bytes\n", papu.nombre, papu.tam)
		err = copiarArchivo(papu)
		if err != nil {
			fmt.Println(err)
		}
	}

}

func leerSuperBloque(bloque []byte) {
	miFS.nombre = string(bloque[:10])
	miFS.version = string(bloque[10:20])
	miFS.etiqueta = string(bloque[20:40])
	miFS.tamCluster = binary.LittleEndian.Uint32(bloque[40:45])
	miFS.tamDirectorio = binary.LittleEndian.Uint32(bloque[45:50])
	miFS.tamUnidad = binary.LittleEndian.Uint32(bloque[50:55])

	fmt.Println(miFS)
}

func leerEntradaDirectorio(buf []byte, offset uint32) (archivo, error) {
	arch := archivo{}

	if buf[0] != '-' {
		return arch, errors.New("Entrada vacía")
	}

	arch.nombre = strings.TrimSpace(string(buf[1:15]))
	arch.tam = binary.LittleEndian.Uint32(buf[16:20])
	arch.cluster = binary.LittleEndian.Uint32(buf[20:24])
	arch.creado = strings.TrimSpace(string(buf[24:37]))
	arch.modificado = strings.TrimSpace(string(buf[38:52]))
	arch.offset = offset

	return arch, nil
}

func copiarArchivo(arch archivo) (err error) {
	_, err = miFS.file.Seek(int64(miFS.tamCluster*arch.cluster), 0)
	if err != nil {
		return err
	}

	dst, err := os.Create(arch.nombre)
	if err != nil {
		fmt.Println(arch.nombre)
		return err
	}

	defer func() {
		err = dst.Close()
	}()

	_, err = io.CopyN(dst, miFS.file, int64(arch.tam))

	return
}

func genErrCheck(err error) {
	if err != nil {
		panic(err)
	}
}
