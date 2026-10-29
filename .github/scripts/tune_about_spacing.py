from pathlib import Path

for rel in ['about.html','es/about.html']:
    p=Path(rel)
    s=p.read_text(encoding='utf-8')

    # Keep story spacing tuned.
    s=s.replace('.story h2{margin:0;max-width:720px;', '.story h2{margin:0 0 20px;max-width:720px;')
    s=s.replace('.story-copy p{margin:0 0 16px;', '.story-copy p{margin:0 0 20px;')

    # Add scroll reveal behavior if it is not already present.
    if '.reveal{opacity:0;' not in s:
        s=s.replace('.footer-bottom{width:min(var(--max),100%);margin:42px auto 0;padding-top:20px;display:flex;justify-content:space-between;border-top:1px solid var(--line);color:#83909c;font-size:9px;letter-spacing:.06em;text-transform:uppercase}', '.footer-bottom{width:min(var(--max),100%);margin:42px auto 0;padding-top:20px;display:flex;justify-content:space-between;border-top:1px solid var(--line);color:#83909c;font-size:9px;letter-spacing:.06em;text-transform:uppercase}.reveal{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease}.reveal.is-visible{opacity:1;transform:none}@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}')

    # Tether needs its own optical sizing/alignment.
    if '.entity.tether .entity-logo img' not in s:
        s=s.replace('.entity.low .entity-logo img{max-height:30px}.entity.usm .entity-logo img{max-height:28px}', '.entity.low .entity-logo img{max-height:30px}.entity.tether .entity-logo img{max-width:160px;max-height:40px;transform:translateX(-3px)}.entity.usm .entity-logo img{max-height:28px}')

    # Add Tether class to the row.
    s=s.replace('<a class="entity" href="/tethereducation">', '<a class="entity tether" href="/tethereducation">')
    s=s.replace('<a class="entity" href="/es/tethereducation">', '<a class="entity tether" href="/es/tethereducation">')

    # Reveal the major sections and cards on scroll.
    s=s.replace('<section class="story">', '<section class="story reveal">')
    s=s.replace('<section class="entities">', '<section class="entities reveal">')
    s=s.replace('<section class="working">', '<section class="working reveal">')
    s=s.replace('<section class="closing">', '<section class="closing reveal">')

    if 'new IntersectionObserver' not in s:
        s=s.replace('</body>', '<script>const io=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add(\'is-visible\');io.unobserve(e.target)}})},{threshold:.12,rootMargin:\'0px 0px -35px\'});document.querySelectorAll(\'.reveal\').forEach(el=>io.observe(el));</script></body>')

    p.write_text(s,encoding='utf-8')
