#!/usr/bin/env python3
# Corrige las 2 huerfanas involuntarias desde el footer de todas las paginas:
#   - Framework del footer apunta al hub /framework/ en vez de a la subpagina
#   - Se agrega Glosario, que hoy no lo linkea nadie
# El nav del header NO se toca: se reescribe entero en la Parte 5.
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(".").resolve()
MARCA = 'footer__col-title">Navegación'

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

VIEJO_FW = '<a href="/framework/como-funciona/">Framework</a>'
NUEVO_FW = '<a href="/framework/">Framework</a>'
RX_CONO = re.compile(r'([ \t]*)<li><a href="/conocimiento/">Conocimiento</a></li>')

paginas = [p for p in sorted(RAIZ.rglob("*.html")) if ".git" not in p.parts]
pendientes = []

for p in paginas:
    txt = p.read_text(encoding="utf-8")
    rel = p.relative_to(RAIZ).as_posix()

    if txt.count(MARCA) == 0:
        continue
    if txt.count(MARCA) != 1:
        print(f"ERROR: {rel} tiene {txt.count(MARCA)} footers. Abortado.")
        sys.exit(1)

    ini = txt.index(MARCA)
    fin = txt.index("</ul>", ini)
    seg = txt[ini:fin]

    if seg.count(VIEJO_FW) != 1 and 'href="/framework/">Framework</a>' not in seg:
        print(f"ERROR: {rel} — link Framework del footer no reconocido. Abortado.")
        sys.exit(1)
    if not RX_CONO.search(seg):
        print(f"ERROR: {rel} — no encuentro el item Conocimiento del footer. Abortado.")
        sys.exit(1)

    pendientes.append((p, rel, ini, fin, seg, txt))

if not pendientes:
    print("Nada que procesar.")
    sys.exit(0)

ya_ok = sum(1 for _, _, _, _, seg, _ in pendientes
            if 'href="/glosario/"' in seg and VIEJO_FW not in seg)
print(f"Paginas con footer: {len(pendientes)}  (ya correctas: {ya_ok})")

if ya_ok == len(pendientes):
    print("Nada que corregir.")
    sys.exit(0)

TAR = RAIZ.parent / f"n2n-site-backup-footer-{datetime.now():%Y%m%d_%H%M%S}.tar.gz"
r = subprocess.run(
    ["tar", "--exclude=.git", "-czf", str(TAR), "-C", str(RAIZ.parent), RAIZ.name],
    capture_output=True, text=True,
)
if r.returncode != 0 or not TAR.is_file():
    print(f"ERROR: fallo el backup. {r.stderr.strip()}. Abortado.")
    sys.exit(1)
print(f"Backup: {TAR}  ({TAR.stat().st_size/1024/1024:.1f} MB)")
print()

hub = 0
glos = 0
for p, rel, ini, fin, seg, txt in pendientes:
    nuevo = seg
    acciones = []

    if VIEJO_FW in nuevo:
        nuevo = nuevo.replace(VIEJO_FW, NUEVO_FW, 1)
        acciones.append("framework->hub")
        hub += 1

    if 'href="/glosario/"' not in nuevo:
        m = RX_CONO.search(nuevo)
        sangria = m.group(1)
        item = f'\n{sangria}<li><a href="/glosario/">Glosario</a></li>'
        nuevo = nuevo[: m.end()] + item + nuevo[m.end():]
        acciones.append("+glosario")
        glos += 1

    if not acciones:
        continue

    p.write_text(txt[:ini] + nuevo + txt[fin:], encoding="utf-8")
    print(f"OK  {rel}  ({', '.join(acciones)})")

print()
print(f"Framework redirigido al hub: {hub}")
print(f"Glosario agregado:           {glos}")
