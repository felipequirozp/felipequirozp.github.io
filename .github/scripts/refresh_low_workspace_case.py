from pathlib import Path

files = {
    Path('lowsignal/low-workspace.html'): {
        'old_hero': '<section class="hero"><div class="shell hero-grid"><div><div class="kicker">lowsignal · Internal product</div><h1>Low Workspace<span>The operating layer behind the company.</span></h1><p>An internal product in development to unify clients, revenue, tasks, team operations and company data in one place.</p></div><div class="hero-media"><img src="/images/panel-demo.png" alt="Low Workspace dashboard"></div></div></section>',
        'new_hero': '<section class="hero"><div class="shell hero-grid"><div><div class="kicker">lowsignal · Internal product</div><h1>Building the operating layer behind lowsignal.</h1><p>An internal product in development to unify clients, revenue, tasks, team operations and company data in one place.</p></div></div></section>',
    },
    Path('es/lowsignal/low-workspace.html'): {
        'old_hero': '<section class="hero"><div class="shell hero-grid"><div><div class="kicker">lowsignal · Producto interno</div><h1>Low Workspace<span>La capa operativa detrás de la compañía.</span></h1><p>Un producto interno en desarrollo para unificar clientes, ingresos, tareas, operación del equipo y datos de la compañía en un solo lugar.</p></div><div class="hero-media"><img src="/images/panel-demo.png" alt="Dashboard de Low Workspace"></div></div></section>',
        'new_hero': '<section class="hero"><div class="shell hero-grid"><div><div class="kicker">lowsignal · Producto interno</div><h1>Construyendo la capa operativa detrás de lowsignal.</h1><p>Un producto interno en desarrollo para unificar clientes, ingresos, tareas, operación del equipo y datos de la compañía en un solo lugar.</p></div></div></section>',
    },
}

old_css = '.hero{padding:64px var(--page) 72px;background:radial-gradient(circle at 82% 16%,rgba(20,103,216,.11),transparent 28%),linear-gradient(180deg,#f4f7f9 0%,#eef3f7 100%);border-bottom:1px solid #dce4eb}.hero-grid{display:grid;grid-template-columns:minmax(0,.8fr) minmax(440px,1.2fr);gap:64px;align-items:center}.hero h1{margin:24px 0 0;font-family:Manrope,sans-serif;font-size:clamp(46px,5vw,72px);line-height:.98;letter-spacing:-.058em;font-weight:500}.hero h1 span{display:block;color:#98a4af}.hero p{margin:28px 0 0;max-width:650px;color:#4d5965;font-size:14px;line-height:1.84}.hero-media{padding:26px;border:1px solid #d5dee6;border-radius:22px;background:rgba(255,255,255,.72)}.hero-media img{width:100%;border-radius:14px;box-shadow:0 20px 46px rgba(20,40,60,.10)}'
new_css = '.hero{padding:64px var(--page) 72px;background:radial-gradient(circle at 82% 16%,rgba(20,103,216,.11),transparent 28%),linear-gradient(180deg,#f4f7f9 0%,#eef3f7 100%);border-bottom:1px solid #dce4eb}.hero-grid{display:grid;grid-template-columns:1fr;align-items:start}.hero-grid>div:first-child{max-width:980px}.hero h1{margin:24px 0 0;max-width:960px;font-family:Manrope,sans-serif;font-size:clamp(44px,4.6vw,66px);line-height:1.03;letter-spacing:-.054em;font-weight:500}.hero p{margin:24px 0 0;max-width:760px;color:#4d5965;font-size:14px;line-height:1.82}'

for path, cfg in files.items():
    text = path.read_text(encoding='utf-8')
    if cfg['new_hero'] in text:
        print('already updated', path)
        continue
    if old_css not in text:
        raise SystemExit(f'old hero css not found in {path}')
    if cfg['old_hero'] not in text:
        raise SystemExit(f'old hero markup not found in {path}')
    text = text.replace(old_css, new_css, 1)
    text = text.replace(cfg['old_hero'], cfg['new_hero'], 1)
    text = text.replace('.hero-grid{gap:34px}.hero-media{padding:14px}', '.hero-grid{gap:0}', 1)
    path.write_text(text, encoding='utf-8')
    print('updated', path)
