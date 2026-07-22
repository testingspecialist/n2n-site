old_block = """casos/           # Casos de estudio
conocimiento/    # Base de conocimiento y guías
comparar/        # Comparativas de enfoque
glosario/        # Glosario de términos
contacto/        # Contacto
legal/           # Páginas legales"""

new_block = """casos/           # Casos de estudio
conocimiento/    # Base de conocimiento y guías
comparar/        # Comparativas de enfoque
glosario/        # Glosario de términos
contacto/        # Contacto
mvp-start/       # Producto de entrada — diagnóstico pago (standalone, sin nav ni footer)
legal/           # Páginas legales"""

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

if 'mvp-start/' in content:
    print("Ya estaba documentado, no se tocó nada.")
elif old_block not in content:
    print("ERROR: no se encontró el bloque de referencia. No se modificó el archivo.")
else:
    content = content.replace(old_block, new_block, 1)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("README.md actualizado.")
