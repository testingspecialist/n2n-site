#!/usr/bin/env python3
# Agrega "@context" a los bloques JSON-LD que no lo tienen
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(".").resolve()
BLOQUE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

# --- deteccion previa -------------------------------------------------------

objetivo = []
for p in sorted(RAIZ.rglob("*.html")):
    if ".git" in p.parts:
        continue
    txt = p.read_text(encoding="utf-8")
    for m in BLOQUE.finditer(txt):
        try:
            j = json.loads(m.group(2))
        except json.JSONDecodeError as e:
            print(f"ERROR: JSON-LD invalido en {p.relative_to(RAIZ)}: {e.msg}. Abortado.")
            sys.exit(1)
        if "@context" not in j:
            objetivo.append(p)
            break

if not objetivo:
    print("Nada que corregir: todos los bloques JSON-LD ya tienen @context.")
    sys.exit(0)

print(f"Archivos a corregir: {len(objetivo)}")

# --- backup -----------------------------------------------------------------

TAR = RAIZ.parent / f"n2n-site-backup-jsonld-{datetime.now():%Y%m%d_%H%M%S}.tar.gz"
r = subprocess.run(
    ["tar", "--exclude=.git", "-czf", str(TAR), "-C", str(RAIZ.parent), RAIZ.name],
    capture_output=True, text=True,
)
if r.returncode != 0 or not TAR.is_file():
    print(f"ERROR: fallo el backup. {r.stderr.strip()}. Abortado.")
    sys.exit(1)
print(f"Backup: {TAR}  ({TAR.stat().st_size/1024/1024:.1f} MB)")

# --- correccion -------------------------------------------------------------

corregidos = 0
for p in objetivo:
    txt = p.read_text(encoding="utf-8")

    def arreglar(m):
        cuerpo = m.group(2)
        try:
            if "@context" in json.loads(cuerpo):
                return m.group(0)
        except json.JSONDecodeError:
            return m.group(0)
        nuevo = re.sub(
            r'(\{\s*\n)([ \t]*)"@type"',
            r'\1\2"@context": "https://schema.org",\n\2"@type"',
            cuerpo,
            count=1,
        )
        if nuevo == cuerpo:
            return m.group(0)
        return m.group(1) + nuevo + m.group(3)

    salida = BLOQUE.sub(arreglar, txt)

    if salida == txt:
        print(f"SIN CAMBIO  {p.relative_to(RAIZ)}  (patron no reconocido)")
        continue

    ok = True
    for m in BLOQUE.finditer(salida):
        try:
            j = json.loads(m.group(2))
        except json.JSONDecodeError as e:
            print(f"ERROR  {p.relative_to(RAIZ)}: quedaria JSON invalido ({e.msg}). No se escribe.")
            ok = False
            break
        if "@context" not in j:
            print(f"ERROR  {p.relative_to(RAIZ)}: sigue sin @context. No se escribe.")
            ok = False
            break
    if not ok:
        continue

    p.write_text(salida, encoding="utf-8")
    corregidos += 1
    print(f"OK          {p.relative_to(RAIZ)}")

print()
print(f"Corregidos: {corregidos} / {len(objetivo)}")
if corregidos != len(objetivo):
    print("ATENCION: quedaron archivos sin corregir. Revisar antes de commitear.")
    sys.exit(1)
