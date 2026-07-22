old_line = '<url><loc>https://n2n.com.ar/legal/</loc><lastmod>2026-06-19</lastmod></url>'
new_line = '<url><loc>https://n2n.com.ar/mvp-start/</loc><lastmod>2026-07-07</lastmod></url>'

with open('sitemap.xml', 'r', encoding='utf-8') as f:
    content = f.read()

if new_line in content:
    print("Ya estaba insertada, no se tocó nada.")
else:
    if old_line not in content:
        print("ERROR: no se encontró la línea de referencia (legal/). No se modificó el archivo.")
    else:
        content = content.replace(old_line, old_line + '\n  ' + new_line, 1)
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Insertada correctamente.")
