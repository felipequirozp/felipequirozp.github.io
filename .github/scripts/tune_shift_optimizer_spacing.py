from pathlib import Path

# Applies spacing polish to both Shift Optimizer locales.
for rel in ['geovictoria/shift-optimizer.html','es/geovictoria/shift-optimizer.html']:
    p = Path(rel)
    s = p.read_text(encoding='utf-8')

    # Remove the visual back-link entirely.
    s = s.replace('<a class="back" href="/geovictoria">← GeoVictoria</a>', '')
    s = s.replace('<a class="back" href="/es/geovictoria">← GeoVictoria</a>', '')

    # More breathing room in hero and section typography.
    s = s.replace('.back{display:inline-flex;margin-bottom:22px;color:#6a7783;font-size:10px;font-weight:600}.back:hover{color:var(--blue)}', '')
    s = s.replace('.hero h1{margin:14px 0 0;', '.hero h1{margin:24px 0 0;')
    s = s.replace('.hero p{margin:22px 0 0;max-width:650px;color:#4d5965;font-size:14px;line-height:1.76}', '.hero p{margin:28px 0 0;max-width:650px;color:#4d5965;font-size:14px;line-height:1.84}')
    s = s.replace('.section h2{margin:0 0 18px;', '.section h2{margin:18px 0 24px;')
    s = s.replace('.section p{margin:0 0 16px;max-width:820px;color:var(--muted);font-size:13px;line-height:1.76}', '.section p{margin:0 0 20px;max-width:820px;color:var(--muted);font-size:13px;line-height:1.84}')
    s = s.replace('.logic-card p{margin:9px 0 0;font-size:12px;line-height:1.65}', '.logic-card p{margin:11px 0 0;font-size:12px;line-height:1.72}')

    p.write_text(s, encoding='utf-8')
