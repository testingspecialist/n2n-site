#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agregar_twitter_nosotros_v1.py

Agrega twitter:title y twitter:description a /nosotros/, la unica pagina
del sitio que tiene twitter:card pero no esos dos campos.

Los valores NO se hardcodean: se leen del propio <title> y de la propia
meta description del archivo, de modo que quedan sincronizados por
construccion.

NO toca: title, description, og:*, JSON-LD, header ni el cuerpo.

Fases: backup verificable -> validacion sin escribir -> escritura ->
verificacion posterior.

Idempotente. Ejecutar desde la raiz del repo n2n-site.
"""

import os
import re
import sys
import time
import tarfile

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"
BACKUP_DIR = "/home/dflorida/GITHUB/n2n"
OBJETIVO = "nosotros/index.html"

RX_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
RX_DESC = re.compile(r'<meta\s+name="description"\s+content="(.*?)">', re.S)
RX_TWCARD = re.compile(r'<meta\s+name="twitter:card"\s+content="[^"]*">')
RX_TWTITLE = re.compile(r'<meta\s+name="twitter:title"')
RX_TWDESC = re.compile(r'<meta\s+name="twitter:description"')


def leer(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def escribir(path, contenido):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(contenido)


def backup():
    print("=" * 74)
    print("FASE 0 - BACKUP")
    print("=" * 74)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(BACKUP_DIR, "n2n-site-backup-nosotros-%s.tar.gz" % stamp)

    if os.path.exists(destino):
        print("ABORTA: el backup ya existe -> %s" % destino)
        sys.exit(1)

    incluidos = 0
    with tarfile.open(destino, "w:gz") as tar:
        for raiz, dirs, files in os.walk(REPO):
            dirs[:] = [d for d in dirs if d != ".git"]
            for f in files:
                completo = os.path.join(raiz, f)
                tar.add(completo, arcname=os.path.relpath(completo, REPO))
                incluidos += 1

    with tarfile.open(destino, "r:gz") as tar:
        nombres = set(tar.getnames())

    print("Archivo     : %s" % destino)
    print("Tamano      : %d KB" % (os.path.getsize(destino) // 1024))
    print("Empaquetados: %d" % incluidos)
    print("Verificados : %d" % len(nombres))

    if len(nombres) != incluidos or OBJETIVO not in nombres:
        print("ABORTA: el backup no verifica.")
        sys.exit(1)

    print("Backup OK.")
    print("")


def main():
    if os.path.realpath(os.getcwd()) != os.path.realpath(REPO):
        print("ABORTA: ejecutar desde %s" % REPO)
        sys.exit(1)

    path = os.path.join(REPO, OBJETIVO)
    if not os.path.isfile(path):
        print("ABORTA: no existe %s" % path)
        sys.exit(1)

    html = leer(path)

    if RX_TWTITLE.search(html) and RX_TWDESC.search(html):
        print("Ya existen twitter:title y twitter:description. No se modifica nada.")
        sys.exit(0)

    backup()

    print("=" * 74)
    print("FASE 1 - VALIDACION (no se escribe nada)")
    print("=" * 74)

    errores = []

    titles = RX_TITLE.findall(html)
    if len(titles) != 1:
        errores.append("%d etiquetas <title> (se esperaba 1)" % len(titles))
    descs = RX_DESC.findall(html)
    if len(descs) != 1:
        errores.append("%d meta description (se esperaba 1)" % len(descs))
    cards = RX_TWCARD.findall(html)
    if len(cards) != 1:
        errores.append("%d etiquetas twitter:card (se esperaba 1)" % len(cards))
    if RX_TWTITLE.search(html):
        errores.append("ya existe twitter:title")
    if RX_TWDESC.search(html):
        errores.append("ya existe twitter:description")

    if errores:
        print("--- ERRORES ---")
        for e in errores:
            print("  " + e)
        print("")
        print("ABORTA: no se escribio nada.")
        sys.exit(1)

    titulo = titles[0].strip()
    desc = descs[0].strip()

    for etiqueta, valor in (("<title>", titulo), ("description", desc)):
        if '"' in valor:
            print("ABORTA: %s contiene comillas dobles, romperia el atributo." % etiqueta)
            sys.exit(1)

    print("twitter:card       : presente")
    print("twitter:title      -> %s" % titulo)
    print("twitter:description-> %s" % desc)
    print("Validacion OK.")
    print("")

    print("=" * 74)
    print("FASE 2 - ESCRITURA")
    print("=" * 74)

    nuevas = ('\n<meta name="twitter:title" content="%s">'
              '\n<meta name="twitter:description" content="%s">') % (titulo, desc)

    nuevo = html.replace(cards[0], cards[0] + nuevas, 1)
    escribir(path, nuevo)
    print("  escrito     : %s  (+%d bytes)" % (OBJETIVO, len(nuevo) - len(html)))
    print("")

    print("=" * 74)
    print("FASE 3 - VERIFICACION POST-ESCRITURA")
    print("=" * 74)

    verif = leer(path)
    fallas = []

    tw_t = re.findall(r'<meta\s+name="twitter:title"\s+content="(.*?)">', verif, re.S)
    tw_d = re.findall(r'<meta\s+name="twitter:description"\s+content="(.*?)">', verif, re.S)

    if len(tw_t) != 1 or tw_t[0] != titulo:
        fallas.append("twitter:title no quedo aplicado o no coincide con <title>")
    if len(tw_d) != 1 or tw_d[0] != desc:
        fallas.append("twitter:description no quedo aplicado o no coincide con la description")
    if RX_TITLE.findall(verif) != titles:
        fallas.append("el <title> cambio")
    if RX_DESC.findall(verif) != descs:
        fallas.append("la meta description cambio")
    if verif.count("<div") != verif.count("</div>"):
        fallas.append("etiquetas <div> desbalanceadas")
    if verif.count("<h1") != 1:
        fallas.append("la pagina quedo con %d h1" % verif.count("<h1"))

    if fallas:
        print("--- FALLAS ---")
        for f in fallas:
            print("  " + f)
        print("")
        print("RESTAURAR desde el tarball de la fase 0.")
        sys.exit(1)

    print("twitter:title y twitter:description agregados y sincronizados.")
    print("title, description y og:* sin cambios.")
    print("")
    print("SIGUIENTE: python3 diagnostico_sitio_v3.py")
    print("")


if __name__ == "__main__":
    main()
