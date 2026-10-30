from pathlib import Path
import re

files = [Path('projects.html'), Path('es/projects.html')]

for path in files:
    html = path.read_text(encoding='utf-8')

    # Target only the Anotate / School Waitlist Registry card.
    pattern = re.compile(r'(<a class="card reveal"[^>]*href="(?:/es)?/tethered/anotate-en-la-lista/".*?</a>)', re.S)
    match = pattern.search(html)
    if not match:
        raise SystemExit(f'Anotate card not found in {path}')

    card = match.group(1)
    card = card.replace('/images/tether-edtech-scale.jpg', '/images/registro-publico.png')

    if path.name == 'projects.html':
        card = card.replace('<h3>Anótate en la Lista</h3>', '<h3>School Waitlist Registry</h3>')
        card = card.replace('alt="Anótate en la Lista · Tether Education"', 'alt="School Waitlist Registry · Tether Education"')
    else:
        card = card.replace('alt="Anótate en la Lista · Tether Education"', 'alt="Anótate en la Lista · Tether Education"')

    html = html[:match.start()] + card + html[match.end():]
    path.write_text(html, encoding='utf-8')
