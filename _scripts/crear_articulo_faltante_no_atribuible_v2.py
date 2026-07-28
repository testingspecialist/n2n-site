#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crear_articulo_faltante_no_atribuible_v2.py

Publica /conocimiento/faltante-no-atribuible/ en n2n-site.
v2: cuerpo revisado por Carlos + H3 en las tres explicaciones + filo restituido
    en el punto tres + pilar 05 nombrado explicitamente.

Patron: verificacion completa sin escribir -> backup -> escribir -> guardas -> abortar ante
cualquier estado inesperado sin tocar nada.

Toca:
  - conocimiento/faltante-no-atribuible/index.html   (nuevo)
  - conocimiento/index.html                          (card nueva)
  - sitemap.xml                                      (URL nueva)

Ejecutar desde la raiz del repo:
  python3 _scripts/crear_articulo_faltante_no_atribuible_v2.py
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime

REPO = os.getcwd()
SLUG = "faltante-no-atribuible"
FECHA = "2026-07-28"
DIR_ART = os.path.join(REPO, "conocimiento", SLUG)
PATH_ART = os.path.join(DIR_ART, "index.html")
PATH_IDX = os.path.join(REPO, "conocimiento", "index.html")
PATH_SITEMAP = os.path.join(REPO, "sitemap.xml")
DIR_BACKUP = os.path.expanduser("~/backups")

TITULO = "Faltante no atribuible: el hueco que nadie puede explicar"
DESCRIPCION = ("Un faltante no atribuible es una diferencia de stock que admite varias "
               "explicaciones, sin evidencia suficiente para determinar cuál ocurrió.")
H1 = "Faltante no atribuible en distribución"
TITULO_CARD = "Faltante no atribuible"
RESUMEN_CARD = ("Una diferencia de stock que admite varias explicaciones y no permite confirmar "
                "ninguna. Por qué el problema no es la pérdida sino la indeterminación")

URL = "https://n2n.com.ar/conocimiento/%s/" % SLUG


def abortar(msg):
    print("ABORTADO: %s" % msg)
    sys.exit(1)


# ---------------------------------------------------------------- cuerpo

CUERPO = """<p><strong>Un faltante no atribuible es una diferencia de inventario que puede tener varias explicaciones, pero ninguna puede demostrarse ni descartarse.</strong> No importa si faltan pocos kilos, varias cajas o un pallet completo. El problema no está solamente en el valor de la mercadería perdida, sino en que la empresa no puede determinar qué ocurrió, dónde ocurrió ni quién tenía la responsabilidad sobre el movimiento.</p>

<p>Puede tratarse de un error administrativo, un traslado mal registrado, una entrega que no se facturó o un desvío deliberado. Cuando todas esas posibilidades dejan el mismo rastro, investigar el faltante no conduce a una conclusión: solo produce hipótesis. Operativamente, esta situación puede ser incluso más dañina que confirmar un robo. Un hecho confirmado permite tomar medidas, corregir el circuito y establecer responsabilidades. Un faltante no atribuible deja la pérdida, mantiene abierta la sospecha y no ofrece una base legítima para actuar.</p>

<h2>Cómo aparece</h2>

<p>En muchos depósitos, la diferencia no se detecta en el momento en que ocurre. Aparece semanas o meses después, durante un inventario, una conciliación administrativa o el cierre de un período. Para entonces, la mercadería ya pasó por distintas manos, vehículos, depósitos y sistemas. Los documentos fueron completados en momentos diferentes y las personas involucradas recuerdan versiones parciales de lo sucedido.</p>

<p>Administración encuentra que el stock físico no coincide con el stock registrado. El responsable del depósito revisa remitos, transferencias, facturas y movimientos internos, pero los documentos disponibles no permiten reconstruir con certeza el recorrido de la mercadería. En ese punto suelen aparecer tres explicaciones posibles.</p>

<h3>Uno: la mercadería se entregó y no se facturó</h3>

<p>La mercadería salió correctamente del depósito y llegó al cliente, pero el circuito administrativo no completó la facturación o registró la operación de manera incorrecta. La baja física del stock fue real. La mercadería no fue robada ni quedó perdida entre depósitos. Lo que falta es la contrapartida comercial que justifica su salida.</p>

<p>En este caso la pérdida proviene de un error de proceso y se corrige modificando el circuito de despacho, facturación y control documental. El problema es que, si no existe evidencia generada durante la carga y la entrega, meses después esta explicación puede resultar tan difícil de demostrar como cualquier otra.</p>

<h3>Dos: el traslado entre depósitos nunca ocurrió como fue declarado</h3>

<p>Un depósito registra la salida de determinada cantidad y el depósito de destino registra o da por recibida la transferencia completa. Sin embargo, el movimiento pudo haberse realizado parcialmente, contener productos diferentes o directamente no haber ocurrido. El sistema muestra una transferencia completa porque alguien cargó administrativamente una transferencia completa, pero ese registro no demuestra por sí solo que la cantidad declarada salió, viajó y fue recibida.</p>

<p>Esto ocurre cuando origen y destino trabajan sobre declaraciones, sin una verificación independiente de los productos, cantidades, pesos, bultos o partidas involucradas. No es necesario que alguien haya mentido. Muchas veces simplemente se dio por hecho que lo declarado coincidía con lo sucedido.</p>

<h3>Tres: hubo desvío</h3>

<p>Quien conoce las debilidades del circuito puede retirar producto aprovechando exactamente las mismas zonas grises que producen los errores administrativos. El faltante termina pareciendo una transferencia mal cargada, una entrega sin facturar o una diferencia de inventario pendiente de revisión.</p>

<p>Este es el punto incómodo: cuando el control depende de declaraciones, un error y un desvío dejan el mismo rastro. <strong>La forma de esconder un robo es hacerlo parecer un traslado mal cargado.</strong> La empresa puede sospechar que hubo una irregularidad y no tener con qué demostrarla, y tampoco puede descartar que todo se haya originado en una falla administrativa.</p>

<h2>Por qué nadie puede determinar qué ocurrió</h2>

<p>La mayoría de las empresas no carece de información. Tiene mucha información, pero distribuida en registros que no se validan entre sí. El sistema de stock registra movimientos de inventario. El sistema administrativo registra facturas y remitos. Los depósitos registran transferencias. El transporte maneja sus propias planillas. Las evidencias fotográficas, cuando existen, suelen quedar dispersas en teléfonos o conversaciones de WhatsApp.</p>

<p>Cada registro puede parecer correcto cuando se analiza por separado. El traslado figura completo, el remito está emitido, la factura coincide con lo cargado, el chofer realizó el viaje y el depósito de destino informó la recepción. Sin embargo, ningún registro demuestra por sí solo que determinada mercadería, en determinada cantidad, salió del punto de origen, fue transportada y llegó al destino previsto.</p>

<p>Cuando los sistemas no comparten una referencia común, la empresa termina administrando varias versiones de un mismo movimiento físico. El faltante aparece precisamente en el espacio que queda entre esas versiones.</p>

<p>Ante cualquier salida, recepción o transferencia de mercadería, la pregunta principal debería ser la siguiente:</p>

<p><strong>¿Existe una evidencia generada en el momento del movimiento, validada por alguien distinto de quien lo ejecutó y capaz de contradecir una explicación posterior?</strong></p>

<p>Si la respuesta es negativa, cualquier futura diferencia será difícil de atribuir. El problema no comenzó el día en que se encontró el faltante. Comenzó cuando se permitió que la mercadería se moviera sin dejar una evidencia verificable sobre qué salió, cuánto salió, quién lo entregó, quién lo transportó y quién lo recibió.</p>

<p>Un documento completado varios días después no reemplaza una evidencia contemporánea. Una declaración realizada por la misma persona que ejecutó el movimiento tampoco constituye una validación independiente.</p>

<h2>Lo que no resuelve el problema</h2>

<p>Una auditoría puede ordenar los registros disponibles, detectar inconsistencias y establecer qué documentos faltan, pero no puede crear evidencia que nunca fue generada. Si el movimiento se realizó sin controles suficientes, la revisión posterior dependerá de declaraciones, recuerdos y registros aislados. La auditoría podrá identificar distintos escenarios posibles, pero difícilmente podrá determinar cuál ocurrió. Cuanto más tiempo pasa, menor es la posibilidad de reconstruir el movimiento con precisión.</p>

<p>Agregar supervisores también puede reducir algunos errores, pero no elimina la indeterminación. Un supervisor puede observar una carga, una descarga o una transferencia, aunque su presencia no siempre deja un registro preciso de productos, cantidades, pesos y documentos relacionados. También puede estar atendiendo varias operaciones al mismo tiempo, ser reemplazado o encontrarse ausente cuando ocurre el movimiento. El control no puede depender exclusivamente de que una persona determinada esté presente, recuerde lo sucedido y pueda explicarlo meses después.</p>

<p>Las cámaras pueden demostrar que un vehículo ingresó, que una carga salió o que se movieron determinados bultos, pero normalmente no permiten confirmar con precisión qué producto contenía cada bulto, cuánto pesaba, a qué partida correspondía o contra qué orden se realizó el movimiento. Son una evidencia complementaria, no un reemplazo de la identificación de la mercadería ni de la validación documental.</p>

<p>Un sistema de stock más moderno tampoco resuelve por sí solo el problema. El sistema registra la información que recibe. Si una transferencia se carga como completa, la mostrará como completa. Si una recepción se confirma sin controlar la mercadería física, registrará una recepción que puede no coincidir con lo recibido. Un sistema más moderno puede procesar con mayor rapidez, generar mejores reportes y reducir errores de carga, pero si los datos continúan siendo declarativos, seguirá registrando declaraciones. La precisión del software no garantiza la veracidad del hecho físico: un sistema puede informar con absoluta exactitud un movimiento que nunca ocurrió de la manera registrada.</p>

<h2>Cómo evitar que el faltante quede sin explicación</h2>

<p>La solución consiste en vincular el movimiento físico con sus registros administrativos y operativos desde el momento en que ocurre. Una salida debe quedar asociada a una orden concreta, a productos identificados, a cantidades verificadas y a una persona responsable de la entrega.</p>

<p>Una transferencia entre depósitos no debería considerarse terminada cuando el depósito de origen declara la salida. Debe permanecer abierta hasta que el destino confirme la recepción de esa misma partida, indicando cantidades, pesos, bultos y cualquier diferencia encontrada. Una entrega a cliente debe relacionar la preparación, la carga, el remito y la recepción. Si falta una de esas etapas, el circuito debe mostrarlo inmediatamente y no varios meses después.</p>

<p>La etapa siguiente no debería poder cerrarse si la anterior no dejó la evidencia requerida. El objetivo no es agregar burocracia, sino evitar que una operación continúe avanzando mientras deja atrás movimientos imposibles de verificar.</p>

<p>La integración operativa tampoco consiste únicamente en transferir información entre programas. Consiste en lograr que un mismo hecho físico tenga una única referencia a lo largo de todo el circuito. La mercadería que sale del depósito debe ser la misma que figura en el remito, la misma que transporta el vehículo, la misma que confirma el destino y la misma que descuenta el sistema de stock.</p>

<p>Si cada área registra su propia versión del movimiento, la empresa conserva información pero pierde trazabilidad. La integración debe permitir que un registro contradiga a otro cuando existe una diferencia. Esa contradicción es necesaria porque señala el punto exacto donde el movimiento dejó de coincidir con lo esperado.</p>

<p>Eso es la <strong>integración con sistemas operativos</strong>, el quinto pilar de <a href="/control/protocolo-cero/">Protocolo CERO</a>: impedir que un hecho físico exista en un área y permanezca invisible para las demás. El <a href="/casos/caso-01/">rediseño del flujo de evidencia en un distribuidor de cadena de frío</a> muestra cómo puede aplicarse este criterio en una operación real. Los conceptos relacionados están definidos en el <a href="/glosario/">glosario</a>.</p>

<h2>El costo que no aparece en los reportes</h2>

<p>El valor de la mercadería faltante puede calcularse y contabilizarse. El daño interno que provoca un faltante no atribuible es mucho más difícil de medir.</p>

<p>La empresa no puede sancionar porque no tiene pruebas suficientes. No puede corregir con precisión porque no sabe qué parte del proceso falló. Tampoco puede descartar que haya existido un desvío. La sospecha queda abierta y termina alcanzando a todas las personas que participaron en el circuito, incluso a quienes realizaron correctamente su trabajo.</p>

<p>El responsable del depósito queda expuesto. Administración desconfía de la operación. La operación considera que los registros administrativos son incorrectos. Los choferes, encargados y camaristas quedan incluidos en una investigación que no puede llegar a una conclusión. Ese deterioro afecta la autoridad, la confianza y la capacidad de trabajo del equipo.</p>

<p>Por eso el verdadero objetivo de un sistema de control no es solamente detectar faltantes. Es generar evidencia suficiente para explicar cada diferencia y ubicar con precisión el punto donde se originó.</p>

<p><strong>Una empresa no controla mejor porque encuentra más faltantes. Controla mejor cuando puede explicar cada uno.</strong></p>

<h2>Preguntas frecuentes</h2>

<h3>¿Qué diferencia existe entre un faltante y un faltante no atribuible?</h3>

<p>Un faltante es una diferencia entre el inventario físico y el inventario registrado. Un faltante no atribuible es una diferencia para la cual existen varias explicaciones posibles, pero no hay evidencia suficiente para confirmar una y descartar las demás. La diferencia no está en el valor de la pérdida, sino en la posibilidad de determinar qué ocurrió.</p>

<h3>¿Puede investigarse un faltante varios meses después?</h3>

<p>Puede investigarse, pero el resultado dependerá de la evidencia generada cuando ocurrió el movimiento. Si solo existen declaraciones, registros aislados y documentos completados posteriormente, la investigación difícilmente será concluyente. Una revisión posterior puede detectar inconsistencias, pero no reconstruir con certeza un hecho que no fue documentado correctamente.</p>

<h3>¿Por qué un sistema de stock no evita estos faltantes?</h3>

<p>Porque el sistema registra lo que los usuarios declaran. Si una salida, transferencia o recepción se carga sin verificar el movimiento físico, el sistema conservará un dato que puede ser administrativamente correcto y físicamente falso. El problema no está únicamente en el software, sino en la falta de conexión entre el registro y el hecho que ese registro representa.</p>"""


FAQ = [
    ("¿Qué diferencia existe entre un faltante y un faltante no atribuible?",
     "Un faltante es una diferencia entre el inventario físico y el inventario registrado. Un "
     "faltante no atribuible es una diferencia para la cual existen varias explicaciones posibles, "
     "pero no hay evidencia suficiente para confirmar una y descartar las demás. La diferencia no "
     "está en el valor de la pérdida, sino en la posibilidad de determinar qué ocurrió."),
    ("¿Puede investigarse un faltante varios meses después?",
     "Puede investigarse, pero el resultado dependerá de la evidencia generada cuando ocurrió el "
     "movimiento. Si solo existen declaraciones, registros aislados y documentos completados "
     "posteriormente, la investigación difícilmente será concluyente. Una revisión posterior puede "
     "detectar inconsistencias, pero no reconstruir con certeza un hecho que no fue documentado "
     "correctamente."),
    ("¿Por qué un sistema de stock no evita estos faltantes?",
     "Porque el sistema registra lo que los usuarios declaran. Si una salida, transferencia o "
     "recepción se carga sin verificar el movimiento físico, el sistema conservará un dato que "
     "puede ser administrativamente correcto y físicamente falso. El problema no está únicamente "
     "en el software, sino en la falta de conexión entre el registro y el hecho que ese registro "
     "representa."),
]

JSONLD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "TechArticle",
            "headline": TITULO,
            "description": DESCRIPCION,
            "url": URL,
            "datePublished": FECHA,
            "dateModified": FECHA,
            "author": {
                "@type": "Person",
                "@id": "https://n2n.com.ar/nosotros/#carlos-petit",
                "name": "Carlos Petit",
                "url": "https://n2n.com.ar/nosotros/",
                "sameAs": ["https://www.linkedin.com/in/carlos-petit-gaitan/"],
            },
            "publisher": {"@id": "https://n2n.com.ar/#organization"},
            "isPartOf": {"@id": "https://n2n.com.ar/#website"},
            "inLanguage": "es",
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in FAQ
            ],
        },
    ],
}

HTML = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(titulo)s</title>
<meta name="description" content="%(desc)s">
<link rel="icon" href="/img/favicon.ico" sizes="any">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/Outfit-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/css/main.css" as="style">
<link rel="stylesheet" href="/css/main.css">
<link rel="canonical" href="%(url)s">
<meta property="og:title" content="%(titulo)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:type" content="article">
<meta property="og:image" content="https://n2n.com.ar/img/og-n2n.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(titulo)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="https://n2n.com.ar/img/og-n2n.png">
<meta property="article:author" content="Carlos Petit">
<meta property="article:published_time" content="%(fecha)s">
<script type="application/ld+json">
%(jsonld)s
</script>
</head>
<body>
<header class="site-header" role="banner">
  <a class="skip-link" href="#main-content">Saltar al contenido</a>
  <div class="container">
    <nav class="nav" aria-label="Navegación principal">
      <a href="/" class="nav__logo" aria-label="N2N — Inicio">
        <img src="/img/logo.png" alt="N2N" width="140" height="38" loading="eager" fetchpriority="high">
      </a>
      <button class="nav__toggle" id="nav-toggle" aria-controls="nav-links" aria-expanded="false" aria-label="Abrir menú" type="button">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
      <ul class="nav__links" id="nav-links" role="list">
        <li><a href="/framework/como-funciona/">Framework</a></li>
        <li><a href="/industrias/">Industrias</a></li>
        <li><a href="/servicios/">Servicios</a></li>
        <li><a href="/casos/">Casos</a></li>
        <li><a href="/conocimiento/" aria-current="page">Conocimiento</a></li>
        <li><a href="/nosotros/">Nosotros</a></li>
        <li><a href="/contacto/" class="nav__cta">Contacto</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main-content">
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="breadcrumb"><a href="/">Inicio</a><span>›</span><a href="/conocimiento/">Conocimiento</a></p>
    <p class="hero__label">Conocimiento</p>
    <h1 class="hero__h1" id="page-h1">%(h1)s</h1>
    <p class="hero__lead">%(desc)s</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="prose">%(cuerpo)s</div>
    <div style="margin-top:var(--s10);padding-top:var(--s8);border-top:1px solid var(--border);display:flex;gap:var(--s4);flex-wrap:wrap">
      <a href="/conocimiento/" class="btn btn--ghost">← Volver a Conocimiento</a>
      <a href="/contacto/" class="btn btn--primary">Evaluar mi operación →</a>
    </div>
  </div>
</section>
<section class="author-bio" aria-label="Sobre el autor" style="background:var(--bg-section);border-top:3px solid var(--orange);padding:var(--s10) 0">
<div class="container">
<div style="max-width:780px;margin:0 auto;display:flex;gap:var(--s6);align-items:flex-start;flex-wrap:wrap">
<img src="/img/carlos-petit.png" alt="Carlos Petit — Fundador de N2N" width="88" height="88" loading="lazy" style="border-radius:50%%;object-fit:cover;aspect-ratio:1/1;border:3px solid var(--orange);flex-shrink:0">
<div style="flex:1;min-width:240px">
<p style="font-weight:800;color:var(--navy);font-size:1.1rem;margin-bottom:2px">Carlos Petit</p>
<p style="color:var(--orange);font-weight:600;font-size:.9rem;margin-bottom:var(--s3)">Fundador y Arquitecto Principal de N2N</p>
<p style="color:var(--text-muted);line-height:1.7;font-size:.95rem;margin-bottom:var(--s4)">Cuatro décadas resolviendo operaciones reales con tecnología actual. Construye y opera en producción los sistemas que N2N comercializa como metodología.</p>
<div style="display:flex;gap:var(--s3);flex-wrap:wrap">
<a href="https://www.linkedin.com/in/carlos-petit-gaitan/" target="_blank" rel="noopener noreferrer" class="btn btn--outline" style="font-size:.82rem;padding:.4em 1em">LinkedIn →</a>
<a href="/nosotros/" class="btn btn--outline" style="font-size:.82rem;padding:.4em 1em">Sobre N2N →</a>
</div>
</div>
</div>
</div>
</section>
</main>
<footer class="site-footer" role="contentinfo">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <a href="/" class="footer__logo"><img src="/img/logo-white.png" alt="N2N" width="120" height="32" loading="lazy"></a>
        <p class="footer__about">N2N diseña sistemas digitales que filtran ruido comercial y habilitan conversaciones B2B reales para operaciones industriales que venden por volumen.</p>
      </div>
      <div class="footer__col">
        <p class="footer__col-title">Navegación</p>
        <ul role="list">
          <li><a href="/framework/como-funciona/">Framework</a></li>
          <li><a href="/industrias/">Industrias</a></li>
          <li><a href="/servicios/">Servicios</a></li>
          <li><a href="/precios/">Precios</a></li>
          <li><a href="/casos/">Casos</a></li>
          <li><a href="/conocimiento/">Conocimiento</a></li>
          <li><a href="/nosotros/">Nosotros</a></li>
          <li><a href="/contacto/">Contacto</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <p class="footer__col-title">Contacto</p>
        <ul role="list">
          <li><a href="mailto:contacto@n2n.com.ar">contacto@n2n.com.ar</a></li>
          <li><a href="https://wa.me/5491138230614" target="_blank" rel="noopener noreferrer">WhatsApp</a></li>
          <li><a href="https://www.linkedin.com/company/node2node/" target="_blank" rel="noopener noreferrer">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <p>Designed by <a href="https://n2n.com.ar">N2N</a> &nbsp;|&nbsp; Copyright &copy; 2026 N2N</p>
      <div class="footer__bottom-links">
        <a href="/legal/">Privacidad</a>
        <a href="/legal/#cookies">Cookies</a>
      </div>
    </div>
  </div>
</footer>
<script src="/js/main.js" defer></script>
<script defer src="https://umami.n2n.com.ar/script.js" data-website-id="05b64f33-b9ae-4ffa-b068-8a2dacff6e33"></script>
</body>
</html>
""" % {
    "titulo": TITULO,
    "desc": DESCRIPCION,
    "url": URL,
    "fecha": FECHA,
    "h1": H1,
    "jsonld": json.dumps(JSONLD, ensure_ascii=False, indent=2),
    "cuerpo": CUERPO,
}

CARD = ('<a href="/conocimiento/%s/" class="card card--link">'
        '<h2 class="card__title">%s</h2>'
        '<p class="card__body">%s…</p>'
        '<span class="card__link">Leer →</span></a>' % (SLUG, TITULO_CARD, RESUMEN_CARD))

SITEMAP_LINE = '  <url><loc>%s</loc><lastmod>%s</lastmod></url>' % (URL, FECHA)


# ================================================================ FASE 1: VERIFICAR

print("=" * 62)
print("FASE 1 — VERIFICACION (no se escribe nada)")
print("=" * 62)

if not os.path.isdir(os.path.join(REPO, ".git")):
    abortar("no estas en la raiz del repo (no hay .git). cd al repo primero.")

for p in (PATH_IDX, PATH_SITEMAP):
    if not os.path.isfile(p):
        abortar("falta %s" % p)

if os.path.exists(DIR_ART):
    abortar("%s ya existe. No piso nada." % DIR_ART)

if len(TITULO) > 62:
    abortar("title de %d chars (max 62)" % len(TITULO))
if not (120 <= len(DESCRIPCION) <= 158):
    abortar("description de %d chars (rango 120-158)" % len(DESCRIPCION))
print("[ok] title %d chars · description %d chars" % (len(TITULO), len(DESCRIPCION)))

try:
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S)
    json.loads(m.group(1))
except Exception as e:
    abortar("JSON-LD invalido: %s" % e)
print("[ok] JSON-LD parsea")

campos = {
    "meta description": re.search(r'<meta name="description" content="([^"]+)"', HTML),
    "og:description": re.search(r'<meta property="og:description" content="([^"]+)"', HTML),
    "twitter:description": re.search(r'<meta name="twitter:description" content="([^"]+)"', HTML),
    "hero__lead": re.search(r'<p class="hero__lead">([^<]+)</p>', HTML),
}
valores = set()
for k, v in campos.items():
    if v is None:
        abortar("no encuentro %s en el HTML generado" % k)
    valores.add(v.group(1))
if len(valores) != 1:
    abortar("los 4 campos de descripcion no coinciden entre si")
print("[ok] meta/og/twitter/hero__lead sincronizados")

# jerarquia de headings: un solo h1, ningun h3 antes del primer h2
h1s = re.findall(r'<h1[ >]', HTML)
if len(h1s) != 1:
    abortar("hay %d h1 en la pagina" % len(h1s))
niveles = [int(x) for x in re.findall(r'<h([23])[ >]', CUERPO)]
if not niveles or niveles[0] != 2:
    abortar("el cuerpo no arranca con h2")
for a, b in zip(niveles, niveles[1:]):
    if b - a > 1:
        abortar("salto de jerarquia h%d -> h%d" % (a, b))
print("[ok] jerarquia de headings: 1 h1, %d h2/h3 sin saltos" % len(niveles))

# el articulo tiene que anclar el pilar 05
if "integración con sistemas operativos" not in CUERPO.lower():
    abortar("el cuerpo no nombra el pilar 05")
print("[ok] pilar 05 nombrado en el cuerpo")

idx_html = open(PATH_IDX, encoding="utf-8").read()
marcador_card = '<span class="card__link">Leer →</span></a>'
n_cards = idx_html.count(marcador_card)
if n_cards == 0:
    abortar("no encuentro el marcador de card en conocimiento/index.html")
print("[ok] %d cards existentes en el indice" % n_cards)

if SLUG in idx_html:
    abortar("el slug ya figura en conocimiento/index.html")

sm = open(PATH_SITEMAP, encoding="utf-8").read()
if URL in sm:
    abortar("la URL ya figura en sitemap.xml")
lineas_sm = sm.split("\n")
conocimiento_idx = [i for i, l in enumerate(lineas_sm)
                    if "n2n.com.ar/conocimiento/" in l and "<loc>" in l]
if not conocimiento_idx:
    abortar("no encuentro URLs de /conocimiento/ en el sitemap")


def slug_de(linea):
    mm = re.search(r'<loc>https://n2n\.com\.ar/conocimiento/([^/]*)/?</loc>', linea)
    return mm.group(1) if mm else ""


destino = None
for i in conocimiento_idx:
    s = slug_de(lineas_sm[i])
    if s and s > SLUG:
        destino = i
        break
if destino is None:
    destino = conocimiento_idx[-1] + 1
print("[ok] sitemap: %d URLs de conocimiento · inserto en linea %d" % (len(conocimiento_idx), destino + 1))

for ruta in ("control/protocolo-cero", "casos/caso-01", "glosario"):
    if not os.path.isfile(os.path.join(REPO, ruta, "index.html")):
        abortar("link interno roto: /%s/ no existe en disco" % ruta)
print("[ok] links internos del cuerpo verificados")

print("\nVERIFICACION COMPLETA. Procedo a escribir.\n")


# ================================================================ FASE 2: BACKUP

print("=" * 62)
print("FASE 2 — BACKUP")
print("=" * 62)

os.makedirs(DIR_BACKUP, exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
for src in (PATH_IDX, PATH_SITEMAP):
    dst = os.path.join(DIR_BACKUP, "%s_%s" % (stamp, src.replace(REPO + "/", "").replace("/", "_")))
    shutil.copy2(src, dst)
    print("[backup] %s" % dst)


# ================================================================ FASE 3: ESCRIBIR

print("\n" + "=" * 62)
print("FASE 3 — ESCRITURA")
print("=" * 62)

os.makedirs(DIR_ART)
with open(PATH_ART, "w", encoding="utf-8") as f:
    f.write(HTML)
print("[escrito] %s (%d bytes)" % (PATH_ART, len(HTML.encode("utf-8"))))

pos = idx_html.rfind(marcador_card) + len(marcador_card)
idx_nuevo = idx_html[:pos] + CARD + idx_html[pos:]
with open(PATH_IDX, "w", encoding="utf-8") as f:
    f.write(idx_nuevo)
print("[escrito] card agregada a conocimiento/index.html")

lineas_sm.insert(destino, SITEMAP_LINE)
with open(PATH_SITEMAP, "w", encoding="utf-8") as f:
    f.write("\n".join(lineas_sm))
print("[escrito] URL agregada a sitemap.xml")


# ================================================================ FASE 4: GUARDAS

print("\n" + "=" * 62)
print("FASE 4 — GUARDAS POSTERIORES")
print("=" * 62)

ok = True

h = open(PATH_ART, encoding="utf-8").read()
mm = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
try:
    json.loads(mm.group(1))
    print("[ok] JSON-LD valido en disco")
except Exception as e:
    print("[FALLO] JSON-LD en disco: %s" % e)
    ok = False

c = open(PATH_IDX, encoding="utf-8").read().count('/conocimiento/%s/' % SLUG)
print("[%s] card en indice: %d ocurrencia(s)" % ("ok" if c == 1 else "FALLO", c))
ok = ok and c == 1

c = open(PATH_SITEMAP, encoding="utf-8").read().count(URL)
print("[%s] URL en sitemap: %d ocurrencia(s)" % ("ok" if c == 1 else "FALLO", c))
ok = ok and c == 1

c2 = open(PATH_IDX, encoding="utf-8").read().count(marcador_card)
print("[%s] cards en indice: %d (antes %d)" % ("ok" if c2 == n_cards + 1 else "FALLO", c2, n_cards))
ok = ok and c2 == n_cards + 1

print("\n" + ("LISTO. Correr los dos auditores antes del commit." if ok
              else "HAY FALLOS. Restaurar desde ~/backups/ antes de seguir."))
