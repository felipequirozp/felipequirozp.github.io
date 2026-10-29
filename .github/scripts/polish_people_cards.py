from pathlib import Path
import re

paths = [Path('people.html'), Path('es/people.html')]

css = r'''
<style id="people-card-polish-v5">
.people-all .people-grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:34px 16px}
.person-copy{padding-top:12px!important}
.company-tag,.context,.profile-link,.role{display:none!important}
.person h3{margin:0!important;font-size:18px!important;line-height:1.08!important;letter-spacing:-.035em!important;font-weight:500!important}
a.person{display:block;color:inherit;text-decoration:none;cursor:pointer}
a.person h3{transition:color .18s ease}a.person:hover h3{color:var(--blue)}
.portrait-inner{position:relative;aspect-ratio:4/4.75!important;overflow:hidden;border-radius:14px!important;background:linear-gradient(145deg,#d8e2ea 0%,#edf3f7 58%,#d5e0e8 100%)!important}
.portrait img{width:100%!important;height:100%!important;object-fit:cover!important;object-position:center center!important;filter:grayscale(100%) contrast(.96) brightness(1.02)!important;transform-origin:center 35%;will-change:transform}
/* Each portrait is tuned independently. Zack is the untouched reference. */
.person:nth-child(1) .portrait img{transform:scale(1.14) translateY(-4%)} /* Christopher */
.person:nth-child(2) .portrait img{transform:scale(1.08) translateY(-2%)} /* Zack */
.person:nth-child(3) .portrait img{transform:scale(1.40) translateY(-10%)} /* Nicolas */
.person:nth-child(4) .portrait img{transform:scale(1.20) translateY(-5%)} /* Damian */
.person:nth-child(5) .portrait img{transform:scale(1.06) translateY(0%)} /* Matias */
.person:nth-child(6) .portrait img{transform:scale(1.11) translateY(-2%)} /* Lia */
.person:nth-child(7) .portrait img{transform:scale(1.24) translateY(-6%)} /* Martin */
.person:nth-child(8) .portrait img{transform:scale(1.30) translateY(-7%)} /* Jorge */
.person:nth-child(9) .portrait img{transform:scale(1.12) translateY(-3%)} /* Francisca */
.person:nth-child(10) .portrait img{transform:scale(1.24) translateY(-6%)} /* Rodrigo */
.person:nth-child(11) .portrait img{transform:scale(1.22) translateY(-6%)} /* Juan */
.person:nth-child(12) .portrait img{transform:scale(1.05) translateY(0%)} /* Karen */
.person:nth-child(13) .portrait img{transform:scale(1.16) translateY(-3%)} /* Javier */
@media(max-width:1320px){.people-all .people-grid{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media(max-width:1100px){.people-all .people-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:900px){.people-all .people-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:700px){.people-all .people-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 12px}.person h3{font-size:16px!important}}
</style>
'''

for path in paths:
    text = path.read_text(encoding='utf-8')

    def simplify_person(match):
        block = match.group(0)
        # Recover LinkedIn from either an existing full-card link or the linked name.
        href_match = re.search(r'<a class="person"[^>]*href="([^"]+)"', block)
        if not href_match:
            href_match = re.search(r'<h3><a href="([^"]+)"', block)
        if not href_match:
            href_match = re.search(r'<a class="profile-link" href="([^"]+)"', block)
        href = href_match.group(1) if href_match else None

        # Normalize article/link wrapper to a plain article first.
        block = re.sub(r'^<a class="person"[^>]*>', '<article class="person">', block)
        block = re.sub(r'</a>$', '</article>', block)
        block = re.sub(r'<h3><a [^>]+>(.*?)</a></h3>', r'<h3>\1</h3>', block, flags=re.S)
        block = re.sub(r'<div class="company-tag">.*?</div>', '', block, flags=re.S)
        block = re.sub(r'<div class="context">.*?</div>', '', block, flags=re.S)
        block = re.sub(r'<div class="role">.*?</div>', '', block, flags=re.S)
        block = re.sub(r'<a class="profile-link".*?</a>', '', block, flags=re.S)

        if href:
            inner = re.sub(r'^<article class="person">|</article>$', '', block)
            block = f'<a class="person" href="{href}" target="_blank" rel="noopener noreferrer">{inner}</a>'
        return block

    text = re.sub(r'<(?:article|a) class="person".*?</(?:article|a)>', simplify_person, text, flags=re.S)
    text = re.sub(r'<style id="people-card-polish-v[345]">.*?</style>\s*', '', text, flags=re.S)
    text = text.replace('</head>', css + '</head>')
    path.write_text(text, encoding='utf-8')
