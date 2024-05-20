from excepciones import EntradaNoValidaException


class Entrada:
    def __init__(self, byte_inicial: int, tipo: str = '/', nombre: str = '', tamano_bytes: int = 0,
                 cluster_inicial: int = 0, fecha_creacion: str = '', fecha_ultima_modificacion: str = '',
                 espacio_no_utilizado: int = 0):
        if tipo != '-':
            raise EntradaNoValidaException("Entrada vacia o no válida")

        self.byte_inicial = byte_inicial
        self.tipo = tipo
        # quitar espacios a los lados para evitar errores al operar los archivos
        self.nombre = nombre.strip()
        self.tamano_bytes = tamano_bytes
        self.cluster_inicial = cluster_inicial
        self.fecha_creacion = fecha_creacion
        self.fecha_ultima_modificacion = fecha_ultima_modificacion
        self.espacio_no_utilizado = espacio_no_utilizado

    def listar(self, detalles=False):
        if detalles:
            print(f"{self.tipo} {self.tamano_bytes} "
                  f"{self.cluster_inicial} {self.fecha_creacion} "
                  f"{self.fecha_ultima_modificacion} {self.nombre}")
            return

        print(self.nombre, end=' ')
