from pathlib import Path

pairs = [
    (
        Path('tethereducation.html'),
        [
            ('<article class="program"><small>Public education</small><h3>SLEP del Pino</h3><p>78 institutions, 35,000+ students, 200+ staff and 5,000+ digital enrollments.</p></article>', '<a class="program" href="/tethered/digital-transformation-public-education"><small>Public education</small><h3>SLEP del Pino</h3><p>78 institutions, 35,000+ students, 200+ staff and 5,000+ digital enrollments.</p><span class="program-link">View project ↗</span></a>'),
            ('<article class="program"><small>Applied AI</small><h3>AI-powered Education Transformation</h3><p>OpenAI and Anthropic partnerships supporting responsible AI adoption in 50+ public schools.</p></article>', '<a class="program" href="/tethered/ai-powered-education-transformation"><small>Applied AI</small><h3>AI-powered Education Transformation</h3><p>OpenAI and Anthropic partnerships supporting responsible AI adoption in 50+ public schools.</p><span class="program-link">View project ↗</span></a>'),
            ('<article class="program"><small>School choice</small><h3>Virtual School Explorer</h3><p>Digital school-discovery experiences across LATAM, the U.S. and Europe.</p></article>', '<a class="program" href="/tethered/virtual-school-explorer"><small>School choice</small><h3>Virtual School Explorer</h3><p>Digital school-discovery experiences across LATAM, the U.S. and Europe.</p><span class="program-link">View project ↗</span></a>'),
            ('<article class="program"><small>Product ecosystem</small><h3>Tether Studio</h3><p>AI-enabled product and experimentation work across the broader Tether platform.</p></article>', '<a class="program" href="/tethered/tether-studio"><small>Product ecosystem</small><h3>Tether Studio</h3><p>AI-enabled product and experimentation work across the broader Tether platform.</p><span class="program-link">View project ↗</span></a>'),
        ],
    ),
    (
        Path('es/tethereducation.html'),
        [
            ('<article class="program"><small>Educación pública</small><h3>SLEP del Pino</h3><p>78 establecimientos, 35.000+ estudiantes, 200+ funcionarios y 5.000+ matrículas digitales.</p></article>', '<a class="program" href="/es/tethered/transformacion-digital-educacion-publica"><small>Educación pública</small><h3>SLEP del Pino</h3><p>78 establecimientos, 35.000+ estudiantes, 200+ funcionarios y 5.000+ matrículas digitales.</p><span class="program-link">Ver proyecto ↗</span></a>'),
            ('<article class="program"><small>IA aplicada</small><h3>Transformación Educativa con IA</h3><p>Partnerships con OpenAI y Anthropic apoyando adopción responsable de IA en 50+ escuelas públicas.</p></article>', '<a class="program" href="/es/tethered/transformacion-educativa-impulsada-por-ia"><small>IA aplicada</small><h3>Transformación Educativa con IA</h3><p>Partnerships con OpenAI y Anthropic apoyando adopción responsable de IA en 50+ escuelas públicas.</p><span class="program-link">Ver proyecto ↗</span></a>'),
            ('<article class="program"><small>Elección escolar</small><h3>Explorador Virtual de Colegios</h3><p>Experiencias de descubrimiento de colegios en LATAM, Estados Unidos y Europa.</p></article>', '<a class="program" href="/es/tethered/explorador-virtual-colegios"><small>Elección escolar</small><h3>Explorador Virtual de Colegios</h3><p>Experiencias de descubrimiento de colegios en LATAM, Estados Unidos y Europa.</p><span class="program-link">Ver proyecto ↗</span></a>'),
            ('<article class="program"><small>Ecosistema de producto</small><h3>Tether Studio</h3><p>Producto y experimentación habilitados por IA dentro del ecosistema Tether.</p></article>', '<a class="program" href="/es/tethered/tether-studio"><small>Ecosistema de producto</small><h3>Tether Studio</h3><p>Producto y experimentación habilitados por IA dentro del ecosistema Tether.</p><span class="program-link">Ver proyecto ↗</span></a>'),
        ],
    ),
]

for path, replacements in pairs:
    s = path.read_text(encoding='utf-8')
    for old, new in replacements:
        s = s.replace(old, new)
    css_old = '.program{padding:24px;border:1px solid #dbe2e8;border-radius:18px;background:#fff}'
    css_new = '.program{display:block;padding:24px;border:1px solid #dbe2e8;border-radius:18px;background:#fff;transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}.program:hover{transform:translateY(-3px);border-color:#c9d6e1;box-shadow:0 18px 38px rgba(11,17,23,.07)}'
    s = s.replace(css_old, css_new)
    css_p = '.program p{margin:10px 0 0;font-size:12px;line-height:1.7}'
    css_p_new = '.program p{margin:10px 0 0;font-size:12px;line-height:1.7}.program-link{display:inline-flex;margin-top:20px;color:#0b1117;font-size:10px;font-weight:700;transition:color .18s ease,transform .18s ease}.program:hover .program-link{color:var(--blue);transform:translateX(3px)}'
    s = s.replace(css_p, css_p_new)
    path.write_text(s, encoding='utf-8')
