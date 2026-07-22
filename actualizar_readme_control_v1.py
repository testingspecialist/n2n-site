#!/usr/bin/env python3
# Actualiza README.md: agrega /control/, corrige analytics (GA4) y rama (main)
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import os
import shutil
import sys
from datetime import datetime

RUTA = "README.md"

if not os.path.isfile(RUTA):
    print(f"ERROR: falta {RUTA}. Abortado.")
    sys.exit(1)

with open(RUTA, encoding="utf-8") as f:
    txt = f.read()

ORIGINAL = len(txt)

CAMBIOS = [
    (
        "estructura: control/",
        "mvp-start/       # Producto de entrada — diagnóstico pago (standalone, sin nav ni footer)",
        "mvp-start/       # Producto de entrada — diagnóstico pago (standalone, sin nav ni footer)\n"
        "control/         # Eje Control Operativo — Protocolo CERO (standalone, fuera del nav)",
    ),
    (
        "estructura: descargas",
        "descargas/       # PDFs descargables (ej: n2n-mvp-start.pdf)",
        "descargas/       # PDFs descargables (n2n-mvp-start.pdf, n2n-protocolo-cero.pdf)",
    ),
    (
        "stack: analytics",
        "| Analytics | Umami |",
        "| Analytics | Google Analytics 4 (G-07T9PCBG7P) |",
    ),
    (
        "deploy: rama",
        "Push a master → publicación automática vía GitHub Pages (~2 minutos). El repo público ES producción.",
        "Push a main → publicación automática vía GitHub Pages (~2 minutos). El repo público ES producción.",
    ),
    (
        "deploy: push",
        "git push origin master",
        "git push origin main",
    ),
    (
        "notas: analytics",
        "- Analytics: Umami ID 05b64f33-b9ae-4ffa-b068-8a2dacff6e33",
        "- Analytics: Google Analytics 4 — G-07T9PCBG7P",
    ),
    (
        "notas: rama",
        "- Master = producción",
        "- main = producción\n- PDFs generados con WeasyPrint mediante scripts versionados en la raiz del repo",
    ),
]

errores = 0
for etiqueta, viejo, nuevo in CAMBIOS:
    n = txt.count(viejo)
    if n != 1:
        print(f"ERROR  {etiqueta}: encontrado {n} veces (esperado 1)")
        errores += 1

if errores:
    print(f"\nAbortado. {errores} patron(es) sin coincidencia. Archivo NO modificado.")
    sys.exit(1)

BACKUP = f"{RUTA}.bak-{datetime.now():%Y%m%d_%H%M%S}"
shutil.copy2(RUTA, BACKUP)
print(f"Backup: {BACKUP}")

for etiqueta, viejo, nuevo in CAMBIOS:
    txt = txt.replace(viejo, nuevo, 1)
    print(f"OK     {etiqueta}")

with open(RUTA, "w", encoding="utf-8") as f:
    f.write(txt)

print(f"\n{RUTA} actualizado")
print(f"Bytes: {ORIGINAL} -> {len(txt)}  (+{len(txt)-ORIGINAL})")
