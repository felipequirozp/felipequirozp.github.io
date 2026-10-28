from pathlib import Path

OLD = '<div class="mini-media"><img src="/images/tether-edtech-scale.jpg" alt="Tether Education"></div>'
NEW = '<div class="mini-media explorer-demo"><video autoplay loop muted playsinline preload="metadata" aria-label="Virtual School Explorer product demo"><source src="/videos/virtual-school-explorer.mp4" type="video/mp4"></video></div>'

for path in [Path('.github/scripts/build_projects_section_v2.py'), Path('projects.html'), Path('es/projects.html')]:
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    text = text.replace(OLD, NEW)
    # Add video styling alongside existing mini media styling.
    marker = '.mini-media img{width:100%;height:100%;object-fit:cover}'
    addition = marker + '.mini-media video{display:block;width:100%;height:100%;object-fit:cover}.mini-media.explorer-demo{background:#10151c}.mini-media.explorer-demo video{object-fit:contain}'
    if marker in text and '.mini-media.explorer-demo' not in text:
        text = text.replace(marker, addition)
    path.write_text(text, encoding='utf-8')
