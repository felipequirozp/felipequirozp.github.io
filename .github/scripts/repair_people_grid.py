from pathlib import Path
import re

GOOD_COMMIT = '00adf6e6692b9970dae01244c1190460ff3feed6'

NEW = {
    'Valentina Gran': ('/images/people/valentina-gran.png?v=20261029-2215','https://www.linkedin.com/in/valentina-gran-koch-0b945325/'),
    'Tomás Recart': ('/images/people/tomas-recart.png?v=20261029-2215','https://www.linkedin.com/in/tomas-recart-balze-a9957918a/'),
    'Tamara Muñoz': ('/images/people/tamara-munoz.png?v=20261029-2215','https://www.linkedin.com/in/tamara-munoz-ojeda/'),
    'Ignacio Lepe': ('/images/people/ignacio-lepe.png?v=20261029-2215','https://www.linkedin.com/in/ignacio-lepe-6026b4215/'),
}

CSS = '''
<style id="people-alignment-fix-v1">
/* stable portrait alignment: do not move people by grid position */
.people-all .portrait-inner{position:relative;aspect-ratio:4/4.5!important;overflow:hidden;border-radius:14px!important;background:#f1f1f1!important}
.people-all .portrait img{width:100%!important;height:100%!important;object-fit:cover!important;object-position:center bottom!important;filter:grayscale(100%) contrast(.96) brightness(1.02)!important;mix-blend-mode:normal!important;transform:none!important}
.people-all .person:nth-child(n) .portrait img{transform:none!important}
.people-all .person:nth-child(n) .portrait-inner::after{display:none!important}
</style>
'''

def card(name, image, link):
    return (f'<article class="person"><a class="card-link" href="{link}" target="_blank" rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a>'
            f'<div class="portrait"><div class="portrait-inner"><img src="{image}" alt="{name}" loading="lazy"></div></div>'
            f'<div class="person-copy"><h3>{name}</h3></div></article>')

def patch(path):
    text = path.read_text(encoding='utf-8')
    for name,(image,link) in NEW.items():
        # replace only the single article that contains this exact h3; never cross </article>
        pat = re.compile(r'<article class="person">(?:(?!</article>).)*?<h3>'+re.escape(name)+r'</h3>(?:(?!</article>).)*?</article>', re.S)
        text,n = pat.subn(card(name,image,link), text, count=1)
        if n != 1:
            raise RuntimeError(f'Missing card {name} in {path}')
    text = re.sub(r'<style id="people-alignment-fix-v\d+">.*?</style>\s*','',text,flags=re.S)
    text = text.replace('</head>', CSS + '</head>')
    # hard safety check: all 19 expected names must exist exactly once
    expected = ['Christopher Neilson','Zack Tseng','Nicolás Muñoz','Leidy Gómez','Rodrigo Lewit','Karen Radonich','Valentina Gran','Tomás Recart','Tamara Muñoz','Ignacio Lepe','Damián Aldunate','Matías Bussinger','Lía Morice','Martín Alvarado','Jorge Muñoz','Francisca Astudillo','Juan Yuz','Javier Robledo','Valentina Wagenreld']
    for name in expected:
        c = text.count(f'<h3>{name}</h3>')
        if c != 1:
            raise RuntimeError(f'{path}: expected exactly one {name}, found {c}')
    path.write_text(text,encoding='utf-8')

for p in [Path('people.html'), Path('es/people.html')]:
    patch(p)
