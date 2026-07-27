#!/usr/bin/env python3
# Diagnostico integral read-only de n2n-site
# NO escribe, NO modifica, NO borra. Solo lee y reporta.
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DOMINIO = "https://n2n.com.ar"
RAIZ = Path(".").resolve()

FALLOS = []
AVISOS = []
INFOS = []


def fallo(cat, msg):
    FALLOS.append((cat, msg))


def aviso(cat, msg):
    AVISOS.append((cat, msg))


def info(cat, msg):
    INFOS.append((cat, msg))


def titulo(t):
    print()
    print("=" * 74)
    print(t)
    print("=" * 74)


# ---------------------------------------------------------------- 0. contexto

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(2)

paginas = sorted(p for p in RAIZ.rglob("*.html") if ".git" not in p.parts)


def url_de(p: Path) -> str:
    rel = p.relative_to(RAIZ).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


titulo("1. INVENTARIO")
print(f"Raiz:            {RAIZ}")
print(f"Archivos .html:  {len(paginas)}")

criticos = ["robots.txt", "sitemap.xml", "CNAME", "llms.txt", "404.html",
            "css/main.css", "js/main.js", "fonts/Outfit-Variable.woff2",
            "img/og-n2n.jpg", "img/favicon.ico", "img/favicon.svg"]
for c in criticos:
    ok = (RAIZ / c).is_file()
    print(f"  {'OK  ' if ok else 'FALTA'}  {c}")
    if not ok:
        fallo("archivos", f"falta archivo critico: {c}")

sueltos = [p.relative_to(RAIZ).as_posix() for p in RAIZ.rglob("*.bak-*")]
sueltos += [p.relative_to(RAIZ).as_posix() for p in RAIZ.rglob("*.bak")]
if sueltos:
    for s in sueltos:
        aviso("limpieza", f"backup suelto en el repo: {s}")

# ---------------------------------------------------------- 1. parseo paginas

RX = {
    "title": re.compile(r"<title>(.*?)</title>", re.S | re.I),
    "desc": re.compile(r'<meta\s+name="description"\s+content="(.*?)"', re.S | re.I),
    "canon": re.compile(r'<link\s+rel="canonical"\s+href="(.*?)"', re.I),
    "ogt": re.compile(r'<meta\s+property="og:title"\s+content="(.*?)"', re.S | re.I),
    "ogd": re.compile(r'<meta\s+property="og:description"\s+content="(.*?)"', re.S | re.I),
    "ogu": re.compile(r'<meta\s+property="og:url"\s+content="(.*?)"', re.I),
    "ogi": re.compile(r'<meta\s+property="og:image"\s+content="(.*?)"', re.I),
    "tw": re.compile(r'<meta\s+name="twitter:card"\s+content="(.*?)"', re.I),
    "robots": re.compile(r'<meta\s+name="robots"\s+content="(.*?)"', re.I),
    "lang": re.compile(r'<html\s+lang="([a-z-]+)"', re.I),
    "ld": re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S),
    "ga4": re.compile(r"G-07T9PCBG7P"),
    "viewport": re.compile(r'<meta\s+name="viewport"', re.I),
    "href": re.compile(r'href="([^"]+)"'),
    "src": re.compile(r'src="([^"]+)"'),
    "srcset": re.compile(r'srcset="([^"]+)"'),
}

datos = {}
for p in paginas:
    txt = p.read_text(encoding="utf-8", errors="replace")
    d = {"txt": txt, "url": url_de(p), "path": p}
    for k, rx in RX.items():
        if k in ("ld", "href", "src", "srcset"):
            continue
        m = rx.search(txt)
        d[k] = m.group(1).strip() if (m and m.groups()) else (bool(m) if m else None)
    d["ld"] = RX["ld"].findall(txt)
    datos[d["url"]] = d

# ------------------------------------------------------------------- 2. head

titulo("2. HEAD / SEO POR PAGINA")

for url in sorted(datos):
    d = datos[url]
    es404 = d["path"].name == "404.html" and d["path"].parent == RAIZ
    problemas = []

    if not d["title"]:
        problemas.append("sin <title>")
    elif len(d["title"]) > 60:
        aviso("title", f'{url} — {len(d["title"])} chars (se trunca en SERP)')

    if not d["desc"] and not es404:
        problemas.append("sin meta description")
    elif d["desc"] and len(d["desc"]) < 100:
        aviso("description", f'{url} — {len(d["desc"])} chars (corta)')
    elif d["desc"] and len(d["desc"]) > 160:
        aviso("description", f'{url} — {len(d["desc"])} chars (larga)')

    if not es404:
        if not d["canon"]:
            problemas.append("sin canonical")
        else:
            esperada = DOMINIO + url
            if d["canon"] != esperada:
                problemas.append(f'canonical {d["canon"]} != {esperada}')
        for campo, etiqueta in (("ogt", "og:title"), ("ogd", "og:description"),
                                ("ogu", "og:url"), ("ogi", "og:image"), ("tw", "twitter:card")):
            if not d[campo]:
                problemas.append(f"sin {etiqueta}")
        if d["ogu"] and d["canon"] and d["ogu"] != d["canon"]:
            problemas.append("og:url != canonical")
        if not d["ld"]:
            problemas.append("sin JSON-LD")
        if d["ogd"] and d["desc"] and d["ogd"] != d["desc"]:
            aviso("og", f"{url} — og:description difiere de meta description")
    else:
        if not d["robots"] or "noindex" not in (d["robots"] or ""):
            problemas.append("404 sin robots noindex")
        if d["desc"] == "":
            aviso("404", "404.html tiene meta description vacia (peor que ausente)")

    if d["lang"] != "es":
        problemas.append(f'html lang="{d["lang"]}"')
    if not d["ga4"]:
        problemas.append("sin GA4")
    if not d["viewport"]:
        problemas.append("sin viewport")

    for b in d["ld"]:
        try:
            j = json.loads(b)
        except json.JSONDecodeError as e:
            problemas.append(f"JSON-LD invalido ({e.msg})")
            continue
        if "@context" not in j:
            problemas.append("JSON-LD sin @context")

    if problemas:
        print(f"FAIL  {url}")
        for x in problemas:
            print(f"        - {x}")
            fallo("head", f"{url}: {x}")
    else:
        print(f"OK    {url}")

# --------------------------------------------------------- 3. duplicados

titulo("3. DUPLICADOS")

for campo, etiqueta in (("title", "title"), ("desc", "meta description")):
    cont = Counter(d[campo] for d in datos.values() if d[campo])
    dups = {k: v for k, v in cont.items() if v > 1}
    if dups:
        for k, v in dups.items():
            corto = (k[:60] + "…") if len(k) > 60 else k
            print(f"AVISO {etiqueta} repetido x{v}: {corto}")
            aviso("duplicados", f"{etiqueta} repetido x{v}: {corto}")
    else:
        print(f"OK    sin {etiqueta} duplicados")

seps = Counter()
for d in datos.values():
    t = d["title"] or ""
    if "—" in t:
        seps["— (em dash)"] += 1
    elif "|" in t:
        seps["| (pipe)"] += 1
    else:
        seps["sin separador"] += 1
print("Separadores en titles:", dict(seps))
if len([k for k in seps if k != "sin separador"]) > 1:
    aviso("marca", f"separador de title inconsistente: {dict(seps)}")

# ------------------------------------------------------ 4. links internos

titulo("4. LINKS INTERNOS Y ASSETS")


def resolver(ref: str):
    ref = ref.split("#")[0].split("?")[0]
    if not ref or ref.startswith(("http", "mailto:", "tel:", "//", "data:")):
        return None
    if not ref.startswith("/"):
        return None
    destino = RAIZ / ref.lstrip("/")
    if ref.endswith("/"):
        return destino / "index.html"
    return destino


rotos = defaultdict(list)
entrantes = defaultdict(set)
total_links = 0

for url, d in datos.items():
    refs = set(RX["href"].findall(d["txt"])) | set(RX["src"].findall(d["txt"]))
    for s in RX["srcset"].findall(d["txt"]):
        for parte in s.split(","):
            refs.add(parte.strip().split(" ")[0])
    for r in refs:
        destino = resolver(r)
        if destino is None:
            continue
        total_links += 1
        if not destino.exists():
            rotos[url].append(r)
        elif destino.suffix == ".html":
            entrantes[url_de(destino)].add(url)

print(f"Referencias internas verificadas: {total_links}")
if rotos:
    for url in sorted(rotos):
        for r in rotos[url]:
            print(f"FAIL  {url} -> {r}  (no existe)")
            fallo("links", f"{url} -> {r} no existe")
else:
    print("OK    sin links internos rotos")

huerfanas = []
for url in sorted(datos):
    if url == "/" or datos[url]["path"].name == "404.html":
        continue
    if not entrantes.get(url):
        huerfanas.append(url)
if huerfanas:
    print("\nPaginas sin ningun link entrante (huerfanas):")
    for u in huerfanas:
        print(f"      {u}")
        info("huerfanas", u)

# ------------------------------------------------------------- 5. sitemap

titulo("5. SITEMAP")

sm = (RAIZ / "sitemap.xml").read_text(encoding="utf-8")
locs = re.findall(r"<loc>(.*?)</loc>", sm)
sin_lastmod = len(re.findall(r"<url>(?!.*<lastmod>).*?</url>", sm, re.S))

print(f"URLs en sitemap: {len(locs)}")

dup = [k for k, v in Counter(locs).items() if v > 1]
for k in dup:
    print(f"FAIL  URL duplicada en sitemap: {k}")
    fallo("sitemap", f"URL duplicada: {k}")

en_sitemap = set()
for loc in locs:
    if not loc.startswith(DOMINIO):
        print(f"FAIL  loc fuera de dominio: {loc}")
        fallo("sitemap", f"loc fuera de dominio: {loc}")
        continue
    ruta = loc[len(DOMINIO):]
    en_sitemap.add(ruta)
    if ruta not in datos:
        print(f"FAIL  en sitemap pero no existe el archivo: {ruta}")
        fallo("sitemap", f"URL sin archivo: {ruta}")
    else:
        rb = datos[ruta]["robots"] or ""
        if "noindex" in rb:
            print(f"FAIL  {ruta} esta en sitemap y tiene noindex (contradiccion)")
            fallo("sitemap", f"{ruta} en sitemap con noindex")

for url, d in datos.items():
    if d["path"].name == "404.html":
        continue
    rb = d["robots"] or ""
    if url not in en_sitemap and "noindex" not in rb:
        print(f"AVISO indexable pero fuera del sitemap: {url}")
        aviso("sitemap", f"indexable fuera del sitemap: {url}")

if sin_lastmod:
    aviso("sitemap", f"{sin_lastmod} entradas sin <lastmod>")

orden = locs == sorted(locs)
print(f"Orden alfabetico: {'OK' if orden else 'no ordenado'}")
if not orden:
    aviso("sitemap", "las URLs no estan en orden alfabetico")

# ----------------------------------------------------- 6. robots y llms

titulo("6. ROBOTS.TXT / LLMS.TXT")

robots = (RAIZ / "robots.txt").read_text(encoding="utf-8")
print(robots.strip()[:400])
if "Sitemap:" not in robots:
    fallo("robots", "robots.txt sin directiva Sitemap")
for bot in ("GPTBot", "ClaudeBot", "anthropic-ai", "Google-Extended", "PerplexityBot"):
    if bot not in robots:
        info("robots", f"{bot} no declarado explicitamente en robots.txt")

if (RAIZ / "llms.txt").is_file():
    llms = (RAIZ / "llms.txt").read_text(encoding="utf-8")
    urls_llms = set(re.findall(r"https://n2n\.com\.ar(/[^\s\)>]*)", llms))
    faltan = sorted(u for u in datos if u not in urls_llms and u != "/404.html"
                    and "noindex" not in (datos[u]["robots"] or ""))
    print(f"\nllms.txt: {len(urls_llms)} URLs declaradas")
    for u in faltan:
        info("llms", f"no figura en llms.txt: {u}")

# ------------------------------------------------------------- 7. pesos

titulo("7. PESO DE ASSETS")

LIMITES = {".png": 300, ".jpg": 300, ".jpeg": 300, ".webp": 200,
           ".svg": 30, ".pdf": 600, ".woff2": 60}
pesados = []
for p in RAIZ.rglob("*"):
    if ".git" in p.parts or not p.is_file():
        continue
    lim = LIMITES.get(p.suffix.lower())
    if lim is None:
        continue
    kb = p.stat().st_size / 1024
    if kb > lim:
        pesados.append((kb, p.relative_to(RAIZ).as_posix(), lim))

if pesados:
    for kb, rel, lim in sorted(pesados, reverse=True):
        print(f"AVISO {kb:8.0f} KB  (limite {lim} KB)  {rel}")
        aviso("peso", f"{rel} = {kb:.0f} KB")
else:
    print("OK    ningun asset sobre el limite")

png_sin_webp = []
for p in RAIZ.rglob("*.png"):
    if ".git" in p.parts or "favicon" in p.name or "icon-" in p.name or "og-" in p.name:
        continue
    if not p.with_suffix(".webp").is_file():
        png_sin_webp.append(p.relative_to(RAIZ).as_posix())
for x in png_sin_webp:
    info("imagenes", f"PNG sin WebP equivalente: {x}")

# ---------------------------------------------------------- 8. estructura

titulo("8. BALANCE DE TAGS")

for url in sorted(datos):
    t = datos[url]["txt"]
    pares = [("<section", "</section>"), ("<div", "</div>"),
             ("<ul", "</ul>"), ("<table", "</table>")]
    malos = [(a, t.count(a), t.count(b)) for a, b in pares if t.count(a) != t.count(b)]
    h1 = len(re.findall(r"<h1[\s>]", t))
    if malos or h1 != 1:
        print(f"FAIL  {url}")
        for a, na, nb in malos:
            print(f"        - {a} {na} != {nb}")
            fallo("estructura", f"{url}: {a} desbalanceado {na}/{nb}")
        if h1 != 1:
            print(f"        - {h1} etiquetas h1 (deberia ser 1)")
            fallo("estructura", f"{url}: {h1} h1")
if not FALLOS or all(c != "estructura" for c, _ in FALLOS):
    print("OK    todas las paginas balanceadas y con un unico h1")

# ------------------------------------------------------------- 9. resumen

titulo("RESUMEN")

print(f"Paginas analizadas: {len(datos)}")
print(f"FALLOS:  {len(FALLOS)}")
print(f"AVISOS:  {len(AVISOS)}")
print(f"INFO:    {len(INFOS)}")

for etiqueta, lista in (("FALLOS", FALLOS), ("AVISOS", AVISOS), ("INFO", INFOS)):
    if not lista:
        continue
    print(f"\n--- {etiqueta} ---")
    por_cat = defaultdict(list)
    for cat, msg in lista:
        por_cat[cat].append(msg)
    for cat in sorted(por_cat):
        print(f"[{cat}] {len(por_cat[cat])}")
        for m in por_cat[cat]:
            print(f"    {m}")

print()
if FALLOS:
    print("ESTADO: HAY FALLOS QUE CORREGIR")
    sys.exit(1)
print("ESTADO: SIN FALLOS")
sys.exit(0)
