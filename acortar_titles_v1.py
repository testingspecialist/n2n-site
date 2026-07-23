#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
acortar_titles_v1.py

Acorta los 25 <title> que se truncan en SERP y sincroniza og:title y
twitter:title con el nuevo valor en cada pagina.

NO toca: <h1>, JSON-LD, <header>, description, og:description, ni ninguna
otra parte del documento.

Fases:
  0. Backup verificable del repo completo fuera del repo
  1. Validacion de las 25 paginas SIN escribir nada
  2. Escritura solo si la fase 1 pasa entera

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

# ruta_archivo : (title_viejo, title_nuevo)
TITLES = {
    "casos/caso-01/index.html": (
        "Caso de Estudio: De planillas y llamados a un ecosistema operativo digital",
        "Caso: de planillas a un ecosistema operativo digital",
    ),
    "casos/caso-02/index.html": (
        "Caso de Estudio: Estructurar la Venta por Volumen con Arquitectura Digital",
        "Caso: arquitectura digital para venta por volumen",
    ),
    "casos/caso-03/index.html": (
        "Caso de Estudio: Plataforma B2B Integrada con ERP para Operaciones Industriales",
        "Caso: plataforma B2B industrial integrada con ERP",
    ),
    "comparar/custom-vs-saas/index.html": (
        "Arquitectura Digital Propia vs Plataformas SaaS para B2B Industrial",
        "Arquitectura digital propia vs SaaS en B2B industrial",
    ),
    "comparar/ecommerce-b2b-vs-arquitectura-comercial/index.html": (
        "Ecommerce B2B Industrial vs Arquitectura Comercial Digital: Diferencias Estructurales",
        "Ecommerce B2B vs Arquitectura Comercial Digital",
    ),
    "conocimiento/como-digitalizar-pedidos-distribuidora/index.html": (
        "C\u00f3mo digitalizar los pedidos de una distribuidora mayorista | N2N",
        "C\u00f3mo digitalizar los pedidos de una distribuidora mayorista",
    ),
    "conocimiento/guia-ceo-digital-industrial/index.html": (
        "Gu\u00eda para CEOs Industriales: Transformaci\u00f3n Digital Comercial en B2B",
        "Gu\u00eda para CEOs: transformaci\u00f3n digital comercial B2B",
    ),
    "conocimiento/integracion-erp/index.html": (
        "Integraci\u00f3n de ERP en Arquitectura Comercial Digital Industrial",
        "Integraci\u00f3n de ERP en arquitectura comercial digital",
    ),
    "conocimiento/marketing-despues-estructura/index.html": (
        "Cu\u00e1ndo el Marketing Tiene Sentido en la Estrategia Digital Industrial B2B",
        "Cu\u00e1ndo el marketing tiene sentido en la industria B2B",
    ),
    "conocimiento/playbook-gerente-ventas/index.html": (
        "C\u00f3mo los Gerentes de Ventas Industriales B2B Usan la Arquitectura Comercial Digital",
        "Playbook del gerente de ventas industrial B2B",
    ),
    "conocimiento/portales-roles-permisos/index.html": (
        "Dise\u00f1o de Portales B2B con Roles y Permisos en Entornos Industriales",
        "Portales B2B: dise\u00f1o de roles y permisos",
    ),
    "conocimiento/precios-complejos-ventas-volumen/index.html": (
        "C\u00f3mo Gestionar Precios Complejos en Ventas Industriales B2B por Volumen",
        "C\u00f3mo gestionar precios complejos en venta por volumen",
    ),
    "conocimiento/proporcionalidad-arquitectonica/index.html": (
        "Proporcionalidad Arquitect\u00f3nica: Cu\u00e1ndo la Arquitectura Correcta es la Simple",
        "Proporcionalidad: cu\u00e1ndo la arquitectura correcta es la simple",
    ),
    "conocimiento/que-es-arquitectura-comercial-digital/index.html": (
        "\u00bfQu\u00e9 es la Arquitectura Comercial Digital en entornos industriales B2B?",
        "\u00bfQu\u00e9 es la Arquitectura Comercial Digital?",
    ),
    "conocimiento/secuencia-implementacion/index.html": (
        "Secuencia de Implementaci\u00f3n en Arquitectura Comercial Digital Industrial",
        "Secuencia de implementaci\u00f3n en arquitectura comercial",
    ),
    "conocimiento/sistemas-calificacion-b2b/index.html": (
        "C\u00f3mo Dise\u00f1ar Sistemas de Calificaci\u00f3n en Ventas Industriales B2B",
        "C\u00f3mo dise\u00f1ar sistemas de calificaci\u00f3n en venta B2B",
    ),
    "conocimiento/superficie-especificacion-comprador/index.html": (
        "Superficie de Especificaciones: C\u00f3mo Presentar Informaci\u00f3n T\u00e9cnica en Plataformas Industriales B2B",
        "Superficie de especificaciones para el comprador t\u00e9cnico",
    ),
    "framework/como-funciona/index.html": (
        "Por Qu\u00e9 Vender por Volumen Define la Estrategia Digital Industrial B2B",
        "Por qu\u00e9 vender por volumen define la estrategia digital",
    ),
    "framework/componentes/index.html": (
        "Componentes de una Arquitectura Comercial Digital para Empresas Industriales B2B",
        "Componentes de una Arquitectura Comercial Digital",
    ),
    "glosario/index.html": (
        "Glosario de T\u00e9rminos en Arquitectura Comercial Digital para Industria B2B",
        "Glosario de Arquitectura Comercial Digital",
    ),
    "industrias/distribuidores/index.html": (
        "Arquitectura Comercial Digital para Distribuidores Industriales y Mayoristas",
        "Arquitectura digital para distribuidores mayoristas",
    ),
    "industrias/operadores-logisticos/index.html": (
        "Arquitectura Comercial Digital para Operadores Log\u00edsticos y de Cadena de Suministro B2B",
        "Arquitectura digital para operadores log\u00edsticos",
    ),
    "servicios/arquitectura-comercial/index.html": (
        "Dise\u00f1o de Arquitectura Comercial para Operaciones Industriales B2B",
        "Dise\u00f1o de arquitectura comercial para operaciones B2B",
    ),
    "servicios/consultoria-infraestructura/index.html": (
        "Consultor\u00eda de Infraestructura Digital Avanzada para B2B Industrial",
        "Consultor\u00eda de infraestructura digital para B2B industrial",
    ),
    "servicios/plataformas-industriales/index.html": (
        "Desarrollo de Plataformas B2B Industriales Alineadas a la Estructura Operativa",
        "Plataformas B2B alineadas a la estructura operativa",
    ),
}

RE_TITLE = re.compile(r"<title>(.*?)</title>", re.S)


def meta_regex(prop):
    """Devuelve regex que captura un <meta ...> cuyo property/name es prop."""
    return re.compile(
        r'<meta\b[^>]*\b(?:property|name)\s*=\s*["\']' + re.escape(prop) + r'["\'][^>]*>',
        re.I,
    )


RE_OG = meta_regex("og:title")
RE_TW = meta_regex("twitter:title")
RE_CONTENT = re.compile(r'(content\s*=\s*)(["\'])(.*?)\2', re.S | re.I)


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


def fase_0_backup():
    print("=" * 74)
    print("FASE 0 - BACKUP")
    print("=" * 74)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(BACKUP_DIR, "n2n-site-backup-titles-%s.tar.gz" % stamp)

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

    tam = os.path.getsize(destino)
    print("Archivo   : %s" % destino)
    print("Tamano    : %d KB" % (tam // 1024))
    print("Empaquetados: %d" % incluidos)
    print("Verificados : %d" % verificados)

    if verificados != incluidos or verificados == 0:
        print("ABORTA: el backup no verifica.")
        sys.exit(1)

    faltan = [p for p in sorted(TITLES) if p not in nombres]
    if faltan:
        print("ABORTA: faltan archivos en el backup: %s" % faltan)
        sys.exit(1)

    print("Backup OK - las 25 paginas estan dentro del tarball.")
    print("")
    return destino


def fase_1_validar():
    print("=" * 74)
    print("FASE 1 - VALIDACION (no se escribe nada)")
    print("=" * 74)

    errores = []
    plan = {}

    for rel, (viejo, nuevo) in sorted(TITLES.items()):
        path = os.path.join(REPO, rel)

        if not os.path.isfile(path):
            errores.append("%s : NO EXISTE" % rel)
            continue

        html = leer(path)
        titles = RE_TITLE.findall(html)

        if len(titles) != 1:
            errores.append("%s : %d etiquetas <title> (se esperaba 1)" % (rel, len(titles)))
            continue

        actual = titles[0].strip()
        if actual == viejo:
            estado_title = "cambia"
        elif actual == nuevo:
            estado_title = "ya aplicado"
        else:
            errores.append("%s : <title> inesperado -> %r" % (rel, actual))
            continue

        ogs = RE_OG.findall(html)
        if len(ogs) != 1:
            errores.append("%s : %d etiquetas og:title (se esperaba 1)" % (rel, len(ogs)))
            continue
        og_actual = contenido_de(ogs[0])
        if og_actual is None:
            errores.append("%s : og:title sin atributo content" % rel)
            continue

        tws = RE_TW.findall(html)
        if len(tws) > 1:
            errores.append("%s : %d etiquetas twitter:title (maximo 1)" % (rel, len(tws)))
            continue
        tw_actual = contenido_de(tws[0]) if tws else None
        if tws and tw_actual is None:
            errores.append("%s : twitter:title sin atributo content" % rel)
            continue

        plan[rel] = {
            "viejo": viejo,
            "nuevo": nuevo,
            "estado_title": estado_title,
            "og_actual": og_actual,
            "og_tag": ogs[0],
            "tw_actual": tw_actual,
            "tw_tag": tws[0] if tws else None,
        }

        marca_og = "=" if og_actual == nuevo else ">"
        marca_tw = "-" if tw_actual is None else ("=" if tw_actual == nuevo else ">")
        print("%-52s title:%-11s og:%s tw:%s  (%d chars)"
              % (rel.replace("/index.html", "/"), estado_title, marca_og, marca_tw, len(nuevo)))

    print("")
    print("Paginas en el plan: %d de %d" % (len(plan), len(TITLES)))

    if errores:
        print("")
        print("--- ERRORES ---")
        for e in errores:
            print("  " + e)
        print("")
        print("ABORTA: no se escribio ningun archivo.")
        sys.exit(1)

    if len(plan) != len(TITLES):
        print("ABORTA: el plan no cubre las 25 paginas.")
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

        html = RE_TITLE.sub(lambda m: "<title>%s</title>" % nuevo, html, count=1)

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
    for rel, (viejo, nuevo) in sorted(TITLES.items()):
        html = leer(os.path.join(REPO, rel))

        titles = RE_TITLE.findall(html)
        if len(titles) != 1 or titles[0].strip() != nuevo:
            fallas.append("%s : <title> no quedo aplicado" % rel)
            continue

        ogs = RE_OG.findall(html)
        if len(ogs) != 1 or contenido_de(ogs[0]) != nuevo:
            fallas.append("%s : og:title desincronizado" % rel)
            continue

        tws = RE_TW.findall(html)
        if tws and contenido_de(tws[0]) != nuevo:
            fallas.append("%s : twitter:title desincronizado" % rel)
            continue

        if len(nuevo) > 62:
            fallas.append("%s : title de %d chars (supera 62)" % (rel, len(nuevo)))

    if fallas:
        print("--- FALLAS ---")
        for f in fallas:
            print("  " + f)
        print("")
        print("RESTAURAR desde el tarball de la fase 0.")
        sys.exit(1)

    largos = [len(v[1]) for v in TITLES.values()]
    print("25/25 titles aplicados y sincronizados con og:title / twitter:title.")
    print("Largo minimo: %d chars   maximo: %d chars" % (min(largos), max(largos)))
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
