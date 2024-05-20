from super_bloque import SuperBloque
from entrada import Entrada
from constantes import *

class Directorio:
    # Se almacenran las direcciones para cada dato
    def __init__(self, super_bloque: SuperBloque, entradas_ocupadas: list = [], entradas_desocupadas: list = []):
        # de tipo
        self.entradas_ocupadas = entradas_ocupadas
        self.entradas_desocupadas = entradas_desocupadas

        # ejm 512 bytes * 4 sectores * 1 cluster = 2048 = inicio del directorio
        self.tamano_cluster = TAMANO_CLUSTER_BYTES

        # Cuando acaba superbloque
        self.byte_inicio = self.tamano_cluster
        # ejm 2048 bytes * 4 sectores del directorio = 8192
        self.byte_fin = self.tamano_cluster * super_bloque.tamano_cluster_directorio

    def listar(self, detalles=False) -> None:
        for entrada in self.entradas_ocupadas:
            if detalles:
                entrada.listar(detalles)
                continue
            entrada.listar(detalles)

    def set_entradas_ocupadas(self, entradas_ocupadas: list):
        self.entradas_ocupadas = entradas_ocupadas

    def pop_entrada_vacia(self) -> int:
        return self.entradas_desocupadas.pop(0)



