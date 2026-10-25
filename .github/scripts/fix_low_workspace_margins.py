from pathlib import Path

for path in [Path('low-workspace.html'), Path('es/low-workspace.html')]:
    text = path.read_text(encoding='utf-8')
    old = '--page:clamp(22px,4vw,64px);--max:1520px'
    new = '--page:8vw;--max:1520px'
    if old not in text:
        raise RuntimeError(f'Expected margin token not found in {path}')
    text = text.replace(old, new, 1)
    path.write_text(text, encoding='utf-8')
