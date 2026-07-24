#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
actualizar_readme_scripts_v1.py

Reemplaza la tabla "Scripts en la raiz" del README por la version completa,
que incluye diagnostico_sitio_v3.py y los scripts sumados en la sesion.

Backup del README fuera del repo antes de escribir. Idempotente: si la
tabla ya esta actualizada, sale sin tocar nada.
"""

import os
import sys
import time

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"
README = os.path.join(REPO, "README.md")

INICIO = "## Scripts en la raiz"
FIN = "## Desarrollado por"

MARCA_NUEVA = "diagnostico_sitio_v3.py"

TABLA = """## Scripts en la raiz

Auditor vigente: `diagnostico_sitio_v3.py`. Correr antes de cada commit.

| Script | Funcion |
|---|---|
| `diagnostico_sitio_v3.py` | Auditor read-only vigente. Umbrales alineados al criterio editorial (title <= 62, description 120-158), auditoria de sincronizacion de og y twitter, robots.txt completo. |
| `diagnostico_sitio_v2.py` | Auditor anterior. Se conserva para comparar salidas. Umbrales 60 / 100-160 y sin chequeo de sincronizacion. |
| `acortar_titles_v1.py` | Acorto 25 titles que se truncaban en SERP y sincronizo og:title / twitter:title. |
| `reescribir_descriptions_hubs_v1.py` | Reescribio las 7 descriptions cortas de las hub pages al rango 120-158. |
| `exportar_descriptions_largas_v1.py` | Read-only. Vuelca a Markdown las descriptions que superan el maximo, para trabajarlas fuera del repo. |
| `aplicar_descriptions_largas_v1.py` | Reescribio 28 descriptions largas al rango y sincronizo og y twitter. |
| `insertar_diagnosticos_precios_v1.py` | Inserto en /precios/ el bloque con las dos entradas de precio fijo. Saco a /mvp-start/ y /control/protocolo-cero/ de huerfanas. |
| `agregar_twitter_nosotros_v1.py` | Agrego twitter:title y twitter:description a /nosotros/, la unica pagina que no los tenia. |

Todos los scripts de escritura siguen el mismo patron: backup verificable,
validacion sin escribir, escritura, verificacion posterior. Son idempotentes
y abortan ante cualquier estado inesperado.

"""


def main():
    if not os.path.isfile(README):
        print("ABORTA: no existe %s" % README)
        sys.exit(1)

    with open(README, "r", encoding="utf-8") as fh:
        contenido = fh.read()

    if MARCA_NUEVA in contenido:
        print("La tabla ya esta actualizada. No se modifica nada.")
        sys.exit(0)

    for ancla in (INICIO, FIN):
        if contenido.count(ancla) != 1:
            print("ABORTA: el ancla %r aparece %d veces (se esperaba 1)."
                  % (ancla, contenido.count(ancla)))
            sys.exit(1)

    i = contenido.index(INICIO)
    j = contenido.index(FIN)
    if j <= i:
        print("ABORTA: las anclas estan en orden inesperado.")
        sys.exit(1)

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup = os.path.normpath(os.path.join(REPO, "..", "README-backup-%s.md" % stamp))
    with open(backup, "w", encoding="utf-8") as fh:
        fh.write(contenido)

    if os.path.getsize(backup) != len(contenido.encode("utf-8")):
        print("ABORTA: el backup del README no verifica.")
        sys.exit(1)
    print("Backup: %s (%d bytes)" % (backup, os.path.getsize(backup)))

    nuevo = contenido[:i] + TABLA + contenido[j:]

    with open(README, "w", encoding="utf-8") as fh:
        fh.write(nuevo)

    with open(README, "r", encoding="utf-8") as fh:
        verif = fh.read()

    fallas = []
    if MARCA_NUEVA not in verif:
        fallas.append("la tabla nueva no quedo escrita")
    if verif.count(INICIO) != 1 or verif.count(FIN) != 1:
        fallas.append("las anclas quedaron duplicadas o se perdieron")
    if "## Criterio editorial" not in verif:
        fallas.append("se perdio la seccion de criterio editorial")

    if fallas:
        print("--- FALLAS ---")
        for f in fallas:
            print("  " + f)
        print("RESTAURAR desde %s" % backup)
        sys.exit(1)

    print("README actualizado: %+d bytes" % (len(verif) - len(contenido)))
    print("Tabla de scripts: 8 entradas.")


if __name__ == "__main__":
    main()
