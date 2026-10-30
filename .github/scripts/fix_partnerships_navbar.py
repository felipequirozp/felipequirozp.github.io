from pathlib import Path

FILES = [
    Path('es/tethered/alianzas-estrategicas/index.html'),
    Path('tethered/strategic-partnerships/index.html'),
]

old_nav = ".nav{position:fixed;inset:0 0 auto;z-index:9999;height:var(--nav-h);padding:0 var(--page);display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,.96);border-bottom:1px solid rgba(11,17,23,.08);backdrop-filter:blur(16px)}.brand{font-family:Manrope;font-size:22px;font-weight:600;letter-spacing:-.045em}.nav-right,.nav-center{display:flex;align-items:center;gap:28px}.nav a{font-size:11px;font-weight:500}.nav-center a{position:relative}.nav-center a:after{content:\"\";position:absolute;left:0;bottom:-7px;width:0;height:1px;background:#111820;transition:.2s}.nav-center a:hover:after,.nav-center a.active:after{width:100%}.lang{width:38px;height:38px;display:grid;place-items:center;border:1px solid #d7dde4;border-radius:50%;font-size:10px!important;transition:.18s}.lang:hover{background:#0b1117;color:#fff;border-color:#0b1117}"

new_nav = ".nav{position:fixed;inset:0 0 auto 0;z-index:9999;height:var(--nav-h);padding:0 var(--page);display:flex;align-items:center;justify-content:space-between;gap:28px;background:rgba(255,255,255,.96);border-bottom:1px solid rgba(11,17,23,.08);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)}.brand{font-family:Manrope,sans-serif;font-size:22px!important;font-weight:600;letter-spacing:-.045em}.nav-center,.nav-right{display:flex;align-items:center;gap:28px}.nav a{font-size:11px;font-weight:500;color:#1a232d}.nav-center a,.nav-right a:not(.lang){position:relative}.nav-center a::after,.nav-right a:not(.lang)::after{content:\"\";position:absolute;left:0;bottom:-7px;width:0;height:1px;background:#111820;transition:.2s}.nav-center a:hover::after,.nav-center a.active::after{width:100%}.lang{width:38px;height:38px;display:grid;place-items:center;border:1px solid #d7dde4;border-radius:50%;font-size:10px!important;transition:.2s}.lang:hover{background:#0b1117;color:#fff;border-color:#0b1117;transform:translateY(-1px)}"

for path in FILES:
    s = path.read_text(encoding='utf-8')
    if old_nav in s:
        s = s.replace(old_nav, new_nav, 1)
    else:
        # Defensive override if the original block has drifted.
        marker = '</style></head>'
        fix = '<style id="partnerships-nav-fix">.nav{gap:28px;-webkit-backdrop-filter:blur(16px)}.brand{font-family:Manrope,sans-serif!important;font-size:22px!important}.nav a{color:#1a232d}.lang:hover{transform:translateY(-1px)}</style>'
        if 'id="partnerships-nav-fix"' not in s:
            s = s.replace(marker, '</style>'+fix+'</head>', 1)
    if '/mobile-nav.js' not in s:
        s = s.replace('</body>', '<script src="/mobile-nav.js" defer></script></body>', 1)
    path.write_text(s, encoding='utf-8')
