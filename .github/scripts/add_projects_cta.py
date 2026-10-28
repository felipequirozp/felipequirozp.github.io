from pathlib import Path

FILES = [Path('projects.html'), Path('es/projects.html')]

CSS_OLD = '.footer{padding:72px var(--page) 34px;background:#fff;border-top:1px solid var(--line)}'
CSS_NEW = '.projects-cta{padding:0 var(--page) 96px;background:#fff}.projects-cta-inner{width:min(var(--max),100%);margin:0 auto;padding:54px 58px;border-radius:26px;background:#07101a;color:#fff;display:grid;grid-template-columns:1fr auto;gap:48px;align-items:end}.projects-cta-kicker{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#80baff}.projects-cta h2{margin:12px 0 0;max-width:760px;font-family:Manrope,sans-serif;font-size:clamp(36px,4vw,58px);line-height:1;letter-spacing:-.055em;font-weight:500}.projects-cta p{margin:18px 0 0;max-width:700px;color:#b8c3ce;font-size:14px;line-height:1.72}.projects-cta-link{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:0 18px;border-radius:999px;background:#fff;color:#0b1117;font-size:11px;font-weight:700;white-space:nowrap;transition:.2s ease}.projects-cta-link:hover{background:#1467d8;color:#fff;transform:translateY(-2px)}.footer{padding:72px var(--page) 34px;background:#fff;border-top:1px solid var(--line)}'

for path in FILES:
    s = path.read_text(encoding='utf-8')
    if 'projects-cta-inner' not in s:
        s = s.replace(CSS_OLD, CSS_NEW)
        s = s.replace('@media(max-width:860px){.nav-center{display:none}.hero-grid{grid-template-columns:1fr;gap:28px}.grid{grid-template-columns:1fr}}', '@media(max-width:860px){.nav-center{display:none}.hero-grid{grid-template-columns:1fr;gap:28px}.grid{grid-template-columns:1fr}.projects-cta-inner{grid-template-columns:1fr;align-items:start}.projects-cta-link{justify-self:start}}')
        s = s.replace('@media(max-width:640px){:root{--page:20px}.nav{min-height:68px}', '@media(max-width:640px){:root{--page:20px}.nav{min-height:68px}')
        s = s.replace('.portfolio{padding-top:26px;padding-bottom:82px}.footer-grid', '.portfolio{padding-top:26px;padding-bottom:82px}.projects-cta{padding-bottom:72px}.projects-cta-inner{padding:36px 28px}.footer-grid')

    if '</main><footer class="footer">' in s and '<section class="projects-cta">' not in s:
        if 'lang="es"' in s:
            cta = '<section class="projects-cta"><div class="projects-cta-inner"><div><div class="projects-cta-kicker">Construyamos algo</div><h2>¿Construyendo algo ambicioso?</h2><p>Siempre me interesan productos, compañías e ideas donde se cruzan estrategia, tecnología y ejecución.</p></div><a class="projects-cta-link" href="https://calendly.com/felipe-lowsignal/30min" target="_blank" rel="noopener noreferrer">Hablemos ↗</a></div></section>'
        else:
            cta = '<section class="projects-cta"><div class="projects-cta-inner"><div><div class="projects-cta-kicker">Let\'s build</div><h2>Building something ambitious?</h2><p>I’m always interested in products, companies and ideas where strategy, technology and execution meet.</p></div><a class="projects-cta-link" href="https://calendly.com/felipe-lowsignal/30min" target="_blank" rel="noopener noreferrer">Let\'s talk ↗</a></div></section>'
        s = s.replace('</main><footer class="footer">', cta + '</main><footer class="footer">')

    path.write_text(s, encoding='utf-8')
