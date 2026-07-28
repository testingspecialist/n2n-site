#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corregir_head_faltante_no_atribuible_v1.py

Cierra los 3 defectos del articulo /conocimiento/faltante-no-atribuible/ mas el INFO de llms.txt,
en un solo pase. Origen: la plantilla del skill esta desactualizada (sin GA4, rutas .png que en el
repo son .jpg).

  1. inserta el bloque GA4 (G-07T9PCBG7P)
  2. og:image y twitter:image  -> og-n2n.jpg
  3. author-bio img            -> carlos-petit.jpg
  4. alta en llms.txt, orden alfabetico, formato clonado de las lineas existentes

Patron: verificacion completa sin escribir -> backup -> escribir -> guardas.

Ejecutar desde la raiz del repo:
  python3 _scripts/corregir_head_faltante_no_atribuible_v1.py
"""

import os
import re
import shutil
import sys
from datetime import datetime

REPO = os.getcwd()
SLUG = "faltante-no-atribuible"
PATH_ART = os.path.join(REPO, "conocimiento", SLUG, "index.html")
PATH_LLMS = os.path.join(REPO, "llms.txt")
DIR_BACKUP = os.path.expanduser("~/backups")

URL = "https://n2n.com.ar/conocimiento/%s/" % SLUG
TITULO = "Faltante no atribuible: el hueco que nadie puede explicar"
DESCRIPCION = ("Un faltante no atribuible es una diferencia de stock que admite varias "
               "explicaciones, sin evidencia suficiente para determinar cuál ocurrió.")

GA4 = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-07T9PCBG7P"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-07T9PCBG7P');
</script>
"""

ANCLA_GA4 = '<meta name="viewport" content="width=device-width,initial-scale=1">\n'


def abortar(msg):
    print("ABORTADO: %s" % msg)
    sys.exit(1)


# ================================================================ FASE 1: VERIFICAR

print("=" * 62)
print("FASE 1 — VERIFICACION (no se escribe nada)")
print("=" * 62)

if not os.path.isdir(os.path.join(REPO, ".git")):
    abortar("no estas en la raiz del repo")
for p in (PATH_ART, PATH_LLMS):
    if not os.path.isfile(p):
        abortar("falta %s" % p)

html = open(PATH_ART, encoding="utf-8").read()

if "googletagmanager" in html:
    abortar("el articulo ya tiene GA4")
if html.count(ANCLA_GA4) != 1:
    abortar("no encuentro el ancla del viewport exactamente una vez")
print("[ok] ancla de GA4 localizada")

n_og = html.count("og-n2n.png")
n_carlos = html.count("carlos-petit.png")
if n_og != 2:
    abortar("esperaba 2 referencias a og-n2n.png, encontre %d" % n_og)
if n_carlos != 1:
    abortar("esperaba 1 referencia a carlos-petit.png, encontre %d" % n_carlos)
print("[ok] %d og-n2n.png · %d carlos-petit.png a corregir" % (n_og, n_carlos))

for f in ("img/og-n2n.jpg", "img/carlos-petit.jpg"):
    if not os.path.isfile(os.path.join(REPO, f)):
        abortar("el destino %s no existe en disco" % f)
print("[ok] destinos .jpg existen en disco")

# --- llms.txt
llms = open(PATH_LLMS, encoding="utf-8").read()
if URL in llms:
    abortar("la URL ya figura en llms.txt")

lineas = llms.split("\n")
PAT = re.compile(r'^(\s*[-*]\s*)\[(.+?)\]\((https://n2n\.com\.ar/conocimiento/([^)]+?)/?)\)(\s*[:\-–—]\s*)?(.*)$')
cono = []
for i, l in enumerate(lineas):
    m = PAT.match(l)
    if m:
        cono.append((i, m))
if not cono:
    muestra = [l for l in lineas if "conocimiento/" in l][:3]
    abortar("no reconozco el formato de llms.txt. Muestra:\n  " + "\n  ".join(muestra))

_, ref = cono[0]
sep = ref.group(5) or ""
tiene_desc = bool(ref.group(6).strip())
print("[ok] llms.txt: %d entradas de conocimiento · separador %r · con descripcion: %s"
      % (len(cono), sep, tiene_desc))

destino = None
for i, m in cono:
    if m.group(4).rstrip("/") > SLUG:
        destino = i
        break
if destino is None:
    destino = cono[-1][0] + 1

nueva = "%s[%s](%s)" % (ref.group(1), TITULO, URL)
if tiene_desc:
    nueva += "%s%s" % (sep, DESCRIPCION)
print("[ok] llms.txt: inserto en linea %d" % (destino + 1))
print("     %s" % nueva)

print("\nVERIFICACION COMPLETA. Procedo a escribir.\n")


# ================================================================ FASE 2: BACKUP

print("=" * 62)
print("FASE 2 — BACKUP")
print("=" * 62)

os.makedirs(DIR_BACKUP, exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
for src in (PATH_ART, PATH_LLMS):
    dst = os.path.join(DIR_BACKUP, "%s_%s" % (stamp, src.replace(REPO + "/", "").replace("/", "_")))
    shutil.copy2(src, dst)
    print("[backup] %s" % dst)


# ================================================================ FASE 3: ESCRIBIR

print("\n" + "=" * 62)
print("FASE 3 — ESCRITURA")
print("=" * 62)

html_nuevo = html.replace(ANCLA_GA4, ANCLA_GA4 + GA4, 1)
html_nuevo = html_nuevo.replace("og-n2n.png", "og-n2n.jpg")
html_nuevo = html_nuevo.replace("carlos-petit.png", "carlos-petit.jpg")
with open(PATH_ART, "w", encoding="utf-8") as f:
    f.write(html_nuevo)
print("[escrito] GA4 + rutas de imagen en %s" % PATH_ART)

lineas.insert(destino, nueva)
with open(PATH_LLMS, "w", encoding="utf-8") as f:
    f.write("\n".join(lineas))
print("[escrito] entrada agregada a llms.txt")


# ================================================================ FASE 4: GUARDAS

print("\n" + "=" * 62)
print("FASE 4 — GUARDAS POSTERIORES")
print("=" * 62)

ok = True
h = open(PATH_ART, encoding="utf-8").read()

c = h.count("G-07T9PCBG7P")
print("[%s] GA4 presente: %d referencia(s) (esperado 2)" % ("ok" if c == 2 else "FALLO", c))
ok = ok and c == 2

for viejo in ("og-n2n.png", "carlos-petit.png"):
    c = h.count(viejo)
    print("[%s] %s residual: %d" % ("ok" if c == 0 else "FALLO", viejo, c))
    ok = ok and c == 0

c = h.count("og-n2n.jpg")
print("[%s] og-n2n.jpg: %d (esperado 2)" % ("ok" if c == 2 else "FALLO", c))
ok = ok and c == 2

c = h.count("carlos-petit.jpg")
print("[%s] carlos-petit.jpg: %d (esperado 1)" % ("ok" if c == 1 else "FALLO", c))
ok = ok and c == 1

c = open(PATH_LLMS, encoding="utf-8").read().count(URL)
print("[%s] URL en llms.txt: %d (esperado 1)" % ("ok" if c == 1 else "FALLO", c))
ok = ok and c == 1

print("\n" + ("LISTO. Correr los dos auditores." if ok
              else "HAY FALLOS. Restaurar desde ~/backups/."))
