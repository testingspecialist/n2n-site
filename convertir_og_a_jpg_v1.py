#!/usr/bin/env python3
# Convierte img/og-n2n.png a JPEG y actualiza og:image / twitter:image en todo el sitio.
# PNG es mal formato para una placa con degradados: 711 KB originales.
# Usa el backup original como fuente para no comprimir sobre una paleta ya dithereada.
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: falta Pillow.")
    sys.exit(1)

RAIZ = Path(".").resolve()
PNG = RAIZ / "img" / "og-n2n.png"
JPG = RAIZ / "img" / "og-n2n.jpg"
VIEJO = "/img/og-n2n.png"
NUEVO = "/img/og-n2n.jpg"

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

# --- 1. escaneo COMPLETO antes de tocar nada -------------------------------

paginas = [p for p in sorted(RAIZ.rglob("*.html")) if ".git" not in p.parts]
afectadas = []
for p in paginas:
    txt = p.read_text(encoding="utf-8")
    if VIEJO in txt:
        afectadas.append((p, txt, txt.count(VIEJO)))

otros = []
for p in RAIZ.rglob("*"):
    if p.is_file() and p.suffix in (".txt", ".xml", ".md") and ".git" not in p.parts:
        if "og-n2n.png" in p.read_text(encoding="utf-8", errors="ignore"):
            otros.append(p.relative_to(RAIZ).as_posix())

print(f"Paginas HTML que referencian el PNG: {len(afectadas)}")
if otros:
    print(f"Otros archivos que lo mencionan: {otros}")

# --- 2. fuente en calidad plena --------------------------------------------

backups = sorted(RAIZ.parent.glob("og-n2n-original-*.png"), reverse=True)
fuente = backups[0] if backups else PNG
if not fuente.is_file():
    print("ERROR: no hay imagen fuente. Abortado.")
    sys.exit(1)
print(f"Fuente: {fuente.name}")

im = Image.open(fuente).convert("RGB")
print(f"Dimensiones: {im.size[0]}x{im.size[1]}")

# --- 3. generar y elegir calidad -------------------------------------------

elegida = None
for q in (88, 84, 80):
    im.save(JPG, "JPEG", quality=q, optimize=True, progressive=True)
    kb = JPG.stat().st_size / 1024
    print(f"  calidad {q}: {kb:.0f} KB")
    if elegida is None and kb <= 200:
        elegida = (q, kb)
        break
    elegida = (q, kb)

q, kb = elegida
im.save(JPG, "JPEG", quality=q, optimize=True, progressive=True)
kb_antes = PNG.stat().st_size / 1024 if PNG.is_file() else 0
print(f"\nAplicado: calidad {q} — {JPG.stat().st_size/1024:.0f} KB")

# --- 4. actualizar referencias ---------------------------------------------

total = 0
for p, txt, n in afectadas:
    p.write_text(txt.replace(VIEJO, NUEVO), encoding="utf-8")
    total += n
print(f"Referencias actualizadas en HTML: {total}")

# --- 5. verificar ANTES de borrar ------------------------------------------

restan = [p.relative_to(RAIZ).as_posix() for p in paginas
          if "og-n2n.png" in p.read_text(encoding="utf-8")]
if restan:
    print("ERROR: quedan referencias al PNG, NO lo borro:", restan)
    sys.exit(1)

if PNG.is_file():
    PNG.unlink()
    print(f"PNG eliminado ({kb_antes:.0f} KB liberados)")

print()
print("Verificado: ninguna pagina referencia el PNG.")
print("ATENCION: revisar la placa a ojo antes de commitear — es la que se ve al compartir.")
