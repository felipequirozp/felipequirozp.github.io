from pathlib import Path
import re

ROOT = Path('.')

STYLE = '''<style id="site-footer-v2">
.footer{padding:58px var(--page,8vw) 28px!important;background:#fff!important;border-top:1px solid var(--line,#e1e6eb)!important}
.footer-grid{width:min(var(--max,1520px),100%)!important;margin:0 auto!important;display:grid!important;grid-template-columns:1.15fr .7fr .7fr .7fr!important;gap:clamp(30px,5vw,72px)!important;align-items:start!important}
.footer-eyebrow{margin-bottom:10px;color:#71808f;font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.footer-brand{font-family:Manrope,sans-serif!important;font-size:28px!important;line-height:1.05!important;letter-spacing:-.045em!important;font-weight:600!important}
.footer-copy{margin-top:12px!important;max-width:330px!important;color:#65717d!important;font-size:12px!important;line-height:1.68!important}
.footer-col strong{display:block!important;margin-bottom:13px!important;color:#111820!important;font-size:11px!important;font-weight:700!important}
.footer-col a{display:block!important;width:max-content!important;max-width:100%!important;margin:9px 0!important;color:#687583!important;font-size:12px!important;transition:color .18s ease,transform .18s ease!important}
.footer-col a:hover{color:#0b1117!important;transform:translateX(3px)!important}
.footer-bottom{width:min(var(--max,1520px),100%)!important;margin:46px auto 0!important;padding-top:20px!important;display:flex!important;justify-content:space-between!important;gap:20px!important;border-top:1px solid var(--line,#e1e6eb)!important;color:#83909d!important;font-size:9px!important;letter-spacing:.08em!important;text-transform:uppercase!important}
@media(max-width:1000px){.footer-grid{grid-template-columns:1fr 1fr!important}}
@media(max-width:700px){.footer{padding-top:48px!important}.footer-grid{grid-template-columns:1fr!important;gap:30px!important}.footer-bottom{margin-top:36px!important;flex-direction:column!important;gap:10px!important}}
</style>'''

EN_EYEBROW = 'Product · Growth · Operations · Company building'
ES_EYEBROW = 'Producto · Growth · Operaciones · Company building'

changed = []

for path in ROOT.rglob('*.html'):
    if '.git' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    if '<footer' not in text or 'footer-brand' not in text:
        continue

    original = text
    is_es = path.parts and path.parts[0] == 'es' or 'lang="es"' in text.lower()
    eyebrow = ES_EYEBROW if is_es else EN_EYEBROW

    if 'id="site-footer-v2"' not in text:
        text = text.replace('</head>', STYLE + '</head>', 1)

    if 'footer-eyebrow' not in text:
        pattern = r'(<div\s+class=["\']footer-brand["\']>\s*Felipe Quiroz\s*</div>)'
        repl = f'<div class="footer-eyebrow">{eyebrow}</div>\\1'
        text = re.sub(pattern, repl, text, count=1, flags=re.I)

    text = text.replace('Santiago / CL', 'Santiago, Chile')
    text = text.replace('SANTIAGO / CL', 'SANTIAGO, CHILE')

    if text != original:
        path.write_text(text, encoding='utf-8')
        changed.append(str(path))

print(f'Updated {len(changed)} HTML files')
for item in changed:
    print(item)
