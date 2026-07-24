#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
insertar_diagnosticos_precios_v1.py

Inserta en /precios/ un bloque con las dos entradas de precio fijo:
N2N MVP Start y Protocolo CERO. Con esto ambas paginas dejan de estar
huerfanas sin tocar el <header>.

NO toca: el <header>, el nav, /mvp-start/, /control/protocolo-cero/,
metadatos, JSON-LD ni ninguna otra pagina.

Punto de insercion: inmediatamente antes de la seccion final que abre con
el h2 "La cotizacion empieza por entender tu operacion".

Fases: backup verificable -> validacion sin escribir -> escritura ->
verificacion posterior.

Idempotente: si el bloque ya existe, sale sin tocar nada.
Ejecutar desde la raiz del repo n2n-site.
"""

import os
import re
import sys
import time
import tarfile

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"
BACKUP_DIR = "/home/dflorida/GITHUB/n2n"
OBJETIVO = "precios/index.html"

MARCA = 'id="diagnosticos-precio-fijo"'
ANCLA_H2 = "La cotización empieza por entender tu operación"

BLOQUE = """    <section class="section" id="diagnosticos-precio-fijo">
      <div class="wrap">
        <div class="section__head">
          <h2>Dos diagnósticos con precio fijo</h2>
          <p>La regla tiene dos excepciones: dos puntos de entrada con alcance cerrado, plazo definido y valor publicado.</p>
        </div>
        <div class="grid grid--2">
          <div class="card">
            <div class="card__tag">Eje Comercial</div>
            <h3 class="card__title">N2N MVP Start</h3>
            <p class="card__body">Diagnóstico comercial digital para industria B2B. Detecta dónde se pierde tiempo y margen en el circuito de consulta, cotización y pedido. 10 días hábiles.</p>
            <p class="card__body" style="margin-top:var(--s3);color:var(--navy);font-weight:600">USD 1.500 valor fijo.</p>
            <a href="/mvp-start/" class="card__link">Ver el diagnóstico &rarr;</a>
          </div>
          <div class="card">
            <div class="card__tag">Eje Control Operativo</div>
            <h3 class="card__title">Protocolo CERO</h3>
            <p class="card__body">Diagnóstico de pérdidas para distribuidoras de cadena de frío. Identifica puntos de fuga, estima la magnitud y define los controles faltantes. 2 a 3 semanas.</p>
            <p class="card__body" style="margin-top:var(--s3);color:var(--navy);font-weight:600">USD 1.500 valor fijo.</p>
            <a href="/control/protocolo-cero/" class="card__link">Ver el método &rarr;</a>
          </div>
        </div>
      </div>
    </section>

"""


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
    destino = os.path.join(BACKUP_DIR, "n2n-site-backup-precios-%s.tar.gz" % stamp)

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


def validar(html):
    print("=" * 74)
    print("FASE 1 - VALIDACION (no se escribe nada)")
    print("=" * 74)

    errores = []

    n_ancla = html.count(ANCLA_H2)
    if n_ancla != 1:
        errores.append("el ancla aparece %d veces (se esperaba 1)" % n_ancla)

    m = re.search(r'<section[^>]*>(?:(?!</section>).)*?' + re.escape(ANCLA_H2), html, re.S)
    if not m:
        errores.append("no se encontro la <section> que contiene el ancla")

    for ruta in ("/mvp-start/", "/control/protocolo-cero/"):
        if not os.path.isfile(os.path.join(REPO, ruta.strip("/"), "index.html")):
            errores.append("no existe la pagina destino %s" % ruta)
        if 'href="%s"' % ruta in html:
            errores.append("ya existe un link a %s en la pagina" % ruta)

    if "grid--2" not in html and "grid--3" not in html:
        errores.append("no se detecta el patron de grid de cards en la pagina")

    if errores:
        print("--- ERRORES ---")
        for e in errores:
            print("  " + e)
        print("")
        print("ABORTA: no se escribio nada.")
        sys.exit(1)

    inicio = m.start()
    print("Ancla encontrada. La <section> final arranca en el offset %d." % inicio)
    print("El bloque se inserta inmediatamente antes.")
    print("Links nuevos: /mvp-start/ y /control/protocolo-cero/")
    print("Validacion OK.")
    print("")
    return inicio


def main():
    if os.path.realpath(os.getcwd()) != os.path.realpath(REPO):
        print("ABORTA: ejecutar desde %s" % REPO)
        sys.exit(1)

    path = os.path.join(REPO, OBJETIVO)
    if not os.path.isfile(path):
        print("ABORTA: no existe %s" % path)
        sys.exit(1)

    html = leer(path)

    if MARCA in html:
        print("El bloque ya existe en /precios/. No se modifica nada.")
        sys.exit(0)

    backup()
    inicio = validar(html)

    print("=" * 74)
    print("FASE 2 - ESCRITURA")
    print("=" * 74)

    nuevo = html[:inicio] + BLOQUE + html[inicio:]
    escribir(path, nuevo)
    print("  escrito     : %s  (+%d bytes)" % (OBJETIVO, len(nuevo) - len(html)))
    print("")

    print("=" * 74)
    print("FASE 3 - VERIFICACION POST-ESCRITURA")
    print("=" * 74)

    verif = leer(path)
    fallas = []

    if verif.count(MARCA) != 1:
        fallas.append("el bloque no quedo insertado una sola vez")
    for ruta in ("/mvp-start/", "/control/protocolo-cero/"):
        if verif.count('href="%s"' % ruta) != 1:
            fallas.append("el link a %s no quedo exactamente una vez" % ruta)
    if verif.count("<section") != verif.count("</section>"):
        fallas.append("las etiquetas <section> quedaron desbalanceadas")
    if verif.count("<div") != verif.count("</div>"):
        fallas.append("las etiquetas <div> quedaron desbalanceadas")
    if verif.count("<h1") != 1:
        fallas.append("la pagina quedo con %d h1" % verif.count("<h1"))
    if verif.count(ANCLA_H2) != 1:
        fallas.append("el ancla quedo duplicada")

    if fallas:
        print("--- FALLAS ---")
        for f in fallas:
            print("  " + f)
        print("")
        print("RESTAURAR desde el tarball de la fase 0.")
        sys.exit(1)

    print("Bloque insertado. Etiquetas balanceadas, un solo h1, un link a cada destino.")
    print("/mvp-start/ y /control/protocolo-cero/ dejan de estar huerfanas.")
    print("El <header> no fue modificado.")
    print("")
    print("SIGUIENTE: python3 diagnostico_sitio_v2.py")
    print("")


if __name__ == "__main__":
    main()
