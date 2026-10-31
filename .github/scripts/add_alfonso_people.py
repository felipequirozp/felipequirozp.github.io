from pathlib import Path

FILES = [Path('people.html'), Path('es/people.html')]

IGNACIO = '<article class="person"><a class="card-link" href="https://www.linkedin.com/in/ignacio-lepe-6026b4215/" target="_blank" rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a><div class="portrait"><div class="portrait-inner"><img src="/images/people/ignacio-lepe.png?v=20261030-0202" alt="Ignacio Lepe" loading="lazy"></div></div><div class="person-copy"><h3>Ignacio Lepe</h3></div></article>'
ALFONSO = '<article class="person"><div class="portrait"><div class="portrait-inner"><img src="/images/alfonso.png?v=20261031" alt="Alfonso" loading="lazy"></div></div><div class="person-copy"><h3>Alfonso</h3></div></article>'

for path in FILES:
    text = path.read_text(encoding='utf-8')
    if ALFONSO in text:
        continue
    if IGNACIO not in text:
        raise RuntimeError(f'Ignacio Lepe card not found in {path}')
    text = text.replace(IGNACIO, IGNACIO + ALFONSO, 1)
    path.write_text(text, encoding='utf-8')
