from pathlib import Path

files = {
    'geovictoria/shift-optimizer.html': {
        'title_old': '<h1>Shift Optimizer<span>From MVP to production.</span></h1>',
        'title_new': '<h1>Taking workforce optimization from MVP to production.</h1>',
        'validation_old': '<section class="section soft"><div class="shell validation-grid reveal"><div class="validation-media"><img src="/images/geo-shift-optimizer.webp" alt="Shift Optimizer product validation"></div><div><div class="kicker">Validation</div><h2>Enterprise pilots were part of the product loop.</h2><p>The product was validated with real operational teams, using pilots to test rules, usability and whether the optimizer actually supported better planning decisions in practice.</p><p>That feedback informed the transition from an MVP toward a production-ready product and helped connect product decisions with commercial value.</p><div class="chips"><span>Enterprise pilots</span><span>Customer validation</span><span>Operational rules</span><span>Usability</span><span>Commercial value</span></div></div></div></section>',
        'validation_new': '<section class="section soft"><div class="shell validation-copy reveal"><div><div class="kicker">Validation</div><h2>Enterprise pilots were part of the product loop.</h2><p>The product was validated with real operational teams, using pilots to test rules, usability and whether the optimizer actually supported better planning decisions in practice.</p><p>That feedback informed the transition from an MVP toward a production-ready product and helped connect product decisions with commercial value.</p><div class="chips"><span>Enterprise pilots</span><span>Customer validation</span><span>Operational rules</span><span>Usability</span><span>Commercial value</span></div></div></div></section>'
    },
    'es/geovictoria/shift-optimizer.html': {
        'title_old': '<h1>Optimizador de Turnos<span>De MVP a producción.</span></h1>',
        'title_new': '<h1>Llevando la optimización de turnos desde MVP a producción.</h1>',
        'validation_old': '<section class="section soft"><div class="shell validation-grid reveal"><div class="validation-media"><img src="/images/geo-shift-optimizer.webp" alt="Validación de producto de Optimizador de Turnos"></div><div><div class="kicker">Validación</div><h2>Los pilotos enterprise son parte del loop de producto.</h2><p>El producto se valida con equipos operativos reales, usando pilotos para probar reglas, usabilidad y si el optimizador efectivamente apoya mejores decisiones de planificación en la práctica.</p><p>Ese feedback alimenta la transición desde un MVP hacia un producto listo para producción y ayuda a conectar decisiones de producto con valor comercial.</p><div class="chips"><span>Pilotos enterprise</span><span>Validación con clientes</span><span>Reglas operativas</span><span>Usabilidad</span><span>Valor comercial</span></div></div></div></section>',
        'validation_new': '<section class="section soft"><div class="shell validation-copy reveal"><div><div class="kicker">Validación</div><h2>Los pilotos enterprise son parte del loop de producto.</h2><p>El producto se valida con equipos operativos reales, usando pilotos para probar reglas, usabilidad y si el optimizador efectivamente apoya mejores decisiones de planificación en la práctica.</p><p>Ese feedback alimenta la transición desde un MVP hacia un producto listo para producción y ayuda a conectar decisiones de producto con valor comercial.</p><div class="chips"><span>Pilotos enterprise</span><span>Validación con clientes</span><span>Reglas operativas</span><span>Usabilidad</span><span>Valor comercial</span></div></div></div></section>'
    }
}

css_old = '.hero-grid{display:grid;grid-template-columns:minmax(0,.8fr) minmax(440px,1.2fr);gap:64px;align-items:center}.hero h1{margin:24px 0 0;font-family:Manrope,sans-serif;font-size:clamp(46px,5vw,72px);line-height:.98;letter-spacing:-.058em;font-weight:500}.hero h1 span{display:block;color:#98a4af}.hero p{margin:28px 0 0;max-width:650px;color:#4d5965;font-size:14px;line-height:1.84}.hero-media{padding:26px;border:1px solid #d5dee6;border-radius:22px;background:rgba(255,255,255,.72)}.hero-media img{width:100%;border-radius:14px;box-shadow:0 20px 46px rgba(20,40,60,.10)}'
css_new = '.hero-grid{display:grid;grid-template-columns:1fr;gap:36px;align-items:start}.hero-grid>div:first-child{max-width:980px}.hero h1{margin:24px 0 0;max-width:960px;font-family:Manrope,sans-serif;font-size:clamp(44px,4.6vw,66px);line-height:1.03;letter-spacing:-.054em;font-weight:500}.hero p{margin:24px 0 0;max-width:760px;color:#4d5965;font-size:14px;line-height:1.82}.hero-media{width:min(1120px,100%);padding:18px;border:1px solid #d5dee6;border-radius:22px;background:rgba(255,255,255,.78)}.hero-media img{width:100%;max-height:520px;object-fit:contain;border-radius:14px;box-shadow:0 20px 46px rgba(20,40,60,.10)}'
validation_css_old = '.validation-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:64px;align-items:center}.validation-media{padding:24px;border-radius:20px;background:#dce6ee;border:1px solid #d1dce5}.validation-media img{width:100%;border-radius:12px}'
validation_css_new = '.validation-copy{max-width:980px}.validation-copy h2{max-width:820px}.validation-copy p{max-width:820px}'
media_old = '@media(max-width:1000px){.hero-grid,.two-col,.role-grid,.validation-grid{grid-template-columns:1fr}'
media_new = '@media(max-width:1000px){.hero-grid,.two-col,.role-grid{grid-template-columns:1fr}'
mobile_old = '.hero-grid{gap:34px}.hero-media{padding:14px}'
mobile_new = '.hero-grid{gap:28px}.hero-media{padding:12px}'

for path_str, cfg in files.items():
    path = Path(path_str)
    text = path.read_text()
    for old,new,label in [
        (cfg['title_old'], cfg['title_new'], 'title'),
        (css_old, css_new, 'hero css'),
        (validation_css_old, validation_css_new, 'validation css'),
        (media_old, media_new, 'media css'),
        (mobile_old, mobile_new, 'mobile css'),
        (cfg['validation_old'], cfg['validation_new'], 'validation html')
    ]:
        if old not in text:
            raise SystemExit(f'{label} pattern not found in {path_str}')
        text = text.replace(old,new,1)
    path.write_text(text)
    print('updated', path_str)
