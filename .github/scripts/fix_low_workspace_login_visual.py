from pathlib import Path

paths = [Path('lowsignal/low-workspace.html'), Path('es/lowsignal/low-workspace.html')]
old = ".login-visual img{width:100%;height:auto;border:1px solid #dce2e8;background:#fff}"
new = ".login-visual{overflow:hidden;border-radius:12px}.login-visual img{width:100%;height:auto;display:block;transform:translateY(-4px);margin-bottom:-4px;border:0;border-radius:12px;background:#fff}"

for path in paths:
    text = path.read_text(encoding='utf-8')
    if old in text:
        text = text.replace(old, new)
    elif new not in text:
        raise SystemExit(f'Expected login visual CSS not found in {path}')
    path.write_text(text, encoding='utf-8')
