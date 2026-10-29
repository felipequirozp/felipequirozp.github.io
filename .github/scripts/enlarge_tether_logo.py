from pathlib import Path

# Keep Tether hero logo visually balanced with the hero metadata.
for path in [Path('tethereducation.html'), Path('es/tethereducation.html')]:
    s = path.read_text(encoding='utf-8')
    s = s.replace('.hero-logo img{height:34px;width:auto;max-width:250px;object-fit:contain}', '.hero-logo img{height:44px;width:auto;max-width:300px;object-fit:contain}')
    path.write_text(s, encoding='utf-8')
