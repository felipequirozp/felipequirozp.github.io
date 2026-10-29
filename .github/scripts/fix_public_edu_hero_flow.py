from pathlib import Path

files = {
    Path('tethered/digital-transformation-public-education.html'): (
        'Digitizing public education operations through one connected system.'
    ),
    Path('es/tethered/transformacion-digital-educacion-publica.html'): (
        'Digitalizando la operación de la educación pública a través de un sistema conectado.'
    ),
}

old_css = '.hero h1{margin:34px 0 0;max-width:980px;font-family:Manrope,sans-serif;font-size:clamp(42px,4.25vw,62px);line-height:1.04;letter-spacing:-.052em;font-weight:500}.hero h1 span{display:block;margin-top:10px;color:#98a4af}'
new_css = '.hero h1{margin:34px 0 0;max-width:980px;font-family:Manrope,sans-serif;font-size:clamp(42px,4.25vw,62px);line-height:1.04;letter-spacing:-.052em;font-weight:500}'

for path, headline in files.items():
    s = path.read_text(encoding='utf-8')
    if old_css in s:
        s = s.replace(old_css, new_css, 1)

    start = s.find('<h1>')
    end = s.find('</h1>', start)
    if start == -1 or end == -1:
        raise SystemExit(f'Hero h1 not found in {path}')
    s = s[:start] + f'<h1>{headline}</h1>' + s[end + len('</h1>'):]
    path.write_text(s, encoding='utf-8')
