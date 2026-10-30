from pathlib import Path

EN_PATH = Path('projects.html')
ES_PATH = Path('es/projects.html')

EN_CARD = '''\n<a class="card reveal" data-cat="education product" href="/tethered/anotate-en-la-lista/"><div class="visual"><img src="/images/tether-edtech-scale.jpg" alt="Anótate en la Lista · Tether Education"></div><div class="body"><div class="meta"><span>Tether Education</span><span>2024</span></div><h3>Anótate en la Lista</h3><p>Chile's school regularization process moved from physical queues to a national digital registry for families seeking available seats.</p><div class="impact"><span>National</span><span>GovTech</span><span>Public education</span><span>Admissions</span></div><span class="cta">View project ↗</span></div></a>'''

ES_CARD = '''\n<a class="card reveal" data-cat="education product" href="/es/tethered/anotate-en-la-lista/"><div class="visual"><img src="/images/tether-edtech-scale.jpg" alt="Anótate en la Lista · Tether Education"></div><div class="body"><div class="meta"><span>Tether Education</span><span>2024</span></div><h3>Anótate en la Lista</h3><p>La regularización escolar pasó de filas presenciales a un registro digital nacional para familias que buscaban vacantes disponibles.</p><div class="impact"><span>Nacional</span><span>GovTech</span><span>Educación pública</span><span>Admisión</span></div><span class="cta">Ver proyecto ↗</span></div></a>'''

EN_ANCHOR = '<a class="card reveal" data-cat="education partnerships" href="/tethered/strategic-partnerships/">'
ES_ANCHOR = '<a class="card reveal" data-cat="education partnerships" href="/es/tethered/alianzas-estrategicas/">'

def patch(path, card, anchor, href):
    text = path.read_text()
    if href in text:
        print(f'{path}: already present')
        return
    if anchor not in text:
        raise SystemExit(f'Anchor not found in {path}')
    text = text.replace(anchor, card + '\n' + anchor, 1)
    path.write_text(text)
    print(f'{path}: added')

patch(EN_PATH, EN_CARD, EN_ANCHOR, 'href="/tethered/anotate-en-la-lista/"')
patch(ES_PATH, ES_CARD, ES_ANCHOR, 'href="/es/tethered/anotate-en-la-lista/"')
