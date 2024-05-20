import constantes
from entrada import Entrada
from directorio import Directorio
import math
from excepciones import EspacioInsuficienteException




def buscar_clusters_desocupados(directorio: Directorio, cluster_archivos_inicio: int, cluster_archivos_fin: int) -> list:
    """
    Genera una lista de clusters desocupados mediante las entradas del directorio actual
    """
    cluster_desocupados = list(range(cluster_archivos_inicio, cluster_archivos_fin+1))
    for entrada in directorio.entradas_ocupadas:
        cluster_fin_ocupado = math.ceil(entrada.cluster_inicial + (entrada.tamano_bytes / constantes.TAMANO_CLUSTER_BYTES))

        for cluster_ocupado in range(entrada.cluster_inicial, cluster_fin_ocupado):
            cluster_desocupados.remove(cluster_ocupado)

    return cluster_desocupados

def buscar_cluster_contiguo_desocupado(tamano_bytes: int, directorio: Directorio, cluster_archivos_inicio: int, cluster_archivos_fin: int) -> int:
    """
    A partir de un tamaño en bytes realiza una búsqueda de los clusters desocupados, contiguos y que cumplan con
    los clusters calculados para albergar el archivo, se calcularon mediante la fórmula de
    bytes por cada cluster = 4 sector/cluster * 512 bytes/sector
    """
    clusters_necesarios = math.ceil(tamano_bytes / constantes.TAMANO_CLUSTER_BYTES)
    clusters_desocupados = buscar_clusters_desocupados(directorio, cluster_archivos_inicio, cluster_archivos_fin)
    clusters_disponibles_contiguos = 0
    primer_cluster_disponible_registrado = False
    primer_cluster_disponible = 0
    for i in range(len(clusters_desocupados)):
        # buscar que sean consecutivos
        while ((((clusters_desocupados[i] + 1) == clusters_desocupados[i + 1]) and # verifica que el valor actual y el siguiente sean consecutivos
               i != len(clusters_desocupados)) and # si ya se alcanzo el total de clusters desocupados y no se encontró continuidad, se rompe
               (clusters_disponibles_contiguos != clusters_necesarios)):

            # si entra en el condicional empieza a contar la cantidad de clusters consecutivos desocupados
            if not primer_cluster_disponible_registrado:
                primer_cluster_disponible = clusters_desocupados[i]

            primer_cluster_disponible_registrado = True
            clusters_disponibles_contiguos += 1
            i += 1

        if clusters_disponibles_contiguos >= clusters_necesarios:
            return primer_cluster_disponible


        clusters_disponibles_contiguos = 0
        primer_cluster_disponible = 0
        primer_cluster_disponible_registrado = False

    raise EspacioInsuficienteException("Espacio insuficiente")
