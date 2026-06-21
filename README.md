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
| Analytics | Umami |
| Formularios | Web3Forms |

## Deploy

Push a master → publicación automática vía GitHub Pages (~2 minutos). El repo público ES producción.

```bash
git add .
git commit -m "contenido: descripcion"
git push origin master
```

## Notas
- Fuente de verdad única — no hay copia en servidor Hetzner
- Sin Hugo, sin generador — HTML directo editado a mano
- Analytics: Umami ID 05b64f33-b9ae-4ffa-b068-8a2dacff6e33
- AI crawlers permitidos (robots.txt + llms.txt)
- Master = producción

## Desarrollado por
N2N — https://n2n.com.ar
