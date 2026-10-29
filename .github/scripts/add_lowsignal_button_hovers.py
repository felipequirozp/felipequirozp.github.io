from pathlib import Path

paths = [Path('lowsignal.html'), Path('es/lowsignal.html')]

for p in paths:
    s = p.read_text(encoding='utf-8')

    s = s.replace(
        '.lang{width:38px;height:38px;display:grid;place-items:center;border:1px solid #d7dde4;border-radius:50%;font-size:10px!important}',
        '.lang{width:38px;height:38px;display:grid;place-items:center;border:1px solid #d7dde4;border-radius:50%;font-size:10px!important;transition:background .18s ease,color .18s ease,border-color .18s ease,transform .18s ease}.lang:hover{background:#0b1117;color:#fff;border-color:#0b1117;transform:translateY(-1px)}'
    )

    s = s.replace(
        '.closing a{min-height:40px;display:inline-flex;align-items:center;padding:0 14px;border-radius:999px;background:#fff;color:#0b1117;font-size:10px;font-weight:700}.closing a.secondary{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.24)}',
        '.closing a{min-height:40px;display:inline-flex;align-items:center;padding:0 14px;border-radius:999px;background:#fff;color:#0b1117;font-size:10px;font-weight:700;border:1px solid #fff;transition:background .18s ease,color .18s ease,border-color .18s ease,transform .18s ease}.closing a.secondary{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.24)}.closing a:hover,.closing a.secondary:hover{background:var(--blue);color:#fff;border-color:var(--blue);transform:translateY(-2px)}'
    )

    # The Low Workspace CTA is intentionally a text-link, but should still react on hover.
    marker = '.workspace-media img{width:100%;border-radius:12px;box-shadow:0 20px 44px rgba(11,17,23,.10)}'
    if '.workspace-grid a:hover' not in s:
        s = s.replace(
            marker,
            marker + '.workspace-grid a{transition:color .18s ease,border-color .18s ease,transform .18s ease}.workspace-grid a:hover{color:var(--blue);border-color:var(--blue)!important;transform:translateY(-1px)}'
        )

    p.write_text(s, encoding='utf-8')
