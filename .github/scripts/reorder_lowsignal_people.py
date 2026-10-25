from pathlib import Path
import re

paths = [Path('lowsignal.html'), Path('es/lowsignal.html')]
order = ['Matías Bussinger', 'Lía Morice', 'Jorge Muñoz', 'Martín Alvarado']

for path in paths:
    text = path.read_text(encoding='utf-8')
    m = re.search(r'(<div class="people-grid">)(.*?)(\n\s*</div>)', text, re.S)
    if not m:
        raise SystemExit(f'people-grid not found in {path}')
    body = m.group(2)
    articles = re.findall(r'\n\s*<article class="person">.*?</article>', body, re.S)
    by_name = {}
    for article in articles:
        for name in order + ['Marco Kroeger']:
            if name in article:
                by_name[name] = article
                break
    missing = [n for n in order if n not in by_name]
    if missing:
        raise SystemExit(f'Missing people in {path}: {missing}')
    new_body = ''.join(by_name[name] for name in order) + '\n        '
    new_block = m.group(1) + new_body + m.group(3)
    text = text[:m.start()] + new_block + text[m.end():]
    path.write_text(text, encoding='utf-8')
