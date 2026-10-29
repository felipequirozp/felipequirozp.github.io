from pathlib import Path
import re

FILES = [
    Path('blog/ai-future-students.html'),
    Path('blog/ai-leaves-the-demo.html'),
    Path('blog/ai-native-core.html'),
    Path('blog/building-lowsignal.html'),
    Path('blog/edtech-startup-scale.html'),
    Path('blog/future-of-education.html'),
    Path('blog/partnerships-infrastructure.html'),
    Path('blog/scaling-technology-without-losing-speed.html'),
    Path('blog/when-ai-becomes-the-strategy.html'),
    Path('es/blog/ai-future-students.html'),
    Path('es/blog/ai-leaves-the-demo.html'),
    Path('es/blog/ai-native-core.html'),
    Path('es/blog/building-lowsignal.html'),
    Path('es/blog/cuando-la-ia-se-vuelve-la-estrategia.html'),
    Path('es/blog/edtech-startup-scale.html'),
    Path('es/blog/escalar-tecnologia-sin-perder-velocidad.html'),
    Path('es/blog/future-of-education.html'),
    Path('es/blog/partnerships-infrastructure.html'),
]

CSS = r'''
<style id="blog-article-system-v1">
:root{--article-max:1520px;--article-copy:760px}
.hero,.article-hero{padding:74px var(--page) 58px!important;background:radial-gradient(circle at 82% 18%,rgba(20,103,216,.10),transparent 28%),linear-gradient(180deg,#f4f7f9 0%,#eef3f7 100%)!important;border-bottom:1px solid #dce4eb!important}
.hero-inner,.article-hero-inner{width:min(var(--article-max),100%)!important;margin:0 auto!important}
.hero-top,.article-meta{margin-bottom:28px!important;align-items:center!important;justify-content:flex-start!important}
.chips,.article-meta-left{display:flex!important;flex-wrap:wrap!important;gap:8px!important}
.chip,.article-meta-left span{min-height:auto!important;padding:0!important;border:0!important;border-radius:0!important;background:transparent!important;color:var(--blue)!important;font-size:10px!important;font-weight:700!important;letter-spacing:.12em!important;text-transform:uppercase!important}
.chip+.chip:before,.article-meta-left span+span:before{content:'·';margin:0 8px;color:#8a98a6}
.back,.article-back{display:none!important}
.hero h1,.article-title{margin:0!important;max-width:900px!important;font-family:Manrope,sans-serif!important;font-size:clamp(42px,4.4vw,64px)!important;line-height:1.02!important;letter-spacing:-.052em!important;font-weight:500!important}
.hero h1 span,.article-title span{display:block!important;color:inherit!important}
.deck,.article-deck{margin:20px 0 0!important;max-width:720px!important;color:#3f4c58!important;font-family:Manrope,sans-serif!important;font-size:clamp(17px,1.55vw,23px)!important;line-height:1.48!important;letter-spacing:-.02em!important}
.hero-media{width:min(82%,calc(var(--article-max) * .82))!important;max-width:calc(100% - (var(--page) * 2))!important;margin:28px 0 0 var(--page)!important;padding:0!important;overflow:visible!important;background:transparent!important}
.hero-media-inner{width:100%!important;margin:0!important}
.hero-media-frame,.hero-media{border-radius:20px!important}
.hero-media-frame{overflow:hidden!important;border:1px solid #dfe5ea!important;background:#e8edf2!important;box-shadow:0 10px 26px rgba(27,49,70,.04)!important}
.hero-media>img,.hero-media-frame img{width:100%!important;aspect-ratio:16/8.7!important;object-fit:cover!important}
.caption,.image-caption{width:100%!important;margin:12px 0 0!important;padding:0!important;color:#83909c!important;font-size:9px!important;letter-spacing:.06em!important;text-transform:uppercase!important}
.article{padding:72px var(--page) 96px!important;background:#fff!important;border-top:0!important}
.article-grid,.article-layout{width:min(1120px,100%)!important;margin:0 auto!important;display:grid!important;grid-template-columns:180px minmax(0,var(--article-copy))!important;gap:64px!important;justify-content:center!important;align-items:start!important}
.article-aside{position:sticky!important;top:110px!important;padding-top:2px!important;color:#7b8794!important;font-size:9px!important;line-height:1.7!important;letter-spacing:.1em!important;text-transform:uppercase!important}
.article-aside strong{display:block!important;margin-bottom:12px!important;color:#17202b!important;font-family:Manrope,sans-serif!important;font-size:14px!important;font-weight:500!important;line-height:1.4!important;letter-spacing:-.02em!important;text-transform:none!important}
.body,.article-body{max-width:var(--article-copy)!important}
.lead,.article-body .lead{margin:0 0 36px!important;font-family:Manrope,sans-serif!important;font-size:clamp(26px,2.5vw,36px)!important;line-height:1.34!important;letter-spacing:-.035em!important;color:#17202b!important}
.body p,.article-body p{margin:0 0 24px!important;color:#46515d!important;font-size:16px!important;line-height:1.8!important}
.body h2,.article-body h2{margin:64px 0 20px!important;font-family:Manrope,sans-serif!important;font-size:clamp(30px,3vw,42px)!important;line-height:1.08!important;letter-spacing:-.043em!important;font-weight:500!important;color:#111820!important}
blockquote,.article-body blockquote{margin:46px 0!important;padding:24px 26px!important;border:1px solid #dfe5ea!important;border-left:3px solid var(--blue)!important;border-radius:16px!important;background:#f4f7f9!important;font-family:Manrope,sans-serif!important;font-size:clamp(23px,2.3vw,32px)!important;line-height:1.4!important;letter-spacing:-.03em!important;color:#17202b!important}
.article-note{margin:46px 0!important;padding:20px 0!important;border-top:1px solid #e1e6eb!important;border-bottom:1px solid #e1e6eb!important}
.article-note strong,.article-note span{display:block!important;margin-bottom:8px!important;color:var(--blue)!important;font-size:9px!important;font-weight:700!important;letter-spacing:.12em!important;text-transform:uppercase!important}
.article-note p{margin:0!important;color:#64707d!important;font-size:14px!important;line-height:1.7!important;font-family:Inter,sans-serif!important;letter-spacing:0!important}
.article-end{margin-top:72px!important;padding-top:28px!important;border-top:1px solid #e1e6eb!important;color:#7b8794!important;font-size:10px!important}
.article-author-copy strong{font-size:17px!important;color:#17202b!important}
.article-author-avatar{border:1px solid #dfe5ea!important;background:#eef2f6!important}
.next,.next-article{padding:0 var(--page)!important;background:#0b1117!important;color:#fff!important;border-top:0!important}
.next-inner{width:min(var(--article-max),100%)!important;margin:0 auto!important;display:flex!important;justify-content:space-between!important;align-items:center!important;gap:30px!important;padding:50px 0!important}
.next-label{color:#7fb9ff!important;font-size:9px!important;font-weight:700!important;letter-spacing:.12em!important;text-transform:uppercase!important;flex:0 0 auto!important}
.next-link{display:block!important;flex:1!important;border-top:0!important;padding-top:0!important;text-align:right!important}
.next-link small{color:#aeb8c2!important;font-size:9px!important;font-weight:700!important;letter-spacing:.1em!important;text-transform:uppercase!important}
.next-link h2{margin:10px 0 0 auto!important;max-width:760px!important;color:#fff!important;font-family:Manrope,sans-serif!important;font-size:clamp(28px,3vw,40px)!important;font-weight:500!important;line-height:1.08!important;letter-spacing:-.04em!important;transition:color .2s ease,transform .2s ease!important}
.next-link:hover h2{color:#7fb9ff!important;transform:translateX(3px)!important}
.blog-reveal{opacity:0;transform:translateY(16px);transition:opacity .5s ease,transform .5s ease}.blog-reveal.is-visible{opacity:1;transform:none}
@media(max-width:980px){.article-grid,.article-layout{grid-template-columns:1fr!important;gap:28px!important}.article-aside{position:static!important;max-width:560px}.next-inner{align-items:flex-start!important;flex-direction:column!important}.next-link{text-align:left!important}.next-link h2{margin-left:0!important}.hero-media{width:calc(100% - (var(--page) * 2))!important}}
@media(max-width:700px){.hero,.article-hero{padding-top:50px!important;padding-bottom:44px!important}.hero-top,.article-meta{margin-bottom:24px!important;align-items:flex-start!important;flex-direction:column!important}.hero h1,.article-title{font-size:clamp(42px,11vw,58px)!important}.deck,.article-deck{font-size:17px!important}.hero-media{width:calc(100% - 40px)!important;max-width:none!important;margin:20px 20px 0!important}.hero-media-frame,.hero-media{border-radius:16px!important}.caption,.image-caption{margin-top:10px!important}.article{padding-top:58px!important;padding-bottom:72px!important}.body h2,.article-body h2{margin-top:54px!important}.next-inner{padding:38px 0!important}.next-link h2{font-size:30px!important}}
@media(prefers-reduced-motion:reduce){.blog-reveal{opacity:1!important;transform:none!important;transition:none!important}.next-link h2{transition:none!important}}
</style>
'''

JS = r'''
<script id="blog-article-reveal">
(()=>{const items=[...document.querySelectorAll('.hero-top,.article-meta,.hero h1,.article-title,.deck,.article-deck,.hero-media,.article-aside,.body > *,.article-body > *,.article-end,.next-inner')];if(!items.length||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;items.forEach(el=>el.classList.add('blog-reveal'));const io=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');io.unobserve(entry.target)}}),{threshold:.08,rootMargin:'0px 0px -5% 0px'});items.forEach(el=>io.observe(el));})();
</script>
'''

for path in FILES:
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'<style id="blog-article-system-v\d+">.*?</style>\s*', '', text, flags=re.S)
    text = re.sub(r'<script id="blog-article-reveal">.*?</script>\s*', '', text, flags=re.S)
    text = re.sub(r'<a class="(?:back|article-back)" href="[^"]+">.*?</a>\s*', '', text, flags=re.S)
    text = text.replace('</head>', CSS + '</head>')
    text = text.replace('</body>', JS + '</body>')
    path.write_text(text, encoding='utf-8')
    print('updated', path)
