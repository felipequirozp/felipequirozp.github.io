from pathlib import Path
import re

FILES = [
    Path('tethered/anotate-en-la-lista/index.html'),
    Path('es/tethered/anotate-en-la-lista/index.html'),
]

NAV_CSS = '''.nav{position:fixed;inset:0 0 auto 0;z-index:9999;height:var(--nav-h);padding:0 var(--page);display:flex;align-items:center;justify-content:space-between;gap:28px;background:rgba(255,255,255,.96);border-bottom:1px solid rgba(11,17,23,.08);backdrop-filter:blur(16px)}.brand{font-family:Manrope,sans-serif;font-size:22px!important;font-weight:600;letter-spacing:-.045em}.nav-center,.nav-right{display:flex;align-items:center;gap:28px}.nav a{font-size:11px;font-weight:500;color:#1a232d}.nav-center a{position:relative}.nav-center a::after{content:"";position:absolute;left:0;bottom:-7px;width:0;height:1px;background:#111820;transition:.2s}.nav-center a:hover::after,.nav-center a.active::after{width:100%}.lang{width:38px;height:38px;display:grid;place-items:center;border:1px solid #d7dde4;border-radius:50%;font-size:10px!important;transition:.18s}.lang:hover{background:#0b1117;color:#fff;border-color:#0b1117;transform:translateY(-1px)}'''

FOOTER_CSS = '''.footer{padding:58px var(--page) 28px;background:#fff;border-top:1px solid var(--line)}.footer-grid{width:min(var(--max),100%);margin:auto;display:grid;grid-template-columns:1.15fr repeat(3,.7fr);gap:56px}.footer-eyebrow{margin-bottom:12px;color:var(--blue);font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}.footer-brand{font-family:Manrope,sans-serif;font-size:28px;letter-spacing:-.045em;font-weight:600}.footer-copy{margin-top:12px;max-width:330px;color:#65717d;font-size:12px;line-height:1.65}.footer-col strong{display:block;margin-bottom:14px;font-size:11px}.footer-col a{display:block;width:max-content;max-width:100%;margin:10px 0;color:#66727e;font-size:12px;transition:.18s}.footer-col a:hover{color:#0b1117;transform:translateX(3px)}.footer-bottom{width:min(var(--max),100%);margin:42px auto 0;padding-top:20px;display:flex;justify-content:space-between;border-top:1px solid var(--line);color:#83909c;font-size:9px;letter-spacing:.06em;text-transform:uppercase}'''

EN_FOOTER = '''<footer class="footer"><div class="footer-grid"><div><div class="footer-eyebrow">Product · Growth · Operations · Company building</div><div class="footer-brand">Felipe Quiroz</div><div class="footer-copy">Building products, growth systems and companies across technology and business.</div></div><div class="footer-col"><strong>Explore</strong><a href="/#work">Work</a><a href="/about">About</a><a href="/projects">Projects</a><a href="/initiatives">Initiatives</a><a href="/blog">Blog</a></div><div class="footer-col"><strong>Social</strong><a href="https://www.linkedin.com/in/felipequirozp" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="https://github.com/felipequirozp" target="_blank" rel="noopener noreferrer">GitHub</a></div><div class="footer-col"><strong>Contact</strong><a href="mailto:felipe@lowsignal.cl">Email</a><a href="https://calendly.com/felipe-lowsignal/30min" target="_blank" rel="noopener noreferrer">Calendly</a></div></div><div class="footer-bottom"><div>© 2026 Felipe Quiroz</div><div>Santiago, Chile</div></div></footer>'''

ES_FOOTER = '''<footer class="footer"><div class="footer-grid"><div><div class="footer-eyebrow">Producto · Growth · Operaciones · Company building</div><div class="footer-brand">Felipe Quiroz</div><div class="footer-copy">Construyendo productos, sistemas de crecimiento y compañías entre tecnología y negocio.</div></div><div class="footer-col"><strong>Explorar</strong><a href="/es/#work">Trabajo</a><a href="/es/about">Sobre mí</a><a href="/es/projects">Proyectos</a><a href="/es/initiatives">Iniciativas</a><a href="/es/blog">Blog</a></div><div class="footer-col"><strong>Social</strong><a href="https://www.linkedin.com/in/felipequirozp" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="https://github.com/felipequirozp" target="_blank" rel="noopener noreferrer">GitHub</a></div><div class="footer-col"><strong>Contacto</strong><a href="mailto:felipe@lowsignal.cl">Email</a><a href="https://calendly.com/felipe-lowsignal/30min" target="_blank" rel="noopener noreferrer">Calendly</a></div></div><div class="footer-bottom"><div>© 2026 Felipe Quiroz</div><div>Santiago, Chile</div></div></footer>'''

for path in FILES:
    s = path.read_text()
    # Replace navbar styling with the standard Tether case-study navbar.
    s = re.sub(r'\.nav\{.*?\.lang:hover\{.*?\}', NAV_CSS, s, count=1, flags=re.S)
    # Replace footer styling with the standard site/Tether footer.
    s = re.sub(r'\.footer\{.*?\.footer-bottom\{.*?\}', FOOTER_CSS, s, count=1, flags=re.S)
    # Preserve responsive declarations but ensure the navbar height is explicit on mobile.
    s = s.replace('@media(max-width:700px){:root{--page:20px;--nav-h:68px}.nav-center{display:none}', '@media(max-width:700px){:root{--page:20px;--nav-h:68px}.nav{height:var(--nav-h)}.nav-center{display:none}')
    footer = ES_FOOTER if str(path).startswith('es/') else EN_FOOTER
    s = re.sub(r'<footer class="footer">.*?</footer>', footer, s, count=1, flags=re.S)
    path.write_text(s)

# English project card title should be English.
p = Path('projects.html')
s = p.read_text()
s = s.replace('<h3>Anótate en la Lista</h3><p>Chile\'s school regularization process moved from physical queues to a national digital registry for families seeking available seats.</p>', '<h3>Join the Waitlist</h3><p>Chile\'s school regularization process moved from physical queues to a national digital registry for families seeking available seats.</p>')
s = s.replace('alt="Anótate en la Lista · Tether Education"', 'alt="Join the Waitlist · Tether Education"')
p.write_text(s)
