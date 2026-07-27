#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exportar_descriptions_largas_v1.py

READ-ONLY. No modifica ningun archivo del sitio.

Lee las meta description que superan 158 caracteres y las vuelca a un
Markdown en ~/Descargas para trabajarlas fuera del repo.

Salida: /home/dflorida/Descargas/descriptions-largas.md
"""

import os
import re
import sys
import time

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"
SALIDA = "/home/dflorida/Descargas/descriptions-largas.md"

MIN_CHARS = 120
MAX_CHARS = 158
ESPERADAS = 30

RE_CONTENT = re.compile(r'(content\s*=\s*)(["\'])(.*?)\2', re.S | re.I)
RE_META_DESC = re.compile(
    r'<meta\b[^>]*\b(?:name|property)\s*=\s*["\']description["\'][^>]*>', re.I
)
RE_NOINDEX = re.compile(r'<meta\b[^>]*\bname\s*=\s*["\']robots["\'][^>]*noindex[^>]*>', re.I)


def contenido_de(tag):
    m = RE_CONTENT.search(tag)
    return m.group(3) if m else None


def ruta_publica(rel):
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def recolectar():
    filas = []
    for raiz, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            completo = os.path.join(raiz, f)
            rel = os.path.relpath(completo, REPO)

            with open(completo, "r", encoding="utf-8") as fh:
                html = fh.read()

            tags = RE_META_DESC.findall(html)
            if len(tags) != 1:
                continue

            desc = contenido_de(tags[0])
            if desc is None:
                continue

            largo = len(desc)
            if largo <= MAX_CHARS:
                continue

            filas.append({
                "ruta": ruta_publica(rel),
                "archivo": rel,
                "chars": largo,
                "texto": desc,
                "noindex": bool(RE_NOINDEX.search(html)),
            })

    filas.sort(key=lambda x: x["ruta"])
    return filas


def main():
    if not os.path.isdir(REPO):
        print("ABORTA: no existe %s" % REPO)
        sys.exit(1)

    filas = recolectar()

    print("Descriptions con mas de %d chars: %d" % (MAX_CHARS, len(filas)))
    if len(filas) != ESPERADAS:
        print("AVISO: se esperaban %d. Revisar antes de usar el archivo." % ESPERADAS)

    lineas = []
    lineas.append("# Descriptions largas — n2n.com.ar")
    lineas.append("")
    lineas.append("Generado: %s" % time.strftime("%Y-%m-%d %H:%M"))
    lineas.append("")
    lineas.append("Volcado del estado actual. Rango objetivo: %d-%d caracteres."
                  % (MIN_CHARS, MAX_CHARS))
    lineas.append("Este archivo no modifica nada: es material de trabajo, vive fuera del repo.")
    lineas.append("")
    lineas.append("Total: **%d** paginas." % len(filas))
    lineas.append("")
    lineas.append("---")
    lineas.append("")
    lineas.append("## Indice")
    lineas.append("")
    lineas.append("| # | Ruta | Chars | Sobra |")
    lineas.append("|---|---|---|---|")
    for i, fila in enumerate(filas, 1):
        lineas.append("| %d | `%s` | %d | +%d |"
                      % (i, fila["ruta"], fila["chars"], fila["chars"] - MAX_CHARS))
    lineas.append("")
    lineas.append("---")
    lineas.append("")

    for i, fila in enumerate(filas, 1):
        marca = "  · `noindex`" if fila["noindex"] else ""
        lineas.append("## %d. `%s`" % (i, fila["ruta"]))
        lineas.append("")
        lineas.append("`%s` · **%d chars** (sobran %d)%s"
                      % (fila["archivo"], fila["chars"], fila["chars"] - MAX_CHARS, marca))
        lineas.append("")
        lineas.append("**Actual:**")
        lineas.append("")
        lineas.append("> %s" % fila["texto"])
        lineas.append("")

    contenido = "\n".join(lineas) + "\n"

    with open(SALIDA, "w", encoding="utf-8") as fh:
        fh.write(contenido)

    with open(SALIDA, "r", encoding="utf-8") as fh:
        verif = fh.read()

    if verif != contenido:
        print("ABORTA: la escritura del Markdown no verifica.")
        sys.exit(1)

    print("Archivo: %s" % SALIDA)
    print("Tamano : %d bytes" % os.path.getsize(SALIDA))
    print("Rango  : %d a %d chars"
          % (min(f["chars"] for f in filas), max(f["chars"] for f in filas)))
    print("El repo no fue modificado.")


if __name__ == "__main__":
    main()
