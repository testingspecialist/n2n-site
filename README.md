# N2N — Sitio web

Sitio estático de **N2N** (<https://n2n.com.ar>) — infraestructura digital B2B para operaciones industriales.

## Descripción

Sitio corporativo estático servido por GitHub Pages detrás de Cloudflare. Documenta el framework de trabajo, servicios, casos, industrias atendidas y base de conocimiento de N2N.

## Estructura del sitio

```text
index.html       # Home
framework/       # Framework de arquitectura comercial digital
industrias/      # Páginas por industria atendida
servicios/       # Capas de servicio
casos/           # Casos de estudio
conocimiento/    # Base de conocimiento y guías
comparar/        # Comparativas de enfoque
glosario/        # Glosario de términos
contacto/        # Contacto
mvp-start/       # Producto de entrada — diagnóstico pago (standalone, sin nav ni footer)
control/         # Eje Control Operativo — Protocolo CERO (standalone, fuera del nav)
descargas/       # PDFs descargables (n2n-mvp-start.pdf, n2n-protocolo-cero.pdf)
legal/           # Páginas legales
css/ js/ fonts/ img/   # Assets estáticos
404.html         # Página de error
CNAME            # Dominio custom (n2n.com.ar)
```

## Stack

| Capa | Tecnología |
|---|---|
| Sitio | HTML/CSS/JS estático |
| Hosting | GitHub Pages |
| CDN / DNS | Cloudflare |
| Analytics | Google Analytics 4 (G-07T9PCBG7P) |
| Formularios | Web3Forms |

## Deploy

Push a main → publicación automática vía GitHub Pages (~2 minutos). El repo público ES producción.

```bash
git add .
git commit -m "contenido: descripcion"
git push origin main
```

## Notas
- Fuente de verdad única — no hay copia en servidor Hetzner
- Sin Hugo, sin generador — HTML directo editado a mano
- Analytics: Google Analytics 4 — G-07T9PCBG7P
- AI crawlers permitidos (robots.txt + llms.txt)
- main = producción
- PDFs generados con WeasyPrint mediante scripts versionados en la raiz del repo

## Criterio editorial — titles y metadatos

- `<title>` de maximo 62 caracteres. Google trunca alrededor de los 60 y un
  title cortado rompe la linea clickeable del resultado.
- Sin sufijo de marca en el title. Agregar `— N2N` consume 7 de los 60
  caracteres disponibles y no aporta diferenciacion entre resultados propios.
- Sin capitalizacion tipo titulo: el espanol no la usa y ocupa mas ancho visual
  en el SERP.
- `og:title` y `twitter:title` siempre sincronizados con `<title>`. Si divergen,
  el sitio dice cosas distintas segun el canal.
- El `headline` del JSON-LD NO sigue al `<title>`: se alinea con el `<h1>` de la
  pagina, que es el titulo real del articulo.
- Las `meta description` largas quedan como aviso aceptado del diagnostico. El
  rango 120-158 es una referencia, no un fallo: Google reescribe la description
  en la mayoria de los resultados.

## Scripts (_scripts/)

Los scripts viven en `_scripts/`. El guion bajo hace que GitHub Pages
no los publique: en la raiz quedaban servidos por HTTP con rutas del
filesystem local adentro. Ejecutarlos desde la raiz del repo:
`python3 _scripts/nombre.py`.

Auditores read-only, correr antes de cada commit:
`diagnostico_sitio_v3.py` (metadatos y SEO) y
`diagnostico_estructural_v4.py` (sintaxis, JSON-LD, semantica, deuda).

| Script | Funcion |
|---|---|
| `diagnostico_sitio_v3.py` | Auditor read-only vigente. Umbrales alineados al criterio editorial (title <= 62, description 120-158), auditoria de sincronizacion de og y twitter, robots.txt completo. |
| `diagnostico_sitio_v2.py` | Auditor anterior. Se conserva para comparar salidas. Umbrales 60 / 100-160 y sin chequeo de sincronizacion. |
| `acortar_titles_v1.py` | Acorto 25 titles que se truncaban en SERP y sincronizo og:title / twitter:title. |
| `reescribir_descriptions_hubs_v1.py` | Reescribio las 7 descriptions cortas de las hub pages al rango 120-158. |
| `exportar_descriptions_largas_v1.py` | Read-only. Vuelca a Markdown las descriptions que superan el maximo, para trabajarlas fuera del repo. |
| `aplicar_descriptions_largas_v1.py` | Reescribio 28 descriptions largas al rango y sincronizo og y twitter. |
| `insertar_diagnosticos_precios_v1.py` | Inserto en /precios/ el bloque con las dos entradas de precio fijo. Saco a /mvp-start/ y /control/protocolo-cero/ de huerfanas. |
| `agregar_twitter_nosotros_v1.py` | Agrego twitter:title y twitter:description a /nosotros/, la unica pagina que no los tenia. |
| `reescribir_caso01_control_v1.py` | Reescribio /casos/caso-01/ desde el eje Control: contenido, metadatos en los tres canales y headline JSON-LD. Caso anonimizado a 'un distribuidor de cadena de frio'. |
| `sincronizar_refs_caso01_v1.py` | Sincronizo las referencias externas a caso-01: card e ItemList de /casos/, linea de llms.txt y lastmod del sitemap. |
| `anonimizar_casos_a2_v1.py` | Anonimizo caso-03 (razon social y rubro) para que caso-01 no sea reconstruible por cruce. Reescribio title y description de caso-02 y caso-03, que describian casos distintos. Saco la enumeracion de sistemas de la bio en llms.txt. |
| `diagnostico_estructural_v4.py` | Auditor read-only complementario. Parseo real de HTML, validacion de JSON-LD, jerarquia de headings y accesibilidad, deuda tecnica, y volcado del contenido a TXT para revision semantica. |
| `corregir_semantica_hubs_v1.py` | Elimino la contradiccion de /casos/ (declaraba casos modelados y a la vez sistemas reales), unifico el h1 de caso-01 al criterio descriptivo de caso-02 y caso-03, y acorto el h1 de /nosotros/ que era una oracion de 113 caracteres. |
| `diferenciar_h1_intencion_v1.py` | Reescribio 12 h1 que abrian con la misma keyword y competian entre si. Solo la pagina definicional conserva el termino; el resto abre con su propio diferenciador. |

Todos los scripts de escritura siguen el mismo patron: backup verificable,
validacion sin escribir, escritura, verificacion posterior. Son idempotentes
y abortan ante cualquier estado inesperado.

## Desarrollado por
N2N — https://n2n.com.ar
