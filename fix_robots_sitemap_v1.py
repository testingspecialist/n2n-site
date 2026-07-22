#!/usr/bin/env python3
# 1. robots.txt: declara explicitamente los crawlers de IA (GEO)
# 2. sitemap.xml: ordena las URLs alfabeticamente
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(".").resolve()

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

SELLO = f"{datetime.now():%Y%m%d_%H%M%S}"

# ------------------------------------------------------------- robots.txt

BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "anthropic-ai",
        "Claude-Web", "PerplexityBot", "Google-Extended", "Applebot-Extended",
        "CCBot", "Bytespider", "meta-externalagent"]

ROBOTS = RAIZ / "robots.txt"
txt = ROBOTS.read_text(encoding="utf-8")

if all(b in txt for b in BOTS):
    print("SALTEA  robots.txt: los crawlers de IA ya estan declarados")
else:
    shutil.copy2(ROBOTS, ROBOTS.with_name(f"robots.txt.bak-{SELLO}"))
    bloques = "\n\n".join(f"User-agent: {b}\nAllow: /" for b in BOTS)
    nuevo = (
        "User-agent: *\n"
        "Allow: /\n\n"
        "# Crawlers de IA — permitidos explicitamente (GEO)\n"
        f"{bloques}\n\n"
        "Sitemap: https://n2n.com.ar/sitemap.xml\n"
    )
    ROBOTS.write_text(nuevo, encoding="utf-8")
    print(f"OK      robots.txt: {len(BOTS)} crawlers de IA declarados")

# ------------------------------------------------------------ sitemap.xml

SM = RAIZ / "sitemap.xml"
sm = SM.read_text(encoding="utf-8")

entradas = re.findall(r"[ \t]*<url>.*?</url>", sm, re.S)
if not entradas:
    print("ERROR: no encuentro entradas <url> en el sitemap. Abortado.")
    sys.exit(1)


def clave(e):
    m = re.search(r"<loc>(.*?)</loc>", e)
    return m.group(1) if m else ""


ordenadas = sorted(entradas, key=clave)

if ordenadas == entradas:
    print("SALTEA  sitemap.xml: ya esta ordenado")
else:
    if len(ordenadas) != len(entradas):
        print("ERROR: se perdieron entradas al ordenar. Abortado.")
        sys.exit(1)
    shutil.copy2(SM, SM.with_name(f"sitemap.xml.bak-{SELLO}"))

    cabecera = sm[: sm.index(entradas[0])]
    fin = sm.rindex("</url>") + len("</url>")
    cola = sm[fin:]
    nuevo = cabecera + "\n".join(e.strip() and "  " + e.strip() for e in ordenadas) + cola

    if nuevo.count("<loc>") != sm.count("<loc>"):
        print("ERROR: cambio la cantidad de URLs. No se escribe. Abortado.")
        sys.exit(1)

    SM.write_text(nuevo, encoding="utf-8")
    print(f"OK      sitemap.xml: {len(ordenadas)} URLs ordenadas alfabeticamente")

print()
print("Listo. Correr diagnostico_sitio_v2.py para verificar.")
