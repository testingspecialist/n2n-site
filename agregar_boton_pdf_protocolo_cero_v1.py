#!/usr/bin/env python3
# Agrega el boton de descarga del PDF a /control/protocolo-cero/
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import os
import shutil
import sys
from datetime import datetime

RUTA = "control/protocolo-cero/index.html"
PDF = "descargas/n2n-protocolo-cero.pdf"

if not os.path.isfile(RUTA):
    print(f"ERROR: falta {RUTA}. Abortado.")
    sys.exit(1)

if not os.path.isfile(PDF):
    print(f"ERROR: falta {PDF}. No agrego links rotos. Abortado.")
    sys.exit(1)

with open(RUTA, encoding="utf-8") as f:
    html = f.read()

ORIGINAL = len(html)

BOTON = '\n      <a href="/descargas/n2n-protocolo-cero.pdf" class="btn btn--ghost" target="_blank" rel="noopener noreferrer">Descargar el método (PDF) ↓</a>'

VIEJO = '<a href="/contacto/" class="btn btn--primary">Solicitar diagnóstico →</a>'
NUEVO = VIEJO + BOTON

n = html.count(VIEJO)
if n != 2:
    print(f"ERROR: encontrado {n} veces el boton primario (esperado 2). Archivo NO modificado.")
    sys.exit(1)

if "n2n-protocolo-cero.pdf" in html:
    print("ERROR: el link al PDF ya existe. Abortado.")
    sys.exit(1)

BACKUP = f"{RUTA}.bak-{datetime.now():%Y%m%d_%H%M%S}"
shutil.copy2(RUTA, BACKUP)
print(f"Backup: {BACKUP}")

html = html.replace(VIEJO, NUEVO, 2)

with open(RUTA, "w", encoding="utf-8") as f:
    f.write(html)

print(f"OK  {RUTA} actualizado")
print(f"Bytes: {ORIGINAL} -> {len(html)}  (+{len(html)-ORIGINAL})")
print(f"Links al PDF: {html.count('n2n-protocolo-cero.pdf')}")
