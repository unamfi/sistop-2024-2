
class SuperBloque:
    def __init__(self, nombre: str, version: str, etiqueta_volumen: str, tamano_cluster_bytes: int,
                 tamano_cluster_directorio: int, tamano_cluster_unidad: int):
        self.nombre = nombre
        self.version = version
        self.etiqueta_volumen = etiqueta_volumen
        self.tamano_cluster_bytes = tamano_cluster_bytes
        self.tamano_cluster_directorio = tamano_cluster_directorio
        self.tamano_cluster_unidad = tamano_cluster_unidad

    def __str__(self):
        return (f"Nombre: {self.nombre}\n"
                f"Versión: {self.version}\n"
                f"Etiqueta Volumen: {self.etiqueta_volumen}\n"
                f"Tamaño de cluster bytes: {self.tamano_cluster_bytes}\n"
                f"Tamaño de cluster directorio: {self.tamano_cluster_directorio}\n"
                f"Tamaño de cluster unidad: {self.tamano_cluster_unidad}"
                )
