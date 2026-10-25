from pathlib import Path

paths = [
    Path('lowsignal/low-workspace.html'),
    Path('es/lowsignal/low-workspace.html'),
]

for path in paths:
    text = path.read_text(encoding='utf-8')
    anchor = '.section.dark{background:var(--dark);color:#fff}'
    addition = anchor + '.dark .section-label{color:#5aa7ff}'
    if '.dark .section-label{color:#5aa7ff}' not in text:
        if anchor not in text:
            raise SystemExit(f'Anchor not found in {path}')
        text = text.replace(anchor, addition, 1)
        path.write_text(text, encoding='utf-8')
