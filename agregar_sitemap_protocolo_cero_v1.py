#!/usr/bin/env python3
# Inserta /control/protocolo-cero/ en sitemap.xml
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import re
import shutil
import sys
from datetime import datetime

RUTA = "sitemap.xml"
NUEVA = '<url><loc>https://n2n.com.ar/control/protocolo-cero/</loc><lastmod>2026-07-22</lastmod></url>'

with open(RUTA, encoding="utf-8") as f:
    contenido = f.read()

if "control/protocolo-cero" in contenido:
    print("Ya estaba insertada, no se toco nada.")
    sys.exit(0)

anclas = re.findall(r'<url><loc>https://n2n\.com\.ar/contacto/</loc>.*?</url>', contenido)
if len(anclas) != 1:
    print(f"ERROR: encontrada {len(anclas)} veces la linea de /contacto/ (esperado 1). No se modifico el archivo.")
    sys.exit(1)

ancla = anclas[0]

BACKUP = f"{RUTA}.bak-{datetime.now():%Y%m%d_%H%M%S}"
shutil.copy2(RUTA, BACKUP)
print(f"Backup: {BACKUP}")

contenido = contenido.replace(ancla, ancla + "\n  " + NUEVA, 1)

with open(RUTA, "w", encoding="utf-8") as f:
    f.write(contenido)

print("Insertada correctamente.")
print(f"URLs en sitemap: {contenido.count('<loc>')}")
