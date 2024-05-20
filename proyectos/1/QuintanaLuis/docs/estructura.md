# Estructura del proyecto

```commandline
.
├── docs    
│   ├── cli.md              -- explicación sobre uso de la cli implementada
│   ├── demo_cli.gif        
│   ├── demo_shell.gif
│   ├── estrategia.md       -- estrategia para resolver la problemática
│   ├── estructura.md       -- este
│   ├── manual.txt          -- manual para mostrar en terminal, también incluido aquí
│   └── shell.md            -- explicación de uso de la implementación de shell
├── fiunamfs.img            -- copia del sistema de archivos para casos de prueba
├── README.md               -- explicación general
├── resources               -- incluye imagen de ejemplo, (para hacer push)
│   └── imagen.jpeg         -- esta imagen
└── src                     -- directorio con archivos fuente
    ├── constantes.py       -- constantes utiles como cuantos bytes tiene un cluster
    ├── directorio.py       -- clase directorio, instanciada en sistema_archivos.py
    ├── entrada.py          -- clase para entradas del directorio con información de los archivos
    ├── excepciones.py      -- excepciones personalizadas para control de entradas y espacio
    ├── fifs.py             -- archivo principal, contiene la cli y shell
    ├── helper.py           -- funciones utiles
    ├── __init__.py         -- necesario para paquetes de python
    ├── sistema_archivos.py -- clase sistema de archivos, implementa directorio y superbloque
    └── super_bloque.py     -- clase de superbloque, almacena información de la unidad
```