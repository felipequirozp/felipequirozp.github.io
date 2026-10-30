from pathlib import Path
import re

FILES = [Path('people.html'), Path('es/people.html')]

ORDER = [
    'Christopher Neilson',
    'Zack Tseng',
    'Nicolás Muñoz',
    'Leidy Gómez',
    'Rodrigo Lewit',
    'Karen Radonich',
    'Valentina Gran',
    'Tomás Recart',
    'Tamara Muñoz',
    'Ignacio Lepe',
    'Valentina Wagenreld',
    'Francisca Astudillo',
    'Juan Yuz',
    'Javier Robledo',
    'Damián Aldunate',
    'Jorge Muñoz',
    'Matías Bussinger',
    'Lía Morice',
    'Martín Alvarado',
]

CSS = '''\n<style id="people-grid-7-v1">\n.people-all .people-grid{grid-template-columns:repeat(7,minmax(0,1fr))!important;gap:34px 14px!important}\n@media(max-width:1450px){.people-all .people-grid{grid-template-columns:repeat(6,minmax(0,1fr))!important}}\n@media(max-width:1220px){.people-all .people-grid{grid-template-columns:repeat(5,minmax(0,1fr))!important}}\n@media(max-width:1050px){.people-all .people-grid{grid-template-columns:repeat(4,minmax(0,1fr))!important}}\n@media(max-width:900px){.people-all .people-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important}}\n@media(max-width:700px){.people-all .people-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:28px 12px!important}}\n</style>\n'''

CARD_RE = re.compile(r'<article class="person">(?:(?!</article>).)*?</article>', re.S)
NAME_RE = re.compile(r'<h3>(.*?)</h3>', re.S)

for path in FILES:
    text = path.read_text(encoding='utf-8')
    grid_start = text.find('<div class="people-grid">')
    if grid_start == -1:
        raise RuntimeError(f'{path}: people-grid not found')
    grid_content_start = grid_start + len('<div class="people-grid">')

    cards = []
    pos = grid_content_start
    while True:
        m = CARD_RE.match(text, pos)
        if not m:
            break
        card = m.group(0)
        nm = NAME_RE.search(card)
        if not nm:
            raise RuntimeError(f'{path}: card without h3')
        cards.append((nm.group(1), card))
        pos = m.end()

    if len(cards) != 19:
        raise RuntimeError(f'{path}: expected 19 cards, found {len(cards)}')

    by_name = {name: card for name, card in cards}
    if set(by_name) != set(ORDER):
        missing = set(ORDER) - set(by_name)
        extra = set(by_name) - set(ORDER)
        raise RuntimeError(f'{path}: mismatch missing={missing} extra={extra}')

    new_cards = ''.join(by_name[name] for name in ORDER)
    text = text[:grid_content_start] + new_cards + text[pos:]

    text = re.sub(r'\n?<style id="people-grid-7-v\d+">.*?</style>\n?', '\n', text, flags=re.S)
    text = text.replace('</head>', CSS + '</head>')

    for name in ORDER:
        if text.count(f'<h3>{name}</h3>') != 1:
            raise RuntimeError(f'{path}: invalid count for {name}')

    path.write_text(text, encoding='utf-8')
