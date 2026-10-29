from pathlib import Path

STYLE = r'''<style id="low-workspace-v2">
:root{--page:8vw!important;--max:1520px!important;--nav-h:76px}
body{padding-top:var(--nav-h)!important;overflow-x:hidden!important}
.nav{position:fixed!important;inset:0 0 auto 0!important;height:var(--nav-h)!important;min-height:var(--nav-h)!important;z-index:9999!important}
.hero{padding:66px var(--page) 74px!important;background:radial-gradient(circle at 82% 16%,rgba(20,103,216,.11),transparent 28%),linear-gradient(180deg,#f4f7f9 0%,#eef3f7 100%)!important;border-bottom:1px solid #dce4eb!important}
.hero-top{margin-bottom:34px!important}
.hero-grid{grid-template-columns:minmax(0,.82fr) minmax(440px,1.18fr)!important;gap:70px!important;align-items:center!important}
.hero h1{font-size:clamp(46px,5vw,70px)!important;line-height:1.01!important;letter-spacing:-.056em!important}
.hero h1 span{color:#98a4af!important}
.hero-description{margin-top:28px!important;font-size:14px!important;line-height:1.84!important;max-width:690px!important}
.hero-role{margin-top:26px!important;padding-top:18px!important}
.hero-media{padding:20px!important;border:1px solid #d4dde5!important;border-radius:20px!important;background:#dfe8ef!important;box-shadow:none!important;overflow:visible!important}
.hero-media img{transform:none!important;margin:0!important;border-radius:12px!important;box-shadow:0 20px 48px rgba(11,17,23,.10)!important}
.section{padding:82px var(--page)!important}
.section.soft,.showcase,.project-nav{background:linear-gradient(180deg,#e7edf2,#edf2f6)!important}
.section-grid{grid-template-columns:.38fr 1.12fr!important;gap:76px!important}
.section h2,.showcase h2,.principle h2{font-size:clamp(34px,3.7vw,50px)!important;line-height:1.06!important;letter-spacing:-.045em!important}
.copy p,.showcase-head p,.login-copy p,.principle p{font-size:13px!important;line-height:1.84!important}
.feature-grid{margin-top:30px!important;display:grid!important;grid-template-columns:repeat(3,1fr)!important;gap:14px!important;border-top:0!important}
.feature{padding:22px!important;border:1px solid #dfe5ea!important;border-radius:17px!important;background:#fff!important}
.feature:nth-child(n){padding:22px!important;border:1px solid #dfe5ea!important}
.feature strong{margin-top:18px!important;font-size:21px!important}
.feature p{font-size:11px!important;line-height:1.7!important}
.build-grid{margin-top:30px!important;grid-template-columns:repeat(4,1fr)!important}
.showcase{padding:82px var(--page)!important;border-top:1px solid #d8e1e8!important;border-bottom:1px solid #d8e1e8!important}
.showcase-head{margin-bottom:30px!important}
.product-shot img,.login-visual img{transform:none!important;margin:0!important;clip-path:none!important;border-radius:12px!important}
.login-story{margin-top:44px!important;padding-top:34px!important}
.principle{padding:82px var(--page)!important;text-align:left!important}
.principle h2,.principle p{margin-left:0!important;margin-right:0!important}
.project-nav{padding:0 var(--page)!important;background:#0b1117!important;color:#fff!important}
.project-nav-inner{padding:24px 0!important;border-color:rgba(255,255,255,.14)!important}
.project-nav a{padding:18px 0!important;transition:background .18s ease,color .18s ease,transform .18s ease,padding .18s ease!important}
.project-nav a:hover{padding-left:12px!important;padding-right:12px!important;background:rgba(255,255,255,.06)!important;color:#fff!important;transform:translateY(-1px)!important}
.project-nav-label{color:#8ea0b3!important}
.footer{padding:58px var(--page) 28px!important}
.footer-grid{grid-template-columns:1.15fr repeat(3,.7fr)!important;gap:56px!important}
.footer-brand{font-size:28px!important}.footer-copy{font-size:12px!important;max-width:330px!important}.footer-col strong{font-size:11px!important}.footer-col a{font-size:12px!important;transition:transform .18s ease,color .18s ease!important}.footer-col a:hover{transform:translateX(3px)!important}.footer-bottom{margin-top:42px!important;padding-top:20px!important;font-size:9px!important}
@media(max-width:1000px){.hero-grid,.section-grid{grid-template-columns:1fr!important}.feature-grid{grid-template-columns:1fr!important}.build-grid{grid-template-columns:1fr 1fr!important}.footer-grid{grid-template-columns:1fr 1fr!important}}
@media(max-width:700px){:root{--page:20px!important;--nav-h:68px}.nav{height:var(--nav-h)!important}.hero{padding-top:48px!important}.hero-media{order:-1}.build-grid{grid-template-columns:1fr!important}.footer-grid{grid-template-columns:1fr!important;gap:28px!important}.footer-bottom{flex-direction:column!important;gap:10px!important}}
</style>'''

for rel in ['lowsignal/low-workspace.html','es/lowsignal/low-workspace.html']:
    p=Path(rel)
    s=p.read_text(encoding='utf-8')
    if 'id="low-workspace-v2"' in s:
        import re
        s=re.sub(r'<style id="low-workspace-v2">.*?</style>', STYLE, s, flags=re.S)
    else:
        s=s.replace('</head>', STYLE+'\n</head>',1)
    # Keep the internal-product status explicit.
    s=s.replace('Internal platform · Live build · 2026','Internal product · In development · 2026')
    s=s.replace('Plataforma interna · En construcción · 2026','Producto interno · En desarrollo · 2026')
    p.write_text(s,encoding='utf-8')

# Triggered after workflow creation.
