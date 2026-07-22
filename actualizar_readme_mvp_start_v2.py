old_block = """contacto/        # Contacto
mvp-start/       # Producto de entrada — diagnóstico pago (standalone, sin nav ni footer)
legal/           # Páginas legales"""

new_block = """contacto/        # Contacto
mvp-start/       # Producto de entrada — diagnóstico pago (standalone, sin nav ni footer)
descargas/       # PDFs descargables (ej: n2n-mvp-start.pdf)
legal/           # Páginas legales"""

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

if 'descargas/' in content:
    print("Ya estaba documentado, no se tocó nada.")
elif old_block not in content:
    print("ERROR: no se encontró el bloque de referencia. No se modificó el archivo.")
else:
    content = content.replace(old_block, new_block, 1)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("README.md actualizado.")
