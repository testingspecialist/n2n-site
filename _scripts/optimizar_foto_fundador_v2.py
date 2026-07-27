#!/usr/bin/env python3
# Regenera la foto del fundador al tamano real de uso.
#   - Se muestra en un circulo de 220px con object-fit:cover
#   - El lado MENOR debe ser >= 440 para pantallas 2x
#   - WebP para navegadores modernos, JPEG como fallback (PNG es malo para fotos)
# Reemplaza img/carlos-petit.png por img/carlos-petit.jpg y actualiza /nosotros/
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: falta Pillow. Instalar con: pip install --user Pillow")
    sys.exit(1)

RAIZ = Path(".").resolve()
IMG = RAIZ / "img"
LADO_MENOR = 440
HTML = RAIZ / "nosotros" / "index.html"

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

# --- fuente: el backup original en calidad plena, o el webp actual ----------

candidatos = sorted(RAIZ.parent.glob("carlos-petit-original-*.png"), reverse=True)
if candidatos:
    fuente = candidatos[0]
else:
    fuente = IMG / "carlos-petit.webp"
    print("AVISO: no encuentro el backup original, uso el WebP como fuente.")

if not fuente.is_file():
    print("ERROR: no hay imagen fuente. Abortado.")
    sys.exit(1)

im = Image.open(fuente).convert("RGB")
print(f"Fuente: {fuente.name}  {im.size[0]}x{im.size[1]}")

if min(im.size) < LADO_MENOR:
    print(f"ERROR: la fuente tiene lado menor {min(im.size)} < {LADO_MENOR}. Abortado.")
    sys.exit(1)

escala = LADO_MENOR / min(im.size)
destino = (round(im.size[0] * escala), round(im.size[1] * escala))
im = im.resize(destino, Image.LANCZOS)
print(f"Destino: {destino[0]}x{destino[1]}")

# --- validacion del HTML antes de escribir imagenes ------------------------

if not HTML.is_file():
    print(f"ERROR: falta {HTML}. Abortado.")
    sys.exit(1)

html = HTML.read_text(encoding="utf-8")
VIEJO = 'src="/img/carlos-petit.png"'
NUEVO = 'src="/img/carlos-petit.jpg"'

if NUEVO in html:
    print("SALTEA  /nosotros/ ya apunta al JPEG")
elif html.count(VIEJO) != 1:
    print(f"ERROR: encontrado {html.count(VIEJO)} veces {VIEJO} en /nosotros/ (esperado 1). Abortado.")
    sys.exit(1)

# --- escritura -------------------------------------------------------------

webp = IMG / "carlos-petit.webp"
jpg = IMG / "carlos-petit.jpg"
png = IMG / "carlos-petit.png"

antes_webp = webp.stat().st_size / 1024 if webp.is_file() else 0
antes_png = png.stat().st_size / 1024 if png.is_file() else 0

im.save(webp, "WEBP", quality=82, method=6)
im.save(jpg, "JPEG", quality=84, optimize=True, progressive=True)

print(f"WebP: {antes_webp:.0f} KB -> {webp.stat().st_size/1024:.0f} KB")
print(f"JPEG: {jpg.stat().st_size/1024:.0f} KB  (nuevo fallback)")

if VIEJO in html:
    HTML.write_text(html.replace(VIEJO, NUEVO, 1), encoding="utf-8")
    print("OK    /nosotros/ actualizado al fallback JPEG")

if png.is_file():
    png.unlink()
    print(f"PNG eliminado ({antes_png:.0f} KB liberados)")

restan = [p.relative_to(RAIZ).as_posix() for p in RAIZ.rglob("*.html")
          if "carlos-petit.png" in p.read_text(encoding="utf-8")]
if restan:
    print("ATENCION: todavia referencian el PNG:", restan)
    sys.exit(1)
print("Ninguna pagina referencia el PNG.")
