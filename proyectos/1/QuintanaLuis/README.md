# FiFS - Proyecto 1

![demo](docs/demo_cli.gif)

`Autor`: Luis Quintana

Descripción
---
Programa en terminal que permite copiar, eliminar y listar archivos del sistema de archivos [FI UNAM FI](../fiunamfs.img)

Dependencias
---
`python 3.11`

Instalación
---

1. Clonar el repositorio
```commandline
git clone https://github.com/unamfi/sistop-2024-2.git
```
2. Cambiar de directorio
```commandline
cd sistop-2024-2/proyectos/1/QuintanaLuis/src
```
3. Ejecutar cli (opciones abajo)
```commandline
python3 fifs.py [push|pull|remove|ls|shell] [opciones] [archivos]
```

4. Ejecutar shell (opciones abajo)
```commandline
python3 fifs.py shell
```

__IMPORTANTE__: mantener una copia de [fiunamfs.img](fiunamfs.img) en el directorio raíz de este proyecto

Opciones
---
```commandline
Uso:
python3 fifs.py [push|pull|remove|ls|shell] [opciones] [archivos]

    push <archivo_origen> [archivo_destino]        copia los archivos del sistema al fi unam fs
    pull <archivo_origen> [archivo_destino]        copia los archivos de fi unam fs al sistema
    remove <archivo>                               elimina el archivo indicado de fi unam fs
    ls [-l]                                        muestra los archivos de fi unam fs, se muestran los detalles con -l
    shell                                          modo interactivo en shell personalizada

Uso (shell):
python3 fifs.py shell

    push [archivo_origen] [archivo_destino]        copia los archivos del sistema al fi unam fs, solo colocando push se entra en modo interactivo
    pull [archivo_origen] [archivo_destino]        copia los archivos de fi unam fs al sistema, solo colocando pull se entra en modo interactivo
    remove [archivo]                               elimina el archivo indicado de fi unam fs, solo colocando remove|rm se entra en modo interactivo
    ls [-l]                                        muestra los archivos de fi unam fs, se muestran los detalles con -l
                                                   solo colocando remove|rm se entra en modo interactivo
    exit                                           salir del shell

Opciones:
    -f          Forzar eliminación (solo opción remove y en modo shell)
    -l          Mostrar detalles de archivos (solo opción ls)
```

Más información
---
- [Estrategia](docs/estrategia.md)
- [Uso de CLI](docs/cli.md)
- [Uso de Shell](docs/shell.md)
- [Estructura del proyecto](docs/estructura.md)



