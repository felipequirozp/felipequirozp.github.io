from pathlib import Path
import re

paths = [Path('people.html'), Path('es/people.html')]

css = r'''
<style id="people-card-polish-v3">
.people-all .people-grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:34px 16px}
.person-copy{padding-top:12px!important}
.company-tag,.context,.profile-link{display:none!important}
.person h3{margin:0!important;font-size:18px!important;line-height:1.08!important;letter-spacing:-.035em!important;font-weight:500!important}
.person h3 a{color:inherit;text-decoration:none}
.person h3 a:hover{color:var(--blue)}
.role{margin-top:6px!important;color:#65717d!important;font-size:10px!important;line-height:1.45!important}
.portrait-inner{position:relative;aspect-ratio:4/4.75!important;overflow:hidden;border-radius:14px!important;background:linear-gradient(145deg,#d8e2ea 0%,#edf3f7 58%,#d5e0e8 100%)!important}
.portrait img{width:100%!important;height:100%!important;object-fit:cover!important;object-position:center center!important;filter:grayscale(100%) contrast(.96) brightness(1.02)!important;transform-origin:center 34%;will-change:transform}
/* individual framing: consistent head/shoulder scale across the series */
.person:nth-child(1) .portrait img{transform:scale(1.00) translateY(-1%)}
.person:nth-child(2) .portrait img{transform:scale(1.14) translateY(2%)}
.person:nth-child(3) .portrait img{transform:scale(1.18) translateY(4%)}
.person:nth-child(4) .portrait img{transform:scale(1.07) translateY(2%)}
.person:nth-child(5) .portrait img{transform:scale(1.14) translateY(3%)}
.person:nth-child(6) .portrait img{transform:scale(1.12) translateY(3%)}
.person:nth-child(7) .portrait img{transform:scale(1.12) translateY(3%)}
.person:nth-child(8) .portrait img{transform:scale(1.12) translateY(3%)}
.person:nth-child(9) .portrait img{transform:scale(1.10) translateY(2%)}
.person:nth-child(10) .portrait img{transform:scale(1.10) translateY(2%)}
.person:nth-child(11) .portrait img{transform:scale(1.10) translateY(2%)}
.person:nth-child(12) .portrait img{transform:scale(1.10) translateY(2%)}
.person:nth-child(13) .portrait img{transform:scale(1.10) translateY(2%)}
@media(max-width:1320px){.people-all .people-grid{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media(max-width:1100px){.people-all .people-grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:900px){.people-all .people-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:700px){.people-all .people-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 12px}.person h3{font-size:16px!important}.role{font-size:9px!important}}
</style>
'''

for path in paths:
    text = path.read_text(encoding='utf-8')

    # Preserve existing LinkedIn destination by moving it to the visible name.
    def simplify_person(match):
        block = match.group(0)
        href_match = re.search(r'<a class="profile-link" href="([^"]+)"', block)
        if href_match:
            href = href_match.group(1)
            block = re.sub(r'<h3>(.*?)</h3>', rf'<h3><a href="{href}" target="_blank" rel="noopener noreferrer">\1</a></h3>', block, count=1, flags=re.S)
        block = re.sub(r'<div class="company-tag">.*?</div>', '', block, flags=re.S)
        block = re.sub(r'<div class="context">.*?</div>', '', block, flags=re.S)
        block = re.sub(r'<a class="profile-link".*?</a>', '', block, flags=re.S)
        return block

    text = re.sub(r'<article class="person">.*?</article>', simplify_person, text, flags=re.S)
    text = re.sub(r'<style id="people-card-polish-v3">.*?</style>\s*', '', text, flags=re.S)
    text = text.replace('</head>', css + '</head>')
    path.write_text(text, encoding='utf-8')
