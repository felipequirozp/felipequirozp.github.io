from pathlib import Path
import re

paths = [Path('people.html'), Path('es/people.html')]

css = r'''
<style id="people-card-polish-v10">
.people-all .people-grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:34px 16px}
.person{position:relative;min-width:0}
.person-copy{padding-top:12px!important}
.company-tag,.context,.profile-link,.role{display:none!important}
.person h3{margin:0!important;font-size:18px!important;line-height:1.08!important;letter-spacing:-.035em!important;font-weight:500!important;transition:color .18s ease}
.person:has(.card-link):hover h3{color:var(--blue)}
.card-link{position:absolute;inset:0;z-index:4;border-radius:14px}
.portrait-inner{position:relative;aspect-ratio:4/4.5!important;overflow:hidden;border-radius:14px!important;background:#f1f1f1!important}
.portrait img{width:100%!important;height:100%!important;object-fit:cover!important;object-position:center center!important;filter:grayscale(100%) contrast(.96) brightness(1.02)!important;transform-origin:center 35%;will-change:transform}
/* Individual tuning only — no global portrait scaling. */
.person:nth-child(1) .portrait img{transform:scale(1.14) translateY(-4%)} /* Christopher */
.person:nth-child(2) .portrait img{transform:scale(1.08) translateY(-2%)} /* Zack */
.person:nth-child(3) .portrait img{transform:scale(1.28) translateY(8%)} /* Nicolas */
.person:nth-child(4) .portrait img{transform:scale(1.11) translateY(10%)} /* Damian */
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

    text = re.sub(
        r'<a class="person" href="([^"]+)"[^>]*>(.*?)</article>',
        lambda m: f'<article class="person" data-link="{m.group(1)}">{m.group(2)}</article>',
        text,
        flags=re.S,
    )

    def normalize_person(match):
        block = match.group(0)
        href = None

        data_match = re.search(r'data-link="([^"]+)"', block)
        if data_match:
            href = data_match.group(1)

        inner_link = re.search(r'<h3><a href="([^"]+)"[^>]*>(.*?)</a></h3>', block, flags=re.S)
        if inner_link:
            href = href or inner_link.group(1)
            block = re.sub(r'<h3><a href="[^"]+"[^>]*>(.*?)</a></h3>', r'<h3>\1</h3>', block, count=1, flags=re.S)

        old_card_link = re.search(r'<a class="card-link" href="([^"]+)"', block)
        if old_card_link:
            href = href or old_card_link.group(1)

        old_profile_link = re.search(r'<a class="profile-link" href="([^"]+)"', block)
        if old_profile_link:
            href = href or old_profile_link.group(1)

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
    text = re.sub(r'<style id="people-card-polish-v[345678910]+">.*?</style>\s*', '', text, flags=re.S)
    text = text.replace('</head>', css + '</head>')
    path.write_text(text, encoding='utf-8')
