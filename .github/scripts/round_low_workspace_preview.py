from pathlib import Path

paths = [Path('lowsignal.html'), Path('es/lowsignal.html')]
old_visual = ".low-workspace-feature__visual{display:block;overflow:hidden;border:1px solid #dfe3e9;background:#fff;box-shadow:0 24px 60px rgba(21,26,44,.10)}"
new_visual = ".low-workspace-feature__visual{display:block;overflow:hidden;border:1px solid #dfe3e9;border-radius:18px;background:#fff;box-shadow:0 24px 60px rgba(21,26,44,.10)}"
old_img = ".low-workspace-feature__visual img{display:block;width:100%;height:auto}"
new_img = ".low-workspace-feature__visual img{display:block;width:100%;height:auto;border-radius:18px}"

for path in paths:
    text = path.read_text(encoding='utf-8')
    if old_visual not in text or old_img not in text:
        raise SystemExit(f'Expected Low Workspace preview CSS not found in {path}')
    text = text.replace(old_visual, new_visual, 1)
    text = text.replace(old_img, new_img, 1)
    path.write_text(text, encoding='utf-8')
