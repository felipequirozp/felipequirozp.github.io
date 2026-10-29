from pathlib import Path

paths = [
    Path('tethered/tether-studio.html'),
    Path('es/tethered/tether-studio.html'),
]

old = '.media{overflow:hidden;border-radius:22px;background:#e2eaf0;min-height:360px}.media img{width:100%;height:100%;object-fit:cover}'
new = '.media{overflow:hidden;border-radius:22px;background:#e2eaf0}.media img{width:100%;height:460px;object-fit:cover;object-position:center 42%}@media(max-width:1000px){.media img{height:380px}}@media(max-width:700px){.media img{height:300px}}'

for path in paths:
    s = path.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'Expected media CSS not found in {path}')
    s = s.replace(old, new, 1)
    path.write_text(s, encoding='utf-8')
