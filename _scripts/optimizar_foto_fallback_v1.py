#!/usr/bin/env python3
# Reduce img/carlos-petit.png (fallback de <picture>) a 440x440
# Se muestra a 220px: 440 cubre pantallas 2x. Hoy pesa 2.3 MB.
# No recorta: mantiene proporcion. El recorte circular lo hace el CSS (object-fit).
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import shutil
import sys
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: falta Pillow. Instalar con: pip install --user Pillow")
    sys.exit(1)

RAIZ = Path(".").resolve()
ORIGEN = RAIZ / "img" / "carlos-petit.png"
LADO = 440

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

if not ORIGEN.is_file():
    print(f"ERROR: falta {ORIGEN}. Abortado.")
    sys.exit(1)

im = Image.open(ORIGEN)
kb_antes = ORIGEN.stat().st_size / 1024
print(f"Original: {im.size[0]}x{im.size[1]}  {kb_antes:.0f} KB  modo {im.mode}")

if max(im.size) <= LADO:
    print("Ya esta dentro del tamano objetivo. Nada que hacer.")
    sys.exit(0)

BACKUP = RAIZ.parent / f"carlos-petit-original-{datetime.now():%Y%m%d_%H%M%S}.png"
shutil.copy2(ORIGEN, BACKUP)
print(f"Backup del original: {BACKUP}")

im.thumbnail((LADO, LADO), Image.LANCZOS)

if im.mode not in ("RGB", "RGBA"):
    im = im.convert("RGBA" if "A" in im.mode else "RGB")

im.save(ORIGEN, "PNG", optimize=True)

kb_despues = ORIGEN.stat().st_size / 1024
print(f"Resultado: {im.size[0]}x{im.size[1]}  {kb_despues:.0f} KB")
print(f"Reduccion: {100*(1-kb_despues/kb_antes):.0f}%")
