from pathlib import Path

replacements = {
    Path('tethereducation.html'): (
        '<h1>Building digital infrastructure for education.<span>Across markets, partners and products.</span></h1>',
        '<h1>Building digital infrastructure for education across markets and products.</h1>',
    ),
    Path('es/tethereducation.html'): (
        '<h1>Construyendo infraestructura digital para educación.<span>Entre mercados, partners y productos.</span></h1>',
        '<h1>Construyendo infraestructura digital para educación entre mercados y productos.</h1>',
    ),
}

old_css = '.hero h1{margin:34px 0 0;max-width:980px;font-family:Manrope,sans-serif;font-size:clamp(46px,5vw,70px);line-height:1.01;letter-spacing:-.056em;font-weight:500}.hero h1 span{display:block;color:#98a4af}'
new_css = '.hero h1{margin:34px 0 0;max-width:980px;font-family:Manrope,sans-serif;font-size:clamp(44px,4.6vw,66px);line-height:1.04;letter-spacing:-.052em;font-weight:500}'

for path, (old_h1, new_h1) in replacements.items():
    s = path.read_text(encoding='utf-8')
    if old_h1 not in s:
        raise SystemExit(f'Expected headline not found in {path}')
    if old_css not in s:
        raise SystemExit(f'Expected hero CSS not found in {path}')
    s = s.replace(old_h1, new_h1, 1)
    s = s.replace(old_css, new_css, 1)
    path.write_text(s, encoding='utf-8')
