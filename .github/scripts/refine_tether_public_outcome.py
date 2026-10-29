from pathlib import Path

paths = [
    Path('tethered/digital-transformation-public-education.html'),
    Path('es/tethered/transformacion-digital-educacion-publica.html'),
]

old = '.media-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:stretch}.media{overflow:hidden;border-radius:22px;background:#e2eaf0;min-height:360px}.media img{width:100%;height:100%;object-fit:cover}.result-box{padding:30px;border-radius:22px;background:#0b1117;color:#fff;display:flex;flex-direction:column;justify-content:space-between}.result-box h3{margin:16px 0 0;font-family:Manrope,sans-serif;font-size:32px;font-weight:500;letter-spacing:-.04em}.result-box p{color:#aeb8c1}.chips{display:flex;gap:8px;flex-wrap:wrap}.chips span{padding:8px 10px;border:1px solid rgba(255,255,255,.2);border-radius:999px;font-size:9px;color:#d4dce3}'
new = '.media-grid{display:grid;grid-template-columns:1.08fr .92fr;gap:28px;align-items:stretch}.media{overflow:hidden;border-radius:22px;background:#e2eaf0;min-height:360px}.media img{width:100%;height:100%;object-fit:cover}.result-box{padding:8px 8px 8px 10px;background:#fff;color:var(--ink);display:flex;flex-direction:column;justify-content:center}.result-box .kicker{margin-bottom:4px}.result-box h3{margin:14px 0 0;max-width:620px;font-family:Manrope,sans-serif;font-size:clamp(28px,3vw,42px);line-height:1.08;font-weight:500;letter-spacing:-.04em}.result-box p{margin-top:16px;max-width:620px;color:var(--muted)}.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}.chips span{padding:8px 10px;border:1px solid #dbe2e8;border-radius:999px;background:#f7f9fb;font-size:9px;color:#5f6b78;font-weight:600}'

for path in paths:
    s = path.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'Expected outcome CSS not found in {path}')
    s = s.replace(old, new)
    path.write_text(s, encoding='utf-8')
