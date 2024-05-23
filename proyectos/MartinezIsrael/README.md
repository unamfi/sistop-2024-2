# Sistema de Archivos FiUnamFS

Este proyecto implementa un sistema de archivos simulado llamado FiUnamFS, que es una representación de un diskette de 1440 Kilobytes con un sistema de archivos específico. La implementación permite listar el contenido del directorio, copiar archivos desde y hacia el sistema de archivos, y eliminar archivos. Se proporciona una interfaz gráfica simple usando `tkinter` para facilitar la interacción del usuario.

## Características

- Listar los contenidos del directorio.
- Copiar archivos desde FiUnamFS al sistema de archivos local.
- Copiar archivos desde el sistema de archivos local a FiUnamFS.
- Eliminar archivos de FiUnamFS.
- Interfaz gráfica simple para facilitar la interacción del usuario.

## Requisitos del Sistema

- Python 3.6 o superior
- `tkinter` para la interfaz gráfica
- `prettytable` para la visualización en formato de tabla en la interfaz gráfica

## Uso

1. **Ejecutar la aplicación:**

    Navega al directorio del proyecto y ejecuta el archivo principal:

    ```bash
    python main.py
    ```

2. **Interfaz Gráfica:**

    - **Nombre del archivo:** Ingrese el nombre del archivo en FiUnamFS con el que desea trabajar.
    - **Listar directorio:** Muestra el contenido del directorio de FiUnamFS.
    - **Copiar a local:** Copia un archivo desde FiUnamFS al sistema de archivos local.
    - **Copiar a FiUnamFS:** Copia un archivo desde el sistema de archivos local a FiUnamFS.
    - **Eliminar archivo:** Elimina un archivo de FiUnamFS

## Estructura del Proyecto

- `main.py`: Archivo principal que contiene la lógica y la interfaz gráfica.
- `README.md`: Este archivo de documentación.
- `fiunamfs.img`: Archivo de imagen del sistema de archivos (debe ser proporcionado por el usuario).

## Detalles Técnicos

- **Funciones Principales:**
  - `leer_numero`: Lee un número de 4 bytes en formato little-endian.
  - `escribir_numero`: Escribe un número de 4 bytes en formato little-endian.
  - `leer_ascii`: Lee una cadena en formato ASCII 8-bit.
  - `escribir_ascii`: Escribe una cadena en formato ASCII 8-bit.
  - `validar_FiUnamFS`: Valida la integridad del sistema de archivos FiUnamFS.
  - `leer_directorio`: Lee el contenido del directorio del sistema de archivos.
  - `buscar_archivo`: Busca un archivo en el directorio.
  - `fiunamfs_to_local`: Copia un archivo de FiUnamFS al sistema de archivos local.
  - `local_to_fiunamfs`: Copia un archivo del sistema de archivos local a FiUnamFS.
  - `eliminar_archivo`: Elimina un archivo de FiUnamFS.


