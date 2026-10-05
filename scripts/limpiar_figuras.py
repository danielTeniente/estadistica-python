"""Lista o elimina imágenes de Figures/ no referenciadas por los manuales QMD."""

import argparse
from pathlib import Path
import re
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "Figures"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
REFERENCE = re.compile(r"Figures/[^\s)\"'>}]+", re.IGNORECASE)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--delete", action="store_true", help="Borra las imágenes no usadas."
    )
    args = parser.parse_args()

    manuals = sorted(ROOT.glob("*.qmd"))
    if not manuals or not FIGURES.is_dir():
        parser.error("No se encontraron los manuales QMD o la carpeta Figures/.")

    used = set()
    for manual in manuals:
        contents = manual.read_text(encoding="utf-8")
        for match in REFERENCE.finditer(contents):
            relative = Path(unquote(match.group(0).replace("\\", "/")))
            if relative.suffix.lower() in IMAGE_EXTENSIONS:
                used.add(relative.as_posix().casefold())

    images = sorted(
        (path for path in FIGURES.rglob("*") if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS),
        key=lambda path: path.as_posix().casefold(),
    )
    present = {path.relative_to(ROOT).as_posix().casefold() for path in images}
    missing = sorted(used - present)
    if missing:
        parser.error("Faltan imágenes referenciadas por los QMD: " + ", ".join(missing))

    unused = [path for path in images if path.relative_to(ROOT).as_posix().casefold() not in used]
    print(f"Manuales revisados: {', '.join(path.name for path in manuals)}")
    print(f"Imágenes en Figures/: {len(images)}; usadas: {len(images) - len(unused)}; sin usar: {len(unused)}")
    for path in unused:
        print(path.relative_to(ROOT).as_posix())

    if not args.delete or not unused:
        if unused:
            print("Vista previa. Para borrar, ejecuta: python scripts/limpiar_figuras.py --delete")
        return

    for path in unused:
        path.unlink()
    print(f"Eliminadas: {len(unused)}.")


if __name__ == "__main__":
    main()
