from pathlib import Path

files = {
    'geovictoria/shift-optimizer.html': {
        'hero_media': '<div class="hero-media"><img src="/images/geo-shift-optimizer.webp" alt="Shift Optimizer interface"></div>',
        'validation_old': '<section class="section soft"><div class="shell validation-copy reveal"><div><div class="kicker">Validation</div><h2>Enterprise pilots were part of the product loop.</h2><p>The product was validated with real operational teams, using pilots to test rules, usability and whether the optimizer actually supported better planning decisions in practice.</p><p>That feedback informed the transition from an MVP toward a production-ready product and helped connect product decisions with commercial value.</p><div class="chips"><span>Enterprise pilots</span><span>Customer validation</span><span>Operational rules</span><span>Usability</span><span>Commercial value</span></div></div></div></section>',
        'validation_new': '<section class="section soft"><div class="shell validation-grid reveal"><div class="validation-media"><img src="/images/geo-shift-optimizer.webp" alt="Shift Optimizer product validation"></div><div><div class="kicker">Validation</div><h2>Enterprise pilots were part of the product loop.</h2><p>The product was validated with real operational teams, using pilots to test rules, usability and whether the optimizer actually supported better planning decisions in practice.</p><p>That feedback informed the transition from an MVP toward a production-ready product and helped connect product decisions with commercial value.</p><div class="chips"><span>Enterprise pilots</span><span>Customer validation</span><span>Operational rules</span><span>Usability</span><span>Commercial value</span></div></div></div></section>'
    },
    'es/geovictoria/shift-optimizer.html': {
        'hero_media': '<div class="hero-media"><img src="/images/geo-shift-optimizer.webp" alt="Interfaz de Optimizador de Turnos"></div>',
        'validation_old': '<section class="section soft"><div class="shell validation-copy reveal"><div><div class="kicker">Validación</div><h2>Los pilotos enterprise son parte del loop de producto.</h2><p>El producto se valida con equipos operativos reales, usando pilotos para probar reglas, usabilidad y si el optimizador efectivamente apoya mejores decisiones de planificación en la práctica.</p><p>Ese feedback alimenta la transición desde MVP hacia un producto listo para producción y ayuda a conectar decisiones de producto con valor comercial.</p><div class="chips"><span>Pilotos enterprise</span><span>Validación con clientes</span><span>Reglas operativas</span><span>Usabilidad</span><span>Valor comercial</span></div></div></div></section>',
        'validation_new': '<section class="section soft"><div class="shell validation-grid reveal"><div class="validation-media"><img src="/images/geo-shift-optimizer.webp" alt="Validación de producto de Optimizador de Turnos"></div><div><div class="kicker">Validación</div><h2>Los pilotos enterprise son parte del loop de producto.</h2><p>El producto se valida con equipos operativos reales, usando pilotos para probar reglas, usabilidad y si el optimizador efectivamente apoya mejores decisiones de planificación en la práctica.</p><p>Ese feedback alimenta la transición desde MVP hacia un producto listo para producción y ayuda a conectar decisiones de producto con valor comercial.</p><div class="chips"><span>Pilotos enterprise</span><span>Validación con clientes</span><span>Reglas operativas</span><span>Usabilidad</span><span>Valor comercial</span></div></div></div></section>'
    }
}

hero_css_old = '.hero-grid{display:grid;grid-template-columns:1fr;gap:36px;align-items:start}.hero-grid>div:first-child{max-width:980px}.hero h1{margin:24px 0 0;max-width:960px;font-family:Manrope,sans-serif;font-size:clamp(44px,4.6vw,66px);line-height:1.03;letter-spacing:-.054em;font-weight:500}.hero p{margin:24px 0 0;max-width:760px;color:#4d5965;font-size:14px;line-height:1.82}.hero-media{width:min(1120px,100%);padding:18px;border:1px solid #d5dee6;border-radius:22px;background:rgba(255,255,255,.78)}.hero-media img{width:100%;max-height:520px;object-fit:contain;border-radius:14px;box-shadow:0 20px 46px rgba(20,40,60,.10)}'
hero_css_new = '.hero-grid{display:grid;grid-template-columns:1fr;align-items:start}.hero-grid>div:first-child{max-width:980px}.hero h1{margin:24px 0 0;max-width:960px;font-family:Manrope,sans-serif;font-size:clamp(44px,4.6vw,66px);line-height:1.03;letter-spacing:-.054em;font-weight:500}.hero p{margin:24px 0 0;max-width:760px;color:#4d5965;font-size:14px;line-height:1.82}'
validation_css_old = '.validation-copy{max-width:980px}.validation-copy h2{max-width:820px}.validation-copy p{max-width:820px}'
validation_css_new = '.validation-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:64px;align-items:center}.validation-media{padding:20px;border-radius:20px;background:#dce6ee;border:1px solid #d1dce5}.validation-media img{width:100%;max-height:460px;object-fit:contain;border-radius:12px;box-shadow:0 16px 36px rgba(20,40,60,.08)}'
media_old = '@media(max-width:1000px){.hero-grid,.two-col,.role-grid{grid-template-columns:1fr}'
media_new = '@media(max-width:1000px){.hero-grid,.two-col,.role-grid,.validation-grid{grid-template-columns:1fr}'
mobile_old = '.hero-grid{gap:28px}.hero-media{padding:12px}'
mobile_new = '.hero-grid{gap:0}.validation-media{padding:12px}'

for path_str, cfg in files.items():
    path = Path(path_str)
    text = path.read_text(encoding='utf-8')
    replacements = [
        (cfg['hero_media'], '', 'hero media'),
        (hero_css_old, hero_css_new, 'hero css'),
        (validation_css_old, validation_css_new, 'validation css'),
        (media_old, media_new, 'responsive css'),
        (mobile_old, mobile_new, 'mobile css'),
        (cfg['validation_old'], cfg['validation_new'], 'validation html'),
    ]
    for old, new, label in replacements:
        if old not in text:
            raise SystemExit(f'{label} pattern not found in {path_str}')
        text = text.replace(old, new, 1)
    path.write_text(text, encoding='utf-8')
    print('updated', path_str)
