#!/usr/bin/env python3
# Corrige los 3 fallos restantes del diagnostico:
#   1. GA4 ausente en 2 articulos de conocimiento
#   2. 404.html sin robots noindex (y con meta description vacia)
#   3. /legal/ presente en sitemap.xml pese a tener noindex
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(".").resolve()

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

GA4 = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-07T9PCBG7P"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-07T9PCBG7P');
</script>
"""

SIN_GA4 = [
    "conocimiento/como-digitalizar-pedidos-distribuidora/index.html",
    "conocimiento/control-de-cambios-sistemas-criticos/index.html",
]

# ---------------------------------------------------- validacion previa

tareas = []

for rel in SIN_GA4:
    p = RAIZ / rel
    if not p.is_file():
        print(f"ERROR: falta {rel}. Abortado.")
        sys.exit(1)
    t = p.read_text(encoding="utf-8")
    if "G-07T9PCBG7P" in t:
        print(f"SALTEA  {rel}: ya tiene GA4")
        continue
    if t.count("<head>\n") != 1:
        print(f"ERROR: {rel} no tiene un unico '<head>'. Abortado.")
        sys.exit(1)
    tareas.append(("ga4", p, t))

p404 = RAIZ / "404.html"
t404 = p404.read_text(encoding="utf-8")
ANCLA404 = '<meta charset="utf-8">'
DESC_VACIA = '<meta name="description" content="">\n'
if "noindex" in t404:
    print("SALTEA  404.html: ya tiene noindex")
else:
    if t404.count(ANCLA404) != 1:
        print("ERROR: 404.html sin ancla charset unica. Abortado.")
        sys.exit(1)
    tareas.append(("404", p404, t404))

psm = RAIZ / "sitemap.xml"
sm = psm.read_text(encoding="utf-8")
legal = [l for l in sm.splitlines() if "n2n.com.ar/legal/" in l]
if not legal:
    print("SALTEA  sitemap.xml: /legal/ ya no figura")
else:
    if len(legal) != 1:
        print(f"ERROR: /legal/ aparece {len(legal)} veces en el sitemap. Abortado.")
        sys.exit(1)
    tareas.append(("sitemap", psm, sm))

if not tareas:
    print("Nada que corregir.")
    sys.exit(0)

# ---------------------------------------------------------------- backup

TAR = RAIZ.parent / f"n2n-site-backup-fixdiag-{datetime.now():%Y%m%d_%H%M%S}.tar.gz"
r = subprocess.run(
    ["tar", "--exclude=.git", "-czf", str(TAR), "-C", str(RAIZ.parent), RAIZ.name],
    capture_output=True, text=True,
)
if r.returncode != 0 or not TAR.is_file():
    print(f"ERROR: fallo el backup. {r.stderr.strip()}. Abortado.")
    sys.exit(1)
print(f"Backup: {TAR}  ({TAR.stat().st_size/1024/1024:.1f} MB)")
print()

# ------------------------------------------------------------ aplicacion

for tipo, p, t in tareas:
    rel = p.relative_to(RAIZ).as_posix()

    if tipo == "ga4":
        nuevo = t.replace("<head>\n", "<head>\n" + GA4, 1)
        p.write_text(nuevo, encoding="utf-8")
        print(f"OK  {rel}: bloque GA4 insertado")

    elif tipo == "404":
        nuevo = t.replace(ANCLA404, ANCLA404 + '\n<meta name="robots" content="noindex">', 1)
        quitada = False
        if DESC_VACIA in nuevo:
            nuevo = nuevo.replace(DESC_VACIA, "", 1)
            quitada = True
        p.write_text(nuevo, encoding="utf-8")
        print(f"OK  {rel}: robots noindex agregado" + (" + description vacia removida" if quitada else ""))

    elif tipo == "sitemap":
        lineas = [l for l in t.splitlines() if "n2n.com.ar/legal/" not in l]
        nuevo = "\n".join(lineas) + ("\n" if t.endswith("\n") else "")
        p.write_text(nuevo, encoding="utf-8")
        print(f"OK  {rel}: /legal/ removido — {nuevo.count('<loc>')} URLs restantes")

print()
print("Listo. Correr diagnostico_sitio_v1.py para verificar.")
