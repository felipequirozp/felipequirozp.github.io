from pathlib import Path

paths = [
    Path('geovictoria/shift-optimizer.html'),
    Path('es/geovictoria/shift-optimizer.html'),
    Path('geovictoria/shift-change-workflow.html'),
    Path('es/geovictoria/shift-change-workflow.html'),
]

kicker_css = '.kicker{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}'
logo_css = '.hero-logo{display:inline-flex;align-items:center;justify-content:flex-start;margin-bottom:28px}.hero-logo img{height:38px;width:auto;max-width:260px;object-fit:contain;object-position:left center}'
needle = '<div><div class="kicker">GeoVictoria · B2B SaaS · Workforce Management</div>'
replacement = '<div><a class="hero-logo" href="https://www.geovictoria.com" target="_blank" rel="noopener noreferrer" aria-label="GeoVictoria"><img src="/logos/logo-geovictoria.png" alt="GeoVictoria"></a><div class="kicker">GeoVictoria · B2B SaaS · Workforce Management</div>'

for path in paths:
    text = path.read_text(encoding='utf-8')
    if 'class="hero-logo"' not in text:
        if kicker_css not in text:
            raise SystemExit(f'kicker css not found in {path}')
        text = text.replace(kicker_css, kicker_css + logo_css, 1)
        if needle not in text:
            raise SystemExit(f'hero marker not found in {path}')
        text = text.replace(needle, replacement, 1)
        path.write_text(text, encoding='utf-8')
        print('updated', path)
    else:
        print('already updated', path)
