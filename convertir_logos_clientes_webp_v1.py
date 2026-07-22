#!/usr/bin/env python3
# Convierte los logos de clientes que siguen en PNG a WebP, siguiendo la
# convencion del resto de la tira (<img src=".webp"> directo, sin <picture>).
# Se muestran a 52px de alto: se limita la fuente a 156px (3x).
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: falta Pillow.")
    sys.exit(1)

RAIZ = Path(".").resolve()
CLIENTES = RAIZ / "img" / "clientes"
ALTO_MAX = 156

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

pngs = sorted(CLIENTES.glob("*.png"))
if not pngs:
    print("Nada que convertir: no quedan logos en PNG.")
    sys.exit(0)

paginas = [p for p in sorted(RAIZ.rglob("*.html")) if ".git" not in p.parts]

# --- escaneo completo antes de tocar nada ----------------------------------

plan = []
for png in pngs:
    ref_vieja = "/img/clientes/" + png.name
    ref_nueva = ref_vieja[:-4] + ".webp"
    usos = [(p, p.read_text(encoding="utf-8")) for p in paginas
            if ref_vieja in p.read_text(encoding="utf-8")]
    plan.append((png, ref_vieja, ref_nueva, usos))
    print(f"{png.name}: {png.stat().st_size/1024:.0f} KB, referenciado en {len(usos)} pagina(s)")

print()

# --- conversion -------------------------------------------------------------

for png, ref_vieja, ref_nueva, usos in plan:
    im = Image.open(png)
    modo = "RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB"
    im = im.convert(modo)
    orig_size = im.size

    if im.size[1] > ALTO_MAX:
        escala = ALTO_MAX / im.size[1]
        im = im.resize((round(im.size[0] * escala), ALTO_MAX), Image.LANCZOS)

    webp = png.with_suffix(".webp")

    im.save(webp, "WEBP", lossless=True, method=6)
    kb_ll = webp.stat().st_size / 1024

    im.save(webp, "WEBP", quality=90, method=6)
    kb_q = webp.stat().st_size / 1024

    if kb_ll <= kb_q:
        im.save(webp, "WEBP", lossless=True, method=6)
        elegido = f"lossless {kb_ll:.0f} KB"
    else:
        elegido = f"calidad 90 {kb_q:.0f} KB"

    print(f"OK  {png.name}  {orig_size[0]}x{orig_size[1]} {png.stat().st_size/1024:.0f} KB"
          f"  ->  {im.size[0]}x{im.size[1]} {elegido}")

    for p, _ in usos:
        txt = p.read_text(encoding="utf-8")
        p.write_text(txt.replace(ref_vieja, ref_nueva), encoding="utf-8")

# --- verificar antes de borrar ---------------------------------------------

print()
problemas = []
for png, ref_vieja, ref_nueva, usos in plan:
    restan = [p.relative_to(RAIZ).as_posix() for p in paginas
              if ref_vieja in p.read_text(encoding="utf-8")]
    if restan:
        problemas.append((png.name, restan))

if problemas:
    for nombre, restan in problemas:
        print(f"ERROR: quedan referencias a {nombre}, NO lo borro: {restan}")
    sys.exit(1)

liberado = 0
for png, *_ in plan:
    liberado += png.stat().st_size / 1024
    png.unlink()

print(f"PNG eliminados: {len(plan)}  ({liberado:.0f} KB liberados)")
print("Verificado: ninguna pagina referencia los PNG.")
