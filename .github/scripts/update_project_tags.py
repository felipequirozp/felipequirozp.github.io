from pathlib import Path

# Keep Projects business-model tags aligned across EN and ES.
for rel in ['projects.html','es/projects.html']:
    p=Path(rel)
    s=p.read_text(encoding='utf-8')
    s=s.replace('<div class="impact"><span>AI-enabled</span><span>B2B · B2C</span></div>', '<div class="impact"><span>B2G</span><span>B2B</span><span>B2C</span></div>')
    s=s.replace('<div class="impact"><span>MVP → production</span><span>Enterprise pilots</span></div>', '<div class="impact"><span>B2B</span></div>')
    s=s.replace('<div class="impact"><span>0→1</span><span>5 markets</span></div>', '<div class="impact"><span>B2B</span></div>')
    s=s.replace('<div class="impact"><span>MVP → producción</span><span>Pilotos enterprise</span></div>', '<div class="impact"><span>B2B</span></div>')
    s=s.replace('<div class="impact"><span>0→1</span><span>5 mercados</span></div>', '<div class="impact"><span>B2B</span></div>')
    p.write_text(s, encoding='utf-8')
