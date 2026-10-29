from pathlib import Path
import re

ROOT = Path('.')

STYLE = '''<style id="site-footer-v2">
.footer{padding:58px var(--page,8vw) 28px!important;background:#fff!important;border-top:1px solid var(--line,#e1e6eb)!important}
.footer-grid{width:min(var(--max,1520px),100%)!important;margin:0 auto!important;display:grid!important;grid-template-columns:1.15fr .7fr .7fr .7fr!important;gap:56px!important;align-items:start!important}
.footer-eyebrow{margin-bottom:12px!important;color:var(--blue,#1467d8)!important;font-size:9px!important;font-weight:700!important;letter-spacing:.12em!important;text-transform:uppercase!important}
.footer-brand{font-family:Manrope,sans-serif!important;font-size:28px!important;letter-spacing:-.045em!important;font-weight:600!important}
.footer-copy{margin-top:12px!important;max-width:330px!important;color:#65717d!important;font-size:12px!important;line-height:1.65!important}
.footer-col strong{display:block!important;margin-bottom:14px!important;font-size:11px!important;font-weight:700!important}
.footer-col a{display:block!important;width:max-content!important;max-width:100%!important;margin:10px 0!important;color:#66727e!important;font-size:12px!important;transition:transform .18s ease,color .18s ease!important}
.footer-col a:hover{color:#0b1117!important;transform:translateX(3px)!important}
.footer-bottom{width:min(var(--max,1520px),100%)!important;margin:42px auto 0!important;padding-top:20px!important;display:flex!important;justify-content:space-between!important;gap:20px!important;border-top:1px solid var(--line,#e1e6eb)!important;color:#83909c!important;font-size:9px!important;letter-spacing:.06em!important;text-transform:uppercase!important}
@media(max-width:1050px){.footer-grid{grid-template-columns:1fr 1fr!important}}
@media(max-width:700px){.footer{padding-top:46px!important}.footer-grid{grid-template-columns:1fr!important;gap:28px!important}.footer-bottom{margin-top:34px!important;flex-direction:column!important;gap:10px!important}}
</style>'''

EN_FOOTER = '''<footer class="footer"><div class="footer-grid"><div><div class="footer-eyebrow">Product · Growth · Operations · Company building</div><div class="footer-brand">Felipe Quiroz</div><div class="footer-copy">Building products, growth systems and companies across technology and business.</div></div><div class="footer-col"><strong>Explore</strong><a href="/#work">Work</a><a href="/about">About</a><a href="/projects">Projects</a><a href="/initiatives">Initiatives</a><a href="/blog">Blog</a></div><div class="footer-col"><strong>Social</strong><a href="https://www.linkedin.com/in/felipequirozp" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="https://github.com/felipequirozp" target="_blank" rel="noopener noreferrer">GitHub</a><a href="https://www.instagram.com/felipe_quirozp/" target="_blank" rel="noopener noreferrer">Instagram</a></div><div class="footer-col"><strong>Contact</strong><a href="mailto:felipe@lowsignal.cl">Email</a><a href="https://calendly.com/felipe-lowsignal/30min" target="_blank" rel="noopener noreferrer">Calendly</a></div></div><div class="footer-bottom"><div>© 2026 Felipe Quiroz</div><div>Santiago, Chile</div></div></footer>'''

ES_FOOTER = '''<footer class="footer"><div class="footer-grid"><div><div class="footer-eyebrow">Producto · Growth · Operaciones · Company building</div><div class="footer-brand">Felipe Quiroz</div><div class="footer-copy">Construyendo productos, sistemas de crecimiento y compañías entre tecnología y negocio.</div></div><div class="footer-col"><strong>Explorar</strong><a href="/es/#work">Trabajo</a><a href="/es/about">Sobre mí</a><a href="/es/projects">Proyectos</a><a href="/es/initiatives">Iniciativas</a><a href="/es/blog">Blog</a></div><div class="footer-col"><strong>Social</strong><a href="https://www.linkedin.com/in/felipequirozp" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="https://github.com/felipequirozp" target="_blank" rel="noopener noreferrer">GitHub</a><a href="https://www.instagram.com/felipe_quirozp/" target="_blank" rel="noopener noreferrer">Instagram</a></div><div class="footer-col"><strong>Contacto</strong><a href="mailto:felipe@lowsignal.cl">Email</a><a href="https://calendly.com/felipe-lowsignal/30min" target="_blank" rel="noopener noreferrer">Calendly</a></div></div><div class="footer-bottom"><div>© 2026 Felipe Quiroz</div><div>Santiago, Chile</div></div></footer>'''

changed = []

for path in ROOT.rglob('*.html'):
    if '.git' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    if '<footer' not in text or 'footer-brand' not in text:
        continue

    original = text
    html_lang_match = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)["\']', text, flags=re.I)
    root_lang = html_lang_match.group(1).lower() if html_lang_match else ''
    is_es = (path.parts and path.parts[0] == 'es') or root_lang.startswith('es')
    footer = ES_FOOTER if is_es else EN_FOOTER

    if 'id="site-footer-v2"' in text:
        text = re.sub(r'<style id="site-footer-v2">.*?</style>', STYLE, text, count=1, flags=re.S)
    else:
        text = text.replace('</head>', STYLE + '</head>', 1)

    text = re.sub(r'<footer\s+class=["\']footer["\'][^>]*>.*?</footer>', footer, text, count=1, flags=re.S | re.I)

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(str(path))

# Keep the first three Tether project pills focused on business model.
project_updates = {
    Path('projects.html'): [
        ('<div class="impact"><span>LATAM · U.S. · Europe</span><span>EdTech</span></div>', '<div class="impact"><span>B2G</span><span>B2C</span><span>B2B</span></div>'),
        ('<div class="impact"><span>78 institutions</span><span>35k+ students</span></div>', '<div class="impact"><span>B2G</span><span>B2B</span><span>B2C</span></div>'),
        ('<div class="impact"><span>50+ public schools</span><span>Responsible AI</span></div>', '<div class="impact"><span>B2G</span><span>B2B</span><span>B2C</span></div>'),
    ],
    Path('es/projects.html'): [
        ('<div class="impact"><span>LATAM · U.S. · Europa</span><span>EdTech</span></div>', '<div class="impact"><span>B2G</span><span>B2C</span><span>B2B</span></div>'),
        ('<div class="impact"><span>78 establecimientos</span><span>35k+ estudiantes</span></div>', '<div class="impact"><span>B2G</span><span>B2B</span><span>B2C</span></div>'),
        ('<div class="impact"><span>50+ escuelas públicas</span><span>IA responsable</span></div>', '<div class="impact"><span>B2G</span><span>B2B</span><span>B2C</span></div>'),
    ],
}

for path, replacements in project_updates.items():
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in replacements:
        text = text.replace(old, new, 1)
    if text != original:
        path.write_text(text, encoding='utf-8')
        if str(path) not in changed:
            changed.append(str(path))

print(f'Updated {len(changed)} HTML files')
for item in changed:
    print(item)
