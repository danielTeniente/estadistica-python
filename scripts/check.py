"""Comprueba enlaces locales y la colección descargable tras generar la web."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import zipfile

from build import ROOT, GUIDES

site = ROOT / "_site"
errors = []


class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src") and value:
                url = urlsplit(value)
                if not url.scheme and not url.netloc and url.path:
                    target = site / unquote(url.path).lstrip("/")
                    if not target.exists():
                        errors.append(str(target))


for name in ("index", *GUIDES):
    page = site / f"{name}.html"
    parser = Links()
    parser.feed(page.read_text(encoding="utf-8"))
    if name in GUIDES:
        assert f'descargas/{name}.pdf' in page.read_text(encoding="utf-8")

with zipfile.ZipFile(site / "descargas/Guias_estadistica.zip") as archive:
    assert set(archive.namelist()) == {f"{name}.pdf" for name in GUIDES}
    assert archive.testzip() is None
    for name in GUIDES:
        pdf = (site / "descargas" / f"{name}.pdf").read_bytes()
        assert pdf.startswith(b"%PDF-")
        assert archive.read(f"{name}.pdf") == pdf

assert not errors, "Enlaces rotos: " + ", ".join(errors)
print("Correcto: cinco páginas, enlaces locales, cuatro PDF y ZIP verificados.")
