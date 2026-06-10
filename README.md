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

Push a la rama principal → publicación automática vía GitHub Pages (~2 minutos).

```bash
git add .
git commit -m "contenido: actualización"
git push
```
