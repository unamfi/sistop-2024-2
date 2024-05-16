package main

import (
	"encoding/binary"
	"errors"
	"flag"
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

type Archivo struct {
	nombre, creado, modificado string
	tam, cluster, offset       uint32
}

var miFS FileSystem = FileSystem{}
var archivos map[string]Archivo = make(map[string]Archivo)

func main() {
	exportCmd := flag.NewFlagSet("export", flag.ExitOnError)
	importCmd := flag.NewFlagSet("import", flag.ExitOnError)

	list := flag.Bool("l", false, "Listar archivos en el sistema FiUnamFS.")
	info := flag.Bool("i", false, "Mostrar información del sistema de archivos")
	remove := flag.String("d", "", "Eliminar un archivo.")
	path := flag.String("f", "", "Ruta del archivo de la imagen FiUnamFS.")
	var input, output *string

	usage()

	if len(os.Args) < 2 {
		flag.Usage()
		os.Exit(1)
	}

	switch os.Args[1] {
	case "export":
		output = exportCmd.String("o", "", "Nombre de archivo de destino.")
		input = exportCmd.String("i", "", "Archivo de origen.")
		path = exportCmd.String("f", "", "Ruta del archivo de la imagen FiUnamFS.")
		exportCmd.Parse(os.Args[2:])
		fmt.Println(*input, *output)
	case "import":
		output = importCmd.String("o", "", "Archivo de destino.")
		input = importCmd.String("i", "", "Nombre de archivo de origen.")
		path = importCmd.String("f", "", "Ruta del archivo de la imagen FiUnamFS.")
		importCmd.Parse(os.Args[2:])
		fmt.Println(*input, *output)
	default:
		flag.Parse()
	}

	var err error
	miFS.file, err = os.Open(*path)
	if err != nil {
		log.Fatal(err)
	}
	defer miFS.file.Close()

	leerSuperBloque()
	leerDirectorio()

	if *info {
		mostrarInfo()
	}

	if *list {
		listarArchivos()
	}

	if *remove == "" {
		os.Exit(0)
	}
}

func mostrarInfo() {
	fmt.Printf("Info. del sistema\nNombre: \t\t\t\t%s\n", miFS.nombre)
	fmt.Printf("Versión: \t\t\t\t%s\n", miFS.version)
	fmt.Printf("Etiqueta: \t\t\t\t%s\n", miFS.etiqueta)
	fmt.Printf("Bytes por cluster: \t\t\t%4d\n", miFS.tamCluster)
	fmt.Printf("No. de clusters en el directorio: \t%4d\n", miFS.tamDirectorio)
	fmt.Printf("No. de clusters en la unidad: \t\t%4d\n\n", miFS.tamUnidad)
}

func listarArchivos() {
	fmt.Printf("Archivos:\nNombre \t\tTamaño\n")
	for _, papu := range archivos {
		fmt.Printf("├─ %s \t%7d bytes\n", papu.nombre, papu.tam)
		err := copiarArchivo(papu, papu.nombre)
		if err != nil {
			log.Fatal(err)
		}
	}
}

func usage() {
	flag.Usage = func() {
		w := flag.CommandLine.Output()
		fmt.Fprintf(w, "Uso de %s\n", os.Args[0])
		flag.PrintDefaults()
		fmt.Fprintln(w, "  -h \tMostrar esta página, funciona también en los subcomandos")
		fmt.Fprintln(w, "Subcomandos\n  import \tImporta un archivo desde FiUnamFS al sistema.\n  export \tExporta un archivo desde el sistema a FiUnamFS.")
	}
}

func leerSuperBloque() {
	bloque := make([]byte, 55)
	_, err := miFS.file.Read(bloque)
	genErrCheck(err)

	miFS.nombre = string(bloque[:10])
	miFS.version = string(bloque[10:20])
	miFS.etiqueta = string(bloque[20:40])
	miFS.tamCluster = binary.LittleEndian.Uint32(bloque[40:45])
	miFS.tamDirectorio = binary.LittleEndian.Uint32(bloque[45:50])
	miFS.tamUnidad = binary.LittleEndian.Uint32(bloque[50:55])
}

func leerDirectorio() {
	_, err := miFS.file.Seek(int64(miFS.tamCluster), 0)
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
			archivos[arch.nombre] = arch
		}
	}
}

func leerEntradaDirectorio(buf []byte, offset uint32) (Archivo, error) {
	arch := Archivo{}

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

func copiarArchivo(arch Archivo, nombre string) (err error) {
	_, err = miFS.file.Seek(int64(miFS.tamCluster*arch.cluster), 0)
	if err != nil {
		return
	}

	destino, err := os.Create(nombre)
	if err != nil {
		return
	}

	defer func() {
		err = destino.Close()
	}()

	_, err = io.CopyN(destino, miFS.file, int64(arch.tam))

	return
}

func genErrCheck(err error) {
	if err != nil {
		panic(err)
	}
}
