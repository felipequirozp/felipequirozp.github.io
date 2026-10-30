from pathlib import Path

ES_CARD='''\n<a class="card reveal" data-cat="education partnerships" href="/es/tethered/alianzas-estrategicas/"><div class="visual"><img src="/images/ech-lanzamiento.png" alt="Alianzas estratégicas de Tether Education"></div><div class="body"><div class="meta"><span>Tether Education</span><span>2025</span></div><h3>Alianzas estratégicas</h3><p>Un ecosistema de 15 alianzas en educación construido en Chile, Colombia, Perú y República Dominicana.</p><div class="impact"><span>15 alianzas</span><span>4 países</span><span>Educación</span><span>Partnerships</span></div><span class="cta">Ver proyecto ↗</span></div></a>'''

EN_CARD='''\n<a class="card reveal" data-cat="education partnerships" href="/tethered/strategic-partnerships/"><div class="visual"><img src="/images/ech-lanzamiento.png" alt="Tether Education strategic partnerships"></div><div class="body"><div class="meta"><span>Tether Education</span><span>2025</span></div><h3>Strategic Partnerships</h3><p>An education ecosystem of 15 strategic partnerships built across Chile, Colombia, Peru and the Dominican Republic.</p><div class="impact"><span>15 partnerships</span><span>4 countries</span><span>Education</span><span>Partnerships</span></div><span class="cta">View project ↗</span></div></a>'''

for rel, card, marker, filter_anchor, filter_button, card_anchor in [
    ('es/projects.html', ES_CARD, '/es/tethered/alianzas-estrategicas/', '<button class="filter" data-filter="company">Company building</button>', '<button class="filter" data-filter="partnerships">Partnerships</button>', '<a class="card reveal" data-cat="education ai" href="/es/tethered/habilidades-digitales-ia/">'),
    ('projects.html', EN_CARD, '/tethered/strategic-partnerships/', '<button class="filter" data-filter="company">Company building</button>', '<button class="filter" data-filter="partnerships">Partnerships</button>', '<a class="card reveal" data-cat="education ai" href="/tethered/digital-skills-ai-survey/">'),
]:
    p=Path(rel)
    s=p.read_text(encoding='utf-8')
    if 'data-filter="partnerships"' not in s:
        s=s.replace(filter_anchor, filter_anchor+filter_button, 1)
    if marker not in s:
        s=s.replace(card_anchor, card+'\n'+card_anchor, 1)
    p.write_text(s, encoding='utf-8')
