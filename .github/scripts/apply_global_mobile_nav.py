from pathlib import Path

ROOT = Path('.')
SCRIPT = '<script src="/mobile-nav.js" defer></script>'
HOME_FIXES = '''<style id="home-mobile-polish">\n@media(max-width:700px){\n.hero{padding:46px var(--page) 58px!important}.hero-grid{gap:34px!important}.hero h1{font-size:clamp(42px,12vw,56px)!important;line-height:1.01!important}.hero-copy{font-size:14px!important;line-height:1.72!important}.hero-actions{margin-top:22px!important}.hero-portrait{width:100%!important;max-width:320px!important}.hero-photo{border-radius:18px!important}.companies{padding:0!important}.company-grid{grid-template-columns:1fr 1fr!important}.company{min-height:88px!important;padding:18px!important;justify-content:center!important;border-bottom:1px solid var(--line)!important}.company:first-child{padding-left:18px!important}.company img{max-width:135px!important;max-height:30px!important}.company.tether img{max-width:165px!important;max-height:38px!important}.section{padding:64px var(--page)!important}.section-head,.projects-head,.how-head,.ideas-strip .ideas,.closing-inner{gap:24px!important}.work-list{margin-top:26px!important}.work-row{gap:20px!important;padding:28px 0!important}.work-row:hover{padding-left:0!important}.work-main h3{font-size:30px!important}.work-aside .dark-logo{margin-left:-10px!important}.work-aside .dark-logo img{max-width:185px!important;max-height:42px!important}.projects-section{padding:68px var(--page) 74px!important}.projects{gap:14px!important;margin-top:30px!important}.project{min-height:280px!important;padding:24px!important}.project-index{font-size:46px!important}.project h3{font-size:25px!important}.how{padding:68px var(--page)!important}.how .principles{margin-top:30px!important}.ideas-strip{padding:58px var(--page)!important}.ideas-strip .ideas{grid-template-columns:1fr!important}.idea-links{margin-top:6px!important}.closing-inner{padding:54px 0!important}.closing h2{font-size:40px!important}.footer{padding-left:var(--page)!important;padding-right:var(--page)!important}\n}\n</style>'''

changed = []
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts or '.github' in path.parts:
        continue
    s = path.read_text(encoding='utf-8')
    if '<header class="nav"' not in s:
        continue
    original = s
    if '/mobile-nav.js' not in s:
        s = s.replace('</body>', SCRIPT + '</body>')
    if path.as_posix() in ('index.html','es/index.html'):
        s = s.replace('.work-aside .dark-logo{width:max-content;padding:0;border-radius:0;background:transparent}', '.work-aside .dark-logo{width:max-content;padding:0;border-radius:0;background:transparent;margin-left:-14px}')
        s = s.replace('.work-aside .dark-logo img{max-height:34px;max-width:150px}', '.work-aside .dark-logo img{max-height:42px;max-width:190px}')
        if 'id="home-mobile-polish"' not in s:
            s = s.replace('</head>', HOME_FIXES + '</head>')
    if s != original:
        path.write_text(s, encoding='utf-8')
        changed.append(path.as_posix())

print(f'Updated {len(changed)} HTML files')
for p in changed:
    print(p)
