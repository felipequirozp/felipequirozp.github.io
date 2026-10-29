from pathlib import Path

for path in [Path('index.html'), Path('es/index.html')]:
    text = path.read_text(encoding='utf-8')
    text = text.replace('.company.tether{background:#0d1724;margin:18px;border-radius:12px}.company.tether img{max-height:28px}', '.company.tether{background:transparent;margin:0;border-radius:0}.company.tether img{max-height:34px;max-width:170px}')
    text = text.replace('.work-aside .dark-logo{width:max-content;padding:8px 11px;border-radius:10px;background:#0d1724}.work-aside .dark-logo img{max-height:24px}', '.work-aside .dark-logo{width:max-content;padding:0;border-radius:0;background:transparent}.work-aside .dark-logo img{max-height:34px;max-width:150px}')
    text = text.replace('.company.tether{margin:12px}', '.company.tether{margin:0}')
    path.write_text(text, encoding='utf-8')
    print('updated', path)
