#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aplicar_descriptions_largas_v1.py

Reescribe las 28 meta description que superaban los 158 caracteres y
sincroniza og:description y twitter:description con el nuevo valor.

Fuera de alcance por decision: /casos/caso-01/, /casos/caso-02/ y
/casos/caso-03/ (se trabajan junto con su contenido en la Parte 3), y
/legal/ (noindex).

NO toca: titles, h1, cuerpo, JSON-LD ni el <header>.

Fases:
  0. Backup verificable del repo completo fuera del repo
  1. Validacion de las 28 paginas SIN escribir nada
  2. Escritura solo si la fase 1 pasa entera
  3. Verificacion posterior

Criterio de seguridad: solo se sobrescribe una description que hoy supere
los 158 chars (es decir, que sea una de las paginas objetivo) o que ya sea
igual a la nueva. Cualquier otro caso aborta.

Idempotente. Ejecutar desde la raiz del repo n2n-site.
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

NUEVAS = {
    "index.html":
        "N2N diseña Arquitectura Comercial Digital para empresas industriales B2B "
        "que venden por volumen, alineada con su operación comercial real.",

    "comparar/custom-vs-saas/index.html":
        "Criterios para decidir entre una arquitectura comercial a medida y una "
        "plataforma SaaS genérica en operaciones industriales B2B.",

    "comparar/ecommerce-b2b-vs-arquitectura-comercial/index.html":
        "Diferencias entre ecommerce tradicional y Arquitectura Comercial Digital "
        "para ventas industriales con precios, requisitos y volúmenes complejos.",

    "comparar/n2n-vs-agencia/index.html":
        "N2N diseña sistemas alineados con la operación comercial industrial; una "
        "agencia optimiza comunicación, campañas y percepción de marca.",

    "conocimiento/como-digitalizar-pedidos-distribuidora/index.html":
        "Digitalizar pedidos consiste en cargarlos una sola vez, con datos "
        "estructurados, y eliminar transcripciones manuales entre canales y sistemas.",

    "conocimiento/control-de-cambios-sistemas-criticos/index.html":
        "Método para modificar sistemas críticos sin comprometer la operación: "
        "backup verificado, validación, versionado y reversión controlada.",

    "conocimiento/integracion-erp/index.html":
        "Cómo integrar un ERP con plataformas B2B sin exponer datos innecesarios, "
        "alterar reglas comerciales ni desordenar la operación.",

    "conocimiento/kpis-ruido-vs-trafico/index.html":
        "KPIs para medir rendimiento digital industrial por oportunidades viables, "
        "protección de margen y reducción de consultas sin valor comercial.",

    "conocimiento/marketing-despues-estructura/index.html":
        "Por qué el marketing debe amplificar una estructura comercial ya definida "
        "y no compensar procesos, mensajes o sistemas mal resueltos.",

    "conocimiento/playbook-gerente-ventas/index.html":
        "Guía para gerentes de ventas sobre calificación, información técnica, "
        "precios complejos y participación comercial en el diseño digital.",

    "conocimiento/portales-roles-permisos/index.html":
        "Diseño de portales B2B con accesos, roles y permisos que protegen precios, "
        "documentos, funciones y relaciones comerciales por cuenta.",

    "conocimiento/precios-complejos-ventas-volumen/index.html":
        "Cómo representar precios industriales variables por volumen, contrato, "
        "configuración, logística y condiciones específicas de cada cuenta.",

    "conocimiento/proporcionalidad-arquitectonica/index.html":
        "Principio para construir sistemas con la complejidad exacta que requiere "
        "la operación, evitando tanto el exceso como la falta de estructura.",

    "conocimiento/que-es-arquitectura-comercial-digital/index.html":
        "La Arquitectura Comercial Digital es la disciplina que diseña sistemas que "
        "representan, filtran y alinean la operación comercial real de empresas B2B.",

    "conocimiento/secuencia-implementacion/index.html":
        "Orden correcto para digitalizar una operación industrial: definir la "
        "estructura, implementar la tecnología y recién después generar visibilidad.",

    "conocimiento/sistemas-calificacion-b2b/index.html":
        "Cómo filtrar y clasificar consultas industriales según capacidad operativa, "
        "requisitos técnicos, volumen, plazo y viabilidad económica.",

    "conocimiento/superficie-especificacion-comprador/index.html":
        "Estructura de información técnica, normativa y operativa para que un "
        "comprador industrial valide viabilidad antes del contacto comercial.",

    "control/protocolo-cero/index.html":
        "Diagnóstico USD 1.500 para detectar y reducir pérdidas en distribuidoras de "
        "cadena de frío: controles inevitables y verificación continua.",

    "framework/como-funciona/index.html":
        "Cómo la venta industrial por volumen determina los requisitos de "
        "calificación, información, precios, integración y plataforma digital.",

    "framework/componentes/index.html":
        "Componentes mínimos de una Arquitectura Comercial Digital: entidades, "
        "cotización, calificación, información técnica e integración con ERP.",

    "industrias/distribuidores/index.html":
        "Arquitectura digital para distribuidores: catálogo conectado al ERP, stock "
        "actualizado, precios por cuenta y calificación de consultas.",

    "industrias/manufactura/index.html":
        "Estructura digital para fabricantes: especificaciones técnicas, capacidad "
        "productiva, flujos de cotización e integración con ERP.",

    "industrias/operadores-logisticos/index.html":
        "Arquitectura digital para operadores logísticos: calificación de demanda, "
        "representación de capacidad y ventas basadas en contratos.",

    "nosotros/index.html":
        "Carlos Petit fundó N2N tras cuatro décadas resolviendo operaciones reales "
        "con tecnología actual y construyendo sistemas en producción.",

    "precios/index.html":
        "N2N trabaja por proyecto, no por lista de precios. Cada intervención se "
        "cotiza según la complejidad y magnitud real de la operación.",

    "servicios/arquitectura-comercial/index.html":
        "Diagnóstico de la operación y documento estructural con problemas, "
        "prioridades y diseño de la superficie comercial digital necesaria.",

    "servicios/consultoria-infraestructura/index.html":
        "Consultoría para trazabilidad, integridad de datos, seguridad, "
        "automatización e infraestructura cuando una arquitectura estándar no alcanza.",

    "servicios/plataformas-industriales/index.html":
        "Desarrollo de sitios, portales, cotizadores y catálogos B2B conectados con "
        "la operación, la infraestructura y los datos del ERP.",
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
    return [t for t in RE_DESC.findall(html)
            if not re.search(r'["\'](?:og|twitter):description["\']', t, re.I)]


def fase_0_backup():
    print("=" * 74)
    print("FASE 0 - BACKUP")
    print("=" * 74)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(BACKUP_DIR, "n2n-site-backup-desclargas-%s.tar.gz" % stamp)

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

    if len(nombres) != incluidos or not nombres:
        print("ABORTA: el backup no verifica.")
        sys.exit(1)

    faltan = [p for p in sorted(NUEVAS) if p not in nombres]
    if faltan:
        print("ABORTA: faltan archivos en el backup: %s" % faltan)
        sys.exit(1)

    print("Backup OK - las 28 paginas estan dentro del tarball.")
    print("")


def fase_1_validar():
    print("=" * 74)
    print("FASE 1 - VALIDACION (no se escribe nada)")
    print("=" * 74)

    errores = []
    plan = {}

    for rel in sorted(NUEVAS):
        nuevo = NUEVAS[rel]
        path = os.path.join(REPO, rel)

        if not os.path.isfile(path):
            errores.append("%s : NO EXISTE" % rel)
            continue

        largo = len(nuevo)
        if largo < MIN_CHARS or largo > MAX_CHARS:
            errores.append("%s : la nueva mide %d chars (rango %d-%d)"
                           % (rel, largo, MIN_CHARS, MAX_CHARS))
            continue

        if any(c in nuevo for c in ('"', "&", "<", ">")):
            errores.append("%s : la nueva tiene caracteres que rompen el atributo" % rel)
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

        if actual == nuevo:
            estado = "ya aplicado"
        elif len(actual) > MAX_CHARS:
            estado = "cambia"
        else:
            errores.append("%s : la description actual mide %d chars y no es la esperada. "
                           "Revisar antes de sobrescribir." % (rel, len(actual)))
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
        print("%-54s %-11s %3d -> %3d  og:%s tw:%s"
              % (rel.replace("index.html", "").rstrip("/") or "/",
                 estado, len(actual), largo, marca_og, marca_tw))

    print("")
    print("Paginas en el plan: %d de %d" % (len(plan), len(NUEVAS)))
    print("Leyenda:  = ya sincronizada   > coincide con la vieja   ! divergia de antes   - no existe")

    if errores:
        print("")
        print("--- ERRORES ---")
        for e in errores:
            print("  " + e)
        print("")
        print("ABORTA: no se escribio ningun archivo.")
        sys.exit(1)

    if len(plan) != len(NUEVAS):
        print("ABORTA: el plan no cubre las 28 paginas.")
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
    for rel in sorted(NUEVAS):
        nuevo = NUEVAS[rel]
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

        if not (MIN_CHARS <= len(nuevo) <= MAX_CHARS):
            fallas.append("%s : %d chars fuera de rango" % (rel, len(nuevo)))

    if fallas:
        print("--- FALLAS ---")
        for f in fallas:
            print("  " + f)
        print("")
        print("RESTAURAR desde el tarball de la fase 0.")
        sys.exit(1)

    largos = [len(v) for v in NUEVAS.values()]
    print("28/28 descriptions aplicadas y sincronizadas.")
    print("Largo minimo: %d   maximo: %d   (rango %d-%d)"
          % (min(largos), max(largos), MIN_CHARS, MAX_CHARS))
    print("")
    print("Fuera de alcance por decision: /casos/caso-01/, /casos/caso-02/,")
    print("/casos/caso-03/ (Parte 3) y /legal/ (noindex).")
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
