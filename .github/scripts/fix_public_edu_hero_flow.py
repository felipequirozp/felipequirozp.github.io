from pathlib import Path

paths = [
    Path('tethered/digital-transformation-public-education.html'),
    Path('es/tethered/transformacion-digital-educacion-publica.html'),
]

old = '.hero h1{margin:32px 0 0;max-width:1020px;font-family:Manrope,sans-serif;font-size:clamp(44px,5vw,68px);line-height:1.01;letter-spacing:-.056em;font-weight:500}.hero h1 span{display:block;color:#98a4af}'
new = '.hero h1{margin:32px 0 0;max-width:1280px;font-family:Manrope,sans-serif;font-size:clamp(44px,4.7vw,66px);line-height:1.01;letter-spacing:-.056em;font-weight:500}.hero h1 span{display:inline;color:#98a4af}'

for path in paths:
    s = path.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'Expected hero CSS not found in {path}')
    s = s.replace(old, new, 1)
    path.write_text(s, encoding='utf-8')
