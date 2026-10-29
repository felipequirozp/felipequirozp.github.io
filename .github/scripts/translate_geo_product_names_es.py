from pathlib import Path

replacements = {
    'Smart Scheduler': 'Planificador Inteligente',
    'Shift Optimizer': 'Optimizador de Turnos',
    'Shift Change Workflow': 'Flujo de Cambio de Turnos',
}

changed = []
for p in Path('es').rglob('*.html'):
    s = p.read_text(encoding='utf-8')
    original = s
    for old, new in replacements.items():
        s = s.replace(old, new)
    if s != original:
        p.write_text(s, encoding='utf-8')
        changed.append(str(p))

# Keep future generators from reintroducing the English product names in ES output.
for rel in ['.github/scripts/build_projects_section_v2.py', '.github/scripts/sync_geovictoria_pages.py']:
    p = Path(rel)
    if not p.exists():
        continue
    s = p.read_text(encoding='utf-8')
    marker = '# ES GeoVictoria product-name normalization'
    if marker in s:
        continue
    s += '''\n\n# ES GeoVictoria product-name normalization\nfor _rel in [\n    'es/index.html',\n    'es/projects.html',\n    'es/geovictoria.html',\n    'es/geovictoria/shift-optimizer.html',\n    'es/geovictoria/shift-change-workflow.html',\n]:\n    _p = Path(_rel)\n    if not _p.exists():\n        continue\n    _s = _p.read_text(encoding='utf-8')\n    _s = _s.replace('Smart Scheduler', 'Planificador Inteligente')\n    _s = _s.replace('Shift Optimizer', 'Optimizador de Turnos')\n    _s = _s.replace('Shift Change Workflow', 'Flujo de Cambio de Turnos')\n    _p.write_text(_s, encoding='utf-8')\n'''
    p.write_text(s, encoding='utf-8')

print(f'Updated {len(changed)} Spanish HTML files')
for item in changed:
    print(item)
