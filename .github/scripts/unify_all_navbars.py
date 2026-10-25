from pathlib import Path
import re

ROOT = Path('.')
EXCLUDE_PARTS = {'.git', '.github'}

header_re = re.compile(r'<header class="nav">.*?</header>', re.S)
lang_re = re.compile(r'<a class="lang" href="([^"]+)"[^>]*>(EN|ES)</a>', re.S)

changed=[]
for path in ROOT.rglob('*.html'):
    if any(part in EXCLUDE_PARTS for part in path.parts):
        continue
    text = path.read_text(encoding='utf-8')
    m = header_re.search(text)
    if not m:
        continue
    old = m.group(0)
    lm = lang_re.search(old)
    if not lm:
        continue
    lang_href, lang_label = lm.group(1), lm.group(2)
    is_es = path.parts and path.parts[0] == 'es'

    if is_es:
        brand_href='/es/'
        links=[('/es/#work','Trabajo','work'),('/es/about','Sobre mí','about'),('/es/now','Ahora','now'),('/es/blog','Blog','blog')]
        aria='Principal'
        lang_aria='Cambiar idioma'
    else:
        brand_href='/'
        links=[('/#work','Work','work'),('/about','About','about'),('/now','Now','now'),('/blog','Blog','blog')]
        aria='Primary'
        lang_aria='Switch language'

    p = path.as_posix()
    active=None
    if p.endswith('about.html'): active='about'
    elif p.endswith('now.html'): active='now'
    elif p.endswith('blog.html') or '/blog/' in p: active='blog'
    elif p.endswith('index.html') or any(x in p for x in ['lowsignal','geovictoria','tether','usm']): active='work'

    nav_links=''.join(f'<a href="{href}"'+(' class="active"' if key==active else '')+f'>{label}</a>' for href,label,key in links)
    new=(f'<header class="nav">'
         f'<a class="brand" href="{brand_href}">Felipe Quiroz</a>'
         f'<div class="nav-right">'
         f'<nav class="nav-center" aria-label="{aria}">{nav_links}</nav>'
         f'<a class="lang" href="{lang_href}" aria-label="{lang_aria}">{lang_label}</a>'
         f'</div></header>')

    if old != new:
        text=text[:m.start()]+new+text[m.end():]
        path.write_text(text,encoding='utf-8')
        changed.append(p)

print(f'Updated {len(changed)} navbar(s)')
for p in changed:
    print(p)
