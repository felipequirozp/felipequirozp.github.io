from pathlib import Path

for path in [Path('projects.html'), Path('es/projects.html')]:
    s = path.read_text(encoding='utf-8')
    s = s.replace('.meta{display:flex;justify-content:space-between;gap:16px;color:#75828e;font-size:9px;font-weight:700;letter-spacing:.09em;text-transform:uppercase}', '.meta{display:flex;justify-content:space-between;gap:16px;color:#75828e;font-size:10px;font-weight:600;letter-spacing:0;text-transform:none}')
    path.write_text(s, encoding='utf-8')
