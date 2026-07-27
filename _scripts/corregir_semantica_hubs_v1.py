#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corregir_semantica_hubs_v1.py

Corrige tres defectos semanticos detectados en la revision del volcado v4.

  1. casos/index.html — CONTRADICCION
     El hero declara "Casos modelados basados en patrones estructurales",
     es decir casos ilustrativos, y dos parrafos despues la misma pagina
     afirma que no son ejercicios teoricos sino sistemas en produccion.
     La primera frase es residuo de una etapa sin casos reales. Se reescribe.

  2. casos/caso-01 + casos/index.html — CRITERIO DE H1
     caso-01 usaba una tesis conceptual como h1; caso-02 y caso-03 usan
     nombres descriptivos. Se unifica hacia descriptivo, que es ademas el
     registro de los tres titles. La tesis se conserva en el headline
     del JSON-LD y en la bajada del caso.

  3. nosotros/index.html — H1 QUE NO ES H1
     El h1 era una oracion de 113 caracteres (una bajada, no un
     encabezado). Se acorta a un identificador de pagina y el contenido
     de la oracion se absorbe en el lead.

NO toca: header, footer, metadatos, JSON-LD, caso-02, caso-03.

Aborta sin escribir si cualquier reemplazo o guarda falla.

Uso:
    python3 _scripts/corregir_semantica_hubs_v1.py
"""

import os
import shutil
import sys

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"

# ---------------------------------------------------------------- 1. /casos/

CASOS_LEAD_VIEJO = ('<p class="hero__lead">Casos modelados basados en patrones '
                    'estructurales comunes en operaciones industriales '
                    'latinoamericanas.</p>')

CASOS_LEAD_NUEVO = ('<p class="hero__lead">Sistemas en producci&oacute;n, operando '
                    'todos los d&iacute;as sobre negocios reales. Cada caso documenta '
                    'el problema de partida, lo que se construy&oacute; y qu&eacute; '
                    'cambi&oacute; en la operaci&oacute;n.</p>')

# --------------------------------------------------------- 2. h1 de caso-01

C01_H1_VIEJO = ('<h1 class="hero__h1" id="page-h1">El control que no se puede '
                'saltear</h1>')
C01_H1_NUEVO = ('<h1 class="hero__h1" id="page-h1">Control de p&eacute;rdidas en '
                'cadena de fr&iacute;o con Protocolo CERO</h1>')

CARD_H2_VIEJO = '<h2 class="card__title">El control que no se puede saltear</h2>'
CARD_H2_NUEVO = ('<h2 class="card__title">Control de p&eacute;rdidas en cadena de '
                 'fr&iacute;o con Protocolo CERO</h2>')

ITEMLIST_VIEJO = '"name": "El control que no se puede saltear"'
ITEMLIST_NUEVO = '"name": "Control de pérdidas en cadena de frío con Protocolo CERO"'

# ------------------------------------------------------- 3. h1 de /nosotros/

NOS_H1_VIEJO = ('<h1 id="nosotros-h1" class="hero__h1" style="max-width:760px">'
                'El operador detrás de N2N no diseña sistemas para clientes: '
                'los construye y los usa todos los días en producción.</h1>')
NOS_H1_NUEVO = ('<h1 id="nosotros-h1" class="hero__h1" style="max-width:760px">'
                'El operador detr&aacute;s de N2N</h1>')

NOS_LEAD_VIEJO = ('<p class="hero__lead" style="max-width:640px">Construyo sistemas '
                  'que representan la operación hacia afuera y la controlan hacia '
                  'adentro. Esa diferencia define todo lo que hacemos.</p>')
NOS_LEAD_NUEVO = ('<p class="hero__lead" style="max-width:640px">No dise&ntilde;o '
                  'sistemas para clientes: los construyo y los uso todos los d&iacute;as '
                  'en producci&oacute;n. Representan la operaci&oacute;n hacia afuera y '
                  'la controlan hacia adentro. Esa diferencia define todo lo que '
                  'hacemos.</p>')

CAMBIOS = []


def fail(msg):
    print("ABORTADO: %s" % msg)
    sys.exit(1)


def leer(rel):
    path = os.path.join(REPO, rel)
    if not os.path.isfile(path):
        fail("no existe %s" % path)
    with open(path, "r", encoding="utf-8") as f:
        return path, f.read()


def cambiar(texto, viejo, nuevo, label):
    n = texto.count(viejo)
    if n != 1:
        fail("'%s' aparece %d veces (esperaba 1)" % (label, n))
    print("  OK  %s" % label)
    return texto.replace(viejo, nuevo, 1)


def guardas(texto, items):
    for needle, label in items:
        if needle not in texto:
            fail("guarda rota: %s" % label)
        print("  OK  %s" % label)


def escribir(path, contenido, original):
    shutil.copy2(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenido)
    print("  escrito %s (%d bytes, antes %d)"
          % (os.path.basename(path), len(contenido), len(original)))


def procesar_casos_indice():
    print("casos/index.html")
    path, html = leer("casos/index.html")
    original = html

    html = cambiar(html, CASOS_LEAD_VIEJO, CASOS_LEAD_NUEVO, "hero lead sin contradiccion")
    html = cambiar(html, CARD_H2_VIEJO, CARD_H2_NUEVO, "card__title caso-01")
    html = cambiar(html, ITEMLIST_VIEJO, ITEMLIST_NUEVO, "ItemList name caso-01")

    guardas(html, [
        ("no son ejercicios teóricos ni mockups", "parrafo de sistemas reales intacto"),
        ("<title>Casos — N2N</title>", "title intacto"),
        ('<header class="site-header" role="banner">', "header intacto"),
        ('<footer class="site-footer" role="contentinfo">', "footer intacto"),
        ("Sistema de Presupuestos para RB Limpieza", "card caso-02 intacto"),
        ("Valorización de Stock: ValorFL", "card caso-03 intacto"),
    ])

    if "modelados" in html:
        fail("la palabra 'modelados' sigue presente en /casos/")
    print("  OK  contradiccion eliminada")

    escribir(path, html, original)
    CAMBIOS.append("casos/index.html")


def procesar_caso01():
    print("casos/caso-01/index.html")
    path, html = leer("casos/caso-01/index.html")
    original = html

    html = cambiar(html, C01_H1_VIEJO, C01_H1_NUEVO, "h1 descriptivo")

    guardas(html, [
        ('"headline": "El control que no se puede saltear: Protocolo CERO en cadena de frío"',
         "tesis conservada en el headline JSON-LD"),
        ("<title>Caso 01: control de pérdidas en cadena de frío</title>",
         "title intacto"),
        ('<header class="site-header" role="banner">', "header intacto"),
        ("un distribuidor de cadena de fr&iacute;o", "anonimato intacto"),
    ])

    escribir(path, html, original)
    CAMBIOS.append("casos/caso-01/index.html")


def procesar_nosotros():
    print("nosotros/index.html")
    path, html = leer("nosotros/index.html")
    original = html

    html = cambiar(html, NOS_H1_VIEJO, NOS_H1_NUEVO, "h1 acortado a identificador")
    html = cambiar(html, NOS_LEAD_VIEJO, NOS_LEAD_NUEVO, "lead absorbe la propuesta de valor")

    guardas(html, [
        ('<header class="site-header" role="banner">', "header intacto"),
        ('<footer class="site-footer" role="contentinfo">', "footer intacto"),
        ("<title>Quiénes somos — Carlos Petit, Fundador | N2N</title>",
         "title intacto"),
    ])

    if html.count("<h1") != 1:
        fail("nosotros quedo con %d h1" % html.count("<h1"))
    print("  OK  un unico h1")

    escribir(path, html, original)
    CAMBIOS.append("nosotros/index.html")


def main():
    if not os.path.isdir(os.path.join(REPO, ".git")):
        fail("no parece un repo git: %s" % REPO)

    procesar_casos_indice()
    procesar_caso01()
    procesar_nosotros()

    print("")
    print("Archivos modificados: %s" % ", ".join(CAMBIOS))
    print("Backups .bak junto a cada archivo (borrar tras validar).")
    print("LISTO")


if __name__ == "__main__":
    main()
