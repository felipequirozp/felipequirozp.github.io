from pathlib import Path
import re

NEW = {
    'Valentina Gran': ('/images/people/valentina-gran.png?v=20261029-2220','https://www.linkedin.com/in/valentina-gran-koch-0b945325/'),
    'Tomás Recart': ('/images/people/tomas-recart.png?v=20261029-2220','https://www.linkedin.com/in/tomas-recart-balze-a9957918a/'),
    'Tamara Muñoz': ('/images/people/tamara-munoz.png?v=20261029-2220','https://www.linkedin.com/in/tamara-munoz-ojeda/'),
    'Ignacio Lepe': ('/images/people/ignacio-lepe.png?v=20261029-2220','https://www.linkedin.com/in/ignacio-lepe-6026b4215/'),
}

CSS = '''
<style id="people-alignment-fix-v2">
/* Stable portrait alignment: never depend on grid position. */
.people-all .portrait-inner{position:relative;aspect-ratio:4/4.5!important;overflow:hidden;border-radius:14px!important;background:#f1f1f1!important}
.people-all .portrait img{width:100%!important;height:100%!important;object-fit:cover!important;object-position:center bottom!important;filter:grayscale(100%) contrast(.96) brightness(1.02)!important;mix-blend-mode:normal!important;transform:none!important}
.people-all .person:nth-child(n) .portrait img{transform:none!important}
.people-all .person:nth-child(n) .portrait-inner::after{display:none!important}
/* New transparent cutouts: show the whole subject on the shared gray card background. */
.people-all img[src*="valentina-gran.png"],
.people-all img[src*="tomas-recart.png"],
.people-all img[src*="tamara-munoz.png"],
.people-all img[src*="ignacio-lepe.png"]{object-fit:contain!important;object-position:center bottom!important}
/* Visually normalize the third row's subject heights. */
.people-all img[alt="Lía Morice"]{transform:scale(1.10)!important;transform-origin:center bottom!important}
.people-all img[alt="Martín Alvarado"]{transform:scale(1.12)!important;transform-origin:center bottom!important}
.people-all img[alt="Jorge Muñoz"]{transform:scale(1.10)!important;transform-origin:center bottom!important}
.people-all img[alt="Francisca Astudillo"]{transform:scale(1.04)!important;transform-origin:center bottom!important}
.people-all img[alt="Juan Yuz"]{transform:scale(1.10)!important;transform-origin:center bottom!important}
.people-all img[alt="Javier Robledo"]{transform:scale(1.08)!important;transform-origin:center bottom!important}
</style>
'''

def card(name, image, link):
    return (f'<article class="person"><a class="card-link" href="{link}" target="_blank" rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a>'
            f'<div class="portrait"><div class="portrait-inner"><img src="{image}" alt="{name}" loading="lazy"></div></div>'
            f'<div class="person-copy"><h3>{name}</h3></div></article>')

def extract_card(text, name):
    pat = re.compile(r'<article class="person">(?:(?!</article>).)*?<h3>'+re.escape(name)+r'</h3>(?:(?!</article>).)*?</article>', re.S)
    m = pat.search(text)
    if not m:
        raise RuntimeError(f'Missing card {name}')
    return m.group(0), m.start(), m.end()

def patch(path):
    text = path.read_text(encoding='utf-8')

    for name,(image,link) in NEW.items():
        old, start, end = extract_card(text, name)
        text = text[:start] + card(name,image,link) + text[end:]

    # Place Valentina Wagenreld immediately after Ignacio Lepe.
    wagen, ws, we = extract_card(text, 'Valentina Wagenreld')
    text = text[:ws] + text[we:]
    ignacio, _, ie = extract_card(text, 'Ignacio Lepe')
    text = text[:ie] + wagen + text[ie:]

    text = re.sub(r'<style id="people-alignment-fix-v\d+">.*?</style>\s*','',text,flags=re.S)
    text = text.replace('</head>', CSS + '</head>')

    expected = ['Christopher Neilson','Zack Tseng','Nicolás Muñoz','Leidy Gómez','Rodrigo Lewit','Karen Radonich','Valentina Gran','Tomás Recart','Tamara Muñoz','Ignacio Lepe','Valentina Wagenreld','Damián Aldunate','Matías Bussinger','Lía Morice','Martín Alvarado','Jorge Muñoz','Francisca Astudillo','Juan Yuz','Javier Robledo']
    for name in expected:
        c = text.count(f'<h3>{name}</h3>')
        if c != 1:
            raise RuntimeError(f'{path}: expected exactly one {name}, found {c}')

    # Verify the requested adjacency.
    order = [m.group(1) for m in re.finditer(r'<h3>([^<]+)</h3>', text)]
    if order.index('Valentina Wagenreld') != order.index('Ignacio Lepe') + 1:
        raise RuntimeError(f'{path}: Valentina Wagenreld is not immediately after Ignacio Lepe')

    path.write_text(text,encoding='utf-8')

for p in [Path('people.html'), Path('es/people.html')]:
    patch(p)
