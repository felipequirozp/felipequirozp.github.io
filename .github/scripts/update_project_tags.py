from pathlib import Path

for rel in ['projects.html','es/projects.html']:
    p=Path(rel)
    s=p.read_text(encoding='utf-8')

    # First three Tether projects: restore original impact/context tags and keep business-model tags.
    s=s.replace('<div class="impact"><span>B2G</span><span>B2C</span><span>B2B</span></div>', '<div class="impact"><span>LATAM · U.S. · Europe</span><span>EdTech</span><span>B2G</span><span>B2C</span><span>B2B</span></div>', 1)
    s=s.replace('<div class="impact"><span>B2G</span><span>B2B</span><span>B2C</span></div>', '<div class="impact"><span>78 institutions</span><span>35k+ students</span><span>B2G</span><span>B2B</span><span>B2C</span></div>', 1)
    s=s.replace('<div class="impact"><span>B2G</span><span>B2B</span><span>B2C</span></div>', '<div class="impact"><span>50+ public schools</span><span>Responsible AI</span><span>B2G</span><span>B2B</span><span>B2C</span></div>', 1)

    if rel.startswith('es/'):
        s=s.replace('LATAM · U.S. · Europe', 'LATAM · U.S. · Europa')
        s=s.replace('78 institutions', '78 establecimientos')
        s=s.replace('35k+ students', '35k+ estudiantes')
        s=s.replace('50+ public schools', '50+ escuelas públicas')
        s=s.replace('Responsible AI', 'IA responsable')

    # Tether Studio: keep AI context and add all three models.
    s=s.replace('<div class="impact"><span>B2G</span><span>B2B</span><span>B2C</span></div>', '<div class="impact"><span>AI-enabled</span><span>B2G</span><span>B2B</span><span>B2C</span></div>', 1)

    # GeoVictoria: restore execution/scale tags and add B2B.
    s=s.replace('<div class="impact"><span>B2B</span></div>', '<div class="impact"><span>MVP → production</span><span>Enterprise pilots</span><span>B2B</span></div>', 1)
    s=s.replace('<div class="impact"><span>B2B</span></div>', '<div class="impact"><span>0→1</span><span>5 markets</span><span>B2B</span></div>', 1)

    if rel.startswith('es/'):
        s=s.replace('MVP → production', 'MVP → producción')
        s=s.replace('Enterprise pilots', 'Pilotos enterprise')
        s=s.replace('5 markets', '5 mercados')

    p.write_text(s, encoding='utf-8')

# Keep the GeoVictoria role period shown as ongoing in the case study.
for rel in ['geovictoria.html','es/geovictoria.html']:
    p=Path(rel)
    if not p.exists():
        continue
    s=p.read_text(encoding='utf-8')
    s=s.replace('July — September 2026', 'July 2026 — Present')
    s=s.replace('Julio — Septiembre 2026', 'Julio 2026 — Presente')
    p.write_text(s, encoding='utf-8')
