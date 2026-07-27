#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
documentar_titles_readme_v1.py

Agrega al README.md la seccion de criterio editorial de <title> y la nota
sobre acortar_titles_v1.py.

Backup del README antes de escribir. Idempotente: si la seccion ya existe,
no duplica y sale sin tocar nada.
"""

import os
import sys
import time

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"
README = os.path.join(REPO, "README.md")

ANCLA = "## Desarrollado por"

SECCION = """## Criterio editorial — titles y metadatos

- `<title>` de maximo 62 caracteres. Google trunca alrededor de los 60 y un
  title cortado rompe la linea clickeable del resultado.
- Sin sufijo de marca en el title. Agregar `— N2N` consume 7 de los 60
  caracteres disponibles y no aporta diferenciacion entre resultados propios.
- Sin capitalizacion tipo titulo: el espanol no la usa y ocupa mas ancho visual
  en el SERP.
- `og:title` y `twitter:title` siempre sincronizados con `<title>`. Si divergen,
  el sitio dice cosas distintas segun el canal.
- El `headline` del JSON-LD NO sigue al `<title>`: se alinea con el `<h1>` de la
  pagina, que es el titulo real del articulo.
- Las `meta description` largas quedan como aviso aceptado del diagnostico. El
  rango 120-158 es una referencia, no un fallo: Google reescribe la description
  en la mayoria de los resultados.

## Scripts en la raiz

| Script | Funcion |
|---|---|
| `diagnostico_sitio_v2.py` | Auditor read-only del sitio. Correr antes de cada commit. |
| `acortar_titles_v1.py` | Acorto 25 titles que se truncaban en SERP y sincronizo og:title / twitter:title. Idempotente. |

"""

MARCA = "## Criterio editorial — titles y metadatos"


def main():
    if not os.path.isfile(README):
        print("ABORTA: no existe %s" % README)
        sys.exit(1)

    with open(README, "r", encoding="utf-8") as fh:
        contenido = fh.read()

    if MARCA in contenido:
        print("La seccion ya existe. No se modifica nada.")
        sys.exit(0)

    if contenido.count(ANCLA) != 1:
        print("ABORTA: el ancla %r aparece %d veces (se esperaba 1)."
              % (ANCLA, contenido.count(ANCLA)))
        sys.exit(1)

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup = os.path.join(REPO, "..", "README-backup-%s.md" % stamp)
    backup = os.path.normpath(backup)
    with open(backup, "w", encoding="utf-8") as fh:
        fh.write(contenido)

    if not os.path.isfile(backup) or os.path.getsize(backup) != len(contenido.encode("utf-8")):
        print("ABORTA: el backup del README no verifica.")
        sys.exit(1)

    print("Backup: %s (%d bytes)" % (backup, os.path.getsize(backup)))

    nuevo = contenido.replace(ANCLA, SECCION + ANCLA, 1)

    with open(README, "w", encoding="utf-8") as fh:
        fh.write(nuevo)

    with open(README, "r", encoding="utf-8") as fh:
        verif = fh.read()

    if MARCA not in verif or ANCLA not in verif:
        print("ABORTA: la escritura no verifica. Restaurar desde %s" % backup)
        sys.exit(1)

    print("README actualizado: +%d bytes" % (len(verif) - len(contenido)))
    print("Secciones agregadas: criterio editorial de titles + tabla de scripts.")


if __name__ == "__main__":
    main()
