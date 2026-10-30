from pathlib import Path
import re

PATHS = [Path('people.html'), Path('es/people.html')]

ORDER = [
    'Christopher Neilson','Zack Tseng','Nicolás Muñoz','Leidy Gómez','Rodrigo Lewit','Karen Radonich','Valentina Gran',
    'Tomás Recart','Tamara Muñoz','Ignacio Lepe','Valentina Wagenreld','Francisca Astudillo','Juan Yuz','Javier Robledo',
    'Damián Aldunate','Jorge Muñoz','Matías Bussinger','Lía Morice',
]

FRESH_ASSETS = {
    'Valentina Gran': '/images/vgran.png?v=20261030-0252',
    'Tamara Muñoz': '/images/tamara.png?v=20261030-0252',
}

CSS = r'''
<style id="people-face-polish-v11">
.people-all .people-grid{grid-template-columns:repeat(7,minmax(0,1fr))!important;gap:34px 16px!important}
.people-all .portrait{height:auto!important;min-height:0!important;padding:0!important;border:0!important;background:transparent!important;overflow:hidden!important}
.people-all .portrait-inner{position:relative!important;aspect-ratio:4/4.5!important;background:#f1f1f1!important;overflow:hidden!important;border-radius:14px!important}
.people-all .portrait-inner::after{display:none!important;content:none!important}
.people-all .portrait img{width:100%!important;height:100%!important;object-fit:cover!important;object-position:center 36%!important;transform-origin:center center!important;filter:grayscale(100%) contrast(.96) brightness(1.02)!important;mix-blend-mode:normal!important;clip-path:none!important}
.people-all .person{position:relative!important;min-width:0!important;transform:none!important}
.people-all .person-copy{padding-top:12px!important}
.people-all .person h3{margin:0!important;font-size:16px!important;line-height:1.08!important;letter-spacing:-.035em!important;font-weight:500!important}
.company-tag,.context,.profile-link,.role{display:none!important}.card-link{position:absolute;inset:0;z-index:4;border-radius:14px}
.people-all img[alt="Christopher Neilson"]{transform:scale(1.14) translateY(2%)!important}
.people-all img[alt="Zack Tseng"]{transform:scale(1.13) translateY(2%)!important}
.people-all img[alt="Nicolás Muñoz"]{transform:scale(1.17) translateY(2%)!important}
.people-all img[alt="Leidy Gómez"]{transform:scale(1.13) translateY(2%)!important}
.people-all img[alt="Rodrigo Lewit"]{transform:scale(1.15) translateY(2%)!important}
.people-all img[alt="Karen Radonich"]{transform:scale(1.12) translateY(2%)!important}
.people-all img[alt="Valentina Gran"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(.92) translateY(8%)!important}
.people-all img[alt="Tomás Recart"]{transform:scale(1.46) translateY(12%)!important}
.people-all img[alt="Tamara Muñoz"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(.88) translateY(9%)!important}
.people-all img[alt="Ignacio Lepe"]{transform:scale(1.10) translateY(2%)!important}
.people-all img[alt="Valentina Wagenreld"]{transform:scale(1.38) translateY(16%)!important}
.people-all img[alt="Francisca Astudillo"]{transform:scale(1.06) translateY(2%)!important}
.people-all img[alt="Juan Yuz"]{transform:scale(1.38) translateY(8%)!important}
.people-all img[alt="Javier Robledo"]{transform:scale(1.34) translateY(7%)!important}
.people-all img[alt="Damián Aldunate"]{transform:scale(1.28) translateY(6%)!important}
.people-all img[alt="Jorge Muñoz"]{transform:scale(1.28) translateY(1%)!important}
.people-all img[alt="Matías Bussinger"]{transform:scale(1.20) translateY(0)!important}
.people-all img[alt="Lía Morice"]{transform:scale(1.20) translateY(0)!important}
@media(max-width:1400px){.people-all .people-grid{grid-template-columns:repeat(6,minmax(0,1fr))!important}}
@media(max-width:1180px){.people-all .people-grid{grid-template-columns:repeat(5,minmax(0,1fr))!important}}
@media(max-width:1000px){.people-all .people-grid{grid-template-columns:repeat(4,minmax(0,1fr))!important}}
@media(max-width:820px){.people-all .people-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important}}
@media(max-width:700px){.people-all .people-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:28px 12px!important}.people-all .person h3{font-size:15px!important}}
</style>
'''

def reorder_grid(text):
    m = re.search(r'(<div class="people-grid">)(.*?)(</div></div></section>\s*<section class="closing">)', text, re.S)
    if not m:
        raise RuntimeError('people-grid not found')
    blocks = re.findall(r'<article class="person"[^>]*>.*?</article>', m.group(2), re.S)
    by_name = {}
    for block in blocks:
        nm = re.search(r'<h3>(.*?)</h3>', block, re.S)
        if nm:
            name = re.sub(r'<[^>]+>', '', nm.group(1)).strip()
            by_name[name] = block
    missing = [n for n in ORDER if n not in by_name]
    if missing:
        raise RuntimeError(f'Missing People cards: {missing}')
    ordered = ''.join(by_name[n] for n in ORDER)
    return text[:m.start()] + m.group(1) + ordered + m.group(3) + text[m.end():]

def replace_card_asset(text, name, src):
    pat = re.compile(r'(<article class="person"[^>]*>.*?<img\s+src=")([^"]+)("\s+alt="' + re.escape(name) + r'".*?</article>)', re.S)
    text, n = pat.subn(r'\1' + src + r'\3', text, count=1)
    if n != 1:
        raise RuntimeError(f'Could not update asset for {name}')
    return text

def patch(path):
    text = path.read_text(encoding='utf-8')
    text = reorder_grid(text)
    for name, src in FRESH_ASSETS.items():
        text = replace_card_asset(text, name, src)
    legacy_ids = [r'people-card-polish-v\d+',r'people-face-polish-v\d+',r'people-alignment-fix-v\d+',r'people-grid-7-v\d+']
    for style_id in legacy_ids:
        text = re.sub(rf'<style id="{style_id}">.*?</style>\s*', '', text, flags=re.S)
    text = text.replace('</head>', CSS + '</head>')
    for name in ORDER:
        count = text.count(f'<h3>{name}</h3>')
        if count != 1:
            raise RuntimeError(f'{path}: expected one {name}, found {count}')
    if '<h3>Martín Alvarado</h3>' in text:
        raise RuntimeError(f'{path}: Martín Alvarado was not removed')
    path.write_text(text, encoding='utf-8')

for path in PATHS:
    patch(path)
