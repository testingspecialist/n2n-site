#!/usr/bin/env python3
# Optimiza img/og-n2n.png (placa de marca, 711 KB) sin cambiar nombre ni formato.
# Verifica la degradacion contra el original y aborta si es perceptible.
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import shutil
import sys
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: falta Pillow.")
    sys.exit(1)

RAIZ = Path(".").resolve()
OG = RAIZ / "img" / "og-n2n.png"
TOLERANCIA = 12  # diferencia media maxima aceptada por canal (0-255)

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

if not OG.is_file():
    print(f"ERROR: falta {OG}. Abortado.")
    sys.exit(1)

orig = Image.open(OG)
kb_antes = OG.stat().st_size / 1024
print(f"Original: {orig.size[0]}x{orig.size[1]}  {kb_antes:.0f} KB  modo {orig.mode}")

base = orig.convert("RGB")
colores = base.getcolors(maxcolors=200000)
print(f"Colores unicos: {len(colores) if colores else '>200000 (es una foto)'}")

candidatos = []

# A) paleta de 256 colores
pal = base.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
candidatos.append(("paleta 256", pal))

# B) paleta de 128 colores
pal128 = base.quantize(colors=128, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
candidatos.append(("paleta 128", pal128))

# C) solo recomprimir sin perdida
candidatos.append(("recomprimir", base))

TMP = RAIZ / "img" / ".og-tmp.png"
mejor = None

for nombre, im in candidatos:
    im.save(TMP, "PNG", optimize=True)
    kb = TMP.stat().st_size / 1024

    prueba = Image.open(TMP).convert("RGB")
    dif = 0.0
    px = list(base.getdata())
    py = list(prueba.getdata())
    total = sum(abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]) for a, b in zip(px, py))
    dif = total / (len(px) * 3)

    estado = "OK" if dif <= TOLERANCIA else "degrada"
    print(f"  {nombre:12s} {kb:7.0f} KB   dif media {dif:5.2f}   {estado}")

    if dif <= TOLERANCIA and (mejor is None or kb < mejor[1]):
        mejor = (nombre, kb, im)

TMP.unlink(missing_ok=True)

if mejor is None:
    print("\nNinguna variante pasa la tolerancia. No se toca el archivo.")
    sys.exit(1)

nombre, kb, im = mejor
if kb >= kb_antes:
    print("\nNinguna variante reduce el peso. No se toca el archivo.")
    sys.exit(0)

BACKUP = RAIZ.parent / f"og-n2n-original-{datetime.now():%Y%m%d_%H%M%S}.png"
shutil.copy2(OG, BACKUP)
print(f"\nBackup: {BACKUP}")

im.save(OG, "PNG", optimize=True)
kb_final = OG.stat().st_size / 1024
print(f"Aplicado: {nombre}")
print(f"Resultado: {kb_antes:.0f} KB -> {kb_final:.0f} KB  ({100*(1-kb_final/kb_antes):.0f}% menos)")
print(f"Dimensiones: {Image.open(OG).size}")
