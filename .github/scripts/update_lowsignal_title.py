from pathlib import Path

updates = {
    Path('lowsignal.html'): ('<h1>Building growth systems.<span>Not isolated actions.</span></h1>', '<h1>Building connected systems for sustainable growth.</h1>'),
    Path('es/lowsignal.html'): ('<h1>Construyendo sistemas de crecimiento.<span>No acciones aisladas.</span></h1>', '<h1>Construyendo sistemas conectados para un crecimiento sostenible.</h1>'),
}

for path, (old, new) in updates.items():
    text = path.read_text(encoding='utf-8')
    if new in text:
        print('already updated', path)
        continue
    if old not in text:
        raise SystemExit(f'title pattern not found in {path}')
    text = text.replace(old, new, 1)
    text = text.replace('.hero h1 span{display:block;color:#98a4af}', '', 1)
    path.write_text(text, encoding='utf-8')
    print('updated', path)
