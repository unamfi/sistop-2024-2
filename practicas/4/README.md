# Práctica 4: Ignorando archivos *innecesarios*

    Práctica creada el 2024.03.21
	Entrega: 2024.04.02

Los sistemas de control de cambios están hechos para poder dar
seguimiento a la historia de los archivos que forman parte de nuestro
proyecto. Ahora bien, cuando desarrollamos software, trabajamos con
conjuntos de datos, e incluso cuando escribimos prosa, es frecuente
que se generen archivos *derivados* de nuestro trabajo.

## Presentando el problema

¿A qué me refiero? Imagina que estás programando en C. Algo tan
sencillo como un *hola mundo*. Tu programa se llama `hola.c`:

	#include <stdio.h>
	int main() {
	    printf("Hola mundo!");
		return 0;
	}

Emocionado, agregas tu archivo a Git. Acto seguido, pruebas el código,
y funcionó correctamente... Casi:

    $ git add hola.c
	$ git commit -m 'Hola Mundo en C'
    $ gcc hola.c -o hola
	$ ls
	hola    hola.c
	$ ./hola
	Hola mundo!	$

(Sí, en Unix, el resultado de `gcc` queda en el archivo `hola`, así, a
secas; en Windows probablemente sería sensato denominarlo `hola.exe`,
pues Windows identifica el tipo de cada archivo por su _extensión_)

¡Te faltó el caracter de fin de línea! Bueno, no pasa nada. Editas tu
código, agregas el `\n` faltante, y te dispones a hacer tu commit como
ya aprendiste... Primero revisas el estado actual:

	$ git status
	On branch main
	Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
	  (use "git checkout -- <file>..." to discard changes in working directory)

		modified:   hola.c

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

    	hola

	no changes added to commit (use "git add" and/or "git commit -a")

Ahí están tus cambios, listos para el commit. Pero... ¿Por qué está
ahí `hola`? Sencillamente, porque... ¡Está ahí!  (ah, pero... ¡Qué
bueno que soy para dar malas respuestas 😝)

Como dije, es tu programa ya compilado. Y dado que probablemente no
sirva tal cual a otras personas (ya sea porque sus versiones de las
bibliotecas estándar sean otras, o incluso usen un compilador o
arquitectura distintos), hay que indicar a Git que ignore ese archivo.

## La solución Git: El archivo `.gitignore`

Cada sistema de control de cambios tiene una manera distinta de evitar
este problema. En Git, basta con crear un archivo llamado `.gitignore`
en el directorio en que estés trabajando. Este directorio incluirá los
*patrones* de nombres de archivo a ignorar. En el caso en particular
aquí descrito, basta con que contenga la siguiente línea:

    hola

Pero en un proyecto más grande, podrías requerir ignorar todos los
archivos objeto de C (`*.o`), todos los archivos compilados de Java
(`*.class`), o incluso las bitácoras (`*.log`) o bases de datos
(`*.sqlite`) generadas como parte de la operación de tu sistema.

Volviendo al caso descrito, creas el archivo .gitignore, y vuelves a
pedir el estado:

    $ git status
	On branch main
	Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
	  (use "git checkout -- <file>..." to discard changes in working directory)

		modified:   hola.c

    Untracked files:
      (use "git add <file>..." to include in what will be committed)

    	.gitignore

	no changes added to commit (use "git add" and/or "git commit -a")

Ahora sí, nos está mostrando únicamente los cambios que hicimos
personalmente. Vamos a hacer dos *commits* separados, detallando la
naturaleza de cada uno de estos cambios:

	$ git add .gitignore
	$ git commit -m 'Ignoramos los archivos autogenerados'
	$ git add hola.c
	$ git commit -m 'Agregamos el fin de línea faltante'
	$ git push

Ahora sí, envías un *pull request* a tu maestro, y tienes tu punto
asegurado por un trabajo bien hecho.

# Ahora sí, la práctica

Quiero que repliquen lo que les presenté como situación
hipotética. Dentro del directorio de esta práctica, crea un directorio
con tu nombre, siguiendo la nomenclatura ya acordada. Dentro de este
directorio, crea un archivo que genere un archivo como consecuencia de
su compilación o uso — De preferencia, un programa relacionado con lo
que abordamos en estos días en clase.

Como siempre, *sugiero* manejar cada entrega en una rama separada — Ya
sabes cómo se hace.

Haz un primer commit que incluya a tu programa, *pero no al archivo
autogenerado*.

Haz un segundo commit con el archivo `.gitignore` únicamente.

¡Ojo! Verifica que todo lo que hagas sea *dentro del directorio correcto*, según
la convención de nombres que adoptamos desde la primera práctica.

Como siempre, envíame un *pull request* cuando hayas terminado la
práctica.

# Notas al pie

Un par de notas relacionadas con el manejo de `.gitignore`:

- *El nombre*. Por convención, en Unix se omite del listado de
  directorios, así como de varias herramientas que "expanden" al
  `glob` de archivos ( `*` ) ignoran todos los archivos cuyo nombre
  comienza por `.` — Puede verse raro ante las prácticas actuales,
  pero en tu *directorio personal* vas a encontrar muchos archivos que
  siguen esta lógica. Busca algunos e intenta comprender lo que son.

- *De aquí pa'bajo*. Cuando creas un archivo `.gitignore`, su efecto
  se extiende a todos los subdirectorios debajo del directorio donde
  fue creado. Esto es, podríamos haber creado un `.gitignore` en el
  directorio principal; no lo hice para que cada uno de ustedes lo
  haga por su cuenta (o, como dicen, *¡pa' que aprendan!*). Pueden verificarlo:
  En la raiz de este repositorio tengo ya un `.gitignore` para omitir los
  archivos `.DS_Store` que tienden a agregar como *basura no requerida por el
  usuario* los sistemas operativos de Apple.

  **¡Ojo con la nomenclatura de directorios!** No me vayan a dejar un
  `.gitignore` fuera de su directorio personal, porque no los voy a
  aceptar :-Þ

- *Lo que ya existe no se ignora*. Si habías ya agregado al
  repositorio tu archivo `*.class`, `a.out`, `*.pyc` o similar, Git no
  lo ignorará a pesar de estar su nombre listado en el `.gitignore`;
  tienes que eliminarlo explícitamente del repositorio (con `git rm
  a.out`). Después de esto, cuando se regenere, Git ya lo ignorará.
