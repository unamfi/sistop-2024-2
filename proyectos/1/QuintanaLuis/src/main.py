"""
Proyecto 1

"""

from pathlib import Path
import struct

ruta_fs = "../fiunamfs.img"

fs = Path(ruta_fs).read_bytes()

fs_nombre = fs[:8].decode('ascii')
fs_version = fs[10:14].decode('ascii')
fs_etiqueta_volumen = fs[20:35].decode('ascii')
fs_tamano_cluster_bytes = struct.unpack('i', fs[40:44])[0]
fs_tamano_cluster_directorio = struct.unpack('i', fs[45:49])[0]
fs_tamano_cluster_unidad = struct.unpack('i', fs[50:54])[0]

if fs_nombre == 'FiUnamFS':
    print("Filesystem correcto")


def listar_archivos(detalles = False) -> None:
    i = 2048

    # Se llegará hasta el tamaño en clusters del directorio por
    # 4 sectores por 512 bytes
    while i < fs_tamano_cluster_directorio * 4 * 512:
        tipo_archivo = fs[i:i + 1].decode('ascii')

        # En caso de tener una entrada vacia se omite
        if tipo_archivo == '/':
            i += 64
            continue

        i += 1
        nombre_archivo = fs[i:i + 14].decode('ascii')
        i += 15
        tamano_bytes_archivo = struct.unpack('i', fs[i:i + 4])[0]
        i += 4
        cluster_inicial_archivo = struct.unpack('i', fs[i:i + 4])[0]
        i += 4
        fecha_creacion_archivo = fs[i:i + 14].decode('ascii')
        i += 14
        fecha_ultima_modificacion_archivo = fs[i:i + 14].decode('ascii')
        i += 14
        espacio_no_utilizado = struct.unpack('iii', fs[i:i + 12])[0]
        i += 12


        if (detalles):
            print(f"{tipo_archivo} {tamano_bytes_archivo} {cluster_inicial_archivo} {fecha_creacion_archivo} {fecha_ultima_modificacion_archivo} {nombre_archivo}")
            continue

        print(nombre_archivo)


def copiar_archivo_de_fs(cluster_inicial: int, tamano_bytes: int, destino: str) -> bool:
    # hay 2048 bytes por cluster
    byte_inicial = cluster_inicial * 2048
    byte_final = byte_inicial + tamano_bytes
    contenido_bytes = fs[byte_inicial: byte_final]

    print(byte_inicial, byte_final)

    with open(destino, "wb") as archivo_copiado:
        archivo_copiado.write(contenido_bytes)
        return True



def copiar_archivo_a_fs(origen: str, cluster_inicial: int, tamano_bytes: int) -> bool:
    byte_inicial = cluster_inicial * 2048
    byte_final = byte_inicial + tamano_bytes

    origen_binario = Path(origen).read_bytes()

    with open(ruta_fs, "r+b") as archivo_copiado:
        archivo_copiado.seek(byte_inicial)
        archivo_copiado.write(origen_binario)


#listar_archivos()
listar_archivos(detalles=True)
copiar_archivo_de_fs(6, 31222, 'archivo.org')
copiar_archivo_de_fs(22, 126423, 'logo.png')
copiar_archivo_de_fs(84, 254484, 'mensaje.jpg')

copiar_archivo_a_fs("imagen_prueba.jpeg", 200, 36294)

copiar_archivo_de_fs(200, 36294, 'prueba.jpeg')
