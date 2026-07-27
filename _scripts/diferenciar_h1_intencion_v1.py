#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diferenciar_h1_intencion_v1.py

Corrige la canibalizacion de keyword detectada en la revision semantica:
12 paginas abrian su h1 con "Arquitectura Comercial Digital para...",
compitiendo entre si por la misma intencion de busqueda.

Criterio aplicado:
  - Una sola pagina conserva el termino principal como h1: la definicional
    (/conocimiento/que-es-arquitectura-comercial-digital/), que ademas
    queda alineada exactamente con su title.
  - Las otras 11 abren con su propio diferenciador: el segmento, el
    sistema o la funcion que esa pagina resuelve.
  - /glosario/ y /conocimiento/ suman "control operativo", unica forma de
    dar presencia al eje control sin tocar el header (congelado).

Solo modifica el contenido de <h1>. No toca titles, metadatos, JSON-LD,
header, footer ni el cuerpo de las paginas.

Aborta sin escribir si cualquier h1 no aparece exactamente una vez.

Uso:
    python3 _scripts/diferenciar_h1_intencion_v1.py
"""

import os
import shutil
import sys

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"

PLANTILLA = '<h1 class="hero__h1" id="%s">%s</h1>'

# (archivo, id del h1, texto viejo, texto nuevo)
MAPEO = [
    ("conocimiento/que-es-arquitectura-comercial-digital/index.html",
     "page-h1",
     "¿Qué es la Arquitectura Comercial Digital en entornos industriales B2B?",
     "&iquest;Qu&eacute; es la Arquitectura Comercial Digital?"),

    ("index.html",
     "hero-h1",
     "Arquitectura Comercial Digital para Empresas Industriales B2B que Venden por Volumen",
     "Estructura digital para operaciones que venden por volumen"),

    ("industrias/index.html",
     "page-h1",
     "Arquitectura Comercial Digital por Industria",
     "C&oacute;mo cambia la estructura seg&uacute;n el tipo de operaci&oacute;n"),

    ("industrias/distribuidores/index.html",
     "page-h1",
     "Arquitectura Comercial Digital para Distribuidores Industriales y Mayoristas",
     "Distribuidores mayoristas: cat&aacute;logo, stock y precios por cuenta"),

    ("industrias/manufactura/index.html",
     "page-h1",
     "Arquitectura Comercial Digital para Empresas Manufactureras",
     "Fabricantes: especificaciones, RFQ y capacidad productiva"),

    ("industrias/operadores-logisticos/index.html",
     "page-h1",
     "Arquitectura Comercial Digital para Operadores Logísticos y de Cadena de Suministro B2B",
     "Operadores log&iacute;sticos: cobertura, capacidad y acuerdos de servicio"),

    ("servicios/arquitectura-comercial/index.html",
     "page-h1",
     "Diseño de Arquitectura Comercial para Operaciones Industriales B2B",
     "Capa 01: dise&ntilde;o de la estructura comercial"),

    ("framework/componentes/index.html",
     "page-h1",
     "Componentes de una Arquitectura Comercial Digital para Empresas Industriales B2B",
     "Los componentes y qu&eacute; resuelve cada uno"),

    ("conocimiento/integracion-erp/index.html",
     "page-h1",
     "Integración de ERP en Arquitectura Comercial Digital Industrial",
     "C&oacute;mo integrar el ERP con la superficie comercial"),

    ("conocimiento/secuencia-implementacion/index.html",
     "page-h1",
     "Secuencia de Implementación en Arquitectura Comercial Digital Industrial",
     "En qu&eacute; orden se implementa: secuencia y dependencias"),

    ("glosario/index.html",
     "page-h1",
     "Glosario de Términos en Arquitectura Comercial Digital para Industria B2B",
     "Glosario: arquitectura comercial y control operativo"),

    ("conocimiento/index.html",
     "page-h1",
     "Documentación Técnica — Arquitectura Comercial B2B Industrial",
     "Documentaci&oacute;n t&eacute;cnica: estructura comercial y control operativo"),
]

CAMBIOS = []


def fail(msg):
    print("ABORTADO: %s" % msg)
    sys.exit(1)


def main():
    if not os.path.isdir(os.path.join(REPO, ".git")):
        fail("no parece un repo git: %s" % REPO)

    # --- pasada 1: verificar todo sin escribir nada
    print("Verificacion previa (sin escribir):")
    pendientes = []
    for rel, hid, viejo, nuevo in MAPEO:
        path = os.path.join(REPO, rel)
        if not os.path.isfile(path):
            fail("no existe %s" % rel)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        v = PLANTILLA % (hid, viejo)
        n = PLANTILLA % (hid, nuevo)

        if html.count(v) != 1:
            fail("%s — el h1 esperado aparece %d veces" % (rel, html.count(v)))
        if html.count("<h1") != 1:
            fail("%s — la pagina tiene %d h1" % (rel, html.count("<h1")))

        pendientes.append((path, rel, html, v, n))
        print("  OK  %s" % rel)

    print("")
    print("Aplicando %d cambios:" % len(pendientes))

    # --- pasada 2: escribir
    for path, rel, html, v, n in pendientes:
        original = html
        nuevo_html = html.replace(v, n, 1)
        if nuevo_html == original:
            fail("%s — el reemplazo no produjo cambios" % rel)
        if nuevo_html.count("<h1") != 1:
            fail("%s — quedo con %d h1" % (rel, nuevo_html.count("<h1")))
        # guardas: solo debe cambiar el h1
        if len(original) - len(nuevo_html) != len(v) - len(n):
            fail("%s — el diff no corresponde solo al h1" % rel)

        shutil.copy2(path, path + ".bak")
        with open(path, "w", encoding="utf-8") as f:
            f.write(nuevo_html)
        print("  %-52s %d -> %d bytes" % (rel, len(original), len(nuevo_html)))
        CAMBIOS.append(rel)

    print("")
    print("Archivos modificados: %d" % len(CAMBIOS))
    print("Backups .bak junto a cada archivo (borrar tras validar).")
    print("LISTO")


if __name__ == "__main__":
    main()
