from pathlib import Path
import re

configs = {
    Path('index.html'): '''<header class="nav"><a class="brand" href="/">Felipe Quiroz</a><div class="nav-right"><nav class="nav-center" aria-label="Primary"><a href="#work">Work</a><a href="/about">About</a><a href="/now">Now</a><a href="/blog">Blog</a></nav><a class="lang" href="/es/" aria-label="Switch language">ES</a></div></header>''',
    Path('es/index.html'): '''<header class="nav"><a class="brand" href="/es/">Felipe Quiroz</a><div class="nav-right"><nav class="nav-center" aria-label="Principal"><a href="#work">Trabajo</a><a href="/es/about">Sobre mí</a><a href="/es/now">Ahora</a><a href="/es/blog">Blog</a></nav><a class="lang" href="/" aria-label="Cambiar idioma">EN</a></div></header>'''
}

for path, replacement in configs.items():
    text = path.read_text(encoding='utf-8')
    new_text, count = re.subn(r'<header class="nav">.*?</header>', replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f'Expected exactly one nav header in {path}, found {count}')
    path.write_text(new_text, encoding='utf-8')
