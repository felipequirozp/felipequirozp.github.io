from pathlib import Path
import re

entries = {
    Path('people.html'): '''<article class="person"><div class="portrait"><img src="/images/yuz-rector.png" alt="Juan Yuz"></div><div class="person-copy"><h3>Juan Yuz</h3><div class="role">Rector · Universidad Técnica Federico Santa María</div><div class="context">Worked within the university leadership environment across academic and institutional initiatives.</div></div></article>''',
    Path('es/people.html'): '''<article class="person"><div class="portrait"><img src="/images/yuz-rector.png" alt="Juan Yuz"></div><div class="person-copy"><h3>Juan Yuz</h3><div class="role">Rector · Universidad Técnica Federico Santa María</div><div class="context">Trabajé dentro del entorno de liderazgo universitario en iniciativas académicas e institucionales.</div></div></article>''',
}

pattern = re.compile(r'(<article class="person"><div class="portrait"><img src="/images/karen-radonich\.jpg".*?</article>)', re.S)

for path, card in entries.items():
    text = path.read_text(encoding='utf-8')
    if 'yuz-rector.png' in text:
        continue
    updated, n = pattern.subn(r'\1' + card, text, count=1)
    if n != 1:
        raise RuntimeError(f'Could not locate Karen Radonich card in {path}')
    path.write_text(updated, encoding='utf-8')
