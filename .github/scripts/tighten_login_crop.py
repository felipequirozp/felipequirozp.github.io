from pathlib import Path

paths = [Path('lowsignal/low-workspace.html'), Path('es/lowsignal/low-workspace.html')]
for path in paths:
    text = path.read_text(encoding='utf-8')
    old = ".login-visual img{width:100%;height:auto;display:block;transform:translateY(-4px);margin-bottom:-4px;border:0;border-radius:12px;background:#fff}"
    new = ".login-visual img{width:100%;height:auto;display:block;transform:translateY(-7px);margin-bottom:-7px;border:0;border-radius:12px;background:#fff;clip-path:inset(7px 0 0 0 round 12px)}"
    if old not in text:
        raise SystemExit(f'Expected login crop CSS not found in {path}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')
