from pathlib import Path


def replace_all(text, replacements):
    for old, new in replacements:
        text = text.replace(old, new)
    return text

# Source pages
src_en = Path('low-workspace.html')
src_es = Path('es/low-workspace.html')
if not src_en.exists() or not src_es.exists():
    raise SystemExit('Low Workspace source pages not found')

en = src_en.read_text(encoding='utf-8')
es = src_es.read_text(encoding='utf-8')

# Canonical nested routes and language switch links
en = replace_all(en, [
    ('https://felipequirozp.cl/low-workspace', 'https://felipequirozp.cl/lowsignal/low-workspace'),
    ('https://felipequirozp.cl/es/low-workspace', 'https://felipequirozp.cl/es/lowsignal/low-workspace'),
    ('href="/es/low-workspace"', 'href="/es/lowsignal/low-workspace"'),
])
es = replace_all(es, [
    ('https://felipequirozp.cl/es/low-workspace', 'https://felipequirozp.cl/es/lowsignal/low-workspace'),
    ('https://felipequirozp.cl/low-workspace', 'https://felipequirozp.cl/lowsignal/low-workspace'),
    ('href="/low-workspace"', 'href="/lowsignal/low-workspace"'),
])

# Write canonical pages
Path('lowsignal').mkdir(exist_ok=True)
Path('es/lowsignal').mkdir(parents=True, exist_ok=True)
Path('lowsignal/low-workspace.html').write_text(en, encoding='utf-8')
Path('es/lowsignal/low-workspace.html').write_text(es, encoding='utf-8')

# Old URLs become lightweight redirects
src_en.write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><link rel="canonical" href="https://felipequirozp.cl/lowsignal/low-workspace"><meta http-equiv="refresh" content="0; url=/lowsignal/low-workspace"><script>location.replace('/lowsignal/low-workspace'+location.search+location.hash)</script><title>Low Workspace</title></head><body><a href="/lowsignal/low-workspace">Continue to Low Workspace</a></body></html>''', encoding='utf-8')
src_es.write_text('''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><link rel="canonical" href="https://felipequirozp.cl/es/lowsignal/low-workspace"><meta http-equiv="refresh" content="0; url=/es/lowsignal/low-workspace"><script>location.replace('/es/lowsignal/low-workspace'+location.search+location.hash)</script><title>Low Workspace</title></head><body><a href="/es/lowsignal/low-workspace">Continuar a Low Workspace</a></body></html>''', encoding='utf-8')

# Update links from lowsignal case studies
for path, old, new in [
    ('lowsignal.html', 'href="/low-workspace"', 'href="/lowsignal/low-workspace"'),
    ('es/lowsignal.html', 'href="/es/low-workspace"', 'href="/es/lowsignal/low-workspace"'),
]:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    text = text.replace(old, new)
    p.write_text(text, encoding='utf-8')

print('Low Workspace moved to nested lowsignal routes.')
