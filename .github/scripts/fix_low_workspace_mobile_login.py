from pathlib import Path

paths = [Path('lowsignal/low-workspace.html'), Path('es/lowsignal/low-workspace.html')]
for path in paths:
    text = path.read_text()
    # Ensure mobile Product Experience login visual is always visible and stacked correctly.
    marker = '@media(max-width:640px){:root{--page:20px}'
    if marker in text and '.login-visual{display:block!important' not in text:
        text = text.replace(
            marker,
            '@media(max-width:640px){.login-visual{display:block!important;width:100%!important;opacity:1!important;transform:none!important;visibility:visible!important}.login-visual img{display:block!important;width:100%!important;height:auto!important;opacity:1!important;visibility:visible!important;transform:translateY(-7px)!important;margin-bottom:-7px!important}.login-story{display:grid!important;grid-template-columns:1fr!important}.login-copy{order:1}.login-visual{order:2;margin-top:8px}' + marker[len('@media(max-width:640px){'):]
        )
    text = text.replace('src="/images/login-demo.png" alt=', 'src="/images/login-demo.png" loading="eager" decoding="async" alt=')
    text = text.replace('loading="eager" decoding="async" alt="Low Workspace login screen" loading="lazy"', 'loading="eager" decoding="async" alt="Low Workspace login screen"')
    text = text.replace('loading="eager" decoding="async" alt="Pantalla de acceso de Low Workspace" loading="lazy"', 'loading="eager" decoding="async" alt="Pantalla de acceso de Low Workspace"')
    path.write_text(text)
