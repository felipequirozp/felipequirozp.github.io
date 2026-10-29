from pathlib import Path

# one-off spacing tune
for rel in ['about.html','es/about.html']:
    p=Path(rel)
    s=p.read_text(encoding='utf-8')
    s=s.replace('.story h2{margin:0;max-width:720px;', '.story h2{margin:0 0 20px;max-width:720px;')
    s=s.replace('.story-copy p{margin:0 0 16px;', '.story-copy p{margin:0 0 20px;')
    p.write_text(s,encoding='utf-8')
