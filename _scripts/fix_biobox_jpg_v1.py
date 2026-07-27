#!/usr/bin/env python3
# Actualiza las referencias a carlos-petit.png -> .jpg en TODO el sitio
# (bio-box de autor en los articulos de conocimiento)
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(".").resolve()
VIEJO = "/img/carlos-petit.png"
NUEVO = "/img/carlos-petit.jpg"

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

if not (RAIZ / "img" / "carlos-petit.jpg").is_file():
    print("ERROR: falta img/carlos-petit.jpg. Correr antes optimizar_foto_fundador_v2.py. Abortado.")
    sys.exit(1)

afectados = []
for p in sorted(RAIZ.rglob("*.html")):
    if ".git" in p.parts:
        continue
    txt = p.read_text(encoding="utf-8")
    if VIEJO in txt:
        afectados.append((p, txt, txt.count(VIEJO)))

if not afectados:
    print("Nada que corregir: ninguna pagina referencia el PNG.")
    sys.exit(0)

print(f"Paginas a corregir: {len(afectados)}")

TAR = RAIZ.parent / f"n2n-site-backup-biobox-{datetime.now():%Y%m%d_%H%M%S}.tar.gz"
r = subprocess.run(
    ["tar", "--exclude=.git", "-czf", str(TAR), "-C", str(RAIZ.parent), RAIZ.name],
    capture_output=True, text=True,
)
if r.returncode != 0 or not TAR.is_file():
    print(f"ERROR: fallo el backup. {r.stderr.strip()}. Abortado.")
    sys.exit(1)
print(f"Backup: {TAR}  ({TAR.stat().st_size/1024/1024:.1f} MB)")
print()

total = 0
for p, txt, n in afectados:
    p.write_text(txt.replace(VIEJO, NUEVO), encoding="utf-8")
    total += n
    print(f"OK  {p.relative_to(RAIZ).as_posix()}  ({n})")

print()
print(f"Referencias actualizadas: {total}")

restan = [p.relative_to(RAIZ).as_posix() for p in RAIZ.rglob("*.html")
          if ".git" not in p.parts and VIEJO in p.read_text(encoding="utf-8")]
if restan:
    print("ATENCION: quedan referencias al PNG:", restan)
    sys.exit(1)
print("Verificado: ninguna pagina referencia el PNG.")
