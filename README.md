# gestor_notas

Gestor de notas de línea de comandos escrito en Python, sin dependencias externas. Organiza
notas `.txt` en categorías, las abre con la aplicación por defecto del sistema y les asigna
etiquetas para encontrarlas después.

No inventa un formato propio: una categoría es una carpeta y una nota es un archivo de texto,
así que podés editarlas con cualquier editor sin que el programa se interponga.

---

## Features

- **Tres menús** — notas, categorías y etiquetas, cada uno con su propio submenú
- **Categorías como carpetas reales** — lo que ves en el programa es lo que ves en el explorador de archivos
- **Búsqueda por nombre** — filtra las notas de una categoría por coincidencia parcial
- **Búsqueda por contenido** — recorre todas las notas de todas las categorías línea por línea
- **Vista previa de 5 líneas** — antes de abrir un resultado de búsqueda, para confirmar que es la nota que buscabas
- **Etiquetas** — varias por nota, guardadas en `data.json` e indexadas por la ruta de la nota
- **Búsqueda por etiqueta** — elegís una etiqueta y te lista todas las notas que la tienen
- **Apertura multiplataforma** — `os.startfile` en Windows, `xdg-open` en el resto
- **Operaciones de archivo** — crear, borrar, renombrar y mover notas; crear, borrar y renombrar categorías
- **Cero dependencias** — solo librería estándar

---

## Requisitos

**Python 3.12+**

Usa `match/case` (3.10) y f-strings con comillas anidadas del mismo tipo (PEP 701, 3.12).
No hay `requirements.txt` porque no hay nada que instalar.

---

## Uso

```bash
git clone https://github.com/ThiagoFernandez/gestor_notas.git
cd gestor_notas
python main.py
```

La primera corrida crea `data.json` y la carpeta `notes/`. A partir de ahí, todo lo que
generes vive dentro de `notes/`.

---

## Estructura

```
gestor_notas/
├── main.py       # toda la app: menús, operaciones de archivo y etiquetas
├── data.json     # índice de etiquetas (se crea al arrancar)
└── notes/        # tus notas (se crea al arrancar, no viene en el repo)
    ├── cheat sheets/
    │   ├── linux commands.txt
    │   └── os module.txt
    └── ideas/
        └── proyecto.txt
```

`data.json` mapea la ruta de cada nota a sus etiquetas:

```json
{
    "cheat sheets/linux commands.txt": ["linux", "referencia"],
    "ideas/proyecto.txt": ["pendiente"]
}
```

---

## Cómo funciona

- El programa hace `chdir` a `notes/` al arrancar, así que todas las rutas que maneja son
  relativas a esa carpeta y `data.json` queda un nivel más arriba.
- Las categorías son las carpetas de primer nivel dentro de `notes/`. Una nota es un `.txt`
  dentro de una categoría: hay un solo nivel de anidamiento.
- Renombrar o mover una nota reescribe su clave en `data.json`, así que las etiquetas la siguen.
  Renombrar una categoría reescribe las claves de todas las notas que contiene.
- Borrar una nota o una categoría también borra sus entradas del índice, para que no queden
  etiquetas colgadas de archivos que ya no existen.

---

## Limitaciones conocidas

- Un solo nivel de categorías: no hay subcarpetas dentro de una categoría.
- Las notas tienen que terminar en `.txt`.
- El índice de etiquetas usa el separador de rutas del sistema operativo, así que un
  `data.json` armado en Windows no coincide con las rutas en Linux.
- Todo está en un solo archivo. El próximo paso es separar la lógica de los menús para
  poder montarle una interfaz gráfica: árbol de categorías a la izquierda, editor a la derecha.
