from pathlib import Path

files = {
    Path('geovictoria.html'): {
        'old_title': '<h1>Product systems for <span>real-world operations.</span></h1>',
        'new_title': '<h1>Building workforce products for real-world operations.</h1>',
        'scope_end': '</section>\n<section class="products">',
        'role': '''</section>\n<section class="geo-role"><div class="shell geo-role-grid reveal"><div><div class="kicker">My role</div></div><div><h2>Owning product decisions from discovery to real-world adoption.</h2><p>My role sat between customers, product, engineering, implementation and commercial teams. I translated operational complexity into product priorities, validation plans and launch decisions across multiple LATAM markets.</p><div class="geo-role-cards"><article><span>01 / Product strategy</span><h3>Turn customer problems into product decisions.</h3><p>Defined priorities, rules and roadmap decisions across scheduling, optimization and shift workflows.</p></article><article><span>02 / Validation & pilots</span><h3>Test with real operations before scaling.</h3><p>Led 100+ validations and pilots to pressure-test usability, rules and value with enterprise customers.</p></article><article><span>03 / Cross-functional execution</span><h3>Connect product with commercial reality.</h3><p>Worked across engineering, implementation, sales and customer teams to move products toward adoption and production.</p></article></div></div></div></section>\n<section class="products">'''
    },
    Path('es/geovictoria.html'): {
        'old_title': '<h1>Sistemas de producto para <span>operaciones reales.</span></h1>',
        'new_title': '<h1>Construyendo productos de workforce para operaciones reales.</h1>',
        'scope_end': '</section>\n<section class="products">',
        'role': '''</section>\n<section class="geo-role"><div class="shell geo-role-grid reveal"><div><div class="kicker">Mi rol</div></div><div><h2>Liderando decisiones de producto desde discovery hasta adopción real.</h2><p>Mi rol conectaba clientes, producto, ingeniería, implementación y equipos comerciales. Traducía complejidad operativa en prioridades, planes de validación y decisiones de lanzamiento en distintos mercados de LATAM.</p><div class="geo-role-cards"><article><span>01 / Estrategia de producto</span><h3>Convertir problemas de clientes en decisiones de producto.</h3><p>Definición de prioridades, reglas y roadmap entre planificación, optimización y workflows de turnos.</p></article><article><span>02 / Validación y pilotos</span><h3>Probar con operaciones reales antes de escalar.</h3><p>Lideré 100+ validaciones y pilotos para probar usabilidad, reglas y valor con clientes enterprise.</p></article><article><span>03 / Ejecución cross-functional</span><h3>Conectar producto con la realidad comercial.</h3><p>Trabajé con ingeniería, implementación, ventas y clientes para mover productos hacia adopción y producción.</p></article></div></div></div></section>\n<section class="products">'''
    }
}

css = '''.geo-role{padding:82px var(--page);background:#f7f9fb;border-top:1px solid #e0e6ec;border-bottom:1px solid #e0e6ec}.geo-role-grid{display:grid;grid-template-columns:.42fr 1.15fr;gap:72px}.geo-role h2{margin:0 0 18px;max-width:780px;font-family:Manrope,sans-serif;font-size:clamp(34px,3.5vw,48px);line-height:1.06;letter-spacing:-.045em;font-weight:500}.geo-role p{margin:0;max-width:820px;color:var(--muted);font-size:13px;line-height:1.75}.geo-role-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:30px}.geo-role-cards article{padding:22px;border:1px solid #dbe2e8;border-radius:17px;background:#fff}.geo-role-cards span{font-size:9px;font-weight:700;color:var(--blue);letter-spacing:.08em}.geo-role-cards h3{margin:18px 0 0;font-family:Manrope,sans-serif;font-size:22px;line-height:1.18;letter-spacing:-.035em;font-weight:500}.geo-role-cards article p{margin-top:10px;font-size:12px;line-height:1.7}@media(max-width:1000px){.geo-role-grid{grid-template-columns:1fr}.geo-role-cards{grid-template-columns:1fr}}'''

for path, cfg in files.items():
    text = path.read_text()
    text = text.replace(cfg['old_title'], cfg['new_title'])
    text = text.replace('.hero h1 span{display:block;color:#98a4af}', '')
    if '.geo-role{' not in text:
        text = text.replace('.products{', css + '.products{', 1)
    if cfg['scope_end'] in text and 'class="geo-role"' not in text:
        text = text.replace(cfg['scope_end'], cfg['role'], 1)
    path.write_text(text)
