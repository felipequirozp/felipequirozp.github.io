from pathlib import Path

ROOT = Path('.')
SKIP = {Path('initiatives.html'), Path('es/initiatives.html')}

for path in ROOT.rglob('*.html'):
    if path in SKIP or '.git' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    original = text

    if '/es/' in '/' + str(path).replace('\\','/') or str(path).startswith('es/'):
        if '/es/initiatives' not in text and 'href="/es/projects"' in text:
            text = text.replace(
                '<a href="/es/projects">Proyectos</a>',
                '<a href="/es/projects">Proyectos</a><a href="/es/initiatives">Iniciativas</a>'
            )
            text = text.replace(
                '<a class="active" href="/es/projects">Proyectos</a>',
                '<a class="active" href="/es/projects">Proyectos</a><a href="/es/initiatives">Iniciativas</a>'
            )
    else:
        if '/initiatives' not in text and 'href="/projects"' in text:
            text = text.replace(
                '<a href="/projects">Projects</a>',
                '<a href="/projects">Projects</a><a href="/initiatives">Initiatives</a>'
            )
            text = text.replace(
                '<a class="active" href="/projects">Projects</a>',
                '<a class="active" href="/projects">Projects</a><a href="/initiatives">Initiatives</a>'
            )

    if text != original:
        path.write_text(text, encoding='utf-8')
        print(f'updated {path}')
