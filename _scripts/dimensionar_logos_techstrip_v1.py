#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dimensionar_logos_techstrip_v1.py

Agrega width y height a los 8 logos de la franja de infraestructura de la
home. Sin esos atributos el navegador no reserva el espacio antes de que
cargue la hoja de estilos, y la seccion salta al renderizar (layout shift).

Los valores son 40x40 porque es exactamente lo que ya fija el CSS:

    .tech-strip__item img { width: 40px; height: 40px; object-fit: contain; }

No hay riesgo de deformacion: object-fit contain respeta la proporcion del
viewBox de cada SVG, que va de 24x24 a 256x153. Los atributos solo actuan
como reserva de espacio hasta que el CSS toma el control, y el breakpoint
de 640px que los baja a 32x32 sigue funcionando igual, porque el CSS gana
sobre los atributos.

Solo modifica esos 8 tags img. No toca CSS, header, footer ni contenido.

Aborta sin escribir si cualquier tag no aparece exactamente una vez.

Uso:
    python3 _scripts/dimensionar_logos_techstrip_v1.py
"""

import os
import shutil
import sys

REPO = "/home/dflorida/GITHUB/n2n/n2n-site"
TARGET = os.path.join(REPO, "index.html")

# (archivo svg, texto del alt)
LOGOS = [
    ("hetzner.svg", "Hetzner"),
    ("MaterialIconThemeDocker.svg", "Docker"),
    ("DeviconLinux.svg", "Linux"),
    ("MaterialIconThemePython.svg", "Python"),
    ("FileIconsNestjs.svg", "Next.js"),
    ("LogosCloudflareIcon.svg", "Cloudflare"),
    ("LogosAws.svg", "AWS"),
    ("SimpleIconsOdoo.svg", "Odoo"),
]

LADO = 40

VIEJO = '<img src="/img/logos/%s" alt="%s" loading="lazy">'
NUEVO = '<img src="/img/logos/%s" alt="%s" width="%d" height="%d" loading="lazy">'


def fail(msg):
    print("ABORTADO: %s" % msg)
    sys.exit(1)


def main():
    if not os.path.isfile(TARGET):
        fail("no existe %s" % TARGET)

    with open(TARGET, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # --- pasada 1: verificar los 8 sin escribir
    print("Verificacion previa:")
    pares = []
    for svg, alt in LOGOS:
        v = VIEJO % (svg, alt)
        n = NUEVO % (svg, alt, LADO, LADO)
        c = html.count(v)
        if c != 1:
            fail("%s — el tag aparece %d veces (esperaba 1)" % (svg, c))
        pares.append((v, n, svg))
        print("  OK  %s" % svg)

    # --- pasada 2: aplicar
    print("")
    print("Aplicando:")
    for v, n, svg in pares:
        html = html.replace(v, n, 1)
        print("  %s -> width=%d height=%d" % (svg, LADO, LADO))

    # --- guardas
    restantes = html.count('img/logos/') - html.count('width="%d" height="%d"' % (LADO, LADO))
    sin_dim = 0
    for svg, alt in LOGOS:
        if (VIEJO % (svg, alt)) in html:
            sin_dim += 1
    if sin_dim:
        fail("%d logos quedaron sin dimensionar" % sin_dim)
    print("  OK  los 8 logos dimensionados")

    for needle, label in [
        ('<header class="site-header" role="banner">', "header intacto"),
        ('<footer class="site-footer" role="contentinfo">', "footer intacto"),
        ('class="tech-strip"', "seccion tech-strip intacta"),
        ('<h1 class="hero__h1" id="hero-h1">', "h1 intacto"),
    ]:
        if needle not in html:
            fail("guarda rota: %s" % label)
        print("  OK  %s" % label)

    # el diff debe ser exactamente 8 veces el largo de los atributos nuevos
    delta_esperado = len(LOGOS) * len(' width="%d" height="%d"' % (LADO, LADO))
    delta_real = len(html) - len(original)
    if delta_real != delta_esperado:
        fail("el diff es de %d bytes y se esperaban %d"
             % (delta_real, delta_esperado))
    print("  OK  diff de %d bytes, solo atributos" % delta_real)

    shutil.copy2(TARGET, TARGET + ".bak")
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(html)

    print("")
    print("Escrito: index.html (%d bytes, antes %d)" % (len(html), len(original)))
    print("Backup .bak junto al archivo (borrar tras validar).")
    print("LISTO")


if __name__ == "__main__":
    main()
