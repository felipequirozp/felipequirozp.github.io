from pathlib import Path
import re

PATHS = [Path('people.html'), Path('es/people.html')]

ORDER = [
    'Christopher Neilson','Zack Tseng','Nicolás Muñoz','Leidy Gómez','Rodrigo Lewit','Karen Radonich','Valentina Gran',
    'Tomás Recart','Tamara Muñoz','Ignacio Lepe','Valentina Wagenreld','Francisca Astudillo','Juan Yuz','Javier Robledo',
    'Damián Aldunate','Jorge Muñoz','Matías Bussinger','Lía Morice','Martín Alvarado',
]

CSS = r'''
<style id="people-face-polish-v2">
/* Final People grid: 7-up desktop and consistent head-and-shoulders composition. */
.people-all .people-grid{grid-template-columns:repeat(7,minmax(0,1fr))!important;gap:34px 16px!important}
.people-all .portrait-inner{aspect-ratio:4/4.5!important;background:#f1f1f1!important;overflow:hidden!important;border-radius:14px!important}
.people-all .portrait img{
  width:100%!important;height:100%!important;object-fit:cover!important;
  object-position:center 38%!important;transform-origin:center center!important;
  filter:grayscale(100%) contrast(.96) brightness(1.02)!important;mix-blend-mode:normal!important;
}
.people-all .person h3{font-size:16px!important;line-height:1.08!important}

/* Row 1 — keep faces on the same visual eye line */
.people-all img[alt="Christopher Neilson"]{transform:scale(1.13) translateY(1%)!important;object-position:center 34%!important}
.people-all img[alt="Zack Tseng"]{transform:scale(1.10) translateY(1%)!important;object-position:center 36%!important}
.people-all img[alt="Nicolás Muñoz"]{transform:scale(1.16) translateY(2%)!important;object-position:center 36%!important}
.people-all img[alt="Leidy Gómez"]{transform:scale(1.10) translateY(1%)!important;object-position:center 35%!important}
.people-all img[alt="Rodrigo Lewit"]{transform:scale(1.14) translateY(2%)!important;object-position:center 36%!important}
.people-all img[alt="Karen Radonich"]{transform:scale(1.10) translateY(1%)!important;object-position:center 35%!important}
.people-all img[alt="Valentina Gran"]{transform:scale(1.02) translateY(1%)!important;object-position:center 35%!important}

/* Row 2 — crop excess torso and equalize head size */
.people-all img[alt="Tomás Recart"]{transform:scale(1.34) translateY(6%)!important;object-position:center 34%!important}
.people-all img[alt="Tamara Muñoz"]{transform:scale(.88) translateY(-1%)!important;object-position:center 35%!important}
.people-all img[alt="Ignacio Lepe"]{transform:scale(1.08) translateY(2%)!important;object-position:center 35%!important}
.people-all img[alt="Valentina Wagenreld"]{transform:scale(1.28) translateY(6%)!important;object-position:center 35%!important}
.people-all img[alt="Francisca Astudillo"]{transform:scale(1.02) translateY(1%)!important;object-position:center 35%!important}
.people-all img[alt="Juan Yuz"]{transform:scale(1.31) translateY(6%)!important;object-position:center 34%!important}
.people-all img[alt="Javier Robledo"]{transform:scale(1.27) translateY(5%)!important;object-position:center 35%!important}

/* Row 3 — same portrait depth, no floating/full-body feel */
.people-all img[alt="Damián Aldunate"]{transform:scale(1.22) translateY(4%)!important;object-position:center 35%!important}
.people-all img[alt="Jorge Muñoz"]{transform:scale(1.23) translateY(4%)!important;object-position:center 35%!important}
.people-all img[alt="Matías Bussinger"]{transform:scale(1.13) translateY(2%)!important;object-position:center 35%!important}
.people-all img[alt="Lía Morice"]{transform:scale(1.14) translateY(3%)!important;object-position:center 35%!important}
.people-all img[alt="Martín Alvarado"]{transform:scale(1.20) translateY(4%)!important;object-position:center 35%!important}

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


def patch(path):
    text = path.read_text(encoding='utf-8')
    text = reorder_grid(text)
    text = re.sub(r'<style id="people-face-polish-v\d+">.*?</style>\s*', '', text, flags=re.S)
    text = text.replace('</head>', CSS + '</head>')
    for name in ORDER:
        count = text.count(f'<h3>{name}</h3>')
        if count != 1:
            raise RuntimeError(f'{path}: expected one {name}, found {count}')
    path.write_text(text, encoding='utf-8')

for path in PATHS:
    patch(path)
