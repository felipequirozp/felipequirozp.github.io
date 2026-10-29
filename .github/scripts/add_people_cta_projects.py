from pathlib import Path

pages = [
    (Path('projects.html'), '/people', "People I’ve built with"),
    (Path('es/projects.html'), '/es/people', 'Personas con las que he construido'),
]

css = '''<style id="people-projects-cta">
.people-cta{margin-top:24px;display:inline-flex;align-items:center;min-height:42px;padding:0 15px;border:1px solid #c8d3dc;border-radius:999px;background:#fff;color:#0b1117;font-size:10px;font-weight:700;transition:background .18s,color .18s,border-color .18s,transform .18s}.people-cta:hover{background:#0b1117;color:#fff;border-color:#0b1117;transform:translateY(-1px)}
</style>'''

for path, href, label in pages:
    text = path.read_text(encoding='utf-8')
    if 'id="people-projects-cta"' not in text:
        text = text.replace('</head>', css + '</head>')
    if 'class="people-cta"' not in text:
        marker = '</p></div></section>\n<section class="stats-wrap">'
        replacement = f'</p><a class="people-cta" href="{href}">{label}</a></div></section>\n<section class="stats-wrap">'
        if marker not in text:
            raise SystemExit(f'Hero marker not found in {path}')
        text = text.replace(marker, replacement, 1)
    path.write_text(text, encoding='utf-8')
