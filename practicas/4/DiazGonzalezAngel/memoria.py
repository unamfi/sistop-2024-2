import random


tamano_memoria_fisica = 1000
tamano_memoria_virtual = 5000

tamano_pagina = 100
tamano_marco = 100

# Número de marcos en la memoria física
numero_marcos = tamano_memoria_fisica // tamano_marco

# Número de páginas en la memoria virtual
numero_paginas = tamano_memoria_virtual // tamano_pagina

tabla_paginas = {}

# Generar tabla de páginas aleatoria
for i in range(numero_paginas):
    marco = random.randint(0, numero_marcos - 1)
    tabla_paginas[i] = marco

# Simulación de acceso a la memoria virtual
accesos = []
for i in range(10):
    pagina = random.randint(0, numero_paginas - 1)
    accesos.append(pagina)

traducciones = {}
for pagina in accesos:
    if pagina in tabla_paginas:
        marco = tabla_paginas[pagina]
        direccion_fisica = marco * tamano_marco + random.randint(0, tamano_pagina - 1)
        traducciones[pagina] = direccion_fisica


with open("resultados_memoria_virtual.txt", "w") as archivo:
    archivo.write("Tabla de Páginas:\n")
    for pagina, marco in tabla_paginas.items():
        archivo.write(f"Página {pagina}: Marco {marco}\n")

    archivo.write("\nAccesos a la Memoria Virtual:\n")
    for i, pagina in enumerate(accesos):
        archivo.write(f"Acceso {i+1}: Página {pagina}\n")

    archivo.write("\nTraducciones de Direcciones:\n")
    for pagina, direccion_fisica in traducciones.items():
        archivo.write(f"Página {pagina} -> Dirección Física {direccion_fisica}\n")

print("Archivo 'resultados_memoria_virtual.txt' generado exitosamente.")
