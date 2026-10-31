from pathlib import Path
import re

CONFIG = {
    Path('projects.html'): [
        '/lowsignal/low-workspace',
        '/tethered/anotate-en-la-lista/',
        '/geovictoria/shift-change-workflow',
        '/geovictoria/shift-optimizer',
    ],
    Path('es/projects.html'): [
        '/es/lowsignal/low-workspace',
        '/es/tethered/anotate-en-la-lista/',
        '/es/geovictoria/shift-change-workflow',
        '/es/geovictoria/shift-optimizer',
    ],
}

card_re = re.compile(r'<a class="card reveal"[^>]*href="([^"]+)".*?</a>', re.S)

for path, desired in CONFIG.items():
    s = path.read_text()
    cards = list(card_re.finditer(s))
    found = {m.group(1): m.group(0) for m in cards if m.group(1) in desired}
    if any(href not in found for href in desired):
        missing = [href for href in desired if href not in found]
        raise SystemExit(f'Missing cards in {path}: {missing}')

    # Remove the target cards from their current positions.
    for href in desired:
        s = s.replace(found[href], '', 1)

    # Put them together immediately after the Tether Studio card.
    anchor_href = '/tethered/tether-studio' if path.name == 'projects.html' and str(path).startswith('projects') else '/es/tethered/tether-studio'
    m = re.search(r'<a class="card reveal"[^>]*href="' + re.escape(anchor_href) + r'".*?</a>', s, re.S)
    if not m:
        raise SystemExit(f'Anchor not found in {path}: {anchor_href}')
    block = '\n'.join(found[href] for href in desired)
    s = s[:m.end()] + '\n' + block + s[m.end():]
    path.write_text(s)
