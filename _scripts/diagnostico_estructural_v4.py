#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diagnostico_estructural_v4.py

Auditor READ-ONLY del sitio n2n.com.ar. No modifica ningun archivo del repo.
Complementa a diagnostico_sitio_v3.py (metadatos y SEO); no lo reemplaza.

Que audita v4 que v3 no audita:

  1. SINTAXIS HTML REAL  - parseo con html.parser: tags sin cerrar, cierres
                           sobrantes, anidamiento invalido, atributos
                           duplicados, entidades sospechosas.
  2. JSON-LD PROFUNDO    - parseo, campos obligatorios por @type y
                           referencias @id que no resuelven en el sitio.
  3. SEMANTICA / A11Y    - jerarquia de headings sin saltos, img sin alt,
                           links con texto generico, lang, landmarks,
                           botones sin nombre accesible.
  4. DEUDA TECNICA       - scripts sueltos en la raiz, archivos .bak/.orig,
                           paginas huerfanas, assets no referenciados,
                           estilos inline, TODO/FIXME, rutas absolutas
                           al filesystem local.
  5. VOLCADO DE CONTENIDO- genera un TXT con el contenido textual de cada
                           pagina (title, description, jerarquia de headings
                           y prosa) para revision semantica externa.

Salida:
  - Informe por consola con FALLO / AVISO / INFO.
  - Un archivo TXT en el HOME del usuario:
        ~/n2n_contenido_AAAAMMDD_HHMMSS.txt

Uso:
    python3 diagnostico_estructural_v4.py
    python3 diagnostico_estructural_v4.py --repo /ruta/al/repo
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

# --------------------------------------------------------------------------
# Configuracion
# --------------------------------------------------------------------------

REPO_DEFAULT = "/home/dflorida/GITHUB/n2n/n2n-site"
BASE_URL = "https://n2n.com.ar"

# Tags que no llevan cierre.
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# Tags que el parser puede cerrar implicitamente sin que sea un error.
AUTOCLOSE = {"li", "p", "td", "th", "tr", "option", "dd", "dt", "thead", "tbody"}

# Texto de link que no dice nada fuera de contexto.
LINKS_GENERICOS = {
    "aca", "acá", "aqui", "aquí", "click", "clic", "ver mas", "ver más",
    "leer mas", "leer más", "mas", "más", "link", "este link", "ir",
    "read more", "here", "more",
}

# Campos obligatorios minimos por tipo de schema.
SCHEMA_REQUERIDOS = {
    "Article": ["headline", "author", "datePublished"],
    "BlogPosting": ["headline", "author", "datePublished"],
    "Organization": ["name", "url"],
    "WebSite": ["name", "url"],
    "WebPage": ["name"],
    "CollectionPage": ["name", "url"],
    "BreadcrumbList": ["itemListElement"],
    "ItemList": ["itemListElement"],
    "FAQPage": ["mainEntity"],
    "Service": ["name"],
    "Person": ["name"],
}

EXT_ASSET = {".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg",
             ".ico", ".woff2", ".woff", ".pdf", ".gif", ".avif"}

DIRS_IGNORADOS = {".git", "node_modules", ".github", "__pycache__"}

# --------------------------------------------------------------------------
# Acumuladores
# --------------------------------------------------------------------------

FALLOS = defaultdict(list)
AVISOS = defaultdict(list)
INFOS = defaultdict(list)


def fallo(cat, msg):
    FALLOS[cat].append(msg)


def aviso(cat, msg):
    AVISOS[cat].append(msg)


def info(cat, msg):
    INFOS[cat].append(msg)


def titulo(t):
    print("=" * 74)
    print(t)
    print("=" * 74)


def linea():
    print("-" * 74)


# --------------------------------------------------------------------------
# Parser de sintaxis
# --------------------------------------------------------------------------

class AuditorHTML(HTMLParser):
    """Recorre el documento y registra estructura, errores y contenido."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pila = []              # tags abiertos
        self.errores = []           # errores de sintaxis
        self.headings = []          # (nivel, texto)
        self.imgs = []              # dicts de atributos
        self.links = []             # (href, texto)
        self.buttons = []           # (texto, aria-label)
        self.inline_styles = 0
        self.jsonld = []            # bloques crudos
        self.lang = None
        self.landmarks = Counter()
        self.texto = []             # prosa fuera de header/footer/script
        self._captura = 0           # profundidad de zona ignorada
        self._heading_actual = None
        self._buffer_heading = []
        self._link_actual = None
        self._buffer_link = []
        self._button_actual = None
        self._buffer_button = []
        self._en_jsonld = False
        self._buffer_jsonld = []

    # ---- utilidades

    def _pos(self):
        l, c = self.getpos()
        return "linea %d" % l

    def _ignorar(self, tag):
        return tag in ("script", "style", "header", "footer", "nav", "svg", "head")

    BLOQUE = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote",
              "td", "th", "tr", "div", "section", "figcaption", "dd", "dt"}

    # ---- eventos

    def handle_starttag(self, tag, attrs):
        # atributos duplicados
        nombres = [a[0] for a in attrs]
        dups = [n for n, c in Counter(nombres).items() if c > 1]
        for d in dups:
            self.errores.append("%s: atributo duplicado '%s' en <%s>"
                                % (self._pos(), d, tag))

        d_attrs = dict(attrs)

        if tag == "html":
            self.lang = d_attrs.get("lang")

        if "style" in d_attrs:
            self.inline_styles += 1

        if tag in ("main", "header", "footer", "nav", "aside"):
            self.landmarks[tag] += 1
        if d_attrs.get("role") in ("banner", "contentinfo", "main", "navigation"):
            self.landmarks["role:" + d_attrs["role"]] += 1

        if tag == "img":
            self.imgs.append(d_attrs)

        if tag == "script" and d_attrs.get("type") == "application/ld+json":
            self._en_jsonld = True
            self._buffer_jsonld = []

        if self._ignorar(tag):
            self._captura += 1

        if re.fullmatch(r"h[1-6]", tag):
            self._heading_actual = int(tag[1])
            self._buffer_heading = []

        if tag == "a":
            self._link_actual = d_attrs.get("href", "")
            self._buffer_link = []

        if tag == "button":
            self._button_actual = d_attrs.get("aria-label", "")
            self._buffer_button = []

        if tag not in VOID_TAGS:
            self.pila.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        # <br/> y similares: no abren nada
        nombres = [a[0] for a in attrs]
        dups = [n for n, c in Counter(nombres).items() if c > 1]
        for d in dups:
            self.errores.append("%s: atributo duplicado '%s' en <%s/>"
                                % (self._pos(), d, tag))
        if tag == "img":
            self.imgs.append(dict(attrs))

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            self.errores.append("%s: cierre </%s> sobre un tag vacio"
                                % (self._pos(), tag))
            return

        if self._en_jsonld and tag == "script":
            self._en_jsonld = False
            self.jsonld.append("".join(self._buffer_jsonld))

        if self._ignorar(tag) and self._captura > 0:
            self._captura -= 1

        if re.fullmatch(r"h[1-6]", tag) and self._heading_actual:
            txt = " ".join("".join(self._buffer_heading).split())
            self.headings.append((self._heading_actual, txt))
            self._heading_actual = None

        if tag == "a" and self._link_actual is not None:
            txt = " ".join("".join(self._buffer_link).split())
            self.links.append((self._link_actual, txt))
            self._link_actual = None

        if tag == "button" and self._button_actual is not None:
            txt = " ".join("".join(self._buffer_button).split())
            self.buttons.append((txt, self._button_actual))
            self._button_actual = None

        if tag in self.BLOQUE and self._captura == 0:
            self.texto.append("\x00")

        # verificacion de la pila
        if not self.pila:
            self.errores.append("%s: cierre </%s> sin apertura"
                                % (self._pos(), tag))
            return

        if self.pila[-1][0] == tag:
            self.pila.pop()
            return

        # buscar hacia atras
        idx = None
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i][0] == tag:
                idx = i
                break

        if idx is None:
            self.errores.append("%s: cierre </%s> sin apertura correspondiente"
                                % (self._pos(), tag))
            return

        colgados = [t for t, _ in self.pila[idx + 1:]]
        reales = [t for t in colgados if t not in AUTOCLOSE]
        if reales:
            self.errores.append(
                "%s: </%s> cierra dejando abierto: %s"
                % (self._pos(), tag, ", ".join(reales)))
        self.pila = self.pila[:idx]

    def handle_data(self, data):
        if self._en_jsonld:
            self._buffer_jsonld.append(data)
            return
        if self._heading_actual:
            self._buffer_heading.append(data)
        if self._link_actual is not None:
            self._buffer_link.append(data)
        if self._button_actual is not None:
            self._buffer_button.append(data)
        if self._captura == 0:
            s = data.strip()
            if s:
                self.texto.append(s)

    def finalizar(self):
        for tag, ln in self.pila:
            if tag in AUTOCLOSE or tag == "html":
                continue
            self.errores.append("<%s> abierto en linea %d y nunca cerrado"
                                % (tag, ln))


# --------------------------------------------------------------------------
# Utilidades de archivos
# --------------------------------------------------------------------------

def paginas_html(repo: Path):
    out = []
    for p in sorted(repo.rglob("*.html")):
        if any(part in DIRS_IGNORADOS for part in p.parts):
            continue
        out.append(p)
    return out


def url_de(repo: Path, p: Path) -> str:
    rel = p.relative_to(repo).as_posix()
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return "/" + rel if not rel.startswith("/") else rel


def leer(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def meta_de(html, nombre=None, prop=None):
    if nombre:
        m = re.search(r'<meta\s+name="%s"\s+content="(.*?)"\s*/?>' % nombre,
                      html, re.DOTALL | re.IGNORECASE)
    else:
        m = re.search(r'<meta\s+property="%s"\s+content="(.*?)"\s*/?>' % prop,
                      html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else None


def title_de(html):
    m = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    return " ".join(m.group(1).split()) if m else None


# --------------------------------------------------------------------------
# 1. SINTAXIS
# --------------------------------------------------------------------------

def seccion_sintaxis(repo, docs):
    titulo("1. SINTAXIS HTML (parseo real)")
    total_err = 0
    for p, d in docs.items():
        a = d["parser"]
        if a.errores:
            total_err += len(a.errores)
            print("  %s" % url_de(repo, p))
            for e in a.errores:
                print("      %s" % e)
                fallo("sintaxis", "%s — %s" % (url_de(repo, p), e))

        html = d["html"]
        if not html.lstrip().lower().startswith("<!doctype html>"):
            aviso("sintaxis", "%s — falta o difiere el DOCTYPE" % url_de(repo, p))
        # entidades sospechosas: & suelto que no abre entidad
        sueltos = len(re.findall(r"&(?!#?\w{1,8};)", html))
        if sueltos:
            aviso("sintaxis", "%s — %d '&' sin escapar"
                  % (url_de(repo, p), sueltos))

    if total_err == 0:
        print("  OK    ningun error de estructura en %d paginas" % len(docs))
    linea()


# --------------------------------------------------------------------------
# 2. JSON-LD
# --------------------------------------------------------------------------

def _nodos(obj):
    """Devuelve todos los dicts con @type dentro de un JSON-LD."""
    out = []
    if isinstance(obj, dict):
        if "@graph" in obj:
            for n in obj["@graph"]:
                out.extend(_nodos(n))
        if "@type" in obj:
            out.append(obj)
        for v in obj.values():
            if isinstance(v, (dict, list)):
                out.extend(_nodos(v))
    elif isinstance(obj, list):
        for n in obj:
            out.extend(_nodos(n))
    # deduplicar por identidad
    vistos, unicos = set(), []
    for n in out:
        if id(n) not in vistos:
            vistos.add(id(n))
            unicos.append(n)
    return unicos


def _refs_id(obj, out):
    """Recolecta dicts que son solo referencia: {'@id': ...} sin @type."""
    if isinstance(obj, dict):
        if "@id" in obj and "@type" not in obj and len(obj) == 1:
            out.append(obj["@id"])
        for v in obj.values():
            if isinstance(v, (dict, list)):
                _refs_id(v, out)
    elif isinstance(obj, list):
        for n in obj:
            _refs_id(n, out)
    return out


def seccion_jsonld(repo, docs):
    titulo("2. JSON-LD (parseo y campos obligatorios)")
    ids_definidos = set()
    ids_referenciados = defaultdict(list)
    tipos = Counter()
    paginas_sin = []

    for p, d in docs.items():
        u = url_de(repo, p)
        bloques = d["parser"].jsonld
        if not bloques:
            paginas_sin.append(u)
            continue
        for b in bloques:
            try:
                data = json.loads(b)
            except Exception as e:
                fallo("jsonld", "%s — JSON invalido: %s" % (u, e))
                continue
            for r in _refs_id(data, []):
                ids_referenciados[r].append(u)
            for n in _nodos(data):
                t = n.get("@type")
                if isinstance(t, list):
                    t = t[0] if t else None
                if t:
                    tipos[t] += 1
                if "@id" in n:
                    ids_definidos.add(n["@id"])
                req = SCHEMA_REQUERIDOS.get(t, [])
                for campo in req:
                    if campo not in n:
                        aviso("jsonld", "%s — %s sin campo '%s'" % (u, t, campo))

    for ref, donde in sorted(ids_referenciados.items()):
        if ref not in ids_definidos:
            fallo("jsonld", "@id referenciado y nunca definido: %s (en %s)"
                  % (ref, ", ".join(sorted(set(donde))[:3])))

    print("  Tipos encontrados:")
    for t, c in tipos.most_common():
        print("      %-20s %d" % (t, c))
    print("  @id definidos: %d | referenciados: %d"
          % (len(ids_definidos), len(ids_referenciados)))
    if paginas_sin:
        print("  Paginas sin JSON-LD: %d" % len(paginas_sin))
        for u in paginas_sin[:10]:
            aviso("jsonld", "%s — sin JSON-LD" % u)
    linea()


# --------------------------------------------------------------------------
# 3. SEMANTICA Y ACCESIBILIDAD
# --------------------------------------------------------------------------

def seccion_semantica(repo, docs):
    titulo("3. SEMANTICA Y ACCESIBILIDAD")
    for p, d in docs.items():
        u = url_de(repo, p)
        a = d["parser"]

        if a.lang != "es":
            aviso("a11y", "%s — lang='%s' (esperado 'es')" % (u, a.lang))

        h1s = [t for n, t in a.headings if n == 1]
        if len(h1s) != 1:
            fallo("semantica", "%s — %d h1" % (u, len(h1s)))

        # saltos de jerarquia
        anterior = None
        for nivel, txt in a.headings:
            if anterior is not None and nivel > anterior + 1:
                aviso("semantica",
                      "%s — salto h%d -> h%d en '%s'"
                      % (u, anterior, nivel, txt[:45]))
            anterior = nivel

        # headings vacios
        for nivel, txt in a.headings:
            if not txt:
                fallo("semantica", "%s — h%d vacio" % (u, nivel))

        # imagenes
        for img in a.imgs:
            if "alt" not in img:
                fallo("a11y", "%s — <img> sin atributo alt (src=%s)"
                      % (u, img.get("src", "?")))
            dimensionada = ("width" in img and "height" in img)
            por_css = "style" in img or "logo" in img.get("class", "")
            if not dimensionada and not por_css:
                aviso("a11y", "%s — <img> sin width/height (src=%s)"
                      % (u, img.get("src", "?")))

        # links
        for href, txt in a.links:
            plano = txt.lower().strip(" →›».")
            if not txt and "aria-label" not in str(href):
                pass
            if plano in LINKS_GENERICOS:
                aviso("a11y", "%s — link con texto generico: '%s'" % (u, txt))
            if href.startswith("http") and BASE_URL not in href:
                pass

        # botones sin nombre
        for txt, aria in a.buttons:
            if not txt and not aria:
                fallo("a11y", "%s — <button> sin texto ni aria-label" % u)

        # landmarks
        if a.landmarks.get("main", 0) != 1:
            fallo("semantica", "%s — %d <main>" % (u, a.landmarks.get("main", 0)))

        if a.inline_styles > 12:
            aviso("mantenibilidad", "%s — %d elementos con style inline"
                  % (u, a.inline_styles))

    print("  Revisadas %d paginas" % len(docs))
    linea()


# --------------------------------------------------------------------------
# 4. DEUDA TECNICA
# --------------------------------------------------------------------------

def seccion_deuda(repo, docs):
    titulo("4. DEUDA TECNICA")

    # 4.1 scripts sueltos en la raiz
    scripts = sorted(p.name for p in repo.glob("*.py"))
    if scripts:
        print("  Scripts .py en la raiz del repo: %d" % len(scripts))
        for s in scripts:
            print("      %s" % s)
        aviso("deuda", "%d scripts .py viven en la raiz del repo "
                       "(conviene moverlos a scripts/)" % len(scripts))
    else:
        print("  OK    sin scripts .py sueltos en la raiz")

    # 4.2 residuos
    residuos = []
    for patron in ("*.bak", "*.orig", "*.rej", "*.tmp", "*~", "*.swp"):
        for p in repo.rglob(patron):
            if any(part in DIRS_IGNORADOS for part in p.parts):
                continue
            residuos.append(p.relative_to(repo).as_posix())
    if residuos:
        for r in residuos:
            fallo("deuda", "residuo sin borrar: %s" % r)
    else:
        print("  OK    sin archivos .bak / .orig / .tmp")

    # 4.3 marcadores
    MARCAS = [
        (r"\bTODO\b", "TODO"),
        (r"\bFIXME\b", "FIXME"),
        (r"\bXXX\b", "XXX"),
        (r"\bHACK\b", "HACK"),
        (r"(?i)lorem ipsum", "lorem ipsum"),
        (r"(?i)placeholder", "placeholder"),
    ]
    for p, d in docs.items():
        for patron, etiqueta in MARCAS:
            if re.search(patron, d["html"]):
                aviso("deuda", "%s — contiene '%s'" % (url_de(repo, p), etiqueta))

    # 4.4 rutas locales filtradas
    for p, d in docs.items():
        for m in re.findall(r"/home/\w+[\w/.\-]*", d["html"]):
            fallo("deuda", "%s — ruta local del filesystem en el HTML: %s"
                  % (url_de(repo, p), m))

    # 4.5 paginas huerfanas
    enlazadas = set()
    for p, d in docs.items():
        for href, _ in d["parser"].links:
            if href.startswith("/"):
                enlazadas.add(href.split("#")[0].split("?")[0])
        # links del header/footer no los captura el parser: barrer el crudo
        for href in re.findall(r'href="(/[^"#?]*)"', d["html"]):
            enlazadas.add(href)

    huerfanas = []
    for p in docs:
        u = url_de(repo, p)
        if u == "/":
            continue
        if u not in enlazadas and u.rstrip("/") not in enlazadas:
            huerfanas.append(u)
    if huerfanas:
        for u in huerfanas:
            aviso("deuda", "pagina sin ningun enlace entrante: %s" % u)
    else:
        print("  OK    ninguna pagina huerfana")

    # 4.6 assets no referenciados
    todo_html = "\n".join(d["html"] for d in docs.values())
    assets = []
    for p in repo.rglob("*"):
        if p.is_dir() or any(part in DIRS_IGNORADOS for part in p.parts):
            continue
        if p.suffix.lower() in EXT_ASSET:
            assets.append(p)
    sin_uso = []
    for a in assets:
        if a.name not in todo_html:
            sin_uso.append(a.relative_to(repo).as_posix())
    if sin_uso:
        print("  Assets sin referencia en ningun HTML: %d" % len(sin_uso))
        for s in sorted(sin_uso)[:25]:
            print("      %s" % s)
        aviso("deuda", "%d assets sin referencia" % len(sin_uso))
    else:
        print("  OK    todos los assets estan referenciados")

    linea()


# --------------------------------------------------------------------------
# 5. VOLCADO DE CONTENIDO
# --------------------------------------------------------------------------

def volcado(repo, docs, destino: Path):
    lineas = []
    add = lineas.append

    add("VOLCADO DE CONTENIDO — n2n.com.ar")
    add("Generado: %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    add("Repo: %s" % repo)
    add("Paginas: %d" % len(docs))
    add("")
    add("Proposito: revision semantica externa. Contiene, por pagina, la URL,")
    add("el title, la meta description, la jerarquia de headings y la prosa")
    add("del contenido principal. Header, nav, footer y scripts quedan fuera.")
    add("")

    add("=" * 74)
    add("INDICE DE TITLES")
    add("=" * 74)
    for p in sorted(docs, key=lambda x: url_de(repo, x)):
        d = docs[p]
        t = d["title"] or "(SIN TITLE)"
        add("%-42s %3d  %s" % (url_de(repo, p), len(t), t))
    add("")

    add("=" * 74)
    add("INDICE DE H1")
    add("=" * 74)
    for p in sorted(docs, key=lambda x: url_de(repo, x)):
        h1 = [t for n, t in docs[p]["parser"].headings if n == 1]
        add("%-42s %s" % (url_de(repo, p), h1[0] if h1 else "(SIN H1)"))
    add("")

    for p in sorted(docs, key=lambda x: url_de(repo, x)):
        d = docs[p]
        a = d["parser"]
        u = url_de(repo, p)
        add("=" * 74)
        add("URL         %s" % u)
        add("ARCHIVO     %s" % p.relative_to(repo).as_posix())
        add("=" * 74)
        t = d["title"]
        add("TITLE       (%d) %s" % (len(t) if t else 0, t))
        desc = d["desc"]
        add("DESCRIPTION (%d) %s" % (len(desc) if desc else 0, desc))
        og = meta_de(d["html"], prop="og:title")
        tw = meta_de(d["html"], nombre="twitter:title")
        sync_t = "sincronizados" if (og == t and tw == t) else "DESINCRONIZADOS"
        ogd = meta_de(d["html"], prop="og:description")
        twd = meta_de(d["html"], nombre="twitter:description")
        sync_d = "sincronizadas" if (ogd == desc and twd == desc) else "DESINCRONIZADAS"
        add("TITLES      %s" % sync_t)
        add("DESCRIPTIONS %s" % sync_d)
        add("")
        add("--- ESTRUCTURA DE HEADINGS ---")
        for nivel, txt in a.headings:
            add("%sh%d  %s" % ("   " * (nivel - 1), nivel, txt))
        add("")
        add("--- CONTENIDO ---")
        crudo = []
        actual = []
        for t in a.texto:
            if t == "\x00":
                if actual:
                    crudo.append(" ".join(actual))
                    actual = []
            else:
                actual.append(t)
        if actual:
            crudo.append(" ".join(actual))
        vistos = set()
        for parrafo in crudo:
            parrafo = re.sub(r"\s+", " ", parrafo).strip()
            if len(parrafo) < 2:
                continue
            if parrafo in vistos:
                continue
            vistos.add(parrafo)
            add(parrafo)
        add("")

    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino


# --------------------------------------------------------------------------
# Resumen
# --------------------------------------------------------------------------

def resumen(n_paginas, archivo):
    titulo("RESUMEN")
    nf = sum(len(v) for v in FALLOS.values())
    na = sum(len(v) for v in AVISOS.values())
    ni = sum(len(v) for v in INFOS.values())
    print("Paginas analizadas: %d" % n_paginas)
    print("FALLOS:  %d" % nf)
    print("AVISOS:  %d" % na)
    print("INFO:    %d" % ni)

    for etiqueta, dic in (("FALLOS", FALLOS), ("AVISOS", AVISOS), ("INFO", INFOS)):
        if not any(dic.values()):
            continue
        print("")
        print("--- %s ---" % etiqueta)
        for cat in sorted(dic):
            items = dic[cat]
            if not items:
                continue
            print("[%s] %d" % (cat, len(items)))
            for m in items[:15]:
                print("    %s" % m)
            if len(items) > 15:
                print("    ... y %d mas" % (len(items) - 15))

    print("")
    print("Volcado de contenido: %s" % archivo)
    print("")
    if nf == 0:
        print("ESTADO: SIN FALLOS ESTRUCTURALES")
    else:
        print("ESTADO: %d FALLOS — revisar antes de commitear" % nf)
    return nf


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=REPO_DEFAULT)
    ap.add_argument("--salida", default=None,
                    help="ruta del TXT (por defecto ~/n2n_contenido_FECHA.txt)")
    args = ap.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir():
        print("ABORTADO: no existe el repo %s" % repo)
        sys.exit(1)

    paginas = paginas_html(repo)
    if not paginas:
        print("ABORTADO: no se encontraron .html en %s" % repo)
        sys.exit(1)

    titulo("DIAGNOSTICO ESTRUCTURAL v4 — READ ONLY")
    print("Repo: %s" % repo)
    print("Paginas HTML: %d" % len(paginas))
    print("Este script no modifica ningun archivo del repositorio.")
    linea()

    docs = {}
    for p in paginas:
        html = leer(p)
        parser = AuditorHTML()
        try:
            parser.feed(html)
            parser.close()
        except Exception as e:
            fallo("sintaxis", "%s — el parser aborto: %s" % (url_de(repo, p), e))
        parser.finalizar()
        docs[p] = {
            "html": html,
            "parser": parser,
            "title": title_de(html),
            "desc": meta_de(html, nombre="description"),
        }

    seccion_sintaxis(repo, docs)
    seccion_jsonld(repo, docs)
    seccion_semantica(repo, docs)
    seccion_deuda(repo, docs)

    if args.salida:
        destino = Path(args.salida).expanduser()
    else:
        sello = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = Path.home() / ("n2n_contenido_%s.txt" % sello)
    archivo = volcado(repo, docs, destino)

    nf = resumen(len(paginas), archivo)
    sys.exit(0 if nf == 0 else 2)


if __name__ == "__main__":
    main()
