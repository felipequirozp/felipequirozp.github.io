from pathlib import Path

for path in [Path('blog.html'), Path('es/blog.html')]:
    text = path.read_text(encoding='utf-8')
    old = '.hero h1 span{display:block;color:#9aa6b2}'
    new = '.hero h1 span{display:block;color:inherit}'
    if old not in text:
        raise SystemExit(f'Expected hero title style not found in {path}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')
    print(f'updated {path}')
