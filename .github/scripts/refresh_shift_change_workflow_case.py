from pathlib import Path

files = {
    'geovictoria/shift-change-workflow.html': {
        'old_title': '<h1>Shift Change Workflow<span>Flexibility, with guardrails.</span></h1>',
        'new_title': '<h1>Building a controlled workflow for employee shift changes.</h1>',
        'hero_media': '<div class="hero-media"><img src="/images/geo-shift-change-workflow.webp" alt="Shift Change Workflow interface"></div>',
    },
    'es/geovictoria/shift-change-workflow.html': {
        'old_title': '<h1>Flujo de Cambio de Turnos<span>Flexibilidad, con control.</span></h1>',
        'new_title': '<h1>Construyendo un workflow controlado para cambios de turno.</h1>',
        'hero_media': '<div class="hero-media"><img src="/images/geo-shift-change-workflow.webp" alt="Interfaz del Flujo de Cambio de Turnos"></div>',
    }
}

old_hero_css = '.hero-grid{display:grid;grid-template-columns:minmax(0,.82fr) minmax(440px,1.18fr);gap:66px;align-items:center}.hero h1{margin:24px 0 0;font-family:Manrope,sans-serif;font-size:clamp(46px,5vw,72px);line-height:.98;letter-spacing:-.058em;font-weight:500}.hero h1 span{display:block;color:#98a4af}.hero p{margin:28px 0 0;max-width:650px;color:#4d5965;font-size:14px;line-height:1.84}.hero-media{padding:26px;border:1px solid #d5dee6;border-radius:22px;background:rgba(255,255,255,.72)}.hero-media img{width:100%;border-radius:14px;box-shadow:0 20px 46px rgba(20,40,60,.10)}'
new_hero_css = '.hero-grid{display:grid;grid-template-columns:1fr;align-items:start}.hero-grid>div:first-child{max-width:980px}.hero h1{margin:24px 0 0;max-width:960px;font-family:Manrope,sans-serif;font-size:clamp(44px,4.6vw,66px);line-height:1.03;letter-spacing:-.054em;font-weight:500}.hero p{margin:24px 0 0;max-width:760px;color:#4d5965;font-size:14px;line-height:1.82}'

old_validation_css = '.validation-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:64px;align-items:center}.validation-media{padding:24px;border-radius:20px;background:#dce6ee;border:1px solid #d1dce5}.validation-media img{width:100%;border-radius:12px}'
new_validation_css = '.validation-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:64px;align-items:center}.validation-media{padding:20px;border-radius:20px;background:#dce6ee;border:1px solid #d1dce5}.validation-media img{width:100%;max-height:460px;object-fit:contain;border-radius:12px;box-shadow:0 16px 36px rgba(20,40,60,.08)}'

old_mobile = '.hero-grid{gap:34px}.hero-media{padding:14px}'
new_mobile = '.hero-grid{gap:0}.validation-media{padding:12px}'

for path_str, cfg in files.items():
    path = Path(path_str)
    text = path.read_text(encoding='utf-8')
    replacements = [
        (cfg['old_title'], cfg['new_title'], 'title'),
        (cfg['hero_media'], '', 'hero image'),
        (old_hero_css, new_hero_css, 'hero css'),
        (old_validation_css, new_validation_css, 'validation css'),
        (old_mobile, new_mobile, 'mobile css'),
    ]
    for old, new, label in replacements:
        if old not in text:
            raise SystemExit(f'{label} pattern not found in {path_str}')
        text = text.replace(old, new, 1)
    path.write_text(text, encoding='utf-8')
    print('updated', path_str)
