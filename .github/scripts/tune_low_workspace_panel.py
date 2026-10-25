from pathlib import Path

FILES = [Path('lowsignal/low-workspace.html'), Path('es/lowsignal/low-workspace.html')]

for path in FILES:
    text = path.read_text(encoding='utf-8')

    old_hero = '.hero-media{margin:0;min-width:0}.hero-media img{width:100%;height:auto;border:1px solid #dce2e8;box-shadow:0 22px 54px rgba(11,17,23,.09)}.hero-media figcaption{margin-top:10px;color:var(--muted-2);font-size:10px;line-height:1.5}'
    new_hero = '.hero-media{margin:0;min-width:0;overflow:hidden;border-radius:12px;box-shadow:0 22px 54px rgba(11,17,23,.09)}.hero-media img{width:100%;height:auto;display:block;transform:translateY(-3px);margin-bottom:-3px;border:0;border-radius:12px}.hero-media figcaption{margin-top:10px;padding:0 2px 2px;color:var(--muted-2);font-size:10px;line-height:1.5}'

    old_product = '.product-shot{width:min(var(--max),100%);margin:0 auto}.product-shot img{width:100%;height:auto;border:1px solid #dce2e8;background:#fff;box-shadow:0 20px 50px rgba(11,17,23,.08)}.product-shot figcaption{margin-top:12px;color:var(--muted-2);font-size:11px;line-height:1.55}'
    new_product = '.product-shot{width:min(var(--max),100%);margin:0 auto}.product-shot img{width:100%;height:auto;display:block;transform:translateY(-3px);margin-bottom:-3px;border:0;border-radius:12px;background:#fff;box-shadow:0 20px 50px rgba(11,17,23,.08);clip-path:inset(3px 0 0 0 round 12px)}.product-shot figcaption{margin-top:12px;color:var(--muted-2);font-size:11px;line-height:1.55}'

    if old_hero not in text:
        raise SystemExit(f'Hero CSS pattern not found in {path}')
    if old_product not in text:
        raise SystemExit(f'Product CSS pattern not found in {path}')

    text = text.replace(old_hero, new_hero, 1).replace(old_product, new_product, 1)
    path.write_text(text, encoding='utf-8')
