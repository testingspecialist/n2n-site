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

## Desarrollado por
N2N — https://n2n.com.ar
