# Tus guías de estadística, en web y PDF

Escribes cada guía una sola vez. La publicación genera una web, cuatro PDF independientes y un ZIP que contiene los cuatro PDF.

## 1. Los únicos archivos que necesitas editar

| Archivo | Resultado |
|---|---|
| `01_Pinguinos.qmd` | Episodio 1 y `01_Pinguinos.pdf` |
| `02_Dientes.qmd` | Episodio 2 y `02_Dientes.pdf` |
| `03_Proporciones.qmd` | Episodio 3 y `03_Proporciones.pdf` |
| `Guia_inicial.qmd` | Guía «Empieza aquí» y `Guia_inicial.pdf` |

`index.qmd` contiene la portada. `_quarto.yml` permite cambiar el nombre general del sitio. No cambies los nombres de los archivos: ya están conectados con los botones y la publicación.

## 2. Pegar desde Word

Abre el archivo `.qmd` en RStudio o en VS Code con la extensión de Quarto y usa el editor **Visual**. Se parece a un editor de texto con títulos, listas, enlaces y tablas. Edita los apartados existentes o pega material adicional en la sección correspondiente y guarda.

Conserva el encabezado entre `---` y el bloque del botón de descarga que lo sigue. Puedes cambiar el título y el subtítulo. El contenido del capítulo comienza después de ese bloque.

Pegar desde Word no garantiza conservar exactamente el formato: revisa los niveles de título, ecuaciones, tablas e imágenes. Guarda las imágenes dentro de `imagenes/` e insértalas con el editor. Usa nombres sencillos sin espacios. No pegues rutas locales de tu ordenador.

Si editas como texto, basta con estas convenciones:

```markdown
## Un apartado

Un párrafo con **negrita** y *cursiva*.

1. Primera pregunta.
2. Segunda pregunta.

![Descripción de la figura](imagenes/figura.png)

Una fórmula en línea: $\bar{x}$. Una fórmula separada:

$$
\hat{p} = \frac{x}{n}
$$
```

La colección presenta tres recorridos breves para conocer el software y acompañar clases de estadística inferencial con Python: ANOVA, Kruskal–Wallis y prueba binomial. Cada recorrido conecta las opciones de la interfaz con el código generado. `Guia_inicial.qmd` contiene ahora la guía de inicio «Empieza aquí»; conserva su nombre de archivo para mantener los enlaces de descarga. Las capturas se encuentran en `Figures/`.

## 3. Configurar GitHub Pages (una sola vez)

1. Crea un repositorio público en GitHub con la rama principal llamada `main`.
2. Sube el contenido de esta carpeta, incluida la carpeta oculta `.github`. GitHub Desktop permite hacerlo sin usar comandos. No subas únicamente los PDF: se necesitan los archivos fuente y la automatización.
3. En el repositorio abre **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Para la primera publicación, abre **Actions → Generar y publicar las guías → Run workflow**, selecciona `main` y confirma.
5. Espera a que termine en verde. La dirección aparecerá en **Settings → Pages** y en el resultado de la publicación.

A partir de entonces, guardar cambios y subirlos a GitHub **no publica la web**. La publicación solo se inicia cuando tú la solicitas. Puedes editar los `.qmd` desde GitHub con el botón del lápiz; en ese caso escribirás en Markdown. No necesitas instalar Quarto en tu ordenador si solo editas desde GitHub.

### Publicar cuando tú decidas

Guarda tus cambios en un commit y súbelos a `main` con GitHub Desktop o Git. Cuando quieras actualizar la web, ejecuta desde la carpeta del repositorio:

```powershell
gh workflow run publish.yml --ref main
```

Este comando requiere [GitHub CLI](https://cli.github.com/) instalado y haber iniciado sesión con `gh auth login`. El archivo `.github/workflows/publish.yml` debe estar subido a la rama predeterminada del repositorio. También puedes publicar sin comandos desde **Actions → Generar y publicar las guías → Run workflow**.

El comando inicia la generación en GitHub; espera a que la ejecución termine correctamente en **Actions**. Generará la web, los cuatro PDF y el ZIP a partir de la versión de `main` que está en GitHub al iniciar la ejecución. Los cambios que solo tengas en tu ordenador no se incluyen.

- **Commit:** registra una versión de tus archivos en el historial local.
- **Push:** envía esos commits a GitHub.
- **Publicación manual:** usa una versión ya subida a GitHub para actualizar la web y las descargas.

Puedes hacer varios commits y pushes antes de publicar. Cada publicación queda asociada al commit que utilizó, pero hacer un commit o un push no la inicia. También puedes volver a publicar la misma versión sin crear un commit nuevo.

Referencia: [ejecutar un workflow con GitHub CLI](https://cli.github.com/manual/gh_workflow_run).

## 4. Generarlo en tu ordenador (opcional)

Instala [Quarto](https://quarto.org/docs/get-started/) y Python 3. Para la generación de PDF instala TinyTeX una vez:

```powershell
quarto install tinytex
```

Abre una terminal en esta carpeta y ejecuta:

```powershell
python scripts/build.py
```

El resultado estará en `_site/`. Dentro de `_site/descargas/` encontrarás los cuatro PDF y `Guias_estadistica.zip`.

Para revisar el sitio con sus descargas tras generarlo:

```powershell
python -m http.server 8000 --directory _site
```

Abre <http://localhost:8000>. Detén el servidor con Ctrl+C. Después de editar, vuelve a generar para actualizar las descargas.

Para una vista rápida mientras escribes, `quarto preview --to html` actualiza la web, pero no regenera los PDF ni el ZIP. Usa siempre `python scripts/build.py` para la entrega completa.

Para revisar qué imágenes de `Figures/` no usa ninguno de los manuales `.qmd`:

```powershell
python scripts/limpiar_figuras.py
```

Para eliminarlas de `Figures/`:

```powershell
python scripts/limpiar_figuras.py --delete
```

El documento original `04-demostration.tex` también utiliza algunas de esas imágenes; si vuelves a compilarlo, tendrás que restaurarlas desde tu copia.

## Notas

- Los botones se muestran en la web y se omiten en los PDF.
- Los PDF tienen formato A4, pasos breves e imágenes. Se omite el índice para facilitar una lectura rápida.
- La ejecución de código está desactivada: no necesitas R ni paquetes estadísticos para publicar texto, imágenes, fórmulas y tablas. Si incorporas análisis ejecutables, habrá que configurar sus dependencias.
- La publicación se detiene si falla cualquiera de los PDF; así no se publica una colección incompleta.
- Referencias: [publicación con Quarto y GitHub Pages](https://quarto.org/docs/publishing/github-pages.html) y [editor visual](https://quarto.org/docs/visual-editor/).
