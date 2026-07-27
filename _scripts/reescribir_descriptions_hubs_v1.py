#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reescribir_descriptions_hubs_v1.py

Reescribe las 7 meta description cortas de las hub pages y sincroniza
og:description con el nuevo valor.

NO toca: /legal/ (es noindex, su description no se muestra nunca), ni las
descriptions largas, ni titles, ni h1, ni JSON-LD, ni el <header>.

Fases:
  0. Backup verificable del repo completo fuera del repo
  1. Validacion de las 7 paginas SIN escribir nada
  2. Escritura solo si la fase 1 pasa entera
  3. Verificacion posterior, incluido el rango 120-158 chars

Idempotente: correrlo dos veces no cambia nada la segunda vez.
Uso: ejecutar desde la raiz del repo n2n-site.
"""

import os
import re
import sys
import time
import tarfile

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"
BACKUP_DIR = "/home/dflorida/GITHUB/n2n"

MIN_CHARS = 120
MAX_CHARS = 158

# ruta_archivo : (description_vieja, description_nueva)
DESCRIPCIONES = {
    "casos/index.html": (
        "Casos de arquitectura comercial digital en operaciones industriales latinoamericanas.",
        "Casos reales de arquitectura comercial digital en operaciones industriales de LatAm: "
        "qu\u00e9 se intervino, qu\u00e9 cambi\u00f3 y qu\u00e9 resultado dej\u00f3 en la operaci\u00f3n.",
    ),
    "comparar/index.html": (
        "An\u00e1lisis estructurales: arquitectura comercial digital vs ecommerce, SaaS y agencias.",
        "An\u00e1lisis estructural de la Arquitectura Comercial Digital frente a ecommerce B2B, "
        "plataformas SaaS y agencias digitales: qu\u00e9 resuelve cada enfoque.",
    ),
    "conocimiento/index.html": (
        "Documentos t\u00e9cnicos sobre arquitectura comercial digital para B2B industrial.",
        "Documentos t\u00e9cnicos sobre arquitectura comercial digital para B2B industrial: "
        "calificaci\u00f3n, precios por volumen, integraci\u00f3n con ERP y portales.",
    ),
    "contacto/index.html": (
        "Contacto para evaluaci\u00f3n de operaciones industriales B2B.",
        "Contacto con N2N para evaluar una operaci\u00f3n industrial B2B. Diagn\u00f3stico pago de "
        "entrada, alcance definido y plazo cerrado antes de empezar.",
    ),
    "framework/index.html": (
        "El framework N2N para arquitectura comercial digital industrial.",
        "El framework N2N de arquitectura comercial digital industrial: por qu\u00e9 vender por "
        "volumen define la estrategia y qu\u00e9 componentes la sostienen.",
    ),
    "industrias/index.html": (
        "N2N para manufactura, distribuci\u00f3n y log\u00edstica industrial.",
        "Arquitectura comercial digital para manufactura, distribuci\u00f3n mayorista y operadores "
        "log\u00edsticos: c\u00f3mo cambia el enfoque seg\u00fan la operaci\u00f3n.",
    ),
    "servicios/index.html": (
        "Tres capas de intervenci\u00f3n en arquitectura comercial digital B2B industrial.",
        "Las tres capas de intervenci\u00f3n de N2N: dise\u00f1o de arquitectura comercial, desarrollo "
        "de plataformas B2B y consultor\u00eda de infraestructura.",
    ),
}

RE_CONTENT = re.compile(r'(content\s*=\s*)(["\'])(.*?)\2', re.S | re.I)


def meta_regex(clave):
    return re.compile(
        r'<meta\b[^>]*\b(?:name|property)\s*=\s*["\']' + re.escape(clave) + r'["\'][^>]*>',
        re.I,
    )


RE_DESC = meta_regex("description")
RE_OGDESC = meta_regex("og:description")
RE_TWDESC = meta_regex("twitter:description")


def leer(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def escribir(path, contenido):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(contenido)


def contenido_de(tag):
    m = RE_CONTENT.search(tag)
    return m.group(3) if m else None


def set_contenido(tag, valor):
    def _sub(m):
        return m.group(1) + m.group(2) + valor + m.group(2)
    return RE_CONTENT.sub(_sub, tag, count=1)


def solo_description(html):
    """Devuelve los <meta description> excluyendo og:description y twitter."""
    return [t for t in RE_DESC.findall(html)
            if not re.search(r'["\'](?:og|twitter):description["\']', t, re.I)]


def fase_0_backup():
    print("=" * 74)
    print("FASE 0 - BACKUP")
    print("=" * 74)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(BACKUP_DIR, "n2n-site-backup-desc-%s.tar.gz" % stamp)

    if os.path.exists(destino):
        print("ABORTA: el backup ya existe -> %s" % destino)
        sys.exit(1)

    incluidos = 0
    with tarfile.open(destino, "w:gz") as tar:
        for raiz, dirs, files in os.walk(REPO):
            dirs[:] = [d for d in dirs if d != ".git"]
            for f in files:
                completo = os.path.join(raiz, f)
                rel = os.path.relpath(completo, REPO)
                tar.add(completo, arcname=rel)
                incluidos += 1

    with tarfile.open(destino, "r:gz") as tar:
        nombres = set(tar.getnames())
    verificados = len(nombres)

    print("Archivo     : %s" % destino)
    print("Tamano      : %d KB" % (os.path.getsize(destino) // 1024))
    print("Empaquetados: %d" % incluidos)
    print("Verificados : %d" % verificados)

    if verificados != incluidos or verificados == 0:
        print("ABORTA: el backup no verifica.")
        sys.exit(1)

    faltan = [p for p in sorted(DESCRIPCIONES) if p not in nombres]
    if faltan:
        print("ABORTA: faltan archivos en el backup: %s" % faltan)
        sys.exit(1)

    print("Backup OK - las 7 paginas estan dentro del tarball.")
    print("")
    return destino


def fase_1_validar():
    print("=" * 74)
    print("FASE 1 - VALIDACION (no se escribe nada)")
    print("=" * 74)

    errores = []
    plan = {}

    for rel, (viejo, nuevo) in sorted(DESCRIPCIONES.items()):
        path = os.path.join(REPO, rel)

        if not os.path.isfile(path):
            errores.append("%s : NO EXISTE" % rel)
            continue

        largo = len(nuevo)
        if largo < MIN_CHARS or largo > MAX_CHARS:
            errores.append("%s : la nueva description mide %d chars (rango %d-%d)"
                           % (rel, largo, MIN_CHARS, MAX_CHARS))
            continue

        if '"' in nuevo or "&" in nuevo or "<" in nuevo:
            errores.append("%s : la nueva description tiene caracteres que rompen el atributo" % rel)
            continue

        html = leer(path)

        descs = solo_description(html)
        if len(descs) != 1:
            errores.append("%s : %d etiquetas meta description (se esperaba 1)" % (rel, len(descs)))
            continue

        actual = contenido_de(descs[0])
        if actual is None:
            errores.append("%s : meta description sin atributo content" % rel)
            continue

        if actual == viejo:
            estado = "cambia"
        elif actual == nuevo:
            estado = "ya aplicado"
        else:
            errores.append("%s : meta description inesperada -> %r" % (rel, actual))
            continue

        ogs = RE_OGDESC.findall(html)
        if len(ogs) != 1:
            errores.append("%s : %d etiquetas og:description (se esperaba 1)" % (rel, len(ogs)))
            continue
        og_actual = contenido_de(ogs[0])
        if og_actual is None:
            errores.append("%s : og:description sin atributo content" % rel)
            continue

        tws = RE_TWDESC.findall(html)
        if len(tws) > 1:
            errores.append("%s : %d etiquetas twitter:description (maximo 1)" % (rel, len(tws)))
            continue
        tw_actual = contenido_de(tws[0]) if tws else None
        if tws and tw_actual is None:
            errores.append("%s : twitter:description sin atributo content" % rel)
            continue

        plan[rel] = {
            "nuevo": nuevo,
            "desc_tag": descs[0],
            "og_tag": ogs[0],
            "og_actual": og_actual,
            "tw_tag": tws[0] if tws else None,
            "tw_actual": tw_actual,
        }

        marca_og = "=" if og_actual == nuevo else (">" if og_actual == actual else "!")
        marca_tw = "-" if tw_actual is None else ("=" if tw_actual == nuevo else ">")
        print("%-22s desc:%-11s og:%s tw:%s  (%d chars)"
              % (rel.replace("/index.html", "/"), estado, marca_og, marca_tw, largo))

    print("")
    print("Paginas en el plan: %d de %d" % (len(plan), len(DESCRIPCIONES)))
    print("Leyenda:  = ya sincronizada   > coincide con la vieja   ! divergia de antes   - no existe")

    if errores:
        print("")
        print("--- ERRORES ---")
        for e in errores:
            print("  " + e)
        print("")
        print("ABORTA: no se escribio ningun archivo.")
        sys.exit(1)

    if len(plan) != len(DESCRIPCIONES):
        print("ABORTA: el plan no cubre las 7 paginas.")
        sys.exit(1)

    print("Validacion OK.")
    print("")
    return plan


def fase_2_escribir(plan):
    print("=" * 74)
    print("FASE 2 - ESCRITURA")
    print("=" * 74)

    tocados = 0
    sin_cambio = 0

    for rel in sorted(plan):
        info = plan[rel]
        path = os.path.join(REPO, rel)
        html = leer(path)
        original = html
        nuevo = info["nuevo"]

        html = html.replace(info["desc_tag"], set_contenido(info["desc_tag"], nuevo), 1)

        if info["og_actual"] != nuevo:
            html = html.replace(info["og_tag"], set_contenido(info["og_tag"], nuevo), 1)

        if info["tw_tag"] is not None and info["tw_actual"] != nuevo:
            html = html.replace(info["tw_tag"], set_contenido(info["tw_tag"], nuevo), 1)

        if html == original:
            sin_cambio += 1
            print("  sin cambios : %s" % rel)
            continue

        escribir(path, html)
        tocados += 1
        print("  escrito     : %s" % rel)

    print("")
    print("Archivos escritos: %d" % tocados)
    print("Sin cambios      : %d" % sin_cambio)
    print("")


def fase_3_verificar():
    print("=" * 74)
    print("FASE 3 - VERIFICACION POST-ESCRITURA")
    print("=" * 74)

    fallas = []
    for rel, (viejo, nuevo) in sorted(DESCRIPCIONES.items()):
        html = leer(os.path.join(REPO, rel))

        descs = solo_description(html)
        if len(descs) != 1 or contenido_de(descs[0]) != nuevo:
            fallas.append("%s : meta description no quedo aplicada" % rel)
            continue

        ogs = RE_OGDESC.findall(html)
        if len(ogs) != 1 or contenido_de(ogs[0]) != nuevo:
            fallas.append("%s : og:description desincronizada" % rel)
            continue

        tws = RE_TWDESC.findall(html)
        if tws and contenido_de(tws[0]) != nuevo:
            fallas.append("%s : twitter:description desincronizada" % rel)
            continue

        largo = len(nuevo)
        if largo < MIN_CHARS or largo > MAX_CHARS:
            fallas.append("%s : %d chars fuera de rango" % (rel, largo))

    if fallas:
        print("--- FALLAS ---")
        for f in fallas:
            print("  " + f)
        print("")
        print("RESTAURAR desde el tarball de la fase 0.")
        sys.exit(1)

    largos = [len(v[1]) for v in DESCRIPCIONES.values()]
    print("7/7 descriptions aplicadas y sincronizadas con og:description.")
    print("Largo minimo: %d chars   maximo: %d chars   (rango %d-%d)"
          % (min(largos), max(largos), MIN_CHARS, MAX_CHARS))
    print("")
    print("SIGUIENTE: python3 diagnostico_sitio_v2.py")
    print("")


def main():
    if os.path.realpath(os.getcwd()) != os.path.realpath(REPO):
        print("ABORTA: ejecutar desde %s" % REPO)
        sys.exit(1)

    if not os.path.isfile(os.path.join(REPO, "diagnostico_sitio_v2.py")):
        print("ABORTA: no se encuentra diagnostico_sitio_v2.py en la raiz.")
        sys.exit(1)

    fase_0_backup()
    plan = fase_1_validar()
    fase_2_escribir(plan)
    fase_3_verificar()


if __name__ == "__main__":
    main()
