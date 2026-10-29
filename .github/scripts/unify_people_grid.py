from pathlib import Path
import re

LINKEDIN_ICON = '''<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.94 8.5H3.56V19h3.38V8.5ZM5.25 3A1.96 1.96 0 1 0 5.25 6.92 1.96 1.96 0 0 0 5.25 3ZM19.5 13.01c0-3.18-1.7-4.66-3.97-4.66-1.83 0-2.65 1.01-3.11 1.72V8.5H9.04V19h3.38v-5.2c0-1.37.26-2.69 1.95-2.69 1.67 0 1.69 1.56 1.69 2.78V19h3.38l.06-5.99Z"/></svg>'''

def card(name, image, role, context, company, linkedin=None, loading=False):
    link = ''
    if linkedin:
        link = f'<a class="profile-link" href="{linkedin}" target="_blank" rel="noopener noreferrer" aria-label="{name} on LinkedIn">{LINKEDIN_ICON}<span>LinkedIn</span></a>'
    lazy = ' loading="lazy"' if loading else ''
    return f'''<article class="person"><div class="portrait"><img src="{image}" alt="{name}"{lazy}></div><div class="person-copy"><div class="company-tag">{company}</div><h3>{name}</h3><div class="role">{role}</div><div class="context">{context}</div>{link}</div></article>'''

people_en = [
    card('Christopher Neilson','/images/christopher-neilson.jpg','Founder & CEO · Tether Education<br>Professor of Economics & Global Affairs at Yale','Worked together across company strategy, partnerships and market expansion.','Tether Education','https://www.linkedin.com/in/christopher-a-neilson/'),
    card('Zack Tseng','/images/zack-tseng.jpg','Chief of Staff · Tether Education','Worked together across partnerships, operations and execution.','Tether Education'),
    card('Nicolás Muñoz','https://lowsignal.cl/assets/nicolas-munoz.jpg','Legal Representative · Tether Education','Worked together on local institutional and operational execution.','Tether Education',loading=True),
    card('Damián Aldunate','/images/team_damian-1.png','Co-Founder & CMO · lowsignal','Building lowsignal across brand, growth and company strategy.','lowsignal','https://www.linkedin.com/in/damianaldunate'),
    card('Matías Bussinger','/images/team-matias.png','AI Engineer · lowsignal','Working across AI, automation and internal technology initiatives.','lowsignal','https://www.linkedin.com/in/matias-bussinger-3872b4380/'),
    card('Lía Morice','/images/team_lia-1.png','Content Creator · lowsignal','Working across content, community and client execution.','lowsignal','https://www.linkedin.com/in/l%C3%ADa-morice-b31521419'),
    card('Martín Alvarado','/images/team_martin-1.png','Audiovisual Producer · lowsignal','Building audiovisual systems and client-facing creative work.','lowsignal','https://www.linkedin.com/in/martin-alvaradod'),
    card('Jorge Muñoz','/images/team_jorge-1.png','Audiovisual Editor · lowsignal','Working across post-production and audiovisual delivery.','lowsignal','https://www.linkedin.com/in/jorgemunozve'),
    card('Francisca Astudillo','/images/francisca-astudillo.jpg','CEO · GeoVictoria','Worked within the leadership environment shaping product and company execution.','GeoVictoria'),
    card('Rodrigo Lewit','/images/rodrigo-lewit.jpg','Co-Founder & Chief Commercial Officer · GeoVictoria','Worked together at the intersection of product, commercial priorities and customer needs.','GeoVictoria','https://www.linkedin.com/in/rodrigo-lewit-rozenfeld-05190118/'),
    card('Juan Yuz','/images/yuz-rector.png','Rector · Universidad Técnica Federico Santa María','Worked within the university leadership environment across academic and institutional initiatives.','USM'),
    card('Karen Radonich','/images/karen-radonich.jpg','Directora General de Admisión','Worked together across admissions strategy, coordination and student-facing initiatives.','USM'),
    card('Javier Robledo','/images/javier-robledo.jpg','Programming Coordinator','Worked together across programming, data and academic coordination.','USM'),
]

people_es = [
    card('Christopher Neilson','/images/christopher-neilson.jpg','Founder & CEO · Tether Education<br>Professor of Economics & Global Affairs at Yale','Trabajamos juntos en estrategia de compañía, partnerships y expansión de mercado.','Tether Education','https://www.linkedin.com/in/christopher-a-neilson/'),
    card('Zack Tseng','/images/zack-tseng.jpg','Chief of Staff · Tether Education','Trabajamos juntos en partnerships, operaciones y ejecución.','Tether Education'),
    card('Nicolás Muñoz','https://lowsignal.cl/assets/nicolas-munoz.jpg','Representante Legal · Tether Education','Trabajamos juntos en ejecución institucional y operativa local.','Tether Education',loading=True),
    card('Damián Aldunate','/images/team_damian-1.png','Co-Founder & CMO · lowsignal','Construyendo lowsignal entre marca, growth y estrategia de compañía.','lowsignal','https://www.linkedin.com/in/damianaldunate'),
    card('Matías Bussinger','/images/team-matias.png','AI Engineer · lowsignal','Trabajando en IA, automatización e iniciativas tecnológicas internas.','lowsignal','https://www.linkedin.com/in/matias-bussinger-3872b4380/'),
    card('Lía Morice','/images/team_lia-1.png','Content Creator · lowsignal','Trabajando en contenido, comunidad y ejecución con clientes.','lowsignal','https://www.linkedin.com/in/l%C3%ADa-morice-b31521419'),
    card('Martín Alvarado','/images/team_martin-1.png','Audiovisual Producer · lowsignal','Construyendo sistemas audiovisuales y trabajo creativo para clientes.','lowsignal','https://www.linkedin.com/in/martin-alvaradod'),
    card('Jorge Muñoz','/images/team_jorge-1.png','Audiovisual Editor · lowsignal','Trabajando en postproducción y delivery audiovisual.','lowsignal','https://www.linkedin.com/in/jorgemunozve'),
    card('Francisca Astudillo','/images/francisca-astudillo.jpg','CEO · GeoVictoria','Trabajé dentro del entorno de liderazgo que conectaba producto y ejecución de compañía.','GeoVictoria'),
    card('Rodrigo Lewit','/images/rodrigo-lewit.jpg','Co-Founder & Chief Commercial Officer · GeoVictoria','Trabajamos en la intersección entre producto, prioridades comerciales y necesidades de clientes.','GeoVictoria','https://www.linkedin.com/in/rodrigo-lewit-rozenfeld-05190118/'),
    card('Juan Yuz','/images/yuz-rector.png','Rector · Universidad Técnica Federico Santa María','Trabajé dentro del entorno de liderazgo universitario en iniciativas académicas e institucionales.','USM'),
    card('Karen Radonich','/images/karen-radonich.jpg','Directora General de Admisión','Trabajamos juntos en estrategia de admisión, coordinación e iniciativas orientadas a estudiantes.','USM'),
    card('Javier Robledo','/images/javier-robledo.jpg','Coordinador de Programación','Trabajamos juntos en programación, datos y coordinación académica.','USM'),
]

sections = {
    Path('people.html'): '<section class="people-all"><div class="shell"><div class="people-head"><div class="kicker">Tether · lowsignal · GeoVictoria · USM</div><h2>Built with people across companies, products and institutions.</h2></div><div class="people-grid">' + ''.join(people_en) + '</div></div></section>',
    Path('es/people.html'): '<section class="people-all"><div class="shell"><div class="people-head"><div class="kicker">Tether · lowsignal · GeoVictoria · USM</div><h2>Construido con personas de distintas compañías, productos e instituciones.</h2></div><div class="people-grid">' + ''.join(people_es) + '</div></div></section>',
}

css = '''\n<style id="people-unified-v2">\n.people-all{padding:82px var(--page);background:linear-gradient(180deg,#fff 0%,#f5f8fa 100%);border-bottom:1px solid var(--line)}\n.people-head{margin-bottom:34px}.people-head h2{margin:12px 0 0;max-width:840px;font-family:Manrope,sans-serif;font-size:clamp(32px,3.3vw,46px);line-height:1.06;letter-spacing:-.045em;font-weight:500}\n.people-all .people-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:24px 18px}\n.company-tag{margin-bottom:10px;color:var(--blue);font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}\n.profile-link{margin-top:14px;display:inline-flex;align-items:center;gap:7px;color:#52606d;font-size:10px;font-weight:700;transition:color .18s,transform .18s}.profile-link svg{width:14px;height:14px;flex:0 0 auto}.profile-link:hover{color:var(--blue);transform:translateY(-1px)}\n.person{transition:transform .2s}.person:hover{transform:translateY(-2px)}\n@media(max-width:1000px){.people-all .people-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}\n@media(max-width:700px){.people-all{padding:62px var(--page)}.people-all .people-grid{grid-template-columns:1fr;gap:32px}.people-head{margin-bottom:28px}}\n</style>\n'''

pattern = re.compile(r'<section class="org(?: soft)?">.*?(?=<section class="closing">)', re.S)
for path, section in sections.items():
    text = path.read_text(encoding='utf-8')
    updated, n = pattern.subn(section, text, count=1)
    if n != 1:
        raise RuntimeError(f'Could not replace grouped People sections in {path}')
    updated = re.sub(r'<style id="people-unified-v2">.*?</style>\s*', '', updated, flags=re.S)
    updated = updated.replace('</head>', css + '</head>')
    path.write_text(updated, encoding='utf-8')
