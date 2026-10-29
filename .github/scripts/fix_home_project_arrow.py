from pathlib import Path

for path in [Path('index.html'), Path('es/index.html')]:
    s = path.read_text()

    # Only style the CTA wrapper itself, not the nested SVG span.
    s = s.replace(
        '.project span{display:inline-flex;align-items:center;margin-top:26px;font-size:10px;font-weight:700}',
        '.project>span{display:inline-flex;align-items:center;gap:6px;margin-top:26px;font-size:10px;font-weight:700}'
    )

    # The arrow already has its own width/height; remove extra left margin inside project CTAs.
    s = s.replace(
        '.arrow-icon{display:inline-flex;width:14px;height:14px;margin-left:6px;vertical-align:-2px;flex:0 0 auto}',
        '.arrow-icon{display:inline-flex;width:14px;height:14px;margin-left:6px;vertical-align:-2px;flex:0 0 auto}.project>span .arrow-icon{margin-left:0;vertical-align:0}'
    )

    path.write_text(s)

print('fixed project CTA arrow alignment')
