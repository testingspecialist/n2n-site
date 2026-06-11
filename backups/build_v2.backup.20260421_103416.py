#!/usr/bin/env python3
"""
N2N — build.py
Corre en: ~/n2n-local/
Output:   ~/n2n-local/public/
Assets:   ~/n2n-local/assets/{css,fonts,img,js}  →  public/{css,fonts,img,js}
CSS y JS se sobreescriben siempre desde este script.
Servir:   cd ~/n2n-local/public && python3 -m http.server 8080
"""

import os, re, shutil, glob

BASE    = os.path.expanduser('~/n2n-local')
ASSETS  = os.path.join(BASE, 'assets')
OUT     = os.path.join(BASE, 'public')
CONTENT = '/home/dflorida/proyectos/n2n-web/n2n-web/content/es'

UMAMI_ID  = '05b64f33-b9ae-4ffa-b068-8a2dacff6e33'
UMAMI_SRC = 'https://umami.n2n.com.ar/script.js'

# ─────────────────────────────────────────────────────────────────
# CSS — /fonts/Outfit-Variable.woff2 (sin /assets/)
# ─────────────────────────────────────────────────────────────────
CSS = r"""/* N2N — main.css */

@font-face {
  font-family: 'Outfit';
  src: url('/fonts/Outfit-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --orange:      #ff6600;
  --orange-dark: #cc5200;
  --navy:        #000055;
  --navy-light:  #00007a;
  --bg:          #f4f4f6;
  --bg-white:    #ffffff;
  --bg-section:  #ebebef;
  --text:        #1a1a2e;
  --text-muted:  #52526a;
  --border:      #d8d8e8;
  --font:        'Outfit', system-ui, sans-serif;
  --max-w:       1200px;
  --max-w-text:  780px;
  --radius:      6px;
  --s2:.5rem; --s3:.75rem; --s4:1rem; --s5:1.25rem; --s6:1.5rem;
  --s8:2rem; --s10:2.5rem; --s12:3rem; --s16:4rem; --s20:5rem; --s24:6rem;
  --shadow-sm: 0 1px 3px rgba(0,0,21,.07);
  --shadow:    0 4px 16px rgba(0,0,21,.1);
}

html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body { font-family: var(--font); font-size: 1rem; line-height: 1.65; color: var(--text); background: var(--bg); }
img { max-width: 100%; height: auto; display: block; }
a { color: var(--orange); text-decoration: none; }
a:hover { color: var(--orange-dark); }

.container { width: 100%; max-width: var(--max-w); margin: 0 auto; padding: 0 var(--s6); }

.skip-link { position: absolute; top: -100%; left: var(--s4); background: var(--orange); color: #fff; padding: var(--s2) var(--s4); z-index: 999; border-radius: 0 0 var(--radius) var(--radius); font-weight: 700; }
.skip-link:focus { top: 0; }

/* Header */
.site-header { position: sticky; top: 0; z-index: 100; background: var(--navy); border-bottom: 2px solid rgba(255,102,0,.3); }
.nav { display: flex; align-items: center; justify-content: space-between; height: 64px; gap: var(--s6); }
.nav__logo img { height: 36px; width: auto; }
.nav__links { display: flex; list-style: none; gap: var(--s2); align-items: center; }
.nav__links a { color: rgba(255,255,255,.82); font-size: .9rem; font-weight: 500; padding: var(--s2) var(--s3); border-radius: var(--radius); transition: color .18s, background .18s; }
.nav__links a:hover, .nav__links a[aria-current="page"] { color: var(--orange); background: rgba(255,102,0,.1); }
.nav__cta { background: var(--orange) !important; color: #fff !important; padding: var(--s2) var(--s4) !important; font-weight: 600 !important; }
.nav__cta:hover { background: var(--orange-dark) !important; }
.nav__toggle { display: none; background: none; border: none; color: #fff; cursor: pointer; padding: var(--s2); }

/* Hero */
.hero { background: var(--navy); color: #fff; padding: var(--s20) 0 var(--s16); position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse 60% 50% at 80% 50%, rgba(255,102,0,.12) 0%, transparent 70%), radial-gradient(ellipse 40% 60% at 10% 80%, rgba(0,0,40,.6) 0%, transparent 60%); pointer-events: none; }
.hero .container { position: relative; z-index: 1; }
.hero__label { display: inline-block; font-size: .78rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--orange); margin-bottom: var(--s5); }
.hero__h1 { font-size: clamp(2rem, 4.5vw, 3.4rem); font-weight: 800; line-height: 1.1; letter-spacing: -.02em; max-width: 820px; margin-bottom: var(--s6); }
.hero__lead { font-size: clamp(1rem, 1.8vw, 1.2rem); color: rgba(255,255,255,.75); max-width: 640px; margin-bottom: var(--s8); line-height: 1.6; }
.hero__actions { display: flex; gap: var(--s4); flex-wrap: wrap; align-items: center; }

/* Buttons */
.btn { display: inline-flex; align-items: center; gap: .4em; padding: .72em 1.5em; border-radius: var(--radius); font-family: var(--font); font-size: .95rem; font-weight: 600; cursor: pointer; transition: all .18s; white-space: nowrap; text-decoration: none; border: 2px solid transparent; }
.btn--primary { background: var(--orange); color: #fff; border-color: var(--orange); }
.btn--primary:hover { background: var(--orange-dark); border-color: var(--orange-dark); color: #fff; transform: translateY(-1px); box-shadow: 0 4px 14px rgba(255,102,0,.4); }
.btn--outline-white { background: transparent; color: #fff; border-color: rgba(255,255,255,.45); }
.btn--outline-white:hover { border-color: #fff; background: rgba(255,255,255,.08); color: #fff; }
.btn--navy { background: var(--navy); color: #fff; border-color: var(--navy); }
.btn--navy:hover { background: var(--navy-light); border-color: var(--navy-light); color: #fff; }
.btn--ghost { background: transparent; color: var(--orange); border-color: var(--orange); }
.btn--ghost:hover { background: var(--orange); color: #fff; }

/* Sections */
.section { padding: var(--s16) 0; }
.section--sm { padding: var(--s12) 0; }
.bg-white   { background: var(--bg-white); }
.bg-section { background: var(--bg-section); }
.bg-navy    { background: var(--navy); color: #fff; }

/* Section header */
.section-header { text-align: center; margin-bottom: var(--s10); }
.section-header__label { display: inline-block; font-size: .75rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--orange); margin-bottom: var(--s3); }
.section-header h2 { font-size: clamp(1.6rem, 3vw, 2.4rem); font-weight: 800; letter-spacing: -.02em; line-height: 1.15; color: var(--navy); }
.bg-navy .section-header h2 { color: #fff; }
.section-header p { margin-top: var(--s4); color: var(--text-muted); font-size: 1.05rem; max-width: 580px; margin-left: auto; margin-right: auto; }

/* Grid */
.grid { display: grid; gap: var(--s6); }
.grid--2    { grid-template-columns: repeat(2, 1fr); }
.grid--3    { grid-template-columns: repeat(3, 1fr); }
.grid--4    { grid-template-columns: repeat(4, 1fr); }
.grid--auto { grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }

/* Cards */
.card { background: var(--bg-white); border: 1px solid var(--border); border-radius: calc(var(--radius)*1.5); padding: var(--s8); box-shadow: var(--shadow-sm); transition: box-shadow .2s, transform .2s, border-color .2s; }
.card:hover { box-shadow: var(--shadow); transform: translateY(-3px); border-color: rgba(255,102,0,.25); }
.card--link { display: block; color: inherit; text-decoration: none; }
.card__tag { font-size: .72rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--orange); margin-bottom: var(--s3); }
.card__title { font-size: 1.12rem; font-weight: 700; color: var(--navy); line-height: 1.25; margin-bottom: var(--s3); }
.card__body { font-size: .93rem; color: var(--text-muted); line-height: 1.6; margin-bottom: var(--s4); }
.card__link { font-size: .87rem; font-weight: 600; color: var(--orange); }

/* Pillar */
.pillar { display: flex; gap: var(--s5); align-items: flex-start; }
.pillar__num { flex-shrink: 0; width: 44px; height: 44px; background: var(--navy); color: var(--orange); border-radius: var(--radius); display: flex; align-items: center; justify-content: center; font-size: .82rem; font-weight: 800; }
.pillar__body h3 { font-size: 1.05rem; font-weight: 700; color: var(--navy); margin-bottom: var(--s2); }
.pillar__body p { font-size: .93rem; color: var(--text-muted); line-height: 1.6; }

/* Stats */
.stats { display: flex; gap: var(--s8); flex-wrap: wrap; padding-top: var(--s8); }
.stat__num { font-size: clamp(2rem, 4vw, 3rem); font-weight: 900; color: var(--orange); line-height: 1; letter-spacing: -.03em; }
.stat__label { font-size: .85rem; color: rgba(255,255,255,.65); margin-top: var(--s2); line-height: 1.3; }

/* Not-for */
.not-for { background: var(--bg-section); border-left: 3px solid var(--orange); border-radius: 0 var(--radius) var(--radius) 0; padding: var(--s6) var(--s8); }
.not-for__title { font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: var(--orange); margin-bottom: var(--s4); }
.not-for ul { list-style: none; padding: 0; display: flex; flex-direction: column; gap: var(--s2); }
.not-for li { font-size: .95rem; color: var(--text-muted); padding-left: var(--s5); position: relative; }
.not-for li::before { content: '\00d7'; position: absolute; left: 0; color: var(--orange); font-weight: 700; }

/* Table */
.table-wrap { overflow-x: auto; margin: var(--s6) 0; border-radius: var(--radius); border: 1px solid var(--border); }
table { width: 100%; border-collapse: collapse; font-size: .9rem; background: var(--bg-white); }
th { background: var(--navy); color: #fff; font-weight: 700; text-align: left; padding: .75rem 1rem; font-size: .82rem; letter-spacing: .04em; text-transform: uppercase; }
td { padding: .65rem 1rem; border-bottom: 1px solid var(--border); vertical-align: top; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--bg); }

/* Prose */
.prose { max-width: var(--max-w-text); }
.prose h2 { font-size: clamp(1.3rem, 2.2vw, 1.7rem); font-weight: 800; color: var(--navy); letter-spacing: -.02em; margin: var(--s10) 0 var(--s4); padding-top: var(--s8); border-top: 1px solid var(--border); }
.prose h2:first-child { margin-top: 0; padding-top: 0; border-top: none; }
.prose h3 { font-size: 1.15rem; font-weight: 700; color: var(--navy); margin: var(--s6) 0 var(--s3); }
.prose h4 { font-size: 1rem; font-weight: 700; margin: var(--s4) 0 var(--s2); }
.prose p { margin-bottom: var(--s4); font-size: 1.02rem; line-height: 1.72; }
.prose ul, .prose ol { padding-left: var(--s6); margin-bottom: var(--s4); }
.prose li { margin-bottom: var(--s2); font-size: 1.02rem; line-height: 1.65; }
.prose strong { color: var(--navy); font-weight: 700; }
.prose hr { border: none; border-top: 1px solid var(--border); margin: var(--s8) 0; }

/* Breadcrumb */
.breadcrumb { font-size: .82rem; color: rgba(255,255,255,.5); margin-bottom: var(--s4); }
.breadcrumb a { color: rgba(255,255,255,.6); }
.breadcrumb a:hover { color: var(--orange); }
.breadcrumb span { margin: 0 .4em; }

/* Case badge */
.case-badge { display: inline-block; background: rgba(255,102,0,.15); color: var(--orange); border: 1px solid rgba(255,102,0,.3); border-radius: 100px; padding: .2em .9em; font-size: .75rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; margin-bottom: var(--s4); }

/* Contact form */
.form-grid { display: grid; gap: var(--s4); }
.form-group { display: flex; flex-direction: column; gap: var(--s2); }
.form-group label { font-size: .85rem; font-weight: 600; color: var(--navy); }
.form-group input, .form-group select, .form-group textarea { font-family: var(--font); font-size: .96rem; padding: .7em 1em; border: 1.5px solid var(--border); border-radius: var(--radius); background: var(--bg-white); color: var(--text); transition: border-color .18s, box-shadow .18s; outline: none; width: 100%; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: var(--navy); box-shadow: 0 0 0 3px rgba(0,0,85,.1); }
.form-group textarea { resize: vertical; min-height: 130px; }
.form-row { grid-column: 1 / -1; }

/* Footer */
.site-footer { background: var(--navy); color: rgba(255,255,255,.7); padding: var(--s16) 0 var(--s8); border-top: 2px solid rgba(255,102,0,.25); }
.footer__grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: var(--s10); padding-bottom: var(--s10); border-bottom: 1px solid rgba(255,255,255,.1); }
.footer__logo img { height: 34px; width: auto; margin-bottom: var(--s4); }
.footer__about { font-size: .9rem; line-height: 1.65; color: rgba(255,255,255,.55); max-width: 340px; }
.footer__col-title { font-size: .75rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--orange); margin-bottom: var(--s4); }
.footer__col ul { list-style: none; display: flex; flex-direction: column; gap: var(--s2); }
.footer__col a { color: rgba(255,255,255,.65); font-size: .9rem; transition: color .18s; }
.footer__col a:hover { color: var(--orange); }
.footer__bottom { display: flex; justify-content: space-between; align-items: center; padding-top: var(--s6); font-size: .83rem; color: rgba(255,255,255,.35); flex-wrap: wrap; gap: var(--s4); }
.footer__bottom-links { display: flex; gap: var(--s4); }
.footer__bottom-links a { color: rgba(255,255,255,.45); font-size: .83rem; }
.footer__bottom-links a:hover { color: var(--orange); }


/* Tech strip */
.tech-strip { background: var(--navy); padding: var(--s10) 0; border-top: 1px solid rgba(255,102,0,.2); border-bottom: 1px solid rgba(255,102,0,.2); }
.tech-strip__label { text-align: center; font-size: .75rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: rgba(255,255,255,.35); margin-bottom: var(--s8); }
.tech-strip__grid { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: var(--s8); }
.tech-strip__item { display: flex; flex-direction: column; align-items: center; gap: var(--s2); opacity: .55; transition: opacity .2s; }
.tech-strip__item:hover { opacity: 1; }
.tech-strip__item img { width: 40px; height: 40px; object-fit: contain; filter: brightness(0) invert(1); }
.tech-strip__item span { font-size: .7rem; color: rgba(255,255,255,.4); letter-spacing: .06em; text-transform: uppercase; font-weight: 600; }
@media (max-width: 640px) { .tech-strip__grid { gap: var(--s6); } .tech-strip__item img { width: 32px; height: 32px; } }

/* Responsive */
@media (max-width: 900px) {
  .grid--3, .grid--4 { grid-template-columns: repeat(2, 1fr); }
  .footer__grid { grid-template-columns: 1fr 1fr; }
  .footer__brand { grid-column: 1 / -1; }
}
@media (max-width: 640px) {
  :root { --s16: 3rem; --s20: 3.5rem; }
  .grid--2, .grid--3, .grid--4, .grid--auto { grid-template-columns: 1fr; }
  .nav__links { display: none; flex-direction: column; position: absolute; top: 64px; left: 0; right: 0; background: var(--navy); padding: var(--s4) var(--s6); gap: var(--s2); border-bottom: 2px solid rgba(255,102,0,.3); }
  .nav__links.is-open { display: flex; }
  .nav { position: relative; }
  .nav__toggle { display: block; }
  .footer__grid { grid-template-columns: 1fr; }
  .footer__bottom { flex-direction: column; text-align: center; }
  .hero__actions { flex-direction: column; align-items: flex-start; }
  .container { padding: 0 var(--s4); }
}
"""

# ─────────────────────────────────────────────────────────────────
# JS
# ─────────────────────────────────────────────────────────────────
JS = r"""(function(){
  var toggle = document.getElementById('nav-toggle');
  var links  = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function(){
      var open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function(e){
      if (!toggle.contains(e.target) && !links.contains(e.target)) {
        links.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var btn = form.querySelector('[type=submit]');
      var msg = document.getElementById('form-msg');
      btn.disabled = true; btn.textContent = 'Enviando\u2026';
      var data = {};
      new FormData(form).forEach(function(v,k){ data[k]=v; });
      data['access_key'] = '805e9884-4601-4a15-b3b7-58d507fae8e3';
      data['subject'] = 'Nueva consulta N2N — ' + (data['sector'] || 'sin sector');
      data['from_name'] = 'N2N Contacto';
      fetch('https://api.web3forms.com/submit', {
        method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)
      }).then(function(r){ return r.json(); }).then(function(r){
        if(!r.success) throw new Error();
        if(msg){ msg.textContent='Mensaje enviado. Te contactamos en 24\u201348h h\u00e1biles.'; msg.style.color='#2d8a4e'; }
        form.reset();
      }).catch(function(){
        if(msg){ msg.textContent='Error al enviar. Escrib\u00ednos a contacto@n2n.com.ar'; msg.style.color='#c0392b'; }
      }).finally(function(){
        btn.disabled=false; btn.textContent='Enviar consulta';
      });
    });
  }
})();
"""

# ─────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────
def read_md(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n?(.*)', raw, re.DOTALL)
    if not m:
        return {}, ''
    meta = {}
    for line in m.group(1).splitlines():
        km = re.match(r'^(\w+):\s*"?([^"#\n]+?)"?\s*$', line)
        if km:
            meta[km.group(1)] = km.group(2).strip().strip('"')
    return meta, m.group(2).strip()

def md_to_html(text):
    text = re.sub(r'\{\{<.*?>\}\}', '', text, flags=re.DOTALL)
    def convert_table(m):
        lines = [l for l in m.group(0).strip().splitlines() if l.strip()]
        rows = []
        for i, line in enumerate(lines):
            if re.match(r'^[\s|:-]+$', line):
                continue
            cells = [c.strip() for c in re.split(r'\|', line.strip('|'))]
            tag = 'th' if i == 0 else 'td'
            rows.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
        return '<div class="table-wrap"><table>' + ''.join(rows) + '</table></div>\n'
    text = re.sub(r'(\|.+\n)+', convert_table, text)
    text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$',  r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$',   r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$',    r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^---+$', '<hr>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>', text)
    def convert_list(m):
        items = re.findall(r'^- (.+)$', m.group(0), re.MULTILINE)
        return '<ul>\n' + '\n'.join(f'<li>{i}</li>' for i in items) + '\n</ul>\n'
    text = re.sub(r'(^- .+\n?)+', convert_list, text, flags=re.MULTILINE)
    out = []
    for b in re.split(r'\n{2,}', text.strip()):
        b = b.strip()
        if not b:
            continue
        if re.match(r'^<(h[1-4]|ul|ol|div|hr|table)', b):
            out.append(b)
        else:
            out.append(f'<p>{b}</p>')
    return '\n'.join(out)

def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(html)
    print(f'  \u2713 {path.replace(OUT,"")}')

def nav_html(current=''):
    items = [
        ('/framework/como-funciona/', 'Framework'),
        ('/industrias/',  'Industrias'),
        ('/servicios/',   'Servicios'),
        ('/casos/',       'Casos'),
        ('/conocimiento/','Conocimiento'),
        ('/contacto/',    'Contacto'),
    ]
    li = ''
    for href, name in items:
        sec    = href.strip('/').split('/')[0]
        active = ' aria-current="page"' if current == sec else ''
        cta    = ' class="nav__cta"' if name == 'Contacto' else ''
        li += f'<li><a href="{href}"{active}{cta}>{name}</a></li>\n        '
    return f'''<header class="site-header" role="banner">
  <a class="skip-link" href="#main-content">Saltar al contenido</a>
  <div class="container">
    <nav class="nav" aria-label="Navegaci\u00f3n principal">
      <a href="/" class="nav__logo" aria-label="N2N \u2014 Inicio">
        <img src="/img/logo.png" alt="N2N" width="140" height="38" loading="eager" fetchpriority="high">
      </a>
      <button class="nav__toggle" id="nav-toggle" aria-controls="nav-links" aria-expanded="false" aria-label="Abrir men\u00fa" type="button">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
      <ul class="nav__links" id="nav-links" role="list">
        {li}
      </ul>
    </nav>
  </div>
</header>'''

FOOTER = '''<footer class="site-footer" role="contentinfo">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <a href="/" class="footer__logo"><img src="/img/logo-white.png" alt="N2N" width="120" height="32" loading="lazy"></a>
        <p class="footer__about">N2N dise\u00f1a sistemas digitales que filtran ruido comercial y habilitan conversaciones B2B reales para operaciones industriales que venden por volumen.</p>
      </div>
      <div class="footer__col">
        <p class="footer__col-title">Navegaci\u00f3n</p>
        <ul role="list">
          <li><a href="/framework/como-funciona/">Framework</a></li>
          <li><a href="/industrias/">Industrias</a></li>
          <li><a href="/servicios/">Servicios</a></li>
          <li><a href="/casos/">Casos</a></li>
          <li><a href="/conocimiento/">Conocimiento</a></li>
          <li><a href="/contacto/">Contacto</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <p class="footer__col-title">Contacto</p>
        <ul role="list">
          <li><a href="mailto:contacto@n2n.com.ar">contacto@n2n.com.ar</a></li>
          <li><a href="https://wa.me/5491138230614" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="https://linkedin.com/company/n2n" target="_blank" rel="noopener">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <p>Designed by &lt;/N2N&gt; &mdash; &copy; 2026</p>
      <div class="footer__bottom-links">
        <a href="/legal/">Privacidad</a>
        <a href="/legal/#cookies">Cookies</a>
      </div>
    </div>
  </div>
</footer>'''

def page(title, desc, body, current='', noindex=False):
    robots = '\n<meta name="robots" content="noindex">' if noindex else ''
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{robots}
<title>{title} | N2N</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/img/favicon.ico" sizes="any">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/Outfit-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/css/main.css" as="style">
<link rel="stylesheet" href="/css/main.css">
</head>
<body>
{nav_html(current)}
<main id="main-content">
{body}
</main>
{FOOTER}
<script src="/js/main.js" defer></script>
<script defer src="{UMAMI_SRC}" data-website-id="{UMAMI_ID}"></script>
</body>
</html>'''

def inner_page(label, breadcrumb, title, desc, body_html, current='', extra_actions=''):
    acts = f'<a href="/contacto/" class="btn btn--primary">Evaluar mi operaci\u00f3n \u2192</a>{extra_actions}'
    body = f'''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    {breadcrumb}
    <p class="hero__label">{label}</p>
    <h1 class="hero__h1" id="page-h1">{title}</h1>
    <p class="hero__lead">{desc}</p>
    <div class="hero__actions">{acts}</div>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="prose">{body_html}</div>
    <div style="margin-top:var(--s10);padding-top:var(--s8);border-top:1px solid var(--border);display:flex;gap:var(--s4);flex-wrap:wrap">
      <a href="/contacto/" class="btn btn--primary">Evaluar mi operaci\u00f3n \u2192</a>
    </div>
  </div>
</section>'''
    return page(title, desc, body, current)

# ─────────────────────────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────────────────────────
print('\u2192 Limpiando public/')
# Preservar .git antes de limpiar
_git_tmp = os.path.expanduser('~/n2n-local/.git_tmp')
_git_src = os.path.join(OUT, '.git')
if os.path.exists(_git_src):
    shutil.copytree(_git_src, _git_tmp, dirs_exist_ok=True)
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
# Restaurar .git
if os.path.exists(_git_tmp):
    shutil.copytree(_git_tmp, _git_src, dirs_exist_ok=True)
    shutil.rmtree(_git_tmp)
    print('  \u2713 .git preservado')

for d in ('css', 'fonts', 'img', 'js'):
    src = os.path.join(ASSETS, d)
    dst = os.path.join(OUT, d)
    if os.path.exists(src):
        shutil.copytree(src, dst)
        print(f'  \u2713 /{d}/ copiado')
    else:
        os.makedirs(dst, exist_ok=True)
        print(f'  \u26a0  /{d}/ no encontrado en assets/ \u2014 directorio vac\u00edo creado')

open(os.path.join(OUT, 'css', 'main.css'), 'w', encoding='utf-8').write(CSS)
open(os.path.join(OUT, 'js',  'main.js'),  'w', encoding='utf-8').write(JS)
print('  \u2713 /css/main.css y /js/main.js generados')

print('\n\u2192 Generando HTML...')

# HOME
m, _ = read_md(f'{CONTENT}/_index.md')
home = f'''
<section class="hero" aria-labelledby="hero-h1">
  <div class="container">
    <p class="hero__label">N2N \u2014 Arquitectura Comercial Digital</p>
    <h1 class="hero__h1" id="hero-h1">{m.get('title','Arquitectura Comercial Digital para B2B Industrial')}</h1>
    <p class="hero__lead">{m.get('lead','En B2B industrial, el problema no es visibilidad. Es desrepresentaci\u00f3n operativa y ruido de consultas.')}</p>
    <div class="hero__actions">
      <a href="/framework/como-funciona/" class="btn btn--primary">Ver el Framework \u2192</a>
      <a href="/contacto/" class="btn btn--outline-white">Hablemos de tu operaci\u00f3n</a>
    </div>
    <div class="stats">
      <div><div class="stat__num">5</div><div class="stat__label">Pilares del<br>Framework N2N</div></div>
      <div><div class="stat__num">3</div><div class="stat__label">Capas de<br>entrega</div></div>
      <div><div class="stat__num">B2B</div><div class="stat__label">Solo industrial<br>por volumen</div></div>
    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="container">
    <div class="grid grid--2" style="gap:var(--s12);align-items:start">
      <div>
        <span class="section-header__label">Qu\u00e9 es N2N</span>
        <h2 style="font-size:clamp(1.4rem,2.5vw,2rem);font-weight:800;color:var(--navy);letter-spacing:-.02em;line-height:1.2;margin:var(--s3) 0 var(--s5)">{m.get('what_is_title','')}</h2>
        <p style="color:var(--text-muted);line-height:1.7;margin-bottom:var(--s6)">{m.get('what_is_body','')}</p>
        <a href="/framework/como-funciona/" class="btn btn--navy">Ver Framework \u2192</a>
      </div>
      <div>
        <div class="not-for">
          <p class="not-for__title">No trabajamos con</p>
          <ul>
            <li>Agencias de marketing o dise\u00f1o</li>
            <li>Ecommerce minorista o consumo masivo</li>
            <li>Plataformas SaaS gen\u00e9ricas</li>
            <li>Startups sin modelo operativo definido</li>
            <li>Proyectos que necesitan visibilidad antes que estructura</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section bg-section">
  <div class="container">
    <div class="section-header">
      <span class="section-header__label">El Framework</span>
      <h2>5 Pilares de Arquitectura Comercial Digital</h2>
      <p>El conjunto estructural que define c\u00f3mo representar, filtrar e integrar la operaci\u00f3n comercial industrial.</p>
    </div>
    <div class="grid grid--auto" style="gap:var(--s5)">
      <div class="card"><div class="pillar"><div class="pillar__num">01</div><div class="pillar__body"><h3>L\u00f3gica de Calificaci\u00f3n Comercial</h3><p>Reglas, se\u00f1ales y umbrales que determinan si una consulta representa una oportunidad real. Lead \u2260 Oportunidad.</p></div></div></div>
      <div class="card"><div class="pillar"><div class="pillar__num">02</div><div class="pillar__body"><h3>Representaci\u00f3n Operativa</h3><p>La superficie digital refleja con precisi\u00f3n capacidad real, restricciones y condiciones de la operaci\u00f3n.</p></div></div></div>
      <div class="card"><div class="pillar"><div class="pillar__num">03</div><div class="pillar__body"><h3>Arquitectura de Informaci\u00f3n T\u00e9cnica</h3><p>Fichas, tolerancias, certificaciones y documentaci\u00f3n de proceso para compradores t\u00e9cnicos. No para audiencia general.</p></div></div></div>
      <div class="card"><div class="pillar"><div class="pillar__num">04</div><div class="pillar__body"><h3>Gesti\u00f3n de Precios Complejos</h3><p>Precios por volumen, condiciones escalonadas y flujos RFQ. Sin lista de precios simplificada que rompa el margen.</p></div></div></div>
      <div class="card"><div class="pillar"><div class="pillar__num">05</div><div class="pillar__body"><h3>Integraci\u00f3n con Sistemas Operativos</h3><p>Conexi\u00f3n con ERP (Tango, Bejerman, SAP B1, Odoo) y CRM. La plataforma es extensi\u00f3n de la operaci\u00f3n, no sitio aislado.</p></div></div></div>
    </div>
    <div style="text-align:center;margin-top:var(--s10)">
      <a href="/framework/como-funciona/" class="btn btn--ghost">Ver el framework completo \u2192</a>
    </div>
  </div>
</section>

<section class="section bg-navy">
  <div class="container">
    <div class="section-header">
      <span class="section-header__label">Servicios</span>
      <h2>Tres niveles de intervenci\u00f3n</h2>
      <p style="color:rgba(255,255,255,.65)">Del diagn\u00f3stico estructural a la plataforma operativa.</p>
    </div>
    <div class="grid grid--3">
      <a href="/servicios/arquitectura-comercial/" class="card card--link" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.1)"><div class="card__tag">Capa 01</div><h3 class="card__title" style="color:#fff">Arquitectura Comercial</h3><p class="card__body" style="color:rgba(255,255,255,.6)">An\u00e1lisis de la operaci\u00f3n y documento estructural. Define qu\u00e9 mostrar, filtrar y c\u00f3mo calificar. 3\u20136 semanas.</p><span class="card__link">Ver servicio \u2192</span></a>
      <a href="/servicios/plataformas-industriales/" class="card card--link" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.1)"><div class="card__tag">Capa 02</div><h3 class="card__title" style="color:#fff">Plataformas Industriales</h3><p class="card__body" style="color:rgba(255,255,255,.6)">Sitios, portales B2B, sistemas de cotizaci\u00f3n e integraciones ERP alineados a la arquitectura. 8\u201316 semanas.</p><span class="card__link">Ver servicio \u2192</span></a>
      <a href="/servicios/consultoria-infraestructura/" class="card card--link" style="background:rgba(255,255,255,.05);border-color:rgba(255,255,255,.1)"><div class="card__tag">Capa 03</div><h3 class="card__title" style="color:#fff">Consultor\u00eda de Infraestructura</h3><p class="card__body" style="color:rgba(255,255,255,.6)">Trazabilidad, integridad de datos, automatizaci\u00f3n y cumplimiento normativo AFIP/SENASA.</p><span class="card__link">Ver servicio \u2192</span></a>
    </div>
  </div>
</section>

<section class="section bg-white">
  <div class="container">
    <div class="section-header">
      <span class="section-header__label">Industrias</span>
      <h2>Operaciones donde funciona</h2>
      <p>B2B industrial por volumen en manufactura, distribuci\u00f3n y log\u00edstica latinoamericana.</p>
    </div>
    <div class="grid grid--3">
      <a href="/industrias/manufactura/" class="card card--link"><div class="card__tag">Manufactura</div><h3 class="card__title">Fabricantes Industriales</h3><p class="card__body">Cat\u00e1logos con especificaciones reales, flujos RFQ y representaci\u00f3n de capacidad productiva alineada al ERP.</p><span class="card__link">Ver soluci\u00f3n \u2192</span></a>
      <a href="/industrias/distribuidores/" class="card card--link"><div class="card__tag">Distribuci\u00f3n</div><h3 class="card__title">Distribuidores e Importadores</h3><p class="card__body">Precios por cuenta, stock en tiempo real, portales de cliente y puente entre ERP y comprador.</p><span class="card__link">Ver soluci\u00f3n \u2192</span></a>
      <a href="/industrias/operadores-logisticos/" class="card card--link"><div class="card__tag">Log\u00edstica</div><h3 class="card__title">Operadores Log\u00edsticos</h3><p class="card__body">Representaci\u00f3n de cobertura real, se\u00f1ales de capacidad y filtros de calificaci\u00f3n para contratos y operaciones spot.</p><span class="card__link">Ver soluci\u00f3n \u2192</span></a>
    </div>
  </div>
</section>


<section class="tech-strip" aria-label="Infraestructura con la que operamos">
  <div class="container">
    <p class="tech-strip__label">Infraestructura con la que operamos</p>
    <div class="tech-strip__grid">
      <div class="tech-strip__item"><img src="/img/logos/hetzner.svg" alt="Hetzner" loading="lazy"><span>Hetzner</span></div>
      <div class="tech-strip__item"><img src="/img/logos/MaterialIconThemeDocker.svg" alt="Docker" loading="lazy"><span>Docker</span></div>
      <div class="tech-strip__item"><img src="/img/logos/DeviconLinux.svg" alt="Linux" loading="lazy"><span>Linux</span></div>
      <div class="tech-strip__item"><img src="/img/logos/MaterialIconThemePython.svg" alt="Python" loading="lazy"><span>Python</span></div>
      <div class="tech-strip__item"><img src="/img/logos/FileIconsNestjs.svg" alt="Next.js" loading="lazy"><span>Next.js</span></div>
      <div class="tech-strip__item"><img src="/img/logos/LogosCloudflareIcon.svg" alt="Cloudflare" loading="lazy"><span>Cloudflare</span></div>
      <div class="tech-strip__item"><img src="/img/logos/LogosAws.svg" alt="AWS" loading="lazy"><span>AWS</span></div>
      <div class="tech-strip__item"><img src="/img/logos/SimpleIconsOdoo.svg" alt="Odoo" loading="lazy"><span>Odoo</span></div>
    </div>
  </div>
</section>

<section class="section bg-section">
  <div class="container" style="text-align:center;max-width:620px;margin:0 auto">
    <span class="section-header__label">Contacto</span>
    <h2 style="font-size:clamp(1.6rem,3vw,2.2rem);font-weight:800;color:var(--navy);letter-spacing:-.02em;margin:var(--s3) 0 var(--s5)">\u00bfProblema estructural, no de marketing?</h2>
    <p style="color:var(--text-muted);margin-bottom:var(--s8)">Para operaciones B2B que venden por volumen con procesos definidos. Si el problema es estructural, podemos ayudar.</p>
    <a href="/contacto/" class="btn btn--primary" style="font-size:1.05rem;padding:.8em 2em">Evaluar mi operaci\u00f3n \u2192</a>
  </div>
</section>
'''
write(f'{OUT}/index.html', page(
    'N2N \u2014 Arquitectura Comercial Digital para B2B Industrial',
    m.get('description', 'N2N dise\u00f1a arquitectura comercial digital para empresas industriales B2B que venden por volumen.'),
    home
))

# FRAMEWORK
m, bmd = read_md(f'{CONTENT}/framework/how-it-works.md')
write(f'{OUT}/framework/como-funciona/index.html', inner_page(
    'Framework',
    '<p class="breadcrumb"><a href="/">Inicio</a><span>\u203a</span>Framework</p>',
    m.get('title',''), m.get('description',''), md_to_html(bmd), 'framework',
    '<a href="/framework/componentes/" class="btn btn--outline-white">Ver componentes</a>'
))

m, bmd = read_md(f'{CONTENT}/framework/components.md')
write(f'{OUT}/framework/componentes/index.html', inner_page(
    'Framework',
    '<p class="breadcrumb"><a href="/">Inicio</a><span>\u203a</span><a href="/framework/como-funciona/">Framework</a><span>\u203a</span>Componentes</p>',
    m.get('title',''), m.get('description',''), md_to_html(bmd), 'framework',
    '<a href="/framework/como-funciona/" class="btn btn--outline-white">C\u00f3mo funciona</a>'
))

fw_idx_body = '''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="hero__label">Framework</p>
    <h1 class="hero__h1" id="page-h1">Framework N2N</h1>
    <p class="hero__lead">5 pilares y 3 capas de entrega para operaciones industriales B2B que venden por volumen.</p>
    <div class="hero__actions">
      <a href="/framework/como-funciona/" class="btn btn--primary">C\u00f3mo funciona \u2192</a>
      <a href="/framework/componentes/" class="btn btn--outline-white">Componentes</a>
    </div>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="grid grid--2">
      <a href="/framework/como-funciona/" class="card card--link"><div class="card__tag">Framework</div><h2 class="card__title">C\u00f3mo Funciona</h2><p class="card__body">La cadena causal desde la venta por volumen hasta los requisitos de arquitectura digital.</p><span class="card__link">Leer \u2192</span></a>
      <a href="/framework/componentes/" class="card card--link"><div class="card__tag">Framework</div><h2 class="card__title">Componentes del Sistema</h2><p class="card__body">El conjunto m\u00ednimo de componentes de una arquitectura comercial digital funcional.</p><span class="card__link">Leer \u2192</span></a>
    </div>
  </div>
</section>'''
write(f'{OUT}/framework/index.html', page('Framework \u2014 N2N', 'El framework N2N para arquitectura comercial digital industrial.', fw_idx_body, 'framework'))

# INDUSTRIAS
for fname, slug, label in [
    ('manufacturing',      'manufactura',            'Manufactura'),
    ('distributors',       'distribuidores',         'Distribuci\u00f3n'),
    ('logistics-operators','operadores-logisticos',  'Log\u00edstica'),
]:
    m, bmd = read_md(f'{CONTENT}/industries/{fname}.md')
    write(f'{OUT}/industrias/{slug}/index.html', inner_page(
        m.get('label', label),
        f'<p class="breadcrumb"><a href="/">Inicio</a><span>\u203a</span><a href="/industrias/">Industrias</a><span>\u203a</span>{label}</p>',
        m.get('title',''), m.get('description',''), md_to_html(bmd), 'industrias'
    ))

ind_idx_body = '''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="hero__label">Industrias</p>
    <h1 class="hero__h1" id="page-h1">Arquitectura Comercial Digital por Industria</h1>
    <p class="hero__lead">Soluciones estructurales para operaciones industriales B2B en manufactura, distribuci\u00f3n y log\u00edstica latinoamericana.</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="grid grid--3">
      <a href="/industrias/manufactura/" class="card card--link"><div class="card__tag">Manufactura</div><h2 class="card__title">Fabricantes Industriales</h2><p class="card__body">Cat\u00e1logos con especificaciones reales, flujos RFQ, representaci\u00f3n de capacidad y restricciones de producci\u00f3n.</p><span class="card__link">Ver soluci\u00f3n \u2192</span></a>
      <a href="/industrias/distribuidores/" class="card card--link"><div class="card__tag">Distribuci\u00f3n</div><h2 class="card__title">Distribuidores e Importadores</h2><p class="card__body">Precios espec\u00edficos por cuenta, stock en tiempo real, portales de cliente y puente ERP-comprador.</p><span class="card__link">Ver soluci\u00f3n \u2192</span></a>
      <a href="/industrias/operadores-logisticos/" class="card card--link"><div class="card__tag">Log\u00edstica</div><h2 class="card__title">Operadores Log\u00edsticos</h2><p class="card__body">Representaci\u00f3n de cobertura real, se\u00f1ales de capacidad y calificaci\u00f3n de demanda para contratos y spot.</p><span class="card__link">Ver soluci\u00f3n \u2192</span></a>
    </div>
  </div>
</section>'''
write(f'{OUT}/industrias/index.html', page('Industrias \u2014 N2N', 'N2N para manufactura, distribuci\u00f3n y log\u00edstica industrial.', ind_idx_body, 'industrias'))

# SERVICIOS
for fname, slug, label in [
    ('commercial-architecture',   'arquitectura-comercial',      'Servicio 01'),
    ('industrial-platforms',      'plataformas-industriales',    'Servicio 02'),
    ('infrastructure-consulting', 'consultoria-infraestructura', 'Servicio 03'),
]:
    m, bmd = read_md(f'{CONTENT}/services/{fname}.md')
    write(f'{OUT}/servicios/{slug}/index.html', inner_page(
        m.get('label', label),
        f'<p class="breadcrumb"><a href="/">Inicio</a><span>\u203a</span><a href="/servicios/">Servicios</a><span>\u203a</span>{m.get("label", label)}</p>',
        m.get('title',''), m.get('description',''), md_to_html(bmd), 'servicios'
    ))

serv_idx_body = '''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="hero__label">Servicios</p>
    <h1 class="hero__h1" id="page-h1">Tres Niveles de Intervenci\u00f3n</h1>
    <p class="hero__lead">Del diagn\u00f3stico estructural a la plataforma operativa y la resoluci\u00f3n de problemas t\u00e9cnicos espec\u00edficos.</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="grid grid--3">
      <a href="/servicios/arquitectura-comercial/" class="card card--link"><div class="card__tag">Capa 01</div><h2 class="card__title">Arquitectura Comercial</h2><p class="card__body">An\u00e1lisis de la operaci\u00f3n y documento estructural que define qu\u00e9 mostrar, filtrar y c\u00f3mo calificar demanda. 3\u20136 semanas.</p><span class="card__link">Ver servicio \u2192</span></a>
      <a href="/servicios/plataformas-industriales/" class="card card--link"><div class="card__tag">Capa 02</div><h2 class="card__title">Plataformas Industriales</h2><p class="card__body">Construcci\u00f3n de la plataforma alineada a la arquitectura. Sitios, portales B2B, sistemas de cotizaci\u00f3n, integraciones ERP. 8\u201316 semanas.</p><span class="card__link">Ver servicio \u2192</span></a>
      <a href="/servicios/consultoria-infraestructura/" class="card card--link"><div class="card__tag">Capa 03</div><h2 class="card__title">Consultor\u00eda de Infraestructura</h2><p class="card__body">Trazabilidad, integridad de datos, automatizaci\u00f3n y cumplimiento normativo AFIP/SENASA/exportaci\u00f3n.</p><span class="card__link">Ver servicio \u2192</span></a>
    </div>
  </div>
</section>'''
write(f'{OUT}/servicios/index.html', page('Servicios \u2014 N2N', 'Tres capas de intervenci\u00f3n en arquitectura comercial digital B2B industrial.', serv_idx_body, 'servicios'))

# CASOS
for fname, slug in [('case-01','caso-01'),('case-02','caso-02'),('case-03','caso-03')]:
    m, bmd = read_md(f'{CONTENT}/proof/{fname}.md')
    label = m.get('label', slug)
    b = f'''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="breadcrumb"><a href="/">Inicio</a><span>\u203a</span><a href="/casos/">Casos</a><span>\u203a</span>{label}</p>
    <div class="case-badge">{label}</div>
    <h1 class="hero__h1" id="page-h1">{m.get('title','')}</h1>
    <p class="hero__lead">{m.get('description','')}</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="prose">{md_to_html(bmd)}</div>
    <div style="margin-top:var(--s10);padding-top:var(--s8);border-top:1px solid var(--border);display:flex;gap:var(--s4);flex-wrap:wrap">
      <a href="/contacto/" class="btn btn--primary">Evaluar mi operaci\u00f3n \u2192</a>
      <a href="/casos/" class="btn btn--ghost">Ver todos los casos</a>
    </div>
  </div>
</section>'''
    write(f'{OUT}/casos/{slug}/index.html', page(m.get('title',''), m.get('description',''), b, 'casos'))

casos_idx_body = '''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="hero__label">Casos</p>
    <h1 class="hero__h1" id="page-h1">Resultados en Operaciones Industriales B2B</h1>
    <p class="hero__lead">Casos modelados basados en patrones estructurales comunes en operaciones industriales latinoamericanas.</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="grid grid--3">
      <a href="/casos/caso-01/" class="card card--link"><div class="case-badge" style="background:rgba(0,0,85,.08);color:var(--navy);border-color:rgba(0,0,85,.2)">Caso 01</div><h2 class="card__title">Reducci\u00f3n de Ruido Comercial</h2><p class="card__body">Distribuidor de componentes reduce consultas irrelevantes 65% con arquitectura de calificaci\u00f3n.</p><span class="card__link">Ver caso \u2192</span></a>
      <a href="/casos/caso-02/" class="card card--link"><div class="case-badge" style="background:rgba(0,0,85,.08);color:var(--navy);border-color:rgba(0,0,85,.2)">Caso 02</div><h2 class="card__title">Venta por Volumen con Arquitectura Digital</h2><p class="card__body">Fabricante estructura flujos separados para cat\u00e1logo est\u00e1ndar y RFQ personalizado.</p><span class="card__link">Ver caso \u2192</span></a>
      <a href="/casos/caso-03/" class="card card--link"><div class="case-badge" style="background:rgba(0,0,85,.08);color:var(--navy);border-color:rgba(0,0,85,.2)">Caso 03</div><h2 class="card__title">Plataforma B2B con Integraci\u00f3n ERP</h2><p class="card__body">Distribuidor con 1.200+ SKUs conecta SAP B1 a plataforma con precios por cuenta en tiempo real.</p><span class="card__link">Ver caso \u2192</span></a>
    </div>
  </div>
</section>'''
write(f'{OUT}/casos/index.html', page('Casos \u2014 N2N', 'Casos de arquitectura comercial digital en operaciones industriales latinoamericanas.', casos_idx_body, 'casos'))

# CONOCIMIENTO
knowledge_map = [
    ('what-is-digital-commercial-architecture', 'que-es-arquitectura-comercial-digital'),
    ('why-ecommerce-fails-industrial-b2b',       'por-que-falla-ecommerce-b2b-industrial'),
    ('qualification-systems-b2b',                'sistemas-calificacion-b2b'),
    ('pricing-complexity-volume-sales',          'precios-complejos-ventas-volumen'),
    ('erp-integration-surface',                  'integracion-erp'),
    ('portals-roles-permissions',                'portales-roles-permisos'),
    ('buyer-spec-surface',                       'superficie-especificacion-comprador'),
    ('kpis-noise-vs-traffic',                    'kpis-ruido-vs-trafico'),
    ('implementation-sequence',                  'secuencia-implementacion'),
    ('marketing-after-structure',                'marketing-despues-estructura'),
    ('ceo-guide-industrial-digital',             'guia-ceo-digital-industrial'),
    ('sales-manager-playbook',                   'playbook-gerente-ventas'),
]
know_cards = ''
for fname, slug in knowledge_map:
    m, bmd = read_md(f'{CONTENT}/knowledge/{fname}.md')
    title = m.get('title','')
    desc  = m.get('description','')
    b = f'''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="breadcrumb"><a href="/">Inicio</a><span>\u203a</span><a href="/conocimiento/">Conocimiento</a></p>
    <p class="hero__label">Conocimiento</p>
    <h1 class="hero__h1" id="page-h1">{title}</h1>
    <p class="hero__lead">{desc}</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="prose">{md_to_html(bmd)}</div>
    <div style="margin-top:var(--s10);padding-top:var(--s8);border-top:1px solid var(--border);display:flex;gap:var(--s4);flex-wrap:wrap">
      <a href="/conocimiento/" class="btn btn--ghost">\u2190 Volver a Conocimiento</a>
      <a href="/contacto/" class="btn btn--primary">Evaluar mi operaci\u00f3n \u2192</a>
    </div>
  </div>
</section>'''
    write(f'{OUT}/conocimiento/{slug}/index.html', page(title, desc, b, 'conocimiento'))
    know_cards += f'<a href="/conocimiento/{slug}/" class="card card--link"><h2 class="card__title">{title}</h2><p class="card__body">{desc[:160]}\u2026</p><span class="card__link">Leer \u2192</span></a>\n'

know_idx_body = f'''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="hero__label">Conocimiento</p>
    <h1 class="hero__h1" id="page-h1">Documentaci\u00f3n T\u00e9cnica \u2014 Arquitectura Comercial B2B Industrial</h1>
    <p class="hero__lead">Definiciones, frameworks, patrones de integraci\u00f3n, sistemas de calificaci\u00f3n y KPIs para entornos industriales latinoamericanos.</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="grid grid--auto">{know_cards}</div>
  </div>
</section>'''
write(f'{OUT}/conocimiento/index.html', page('Conocimiento \u2014 N2N', 'Documentos t\u00e9cnicos sobre arquitectura comercial digital para B2B industrial.', know_idx_body, 'conocimiento'))

# COMPARAR
comparar_map = [
    ('b2b-ecommerce-vs-commercial-architecture', 'ecommerce-b2b-vs-arquitectura-comercial'),
    ('custom-vs-saas',                           'custom-vs-saas'),
    ('n2n-vs-agency',                            'n2n-vs-agencia'),
]
comp_cards = ''
for fname, slug in comparar_map:
    m, bmd = read_md(f'{CONTENT}/compare/{fname}.md')
    title = m.get('title','')
    desc  = m.get('description','')
    b = f'''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="breadcrumb"><a href="/">Inicio</a><span>\u203a</span><a href="/comparar/">Comparar</a></p>
    <p class="hero__label">An\u00e1lisis Comparativo</p>
    <h1 class="hero__h1" id="page-h1">{title}</h1>
    <p class="hero__lead">{desc}</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="prose">{md_to_html(bmd)}</div>
    <div style="margin-top:var(--s10);padding-top:var(--s8);border-top:1px solid var(--border);display:flex;gap:var(--s4);flex-wrap:wrap">
      <a href="/comparar/" class="btn btn--ghost">\u2190 Volver a Comparar</a>
      <a href="/contacto/" class="btn btn--primary">Evaluar mi operaci\u00f3n \u2192</a>
    </div>
  </div>
</section>'''
    write(f'{OUT}/comparar/{slug}/index.html', page(title, desc, b))
    comp_cards += f'<a href="/comparar/{slug}/" class="card card--link"><h2 class="card__title">{title}</h2><p class="card__body">{desc[:160]}\u2026</p><span class="card__link">Ver an\u00e1lisis \u2192</span></a>\n'

comp_idx_body = f'''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="hero__label">Comparar</p>
    <h1 class="hero__h1" id="page-h1">An\u00e1lisis Comparativos</h1>
    <p class="hero__lead">Diferencias estructurales entre arquitectura comercial digital y las alternativas habituales en el mercado latinoamericano.</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="grid grid--3">{comp_cards}</div>
  </div>
</section>'''
write(f'{OUT}/comparar/index.html', page('Comparar \u2014 N2N vs Alternativas', 'An\u00e1lisis estructurales: arquitectura comercial digital vs ecommerce, SaaS y agencias.', comp_idx_body))

# CONTACTO
contact_body = '''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="hero__label">Contacto</p>
    <h1 class="hero__h1" id="page-h1">Evaluar si vale la pena resolver el problema</h1>
    <p class="hero__lead">No es para consultas generales. Es el punto de entrada para evaluar si existe un problema comercial estructural que podemos resolver.</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="grid grid--2" style="gap:var(--s12);align-items:start">
      <div>
        <form id="contact-form" novalidate>
          <div class="form-grid">
            <div class="form-group">
              <label for="f-name">Nombre y empresa *</label>
              <input type="text" id="f-name" name="name" placeholder="Juan Garc\u00eda \u2014 Industrias Garc\u00eda SA" required>
            </div>
            <div class="form-group">
              <label for="f-email">Email corporativo *</label>
              <input type="email" id="f-email" name="email" placeholder="jgarcia@industriasgarcia.com" required>
            </div>
            <div class="form-group">
              <label for="f-sector">Sector / operaci\u00f3n *</label>
              <select id="f-sector" name="sector" required>
                <option value="">Seleccionar\u2026</option>
                <option>Manufactura industrial</option>
                <option>Distribuci\u00f3n / importaci\u00f3n</option>
                <option>Operador log\u00edstico</option>
                <option>Otro B2B industrial</option>
              </select>
            </div>
            <div class="form-group">
              <label for="f-problem">\u00bfCu\u00e1l es el problema? *</label>
              <textarea id="f-problem" name="problem" placeholder="Describ\u00edlo brevemente: qu\u00e9 ocurre hoy, qu\u00e9 quer\u00e9s resolver, en qu\u00e9 escala opera tu empresa." required></textarea>
            </div>
            <div class="form-row">
              <button type="submit" class="btn btn--primary" style="width:100%;justify-content:center;font-size:1rem">Enviar consulta</button>
              <p id="form-msg" style="margin-top:var(--s3);font-size:.9rem"></p>
            </div>
          </div>
        </form>
      </div>
      <div style="display:flex;flex-direction:column;gap:var(--s6)">
        <div class="not-for">
          <p class="not-for__title">Criterios m\u00ednimos</p>
          <ul>
            <li>Operaci\u00f3n B2B que vende por volumen (no retail)</li>
            <li>Procesos operativos definidos</li>
            <li>El problema es estructural, no est\u00e9tico</li>
          </ul>
        </div>
        <div style="display:flex;flex-direction:column;gap:var(--s4)">
          <div>
            <p style="font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--orange);margin-bottom:var(--s2)">Email directo</p>
            <a href="mailto:contacto@n2n.com.ar" style="color:var(--navy);font-weight:600">contacto@n2n.com.ar</a>
          </div>
          <div>
            <p style="font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--orange);margin-bottom:var(--s2)">WhatsApp</p>
            <a href="https://wa.me/5491138230614" target="_blank" rel="noopener" style="color:var(--navy);font-weight:600">+54 9 11 3823-0614</a>
          </div>
          <p style="font-size:.85rem;color:var(--text-muted)">Respondemos en 24\u201348 horas h\u00e1biles.</p>
        </div>
      </div>
    </div>
  </div>
</section>'''
write(f'{OUT}/contacto/index.html', page('Contacto \u2014 N2N', 'Contacto para evaluaci\u00f3n de operaciones industriales B2B.', contact_body, 'contacto'))

# GLOSARIO
m, bmd = read_md(f'{CONTENT}/glossary.md')
glos_body = f'''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="hero__label">Glosario</p>
    <h1 class="hero__h1" id="page-h1">{m.get('title','')}</h1>
    <p class="hero__lead">{m.get('description','')}</p>
  </div>
</section>
<section class="section bg-white">
  <div class="container"><div class="prose">{md_to_html(bmd)}</div></div>
</section>'''
write(f'{OUT}/glosario/index.html', page(m.get('title',''), m.get('description',''), glos_body))

# LEGAL
m, bmd = read_md(f'{CONTENT}/legal.md')
legal_body = f'''
<section class="hero" aria-labelledby="page-h1">
  <div class="container">
    <p class="hero__label">Legal</p>
    <h1 class="hero__h1" id="page-h1">{m.get('title','')}</h1>
  </div>
</section>
<section class="section bg-white">
  <div class="container"><div class="prose">{md_to_html(bmd)}</div></div>
</section>'''
write(f'{OUT}/legal/index.html', page(m.get('title',''), m.get('description',''), legal_body, '', noindex=True))

# 404
nf = '''
<section class="hero" style="min-height:65vh;display:flex;align-items:center">
  <div class="container" style="text-align:center">
    <p class="hero__label">404</p>
    <h1 class="hero__h1" style="max-width:none">P\u00e1gina no encontrada</h1>
    <p class="hero__lead" style="margin:0 auto var(--s8)">La URL que busc\u00e1s no existe o fue movida.</p>
    <a href="/" class="btn btn--primary">Volver al inicio \u2192</a>
  </div>
</section>'''
write(f'{OUT}/404.html', page('404', '', nf))

# CNAME para GitHub Pages
open(os.path.join(OUT, 'CNAME'), 'w').write('n2n.com.ar')
print('  2713 CNAME escrito')

total = len(list(glob.glob(f'{OUT}/**/index.html', recursive=True))) + 1
print(f'\n\u2713 {total} archivos en {OUT}')
print(f'  cd {OUT} && python3 -m http.server 8080')
