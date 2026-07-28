#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registrar_scripts_readme_v1.py

Agrega a la tabla de scripts del README.md las dos entradas del hilo de hoy:
  - crear_articulo_faltante_no_atribuible_v2.py
  - corregir_head_faltante_no_atribuible_v1.py

Inserta despues de la ultima fila existente de la tabla, respetando el formato.

Ejecutar desde la raiz del repo:
  python3 _scripts/registrar_scripts_readme_v1.py
"""

import os
import shutil
import sys
from datetime import datetime

REPO = os.getcwd()
PATH_README = os.path.join(REPO, "README.md")
DIR_BACKUP = os.path.expanduser("~/backups")

ANCLA = "| `reescribir_titles_intencion_v1.py` |"

FILAS = [
    "| `crear_articulo_faltante_no_atribuible_v2.py` | Publico "
    "/conocimiento/faltante-no-atribuible/, primer articulo del eje Control en el hub de "
    "conocimiento. Ancla el pilar 05 (integracion con sistemas operativos) y enlaza a "
    "protocolo-cero, caso-01 y glosario, que tenian un solo enlace entrante. Alta en el indice "
    "y en el sitemap. |",
    "| `corregir_head_faltante_no_atribuible_v1.py` | Cerro los 3 fallos del articulo nuevo mas "
    "el alta en llms.txt: bloque GA4 ausente y rutas og-n2n.png y carlos-petit.png que en el repo "
    "son .jpg. Origen del defecto: la plantilla del skill de publicacion esta desactualizada. |",
]


def abortar(msg):
    print("ABORTADO: %s" % msg)
    sys.exit(1)


print("=" * 62)
print("FASE 1 — VERIFICACION")
print("=" * 62)

if not os.path.isdir(os.path.join(REPO, ".git")):
    abortar("no estas en la raiz del repo")
if not os.path.isfile(PATH_README):
    abortar("falta README.md")

texto = open(PATH_README, encoding="utf-8").read()

for f in FILAS:
    nombre = f.split("`")[1]
    if nombre in texto:
        abortar("%s ya figura en el README" % nombre)

lineas = texto.split("\n")
idx = [i for i, l in enumerate(lineas) if l.startswith(ANCLA)]
if len(idx) != 1:
    abortar("esperaba 1 fila ancla, encontre %d" % len(idx))
destino = idx[0] + 1
print("[ok] ancla en linea %d · inserto %d filas" % (idx[0] + 1, len(FILAS)))

n_filas_antes = sum(1 for l in lineas if l.startswith("| `") and l.endswith("|"))
print("[ok] %d filas de script en la tabla" % n_filas_antes)

print("\n" + "=" * 62)
print("FASE 2 — BACKUP")
print("=" * 62)
os.makedirs(DIR_BACKUP, exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
dst = os.path.join(DIR_BACKUP, "%s_README.md" % stamp)
shutil.copy2(PATH_README, dst)
print("[backup] %s" % dst)

print("\n" + "=" * 62)
print("FASE 3 — ESCRITURA")
print("=" * 62)
for offset, fila in enumerate(FILAS):
    lineas.insert(destino + offset, fila)
with open(PATH_README, "w", encoding="utf-8") as f:
    f.write("\n".join(lineas))
print("[escrito] %d filas agregadas" % len(FILAS))

print("\n" + "=" * 62)
print("FASE 4 — GUARDAS")
print("=" * 62)
t = open(PATH_README, encoding="utf-8").read()
ok = True
for fila in FILAS:
    nombre = fila.split("`")[1]
    c = t.count(nombre)
    print("[%s] %s: %d ocurrencia(s)" % ("ok" if c == 1 else "FALLO", nombre, c))
    ok = ok and c == 1

n_ahora = sum(1 for l in t.split("\n") if l.startswith("| `") and l.endswith("|"))
esperado = n_filas_antes + len(FILAS)
print("[%s] filas de script: %d (antes %d)" % ("ok" if n_ahora == esperado else "FALLO",
                                               n_ahora, n_filas_antes))
ok = ok and n_ahora == esperado

print("\n" + ("LISTO." if ok else "HAY FALLOS. Restaurar desde ~/backups/."))
