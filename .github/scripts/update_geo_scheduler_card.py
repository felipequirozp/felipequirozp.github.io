from pathlib import Path

repls = {
    Path('geovictoria.html'): [
        ('/images/geo-smart-scheduler.webp', '/images/planificador.png'),
        ('<h3>Smart Scheduler</h3>', '<h3>Smart Scheduler</h3>'),
        ('<span class="product-link">View product ↗</span>', '<a class="product-link" href="/geovictoria/smart-scheduler">View project ↗</a>'),
    ],
    Path('es/geovictoria.html'): [
        ('/images/geo-smart-scheduler.webp', '/images/planificador.png'),
        ('<span class="product-link">Ver producto ↗</span>', '<a class="product-link" href="/es/geovictoria/smart-scheduler">Ver proyecto ↗</a>'),
    ],
}

for path, pairs in repls.items():
    text = path.read_text(encoding='utf-8')
    # Update only the Smart Scheduler / Planificador Inteligente row link if there is no link yet.
    text = text.replace('/images/geo-smart-scheduler.webp', '/images/planificador.png')
    marker = '<h3>Smart Scheduler</h3>' if path.name == 'geovictoria.html' and path.parent.name != 'es' else '<h3>Planificador Inteligente</h3>'
    idx = text.find(marker)
    if idx != -1:
        row_start = text.rfind('<article class="product-row', 0, idx)
        if row_start == -1:
            row_start = text.rfind('<div class="product-row', 0, idx)
        row_end = text.find('</article>', idx)
        if row_end == -1:
            row_end = text.find('</div></div></article>', idx)
        if row_end == -1:
            row_end = text.find('</section>', idx)
        segment = text[row_start:row_end] if row_start != -1 and row_end != -1 else ''
        href = '/geovictoria/smart-scheduler' if path.parent.name != 'es' else '/es/geovictoria/smart-scheduler'
        label = 'View project ↗' if path.parent.name != 'es' else 'Ver proyecto ↗'
        if segment and href not in segment:
            # Prefer replacing an existing non-linked product-link span inside this row.
            old = '<span class="product-link">View product ↗</span>' if path.parent.name != 'es' else '<span class="product-link">Ver producto ↗</span>'
            new = f'<a class="product-link" href="{href}">{label}</a>'
            if old in segment:
                segment2 = segment.replace(old, new, 1)
            else:
                # Add a link after contribution block / paragraph if no CTA exists.
                insert_at = segment.rfind('</div>')
                segment2 = segment[:insert_at] + new + segment[insert_at:] if insert_at != -1 else segment
            text = text[:row_start] + segment2 + text[row_end:]
    path.write_text(text, encoding='utf-8')
