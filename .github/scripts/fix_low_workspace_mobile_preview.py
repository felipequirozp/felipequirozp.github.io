from pathlib import Path

paths = [Path('lowsignal.html'), Path('es/lowsignal.html')]
for path in paths:
    text = path.read_text(encoding='utf-8')
    text = text.replace('loading="lazy" decoding="async"></a>', 'loading="eager" decoding="async"></a>', 1)
    old = '@media(max-width:640px){.low-workspace-feature{padding:64px var(--page) 68px}.low-workspace-feature h2{font-size:clamp(38px,9vw,48px)}.low-workspace-feature p{font-size:14px}.low-workspace-feature__visual{box-shadow:0 16px 40px rgba(21,26,44,.09)}}'
    new = '@media(max-width:640px){.low-workspace-feature{padding:64px var(--page) 68px}.low-workspace-feature h2{font-size:clamp(38px,9vw,48px)}.low-workspace-feature p{font-size:14px}.low-workspace-feature__visual{display:block!important;visibility:visible!important;opacity:1!important;transform:none!important;box-shadow:0 16px 40px rgba(21,26,44,.09)}.low-workspace-feature__visual img{display:block!important;width:100%!important;height:auto!important;visibility:visible!important;opacity:1!important}}'
    if old not in text:
        raise SystemExit(f'Expected mobile Low Workspace CSS not found in {path}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')
