from pathlib import Path

files = [Path('people.html'), Path('es/people.html')]
old = '''.people-all{padding:82px var(--page);background:linear-gradient(180deg,#fff 0%,#f5f8fa 100%);border-bottom:1px solid var(--line)}
.people-head{margin-bottom:34px}.people-head h2{margin:12px 0 0;max-width:840px;font-family:Manrope,sans-serif;font-size:clamp(32px,3.3vw,46px);line-height:1.06;letter-spacing:-.045em;font-weight:500}
.people-all .people-grid{grid-template-columns:repeat(4,minmax(0,1fr));gap:30px 22px}
.company-tag{margin-bottom:10px;color:var(--blue);font-size:9px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.portrait{aspect-ratio:auto!important;min-height:0!important;height:auto!important;padding:18px;border-radius:16px!important;background:linear-gradient(145deg,#e7edf2,#f2f5f7)!important;border:1px solid #dbe3e9!important;overflow:hidden}
.portrait-inner{width:100%;aspect-ratio:4/4.65;overflow:hidden;border-radius:12px;background:#dce5eb}
'''
new = '''.people-all{padding:82px var(--page);background:linear-gradient(180deg,#fff 0%,#f7f9fb 55%,#f1f5f8 100%);border-bottom:1px solid var(--line)}
.people-head{margin-bottom:38px}.people-head h2{margin:12px 0 0;max-width:840px;font-family:Manrope,sans-serif;font-size:clamp(32px,3.3vw,46px);line-height:1.06;letter-spacing:-.045em;font-weight:500}
.people-all .people-grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:34px 16px}
.company-tag{margin-bottom:9px;color:var(--blue);font-size:8px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.portrait{aspect-ratio:auto!important;min-height:0!important;height:auto!important;padding:0;border-radius:14px!important;background:transparent!important;border:0!important;overflow:hidden}
.portrait-inner{width:100%;aspect-ratio:4/4.75;overflow:hidden;border-radius:14px;background:linear-gradient(145deg,#d8e2ea 0%,#edf3f7 58%,#d5e0e8 100%);box-shadow:inset 0 0 0 1px rgba(17,35,52,.06)}
'''
old_breakpoints = '''@media(max-width:1180px){.people-all .people-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:900px){.people-all .people-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:700px){.people-all{padding:62px var(--page)}.people-all .people-grid{grid-template-columns:1fr 1fr;gap:28px 14px}.people-head{margin-bottom:28px}.portrait{padding:10px}.person h3{font-size:18px}.role{font-size:10px}.context{font-size:9px}}
@media(max-width:480px){.people-all .people-grid{grid-template-columns:1fr}.portrait{padding:14px}.portrait-inner{aspect-ratio:4/4.5}}'''
new_breakpoints = '''@media(max-width:1320px){.people-all .people-grid{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media(max-width:1100px){.people-all .people-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:900px){.people-all .people-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:700px){.people-all{padding:62px var(--page)}.people-all .people-grid{grid-template-columns:1fr 1fr;gap:30px 14px}.people-head{margin-bottom:28px}.person h3{font-size:18px}.role{font-size:10px}.context{font-size:9px}}
@media(max-width:480px){.people-all .people-grid{grid-template-columns:1fr 1fr;gap:28px 12px}.portrait-inner{aspect-ratio:4/4.8}.person h3{font-size:16px}.company-tag{font-size:7px}}'''

for p in files:
    text = p.read_text()
    if old not in text:
        raise SystemExit(f'base People styles not found in {p}')
    text = text.replace(old, new, 1)
    if old_breakpoints not in text:
        raise SystemExit(f'People breakpoints not found in {p}')
    text = text.replace(old_breakpoints, new_breakpoints, 1)
    p.write_text(text)
    print('updated', p)
