package main

import (
	"bytes"
	"encoding/binary"
	"errors"
	"flag"
	"fmt"
	"io"
	"log"
	"os"
	"strings"
	"time"
)

type FileSystem struct {
	nombre, version, etiqueta            string
	tamCluster, tamDirectorio, tamUnidad uint32
	file                                 *os.File
	archivos                             map[string]Archivo
}

type Archivo struct {
	nombre, creado, modificado string
	tam, cluster, offset       uint32
}

var miFS FileSystem = FileSystem{}
var miLog *log.Logger = log.New(os.Stderr, "", 0)

func main() {

	exportCmd := flag.NewFlagSet("export", flag.ExitOnError)
	importCmd := flag.NewFlagSet("import", flag.ExitOnError)

	list := flag.Bool("l", false, "Listar archivos en el sistema FiUnamFS.")
	info := flag.Bool("i", false, "Mostrar información del sistema de archivos")
	remove := flag.String("d", "", "Eliminar un archivo.")
	path := flag.String("f", "", "Ruta del archivo de la imagen FiUnamFS.")
	var input, output *string

	miFS.archivos = make(map[string]Archivo)

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
		defer func() {
			if miFS.archivos[*input].nombre == "" {
				for _, arch := range miFS.archivos {
					fmt.Println(arch.nombre, []byte(arch.nombre))
				}
				miLog.Fatalln("NOOO", miFS.archivos)
			}

			ch := make(chan error)
			go miFS.archivos[*input].copiarASistema(*output, ch)
			err := <- ch
			if err != nil {
				miLog.Fatalf("No pude exportar el archivo: %v\n", err)
			}
			miFS.file.Close()
		}()
	case "import":
		output = importCmd.String("o", "", "Archivo de destino.")
		input = importCmd.String("i", "", "Nombre de archivo de origen.")
		path = importCmd.String("f", "", "Ruta del archivo de la imagen FiUnamFS.")
		importCmd.Parse(os.Args[2:])
		defer func() {
			err := miFS.copiarDesdeSistema(*input, *output)
			if err != nil {
				miLog.Fatalln("No pude importar el archivo")
			}
			miFS.file.Close()
		}()
	default:
		flag.Parse()
		defer func() {
			if *info {
				mostrarInfo()
			}

			if *list {
				listarArchivos()
			}

			if *remove != "" {
				err := miFS.borrarArchivo(*remove)
				if err != nil {
					miLog.Fatalln(err)
				}
			}

			miFS.file.Close()
		}()
	}

	var err error
	miFS.file, err = os.OpenFile(*path, os.O_RDWR, 0644)
	if err != nil {
		miLog.Fatalln(err)
	}

	leerSuperBloque()
	leerDirectorio()

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
	layout := "20060102150405"
	fmt.Printf("Archivos:\nNombre \t\tTamaño\t\t\tCreado\t\t\t\tModificado\n")
	for _, archivo := range miFS.archivos {

		creado, err := time.Parse(layout, archivo.creado)
		if err != nil {
			miLog.Fatalln("Fecha inválida")
			return
		}
		modificado, err := time.Parse(layout, archivo.modificado)
		if err != nil {
			miLog.Fatalln("Fecha inválida")
			return
		}

		fmt.Printf("├─ %s \t%7d bytes\t\t%s\t\t%s\n", archivo.nombre, archivo.tam, creado.Format("2006-01-02 15:04:05"), modificado.Format("2006-01-02 15:04:05"))
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

	dirEntryBuff := make([]byte, 64)
	for {
		offset, err := miFS.file.Seek(0, io.SeekCurrent)
		genErrCheck(err)
		if offset >= int64(miFS.tamCluster*(miFS.tamDirectorio+1)) {
			break
		}

		_, err = miFS.file.Read(dirEntryBuff)
		genErrCheck(err)
		arch, err := leerEntradaDirectorio(dirEntryBuff, uint32(offset))
		if err == nil {
			miFS.archivos[arch.nombre] = arch
		}
	}
}

func leerEntradaDirectorio(buf []byte, offset uint32) (Archivo, error) {
	arch := Archivo{}

	if buf[0] != '-' {
		return arch, errors.New("Entrada vacía")
	}

	arch.nombre = strings.TrimSpace(string(bytes.Trim(buf[1:16], "\x00")))
	arch.tam = binary.LittleEndian.Uint32(buf[16:20])
	arch.cluster = binary.LittleEndian.Uint32(buf[20:24])
	arch.creado = strings.TrimSpace(string(bytes.Trim(buf[24:38], "\x00")))
	arch.modificado = strings.TrimSpace(string(bytes.Trim(buf[38:52], "\x00")))
	arch.offset = offset

	return arch, nil
}

func (a Archivo) copiarASistema(nombre string, ch chan<-error) {
	_, err := miFS.file.Seek(int64(miFS.tamCluster*a.cluster), 0)
	if err != nil {
		ch <- err
		return
	}

	nombre = string(bytes.Trim([]byte(nombre), "\x00")) // Los bytes nulos causan errores al abrir el archivo
	destino, err := os.Create(nombre)
	if err != nil {
		ch <- err
		return
	}

	_, err = io.CopyN(destino, miFS.file, int64(a.tam))

	err = destino.Close()

	ch <- err
}

func (fs FileSystem) borrarArchivo(nombre string) (err error) {
	archivo := fs.archivos[nombre]
	if archivo.nombre == "" {
		return errors.New(fmt.Sprintf("Imposible borrar %s: Archivo inexistente", nombre))
	}

	mybytes := []byte("/###############")
	_, err = fs.file.WriteAt(mybytes, int64(archivo.offset))

	return
}

func (fs FileSystem) copiarDesdeSistema(inPath, outPath string) (err error){
	cluster, err := fs.encontrarLibre(inPath)
	if err != nil {
		err = fs.compactarArchivos()
		if err != nil {
			return
		}
		cluster, err = fs.encontrarLibre(inPath)
		if err != nil {
			return
		}
	}

	inFile, err := os.Open(inPath)
	if err != nil {
		return
	}

	_, err = fs.file.Seek(int64(fs.tamCluster*cluster), 0)
	if err != nil {
		return
	}
	_, err = io.Copy(fs.file, inFile)
	if err != nil {
		return
	}

	fi, err := os.Stat(inPath)
	if err != nil {
		return
	}

	err = fs.crearArchivo(outPath, cluster, uint32(fi.Size()))

	return
}

func (fs FileSystem) crearArchivo(nombre string, cluster, tam uint32) (err error){
	ahora := time.Now()
	fechaStr := ahora.Format("20060102150405")
	offset, err := fs.encontrarEntradaLibre()
	if err != nil {
		return
	}

	archivo := Archivo{
		nombre: nombre,
		cluster: cluster,
		tam: tam,
		modificado: fechaStr,
		creado: fechaStr,
		offset: uint32(offset),
	}

	fs.archivos[nombre] = archivo

	buff := make([]byte, 64)
	for i := range buff {
		buff[i] = 0
	}
	_, err = fs.file.WriteAt(buff, int64(archivo.offset))
	if err != nil {
		return
	}


	buff[0] = '-'
	copy(buff[1:], []byte(archivo.nombre))
	copy(buff[16:], binary.LittleEndian.AppendUint32([]byte{}, archivo.tam))
	copy(buff[20:], binary.LittleEndian.AppendUint32([]byte{}, archivo.cluster))
	copy(buff[24:], []byte(archivo.creado))
	copy(buff[38:], []byte(archivo.modificado))

	_, err = fs.file.WriteAt(buff, int64(archivo.offset))

	return
}

func (fs FileSystem) encontrarEntradaLibre() (offset int64, err error){
	_, err = fs.file.Seek(int64(fs.tamCluster), 0)
	if err != nil {
		return
	}

	dirEntryBuff := make([]byte, 64)
	for {
		offset, err = fs.file.Seek(0, io.SeekCurrent)
		if err != nil {
			return
		}
		if offset >= int64(fs.tamCluster*(fs.tamDirectorio+1)) {
			break
		}

		_, err = miFS.file.Read(dirEntryBuff)
		if err != nil {
			return
		}

		_, errorAlLeer := leerEntradaDirectorio(dirEntryBuff, uint32(offset))
		if errorAlLeer != nil {
			return
		}
	}

	return
}

func (fs FileSystem) compactarArchivos() (err error){
	return
}

func (fs FileSystem) encontrarLibre(path string) (uint32, error) {
	fi, err := os.Stat(path)
	if err != nil {
		return 0, nil
	}

	noClusters := uint32(fi.Size() / int64(fs.tamCluster))

	cluster := fs.tamDirectorio + 1

	ch := make(chan uint32)
	for cluster < fs.tamUnidad {
		go checarDisponibilidad(cluster, noClusters, fs, ch)
		cluster++
	}
	cluster = fs.tamDirectorio + 1
	for cluster < fs.tamUnidad {
		disp := <- ch
		if disp != 0 {
			return disp, nil
		}
		cluster++
	}

	return 0, errors.New("Sin espacio libre")
}

func checarDisponibilidad(cluster, noClusters uint32, fs FileSystem, ch chan<-uint32) {
	libre := true
	for _, ocupado := range fs.archivos {
		if ocupado.cluster >= cluster && ocupado.cluster <= cluster + noClusters {
			noClustersOcupados := ocupado.tam / fs.tamCluster
			cluster = ocupado.cluster + noClustersOcupados + 1
			libre = false
		}
	}
	if libre {
		ch <- cluster
	} else {
		ch <- 0
	}
}

func genErrCheck(err error) {
	if err != nil {
		panic(err)
	}
}
