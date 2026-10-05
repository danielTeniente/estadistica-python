"""Genera los cuatro PDF, la web y el ZIP usando una sola fuente por guía."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ("01_Pinguinos", "02_Dientes", "03_Proporciones", "Guia_inicial")


def main():
    quarto = os.environ.get("QUARTO_BIN") or shutil.which("quarto")
    if not quarto:
        candidate = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Quarto/bin/quarto.cmd"
        if candidate.is_file():
            quarto = str(candidate)
    if not quarto:
        raise SystemExit("No se encontró Quarto. Instálalo desde https://quarto.org/docs/get-started/")

    def render(*args):
        subprocess.run([quarto, "render", *args], cwd=ROOT, check=True)

    # Borrar únicamente los PDF esperados evita empaquetar versiones antiguas.
    for name in GUIDES:
        target = ROOT / "_pdf" / f"{name}.pdf"
        target.unlink(missing_ok=True)
        render(f"{name}.qmd", "--to", "pdf", "--output-dir", "_pdf")
        if not target.is_file():
            raise RuntimeError(f"No se generó {target.name}")

    render("--to", "html")
    downloads = ROOT / "_site" / "descargas"
    downloads.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(downloads / "Guias_estadistica.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for name in GUIDES:
            source = ROOT / "_pdf" / f"{name}.pdf"
            shutil.copy2(source, downloads / source.name)
            archive.write(source, arcname=source.name)
    (ROOT / "_site" / ".nojekyll").touch()
    print("Listo: web en _site; cuatro PDF y ZIP en _site/descargas.")


if __name__ == "__main__":
    try:
        main()
    except (subprocess.CalledProcessError, OSError, RuntimeError) as error:
        print(f"No se completó la generación: {error}", file=sys.stderr)
        sys.exit(1)
