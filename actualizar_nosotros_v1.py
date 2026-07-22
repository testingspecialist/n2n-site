#!/usr/bin/env python3
# Actualiza /nosotros/ — eje Control Operativo (Parte 1)
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import sys

RUTA = "nosotros/index.html"

with open(RUTA, "r", encoding="utf-8") as f:
    html = f.read()

ORIGINAL = len(html)

CAMBIOS = []

# 1 — Hero lead
CAMBIOS.append((
"Hero lead",
'<p class="hero__lead" style="max-width:640px">Esa diferencia define todo lo que hacemos.</p>',
'<p class="hero__lead" style="max-width:640px">Construyo sistemas que representan la operación hacia afuera y la controlan hacia adentro. Esa diferencia define todo lo que hacemos.</p>'
))

# 2 — H2 del bloque bio
CAMBIOS.append((
"H2 bio",
'margin:var(--s3) 0 var(--s5)">Operación real con stack actual. No consultoría teórica.</h2>',
'margin:var(--s3) 0 var(--s5)">Dos oficios que casi nunca están en la misma persona.</h2>'
))

# 3 — Cuerpo bio: 3 parrafos -> 4 parrafos
P = 'color:var(--text-muted);line-height:1.8'
BIO_VIEJA = (
f'<p style="{P};margin-bottom:var(--s5)">Venezolano radicado en Buenos Aires, con más de cuatro décadas de experiencia trabajando en operaciones, tecnología y negocios. A lo largo de mi carrera participé en proyectos de distintos tamaños y sectores, siempre con el mismo enfoque: resolver problemas reales de la forma más simple y eficiente posible.</p>\n'
f'<p style="{P};margin-bottom:var(--s5)">N2N no nació como un emprendimiento para vender servicios. Nació de años de trabajo construyendo soluciones para necesidades concretas, probándolas en producción, mejorándolas y aprendiendo de los resultados.</p>\n'
f'<p style="{P}">Creo en la tecnología como una herramienta para simplificar, automatizar y generar valor. También creo que las mejores soluciones suelen ser las más simples. Este espacio es la forma de compartir esa experiencia, esas metodologías y esa manera de trabajar con otras personas y empresas que buscan resultados reales.</p>'
)
BIO_NUEVA = (
f'<p style="{P};margin-bottom:var(--s5)">Diseño sistemas de control que vuelven inviable la pérdida por desvío interno en operaciones de alto volumen, y construyo el software que los ejecuta. Las dos cosas: el criterio de control y la implementación técnica.</p>\n'
f'<p style="{P};margin-bottom:var(--s5)">Treinta y tres años en análisis de riesgo, investigación de delitos y protección corporativa —carrera militar como oficial superior—, y después dirección de una consultora privada de seguridad corporativa con clientes en el sector empresarial, científico y hotelero.</p>\n'
f'<p style="{P};margin-bottom:var(--s5)">Hace diez años me radiqué en Buenos Aires y volqué esa formación a la tecnología. Hoy soy Gerente de Sistemas de un mayorista de alimentos con cinco depósitos, donde diseño y opero el ecosistema digital completo: stock, trazabilidad, valuación y custodia.</p>\n'
f'<p style="{P}">La mayoría de los que diseñan controles no saben construir el sistema. La mayoría de los que construyen sistemas nunca dirigieron una operación donde las pérdidas se pagan con plata real. N2N existe en ese cruce.</p>'
)
CAMBIOS.append(("Cuerpo bio", BIO_VIEJA, BIO_NUEVA))

# 4 — Seccion Trayectoria (dentro del bloque bg-white existente)
ANCLA = (
'</div>\n</div>\n</div>\n</section>\n\n'
'<section class="section bg-section">\n<div class="container">\n<div class="section-header">\n'
'<span class="section-header__label">Por qué existimos</span>'
)
TRAYECTORIA = (
'</div>\n</div>\n\n'
'<div class="section-header" style="margin-top:var(--s14)">\n'
'<span class="section-header__label">Trayectoria</span>\n'
'<h2>De dónde sale el criterio</h2>\n'
'</div>\n'
'<div class="grid grid--3" style="gap:var(--s5)">\n'
'<div class="card">\n'
'<div class="card__tag">33 años</div>\n'
'<h3 class="card__title">Control y protección corporativa</h3>\n'
'<p class="card__body">Análisis de riesgo, investigación de delitos patrimoniales y diseño de protocolos de custodia en entornos de alta exposición. Dirección de operaciones de custodia y consultora propia de seguridad corporativa.</p>\n'
'</div>\n'
'<div class="card">\n'
'<div class="card__tag">10 años</div>\n'
'<h3 class="card__title">Sistemas en producción</h3>\n'
'<p class="card__body">Arquitectura y operación de ecosistemas digitales industriales: stock multi-depósito, trazabilidad con evidencia, valuación contable e integración ERP.</p>\n'
'</div>\n'
'<div class="card">\n'
'<div class="card__tag">Método</div>\n'
'<h3 class="card__title">Control inevitable</h3>\n'
'<p class="card__body">El control no se pide, se hace estructuralmente inevitable. La operación no avanza sin registro. Ese principio es el núcleo del trabajo.</p>\n'
'</div>\n'
'</div>\n'
'</div>\n</section>\n\n'
'<section class="section bg-section">\n<div class="container">\n<div class="section-header">\n'
'<span class="section-header__label">Por qué existimos</span>'
)
CAMBIOS.append(("Seccion Trayectoria", ANCLA, TRAYECTORIA))

# 5 — Schema: knowsAbout de Person
KA_VIEJO = (
'        "Arquitectura Comercial Digital",\n'
'        "infraestructura digital B2B",'
)
KA_NUEVO = (
'        "Arquitectura Comercial Digital",\n'
'        "control de pérdidas",\n'
'        "prevención de fraude interno",\n'
'        "análisis de riesgo operativo",\n'
'        "cadena de custodia",\n'
'        "seguridad corporativa",\n'
'        "infraestructura digital B2B",'
)
CAMBIOS.append(("Schema knowsAbout", KA_VIEJO, KA_NUEVO))

# 6 — Schema: description de Person
CAMBIOS.append((
"Schema description",
'"description": "40+ años de experiencia operativa en seguridad, inteligencia, operaciones, tecnología y negocios. Construye y opera en producción el ecosistema digital completo de Distribuidora Florida SRL."',
'"description": "Cuatro décadas de experiencia operativa. Treinta y tres años en análisis de riesgo, investigación y protección corporativa; los últimos diez diseñando y operando ecosistemas digitales industriales. Diseña sistemas de control de pérdidas y construye el software que los ejecuta."'
))

# 7 — dateModified
CAMBIOS.append((
"dateModified",
'"dateModified": "2026-06-11"',
'"dateModified": "2026-07-22"'
))

# Validacion previa: cada patron debe existir exactamente una vez
errores = 0
for etiqueta, viejo, nuevo in CAMBIOS:
    n = html.count(viejo)
    if n != 1:
        print(f"ERROR  {etiqueta}: encontrado {n} veces (esperado 1)")
        errores += 1

if errores:
    print(f"\nAbortado. {errores} patron(es) sin coincidencia exacta. Archivo NO modificado.")
    sys.exit(1)

# Aplicacion
for etiqueta, viejo, nuevo in CAMBIOS:
    html = html.replace(viejo, nuevo, 1)
    print(f"OK     {etiqueta}")

with open(RUTA, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n{RUTA} actualizado")
print(f"Bytes: {ORIGINAL} -> {len(html)}  (+{len(html)-ORIGINAL})")
