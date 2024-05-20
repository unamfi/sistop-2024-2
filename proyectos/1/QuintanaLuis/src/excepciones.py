class EntradaNoValidaException(Exception):
    def __init__(self, message='Entrada no válida'):
        self.message = message
        super().__init__(self.message)

class EspacioInsuficienteException(Exception):
    def __init__(self, message='No hay espacio suficiente en el sistema de archivos'):
        self.message = message
        super().__init__(self.message)
