from pathlib import Path
import re

paths = [Path('people.html'), Path('es/people.html')]

LINKS_BY_NAME = {
    'Zack Tseng': 'https://www.linkedin.com/in/zacharytseng/',
    'Nicolás Muñoz': 'https://www.linkedin.com/in/nicolas-munoz-pavez/',
    'Leidy Gómez': 'https://co.linkedin.com/in/leidy-gomez',
    'Karen Radonich': 'https://www.linkedin.com/in/karen-radonich-36114a2b0/',
    'Juan Yuz': 'https://www.linkedin.com/in/juan-i-yuz/',
    'Javier Robledo': 'https://www.linkedin.com/in/javierrobledo/',
    'Valentina Wagenreld': 'https://www.linkedin.com/in/valentina-wagenreld-62042a138/',
}

ORDER = [
    'Christopher Neilson','Zack Tseng','Nicolás Muñoz','Leidy Gómez','Rodrigo Lewit','Karen Radonich',
    'Damián Aldunate','Matías Bussinger','Lía Morice','Martín Alvarado','Jorge Muñoz','Francisca Astudillo',
    'Juan Yuz','Javier Robledo','Valentina Wagenreld',
]

css = r'''
<style id="people-card-polish-v27">
.people-all .people-grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:34px 16px}
.person{position:relative;min-width:0}
.person-copy{padding-top:12px!important}
.company-tag,.context,.profile-link,.role{display:none!important}
.person h3{margin:0!important;font-size:18px!important;line-height:1.08!important;letter-spacing:-.035em!important;font-weight:500!important;transition:color .18s ease}
.person:has(.card-link):hover h3{color:var(--blue)}
.card-link{position:absolute;inset:0;z-index:4;border-radius:14px}
.portrait-inner{position:relative;aspect-ratio:4/4.5!important;overflow:hidden;border-radius:14px!important;background:#f1f1f1!important}
.portrait img{width:100%!important;height:100%!important;object-fit:cover!important;object-position:center center!important;filter:grayscale(100%) contrast(.96) brightness(1.02)!important;transform-origin:center 35%;will-change:transform;mix-blend-mode:normal!important}
.person:nth-child(3) .portrait-inner::after,.person:nth-child(4) .portrait-inner::after,.person:nth-child(6) .portrait-inner::after,.person:nth-child(15) .portrait-inner::after{content:"";position:absolute;z-index:2;left:0;right:0;top:0;height:14px;background:#f1f1f1;pointer-events:none}
.person:nth-child(1) .portrait img{transform:scale(1.14) translateY(-4%)}
.person:nth-child(2) .portrait img{transform:scale(1.08) translateY(-2%)}
.person:nth-child(3) .portrait img{transform:scale(1.27) translateY(8%)}
.person:nth-child(4) .portrait img{transform:scale(1.11) translateY(12%)}
.person:nth-child(5) .portrait img{transform:scale(1.24) translateY(5%)}
.person:nth-child(6) .portrait img{transform:scale(1.11) translateY(9%)}
.person:nth-child(7) .portrait img{transform:scale(1.10) translateY(0)}
.person:nth-child(8) .portrait img{transform:scale(1.06) translateY(0)}
.person:nth-child(9) .portrait img{transform:scale(1.11) translateY(-2%)}
.person:nth-child(10) .portrait img{transform:scale(1.24) translateY(-6%)}
.person:nth-child(11) .portrait img{transform:scale(1.30) translateY(-7%)}
.person:nth-child(12) .portrait img{transform:scale(1.12) translateY(-3%)}
.person:nth-child(13) .portrait img{transform:scale(1.22) translateY(2%)}
.person:nth-child(14) .portrait img{transform:scale(1.16) translateY(4%)}
.person:nth-child(15) .portrait img{transform:scale(1.16) translateY(8%)}

/* Scroll reveal */
.js-reveal{opacity:0;transform:translateY(24px);transition:opacity .65s cubic-bezier(.2,.7,.2,1),transform .65s cubic-bezier(.2,.7,.2,1);transition-delay:var(--reveal-delay,0ms)}
.js-reveal.is-visible{opacity:1;transform:translateY(0)}
.people-head.js-reveal{transform:translateY(18px)}
.people-head.js-reveal.is-visible{transform:translateY(0)}
@media(prefers-reduced-motion:reduce){.js-reveal{opacity:1!important;transform:none!important;transition:none!important}}
@media(max-width:1320px){.people-all .people-grid{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media(max-width:1100px){.people-all .people-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:900px){.people-all .people-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:700px){.people-all .people-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 12px}.person h3{font-size:16px!important}}
</style>
'''

reveal_js = r'''
<script id="people-scroll-reveal">
(()=>{
  const items=[document.querySelector('.people-head'),...document.querySelectorAll('.people-grid .person')].filter(Boolean);
  if(!items.length)return;
  items.forEach((el,i)=>{el.classList.add('js-reveal');el.style.setProperty('--reveal-delay',`${Math.min((i%6)*55,275)}ms`)});
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){items.forEach(el=>el.classList.add('is-visible'));return;}
  const io=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');io.unobserve(entry.target)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  items.forEach(el=>io.observe(el));
})();
</script>
'''

def reorder_grid(text):
    match = re.search(r'(<div class="people-grid">)(.*?)(</div></div></section>\s*<section class="closing">)', text, flags=re.S)
    if not match:
        return text
    blocks = re.findall(r'<article class="person"[^>]*>.*?</article>', match.group(2), flags=re.S)
    if not blocks:
        return text
    by_name = {}
    leftovers = []
    for block in blocks:
        m = re.search(r'<h3>(.*?)</h3>', block, flags=re.S)
        if m:
            by_name[re.sub(r'<[^>]+>', '', m.group(1)).strip()] = block
        else:
            leftovers.append(block)
    ordered = [by_name.pop(name) for name in ORDER if name in by_name]
    ordered.extend(by_name.values())
    ordered.extend(leftovers)
    replacement = match.group(1) + ''.join(ordered) + match.group(3)
    return text[:match.start()] + replacement + text[match.end():]

for path in paths:
    text = path.read_text(encoding='utf-8')
    text = reorder_grid(text)

    text = re.sub(
        r'<a class="person" href="([^"]+)"[^>]*>(.*?)</article>',
        lambda m: f'<article class="person" data-link="{m.group(1)}">{m.group(2)}</article>',
        text, flags=re.S,
    )

    def normalize_person(match):
        block = match.group(0)
        href = None
        m = re.search(r'data-link="([^"]+)"', block)
        if m: href = m.group(1)
        m = re.search(r'<h3><a href="([^"]+)"[^>]*>(.*?)</a></h3>', block, flags=re.S)
        if m:
            href = href or m.group(1)
            block = re.sub(r'<h3><a href="[^"]+"[^>]*>(.*?)</a></h3>', r'<h3>\1</h3>', block, count=1, flags=re.S)
        m = re.search(r'<a class="card-link" href="([^"]+)"', block)
        if m: href = href or m.group(1)
        m = re.search(r'<a class="profile-link" href="([^"]+)"', block)
        if m: href = href or m.group(1)
        m = re.search(r'<h3>(.*?)</h3>', block, flags=re.S)
        if m:
            name = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            href = href or LINKS_BY_NAME.get(name)
        block = re.sub(r'\sdata-link="[^"]+"', '', block)
        block = re.sub(r'<a class="card-link".*?</a>', '', block, flags=re.S)
        block = re.sub(r'<div class="company-tag">.*?</div>', '', block, flags=re.S)
        block = re.sub(r'<div class="context">.*?</div>', '', block, flags=re.S)
        block = re.sub(r'<div class="role">.*?</div>', '', block, flags=re.S)
        block = re.sub(r'<a class="profile-link".*?</a>', '', block, flags=re.S)
        block = re.sub(r'^<article class="person"[^>]*>', '<article class="person">', block)
        if href:
            overlay = f'<a class="card-link" href="{href}" target="_blank" rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a>'
            block = block.replace('<article class="person">', '<article class="person">' + overlay, 1)
        return block

    text = re.sub(r'<article class="person"[^>]*>.*?</article>', normalize_person, text, flags=re.S)
    for slug in ['damian-aldunate','nicolas-munoz','leidy-gomez','karen-radonich']:
        text = re.sub(rf'/images/people/{slug}\.webp(?:\?v=[^\"]+)?', f'/images/people/{slug}.webp?v=20261029-1715', text)
    text = re.sub(r'<style id="people-card-polish-v\d+">.*?</style>\s*', '', text, flags=re.S)
    text = re.sub(r'<script id="people-scroll-reveal">.*?</script>\s*', '', text, flags=re.S)
    text = text.replace('</head>', css + '</head>')
    text = text.replace('</body>', reveal_js + '</body>')
    path.write_text(text, encoding='utf-8')
