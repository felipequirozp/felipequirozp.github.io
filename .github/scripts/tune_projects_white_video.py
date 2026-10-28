from pathlib import Path

for path in [Path('projects.html'), Path('es/projects.html')]:
    s = path.read_text(encoding='utf-8')

    # Pure white canvas / gallery, while keeping the dark hero for contrast.
    s = s.replace('body{margin:0;background:var(--canvas);', 'body{margin:0;background:#fff;')
    s = s.replace(".portfolio{padding:34px var(--page) 120px;background:linear-gradient(180deg,#e9eff4 0%,#f2f5f7 34%,#edf2f6 100%)}", ".portfolio{padding:34px var(--page) 120px;background:#fff}")
    s = s.replace(".filter{appearance:none;border:1px solid #cfd8e1;background:rgba(255,255,255,.72);", ".filter{appearance:none;border:1px solid #d8e0e7;background:#fff;")
    s = s.replace(".card{min-width:0;border:1px solid rgba(203,214,224,.9);border-radius:24px;overflow:hidden;background:rgba(255,255,255,.95);box-shadow:0 14px 36px rgba(27,49,70,.065);", ".card{min-width:0;border:1px solid #e0e5ea;border-radius:24px;overflow:hidden;background:#fff;box-shadow:0 14px 36px rgba(27,49,70,.055);")

    # Let the Explorer card be the one moving element.
    s = s.replace('<video muted playsinline preload="metadata" poster="/logos/virtual-school-explorer-logo.svg">', '<video autoplay loop muted playsinline preload="metadata" poster="/logos/virtual-school-explorer-logo.svg">')

    # Remove the global forced-pause behavior while preserving filters.
    s = s.replace(";document.querySelectorAll('video').forEach(v=>{v.pause();v.addEventListener('play',()=>v.pause())})", "")

    path.write_text(s, encoding='utf-8')
