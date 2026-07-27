#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cerrar_promesas_control_v1.py

Corrige tres defectos detectados al revisar el volcado posterior al
commit de diferenciacion de h1.

  1. glosario/index.html — PROMESA INCUMPLIDA (creada por el commit anterior)
     El h1 pasó a anunciar "arquitectura comercial y control operativo",
     pero los 13 terminos eran todos del eje comercial. Se agregan los
     cinco pilares de Protocolo CERO como terminos 14 a 18, tomados de
     las definiciones ya publicadas en /control/protocolo-cero/ y llms.txt.
     Se agregan tambien al JSON-LD como DefinedTerm.

  2. glosario/index.html — DESCRIPTION FALSA
     Declaraba "13 terminos en EN, ES y PT-BR". El soporte multilingue
     esta eliminado del sitio de forma permanente y no hay ni un rastro
     de EN o PT en la pagina. Se reescribe en los tres canales.

  3. conocimiento/index.html — PROMESA INCUMPLIDA
     El h1 anuncia "estructura comercial y control operativo" pero los 12
     articulos son todos del eje comercial. A diferencia del glosario, aca
     no hay contenido de control que sumar todavia: se revierte el h1 hasta
     que existan articulos del eje.

NO toca: header, footer, caso alguno, ni el resto de los h1.

Aborta sin escribir si cualquier reemplazo o guarda falla.

Uso:
    python3 _scripts/cerrar_promesas_control_v1.py
"""

import os
import shutil
import sys

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"

# ------------------------------------------------- 1. terminos nuevos (HTML)

ANCLA_HTML = ('<h2>13. Oportunidad Calificada</h2>\n'
              '<p>Consulta comercial que cumple todos los criterios de viabilidad '
              'operativa: volumen, compatibilidad técnica, legitimidad empresarial '
              'y factibilidad dentro de las restricciones de producción.</p>')

TERMINOS = [
    (14, "Punto de Custodia",
     "Tramo del circuito f&iacute;sico donde la mercader&iacute;a cambia de "
     "responsable. Es el lugar exacto donde la p&eacute;rdida puede ocurrir sin "
     "dejar rastro si el traspaso no exige evidencia."),
    (15, "Segregaci&oacute;n de Funciones",
     "Separaci&oacute;n entre quien ejecuta un movimiento y quien valida su cierre. "
     "Un control que la misma persona puede firmarse a s&iacute; misma no es un "
     "control."),
    (16, "Evidencia Obligatoria",
     "Registro capturado en el punto y en el momento del movimiento, no "
     "transcripto despu&eacute;s de memoria. Convierte una discusi&oacute;n sobre "
     "versiones en una verificaci&oacute;n documental."),
    (17, "Control Inevitable",
     "Control incorporado al flujo de trabajo de modo que la operaci&oacute;n no "
     "pueda avanzar sin cumplirlo. No depende de disciplina ni de supervisi&oacute;n "
     "presente: saltearlo detiene el trabajo."),
    (18, "Verificaci&oacute;n Permanente",
     "R&eacute;gimen de comprobaci&oacute;n continua que sostiene el control "
     "despu&eacute;s de la implantaci&oacute;n. Sin &eacute;l, todo control se "
     "degrada hasta volverse una formalidad."),
]

# --------------------------------------------- terminos nuevos (JSON-LD)

ANCLA_JSONLD = '''    {
      "@type": "DefinedTerm",
      "@id": "https://n2n.com.ar/glosario/#term-13",
      "name": "Oportunidad Calificada",
      "description": "Consulta comercial que cumple todos los criterios de viabilidad operativa: volumen, compatibilidad técnica, legitimidad empresarial y factibilidad dentro de las restricciones de producción.",
      "inDefinedTermSet": "https://n2n.com.ar/glosario/#set"
    }'''

JSONLD_TERMINOS = [
    (14, "Punto de Custodia",
     "Tramo del circuito físico donde la mercadería cambia de responsable. Es el lugar exacto donde la pérdida puede ocurrir sin dejar rastro si el traspaso no exige evidencia."),
    (15, "Segregación de Funciones",
     "Separación entre quien ejecuta un movimiento y quien valida su cierre. Un control que la misma persona puede firmarse a sí misma no es un control."),
    (16, "Evidencia Obligatoria",
     "Registro capturado en el punto y en el momento del movimiento, no transcripto después de memoria. Convierte una discusión sobre versiones en una verificación documental."),
    (17, "Control Inevitable",
     "Control incorporado al flujo de trabajo de modo que la operación no pueda avanzar sin cumplirlo. No depende de disciplina ni de supervisión presente: saltearlo detiene el trabajo."),
    (18, "Verificación Permanente",
     "Régimen de comprobación continua que sostiene el control después de la implantación. Sin él, todo control se degrada hasta volverse una formalidad."),
]

# ------------------------------------------------------ 2. description real

DESC_VIEJA = ("Definiciones oficiales de los términos clave utilizados en "
              "Arquitectura Comercial Digital para entornos industriales B2B. "
              "13 términos en EN, ES y PT-BR.")

DESC_NUEVA = ("Definiciones de los 18 términos de los dos ejes de N2N: "
              "arquitectura comercial digital B2B y control operativo de "
              "pérdidas en cadena de frío.")

# --------------------------------------------------- 3. revertir conocimiento

CONO_H1_VIEJO = ('<h1 class="hero__h1" id="page-h1">Documentaci&oacute;n '
                 't&eacute;cnica: estructura comercial y control operativo</h1>')
CONO_H1_NUEVO = ('<h1 class="hero__h1" id="page-h1">Documentaci&oacute;n '
                 't&eacute;cnica sobre estructura comercial B2B</h1>')

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


def escribir(path, contenido, original):
    shutil.copy2(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenido)
    print("  escrito %s (%d bytes, antes %d)"
          % (os.path.basename(path), len(contenido), len(original)))


def procesar_glosario():
    print("glosario/index.html")
    path, html = leer("glosario/index.html")
    original = html

    # --- terminos en el cuerpo
    bloque = ANCLA_HTML
    for num, nombre, definicion in TERMINOS:
        bloque += "\n<hr>\n<h2>%d. %s</h2>\n<p>%s</p>" % (num, nombre, definicion)
    html = cambiar(html, ANCLA_HTML, bloque, "5 terminos de control en el cuerpo")

    # --- terminos en el JSON-LD
    bloque_ld = ANCLA_JSONLD
    for num, nombre, definicion in JSONLD_TERMINOS:
        bloque_ld += (',\n    {\n'
                      '      "@type": "DefinedTerm",\n'
                      '      "@id": "https://n2n.com.ar/glosario/#term-%d",\n'
                      '      "name": "%s",\n'
                      '      "description": "%s",\n'
                      '      "inDefinedTermSet": "https://n2n.com.ar/glosario/#set"\n'
                      '    }' % (num, nombre, definicion))
    html = cambiar(html, ANCLA_JSONLD, bloque_ld, "5 DefinedTerm en el JSON-LD")

    # --- description en los tres canales + la bajada visible del hero
    if html.count(DESC_VIEJA) != 4:
        fail("la description vieja aparece %d veces (esperaba 4: tres metadatos "
             "mas la bajada del hero)" % html.count(DESC_VIEJA))
    html = html.replace(DESC_VIEJA, DESC_NUEVA)
    print("  OK  description reescrita en los tres canales y en el hero")

    # --- guardas
    for needle, label in [
        ('<header class="site-header" role="banner">', "header intacto"),
        ('<footer class="site-footer" role="contentinfo">', "footer intacto"),
        ("<h2>1. Arquitectura Comercial Digital</h2>", "termino 1 intacto"),
        ("<h2>13. Oportunidad Calificada</h2>", "termino 13 intacto"),
        ("Glosario: arquitectura comercial y control operativo", "h1 intacto"),
    ]:
        if needle not in html:
            fail("guarda rota: %s" % label)
        print("  OK  %s" % label)

    if "PT-BR" in html or "13 términos" in html:
        fail("la declaracion multilingue sigue presente")
    print("  OK  sin rastro de la declaracion multilingue")

    if html.count("<h2>") != 18:
        fail("el glosario quedo con %d h2 (esperaba 18)" % html.count("<h2>"))
    print("  OK  18 terminos en el cuerpo")

    # longitud de la description
    if not (120 <= len(DESC_NUEVA) <= 158):
        fail("description nueva fuera de rango: %d chars" % len(DESC_NUEVA))
    print("  OK  description %d chars (120-158)" % len(DESC_NUEVA))

    escribir(path, html, original)
    CAMBIOS.append("glosario/index.html")


def procesar_conocimiento():
    print("conocimiento/index.html")
    path, html = leer("conocimiento/index.html")
    original = html

    html = cambiar(html, CONO_H1_VIEJO, CONO_H1_NUEVO,
                   "h1 revertido: no hay articulos de control todavia")

    if html.count("<h1") != 1:
        fail("quedo con %d h1" % html.count("<h1"))
    print("  OK  un unico h1")

    escribir(path, html, original)
    CAMBIOS.append("conocimiento/index.html")


def main():
    if not os.path.isdir(os.path.join(REPO, ".git")):
        fail("no parece un repo git: %s" % REPO)

    procesar_glosario()
    procesar_conocimiento()

    print("")
    print("Archivos modificados: %s" % ", ".join(CAMBIOS))
    print("Backups .bak junto a cada archivo (borrar tras validar).")
    print("LISTO")


if __name__ == "__main__":
    main()
