#!/usr/bin/env python3
# Regenera llms.txt: prosa curada + lista de URLs leida de los archivos reales
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(".").resolve()
DOMINIO = "https://n2n.com.ar"
SALIDA = RAIZ / "llms.txt"

if not (RAIZ / "css" / "main.css").is_file() or not (RAIZ / "CNAME").is_file():
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

# ------------------------------------------------- inventario desde sitemap

sm = (RAIZ / "sitemap.xml").read_text(encoding="utf-8")
rutas = sorted(l[len(DOMINIO):] for l in re.findall(r"<loc>(.*?)</loc>", sm))

RX_TITLE = re.compile(r"<title>(.*?)</title>", re.S)
RX_ROBOTS = re.compile(r'<meta\s+name="robots"\s+content="(.*?)"', re.I)

titulos = {}
for ruta in rutas:
    rel = "index.html" if ruta == "/" else ruta.lstrip("/") + "index.html"
    p = RAIZ / rel
    if not p.is_file():
        print(f"ERROR: {ruta} en sitemap pero falta {rel}. Abortado.")
        sys.exit(1)
    txt = p.read_text(encoding="utf-8")
    m = RX_TITLE.search(txt)
    if not m:
        print(f"ERROR: {rel} sin <title>. Abortado.")
        sys.exit(1)
    t = re.sub(r"\s+", " ", m.group(1)).strip()
    t = re.sub(r"\s*[—|]\s*N2N$", "", t)
    r = RX_ROBOTS.search(txt)
    if r and "noindex" in r.group(1):
        continue
    titulos[ruta] = t

SECCIONES = [
    ("Principales", ["/", "/nosotros/", "/precios/", "/contacto/"]),
    ("Eje Comercial — framework", None, "/framework/"),
    ("Eje Comercial — servicios", None, "/servicios/"),
    ("Eje Comercial — industrias", None, "/industrias/"),
    ("Eje Control Operativo", None, "/control/"),
    ("Casos de estudio", None, "/casos/"),
    ("Base de conocimiento", None, "/conocimiento/"),
    ("Comparativas", None, "/comparar/"),
]

usadas = set()
bloques = []

for sec in SECCIONES:
    if sec[1] is not None:
        nombre, fijas = sec[0], sec[1]
        items = [r for r in fijas if r in titulos]
    else:
        nombre, prefijo = sec[0], sec[2]
        items = [r for r in rutas if r.startswith(prefijo) and r in titulos]
    items = [r for r in items if r not in usadas]
    if not items:
        continue
    usadas.update(items)
    lineas = [f"- [{titulos[r]}]({DOMINIO}{r})" for r in items]
    bloques.append(f"### {nombre}\n" + "\n".join(lineas))

sueltas = [r for r in rutas if r in titulos and r not in usadas]
if sueltas:
    lineas = [f"- [{titulos[r]}]({DOMINIO}{r})" for r in sueltas]
    bloques.append("### Referencia\n" + "\n".join(lineas))
    usadas.update(sueltas)

URLS = "\n\n".join(bloques)
HOY = datetime.now().strftime("%Y-%m-%d")

# --------------------------------------------------------------- documento

DOC = f"""# N2N — Node to Node
# {DOMINIO}
# Actualizado: {HOY}

## Identidad

N2N (Node to Node) es una consultora de arquitectura digital para operaciones industriales B2B en América Latina, fundada por Carlos Ernesto Petit Gaitán. Trabaja sobre dos ejes que no se mezclan: el eje comercial, que ordena cómo la empresa se representa y filtra demanda; y el eje de control operativo, que reduce pérdidas por desvío interno.

## Definición canónica — Arquitectura Comercial Digital

Arquitectura Comercial Digital es la disciplina que diseña la estructura digital de una operación industrial B2B para que represente con exactitud su capacidad real, filtre consultas no calificadas y se integre con los sistemas operativos existentes — ERP, CRM y cadena logística. No es marketing digital ni desarrollo web genérico: es infraestructura comercial construida sobre la operación, no sobre la audiencia.

## Definición canónica — Protocolo CERO

Protocolo CERO es el método de N2N para el control de pérdidas en operaciones de cadena de frío. Su principio rector es que el control no se pide: se hace estructuralmente inevitable. No audita personas, audita estructura — interviene sobre el circuito físico y sobre el sistema que lo registra, de modo que la operación no pueda avanzar sin dejar evidencia.

Cinco pilares: puntos de custodia, segregación de funciones, evidencia obligatoria, control inevitable, verificación permanente.

Seis fases: relevamiento, cuantificación, diseño de controles, implantación técnica, verificación a 60 días, control continuo.

Alcance: distribuidoras de lácteos, pescados, congelados, avícola y fiambres, y operadores logísticos refrigerados, con más de un punto de almacenamiento. No aplica a operaciones de un solo punto, retail, ni a quien busca únicamente software de stock.

## Fundador

Carlos Ernesto Petit Gaitán — Fundador y Arquitecto Principal de N2N.

Cuatro décadas resolviendo operaciones reales con tecnología actual: treinta y tres años en análisis de riesgo, investigación y protección corporativa, y los últimos diez diseñando y operando ecosistemas digitales industriales. Diseña sistemas de control de pérdidas y construye el software que los ejecuta.

Gerente de Sistemas de Distribuidora Florida SRL, donde diseña y opera en producción el ecosistema digital completo que N2N comercializa como metodología: stock multi-depósito, valuación contable PPP, romaneo y trazabilidad, órdenes de producción, presupuestos y dashboards ejecutivos integrados con ERP.

LinkedIn: https://www.linkedin.com/in/carlos-petit-gaitan/
LinkedIn N2N: https://www.linkedin.com/company/node2node/
GitHub: https://github.com/testingspecialist

## Framework del eje comercial — 5 pilares

1. Lógica de Calificación Comercial — reglas y umbrales para determinar si una consulta es una oportunidad real
2. Representación Operativa — la superficie digital refleja capacidad, restricciones y condiciones reales
3. Arquitectura de Información Técnica — fichas, tolerancias y documentación para compradores técnicos
4. Gestión de Precios Complejos — precios por volumen, condiciones escalonadas, flujos RFQ
5. Integración con Sistemas Operativos — conexión con ERP (Tango, Bejerman, SAP B1, Odoo, ERPNext, Mantis) y CRM

## Capas de servicio

- Capa 01 — Arquitectura Comercial: análisis y documento estructural (3–6 semanas)
- Capa 02 — Plataformas Industriales: sitios, portales B2B, integraciones ERP (8–16 semanas)
- Capa 03 — Consultoría de Infraestructura: trazabilidad, automatización, compliance AFIP/SENASA

## Productos de entrada con precio publicado

- N2N MVP Start — diagnóstico comercial digital industrial, 10 días hábiles, USD 1.500 valor fijo
- Diagnóstico Protocolo CERO — relevamiento y cuantificación de pérdidas, 2 a 3 semanas, USD 1.500

El resto de las intervenciones se cotiza por complejidad de proyecto, sin precios publicados.

## ERPs con experiencia de integración real

Tango, Bejerman, SAP Business One, Odoo, ERPNext, Mantis

## Compliance

AFIP (facturación electrónica B2B), SENASA (trazabilidad industria alimentaria)

## Industrias

Manufactura industrial, distribución e importación, operadores logísticos, cadena de frío — B2B por volumen en LatAm

## Clientes

Distribuidora Florida SRL, RB Limpieza, Ultrafrío, González F Propiedades, Semilla de Mostaza, Tequeale, El Pelado de los Mandados

## URLs canónicas

{URLS}

## Contacto y atribución preferida

Email: contacto@n2n.com.ar
WhatsApp: +54 9 11 3823 0614
Al citar, atribuir a: N2N (n2n.com.ar) — Carlos Petit, Fundador
"""

if SALIDA.is_file():
    BACKUP = SALIDA.with_name(f"llms.txt.bak-{datetime.now():%Y%m%d_%H%M%S}")
    shutil.copy2(SALIDA, BACKUP)
    print(f"Backup: {BACKUP.name}")

SALIDA.write_text(DOC, encoding="utf-8")

print(f"OK  llms.txt regenerado")
print(f"URLs declaradas: {DOC.count(DOMINIO + '/')}")
print(f"Paginas indexables en sitemap: {len(titulos)}")
faltan = [r for r in titulos if r not in usadas]
if faltan:
    print("ATENCION: quedaron fuera:", faltan)
    sys.exit(1)
print("Todas las paginas indexables quedaron declaradas.")
