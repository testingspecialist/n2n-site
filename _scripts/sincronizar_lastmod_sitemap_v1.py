#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sincronizar_lastmod_sitemap_v1.py

Actualiza el lastmod de cada URL del sitemap con la fecha real del ultimo
commit que toco ese archivo.

Por que importa: 36 de las 42 URLs declaraban lastmod 2026-06-19, pero 25
de ellas se modificaron despues. El sitemap le estaba diciendo a Google que
no habia cambiado nada, que es exactamente lo que impide que rastree de
nuevo las paginas en estado "Descubierta: actualmente sin indexar".

No pone la fecha de hoy en todas: eso es una señal falsa y los buscadores
la descuentan. Usa `git log -1 --format=%cs` por archivo, que es la fecha
verificable del ultimo cambio real.

Read-only sobre el resto del repo: solo reescribe sitemap.xml.

Aborta sin escribir si alguna URL no resuelve a un archivo, si git no
devuelve fecha, o si cambia la cantidad de URLs.

Uso:
    python3 _scripts/sincronizar_lastmod_sitemap_v1.py
"""

import os
import re
import shutil
import subprocess
import sys

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"
SITEMAP = os.path.join(REPO, "sitemap.xml")
BASE = "https://n2n.com.ar"


def fail(msg):
    print("ABORTADO: %s" % msg)
    sys.exit(1)


def archivo_de(url_path):
    """Traduce /casos/caso-01/ -> casos/caso-01/index.html"""
    rel = url_path.strip("/")
    if not rel:
        return "index.html"
    return os.path.join(rel, "index.html")


def fecha_git(rel):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=REPO, capture_output=True, text=True, timeout=20)
    except Exception as e:
        fail("git fallo sobre %s: %s" % (rel, e))
    if out.returncode != 0:
        fail("git devolvio codigo %d sobre %s" % (out.returncode, rel))
    fecha = out.stdout.strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
        fail("git no devolvio fecha valida para %s: %r" % (rel, fecha))
    return fecha


def main():
    if not os.path.isdir(os.path.join(REPO, ".git")):
        fail("no parece un repo git: %s" % REPO)
    if not os.path.isfile(SITEMAP):
        fail("no existe %s" % SITEMAP)

    with open(SITEMAP, "r", encoding="utf-8") as f:
        xml = f.read()

    original = xml
    entradas = re.findall(
        r"<loc>%s([^<]*)</loc><lastmod>([^<]*)</lastmod>" % re.escape(BASE), xml)
    if not entradas:
        fail("no se pudo parsear ninguna entrada del sitemap")

    print("URLs en el sitemap: %d" % len(entradas))
    print("")

    cambios = 0
    sin_cambio = 0
    for url_path, lastmod_viejo in entradas:
        rel = archivo_de(url_path)
        if not os.path.isfile(os.path.join(REPO, rel)):
            fail("la URL %s no resuelve a un archivo (%s)" % (url_path, rel))

        nueva = fecha_git(rel)
        viejo_tag = ("<loc>%s%s</loc><lastmod>%s</lastmod>"
                     % (BASE, url_path, lastmod_viejo))
        nuevo_tag = ("<loc>%s%s</loc><lastmod>%s</lastmod>"
                     % (BASE, url_path, nueva))

        if xml.count(viejo_tag) != 1:
            fail("la entrada de %s aparece %d veces" % (url_path, xml.count(viejo_tag)))

        if nueva != lastmod_viejo:
            xml = xml.replace(viejo_tag, nuevo_tag, 1)
            print("  %-52s %s -> %s" % (url_path, lastmod_viejo, nueva))
            cambios += 1
        else:
            sin_cambio += 1

    # --- guardas
    if xml.count("<url>") != original.count("<url>"):
        fail("cambio la cantidad de <url>")
    if xml.count("<loc>") != len(entradas):
        fail("cambio la cantidad de <loc>")
    for viejo_frag in ("<urlset", "</urlset>"):
        if viejo_frag not in xml:
            fail("se rompio la estructura del sitemap: falta %s" % viejo_frag)

    print("")
    print("Actualizadas: %d | sin cambio: %d" % (cambios, sin_cambio))

    if cambios == 0:
        print("Nada que escribir.")
        return

    shutil.copy2(SITEMAP, SITEMAP + ".bak")
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(xml)

    print("Escrito: sitemap.xml (%d bytes, antes %d)" % (len(xml), len(original)))
    print("Backup .bak junto al archivo (borrar tras validar).")
    print("LISTO")


if __name__ == "__main__":
    main()
