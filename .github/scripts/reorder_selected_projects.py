from pathlib import Path
import re

CONFIG = {
    Path('projects.html'): {
        'low': '/lowsignal/low-workspace',
        'rest': [
            '/tethered/anotate-en-la-lista/',
            '/geovictoria/shift-change-workflow',
            '/geovictoria/shift-optimizer',
        ],
        'studio': '/tethered/tether-studio',
    },
    Path('es/projects.html'): {
        'low': '/es/lowsignal/low-workspace',
        'rest': [
            '/es/tethered/anotate-en-la-lista/',
            '/es/geovictoria/shift-change-workflow',
            '/es/geovictoria/shift-optimizer',
        ],
        'studio': '/es/tethered/tether-studio',
    },
}

card_re = re.compile(r'<a class="card reveal"[^>]*href="([^"]+)".*?</a>', re.S)

for path, cfg in CONFIG.items():
    s = path.read_text()
    cards = list(card_re.finditer(s))
    wanted = [cfg['low'], *cfg['rest']]
    found = {m.group(1): m.group(0) for m in cards if m.group(1) in wanted}
    missing = [href for href in wanted if href not in found]
    if missing:
        raise SystemExit(f'Missing cards in {path}: {missing}')

    # Remove cards we are repositioning.
    for href in wanted:
        s = s.replace(found[href], '', 1)

    # Low Workspace becomes the very first project card.
    grid_marker = '<div class="projects-grid">'
    grid_pos = s.find(grid_marker)
    if grid_pos == -1:
        raise SystemExit(f'Projects grid not found in {path}')
    insert_at = grid_pos + len(grid_marker)
    s = s[:insert_at] + '\n' + found[cfg['low']] + s[insert_at:]

    # Keep Waitlist + GeoVictoria grouped immediately after Tether Studio.
    studio = re.search(r'<a class="card reveal"[^>]*href="' + re.escape(cfg['studio']) + r'".*?</a>', s, re.S)
    if not studio:
        raise SystemExit(f'Tether Studio anchor not found in {path}')
    block = '\n'.join(found[href] for href in cfg['rest'])
    s = s[:studio.end()] + '\n' + block + s[studio.end():]

    path.write_text(s)
