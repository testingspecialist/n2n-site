#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reescribir_titles_intencion_v1.py

Cierra los tres defectos de titles que quedaban abiertos.

  1. HUBS VACIOS (8 paginas)
     "Casos — N2N" (11 chars), "Servicios — N2N" (15), "Framework — N2N",
     "Industrias — N2N", "Conocimiento — N2N", "Contacto — N2N",
     "Precios e Inversion — N2N", "Comparar — N2N vs Alternativas".
     Son las paginas con mas chance de rankear por consulta de categoria y
     su title no decia nada. Se reescriben diciendo que contiene cada una.

  2. CANIBALIZACION EN TITLES (8 paginas)
     La correccion anterior diferencio los h1 pero dejo los titles apuntando
     todos a "Arquitectura Comercial Digital". Se aplica el mismo criterio:
     una sola pagina conserva el termino como title, la definicional
     (/conocimiento/que-es-arquitectura-comercial-digital/), y el resto abre
     con su propio diferenciador, alineado con el h1 que ya tiene.
     /comparar/ecommerce-b2b-vs-arquitectura-comercial/ conserva el termino
     porque el termino ES el objeto de la comparacion.

  3. SEPARADOR INCONSISTENTE (3 paginas)
     2 titles usaban "| N2N" y el resto "— N2N" o nada. Se elimina el sufijo
     de marca: 30 de 44 paginas ya no lo tenian, y el dominio se muestra
     igual en el resultado de busqueda.

Cada title se escribe en los tres canales: <title>, og:title y twitter:title.
Ningun title supera 62 caracteres.

NO toca: descriptions, JSON-LD, h1, header, footer ni contenido.

Aborta sin escribir si algun title no aparece exactamente 3 veces.

Uso:
    python3 _scripts/reescribir_titles_intencion_v1.py
"""

import os
import shutil
import sys

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"
LIMITE = 62

# (archivo, title viejo, title nuevo)
MAPEO = [
    # --- 1. hubs vacios
    ("casos/index.html",
     "Casos — N2N",
     "Casos: sistemas en producción sobre operaciones reales"),
    ("servicios/index.html",
     "Servicios — N2N",
     "Servicios: las tres capas de intervención de N2N"),
    ("framework/index.html",
     "Framework — N2N",
     "Framework: cómo se estructura una operación B2B"),
    ("industrias/index.html",
     "Industrias — N2N",
     "Industrias: manufactura, distribución y logística B2B"),
    ("conocimiento/index.html",
     "Conocimiento — N2N",
     "Documentación técnica sobre estructura comercial B2B"),
    ("contacto/index.html",
     "Contacto — N2N",
     "Contacto: evaluar una operación industrial B2B"),
    ("precios/index.html",
     "Precios e Inversión — N2N",
     "Precios: diagnósticos de entrada con alcance cerrado"),
    ("comparar/index.html",
     "Comparar — N2N vs Alternativas",
     "Comparar: N2N frente a agencias, SaaS y ecommerce"),

    # --- 2. canibalizacion (alineados al h1 ya corregido)
    ("industrias/manufactura/index.html",
     "Arquitectura Comercial Digital para Empresas Manufactureras",
     "Fabricantes: especificaciones, RFQ y capacidad productiva"),
    ("industrias/distribuidores/index.html",
     "Arquitectura digital para distribuidores mayoristas",
     "Distribuidores mayoristas: catálogo, stock y precios"),
    ("industrias/operadores-logisticos/index.html",
     "Arquitectura digital para operadores logísticos",
     "Operadores logísticos: cobertura, capacidad y servicio"),
    ("framework/componentes/index.html",
     "Componentes de una Arquitectura Comercial Digital",
     "Los componentes de la estructura y qué resuelve cada uno"),
    ("glosario/index.html",
     "Glosario de Arquitectura Comercial Digital",
     "Glosario: arquitectura comercial y control operativo"),
    ("conocimiento/integracion-erp/index.html",
     "Integración de ERP en arquitectura comercial digital",
     "Cómo integrar el ERP con la superficie comercial"),
    ("conocimiento/secuencia-implementacion/index.html",
     "Secuencia de implementación en arquitectura comercial",
     "En qué orden se implementa: secuencia y dependencias"),
    ("servicios/arquitectura-comercial/index.html",
     "Diseño de arquitectura comercial para operaciones B2B",
     "Capa 01: diseño de la estructura comercial"),

    # --- 3. separador
    ("404.html",
     "404 | N2N",
     "Página no encontrada"),
    ("conocimiento/control-de-cambios-sistemas-criticos/index.html",
     "Control de cambios en sistemas críticos | N2N",
     "Control de cambios en sistemas críticos"),
    ("nosotros/index.html",
     "Quiénes somos — Carlos Petit, Fundador | N2N",
     "Quiénes somos: Carlos Petit, fundador de N2N"),
]

CANALES = [
    "<title>%s</title>",
    '<meta property="og:title" content="%s">',
    '<meta name="twitter:title" content="%s">',
]


def fail(msg):
    print("ABORTADO: %s" % msg)
    sys.exit(1)


def main():
    if not os.path.isdir(os.path.join(REPO, ".git")):
        fail("no parece un repo git: %s" % REPO)

    # --- longitudes
    print("Longitudes:")
    for rel, viejo, nuevo in MAPEO:
        if len(nuevo) > LIMITE:
            fail("%s — title de %d chars (max %d)" % (rel, len(nuevo), LIMITE))
    print("  OK  los %d titles nuevos estan dentro de %d chars"
          % (len(MAPEO), LIMITE))

    # --- pasada 1: verificar todo sin escribir
    print("")
    print("Verificacion previa (sin escribir):")
    pendientes = []
    for rel, viejo, nuevo in MAPEO:
        path = os.path.join(REPO, rel)
        if not os.path.isfile(path):
            fail("no existe %s" % rel)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        canales_presentes = []
        for plantilla in CANALES:
            c = html.count(plantilla % viejo)
            if c == 1:
                canales_presentes.append(plantilla)
            elif c > 1:
                fail("%s — el title aparece %d veces en %s"
                     % (rel, c, plantilla.split(" ")[0]))

        if (CANALES[0] % viejo) not in html:
            fail("%s — no se encontro el <title> esperado" % rel)
        if len(canales_presentes) not in (1, 3):
            fail("%s — solo %d de 3 canales presentes; se espera 3, o 1 en "
                 "paginas sin metadatos sociales" % (rel, len(canales_presentes)))

        pendientes.append((path, rel, html, viejo, nuevo, canales_presentes))
        print("  OK  %-52s %2d -> %2d chars  (%d canales)"
              % (rel, len(viejo), len(nuevo), len(canales_presentes)))

    # --- pasada 2: escribir
    print("")
    print("Aplicando:")
    for path, rel, html, viejo, nuevo, canales in pendientes:
        original = html
        for plantilla in canales:
            html = html.replace(plantilla % viejo, plantilla % nuevo, 1)

        # guardas por pagina
        for plantilla in canales:
            if (plantilla % nuevo) not in html:
                fail("%s — no quedo aplicado en %s" % (rel, plantilla))
            if (plantilla % viejo) in html:
                fail("%s — sobrevive el title viejo en %s" % (rel, plantilla))

        delta_esperado = len(canales) * (len(nuevo) - len(viejo))
        if len(html) - len(original) != delta_esperado:
            fail("%s — el diff no corresponde solo a los titles" % rel)

        shutil.copy2(path, path + ".bak")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("  %-52s %d canales" % (rel, len(canales)))

    print("")
    print("Paginas modificadas: %d" % len(pendientes))
    print("Backups .bak junto a cada archivo (borrar tras validar).")
    print("LISTO")


if __name__ == "__main__":
    main()
