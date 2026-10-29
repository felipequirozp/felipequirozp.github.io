from pathlib import Path
import re

FILES = [Path('blog/my-everyday-stack.html'), Path('es/blog/mi-stack-diario.html')]

CSS = r'''
<style id="stack-article-refresh-v1">
:root{--article-max:1520px;--article-copy:760px}
body{background:#fff}
.hero{padding:72px var(--page) 44px!important;background:linear-gradient(180deg,#f6f8fa 0%,#eef3f7 100%)!important;border-bottom:1px solid #dce4eb}
.hero-inner{width:min(var(--article-max),100%)!important}
.hero-top{margin-bottom:44px!important}
.chip{min-height:34px!important;padding:0 12px!important;background:#fff!important;border-color:#dce3e9!important;color:#5e6a76!important;font-size:9px!important;letter-spacing:.04em!important}
.back{font-size:10px!important;color:#71808f!important;transition:color .18s ease,transform .18s ease}
.back:hover{color:var(--blue)!important;transform:translateX(-2px)}
.hero h1{max-width:1180px!important;font-size:clamp(56px,6.5vw,104px)!important;line-height:.98!important;letter-spacing:-.068em!important;font-weight:500!important}
.hero h1 span{display:block!important;color:inherit!important}
.deck{margin-top:30px!important;max-width:790px!important;color:#56626f!important;font-size:16px!important;line-height:1.68!important}
.hero-media{width:min(var(--article-max),calc(100% - (var(--page) * 2)))!important;margin:0 auto!important;border-radius:0 0 24px 24px!important;background:#eef2f6!important;box-shadow:0 1px 0 rgba(11,17,23,.05)}
.hero-media img{aspect-ratio:16/8.4!important;object-position:center 52%!important}
.caption{width:min(var(--article-max),calc(100% - (var(--page) * 2)))!important;margin:12px auto 0!important;color:#8794a0!important;font-size:10px!important;letter-spacing:.02em}
.article{padding:88px var(--page) 118px!important}
.article-grid{width:min(1120px,100%)!important;grid-template-columns:180px minmax(0,var(--article-copy))!important;gap:72px!important}
.article-aside{top:108px!important;padding-top:2px!important;color:#84909c!important;font-size:9px!important;line-height:1.7!important;letter-spacing:.11em!important}
.article-aside strong{margin-bottom:14px!important;color:#17202b!important;font-size:14px!important;line-height:1.42!important}
.body{max-width:var(--article-copy)!important}
.lead{margin-bottom:40px!important;font-size:clamp(27px,2.8vw,38px)!important;line-height:1.33!important;letter-spacing:-.04em!important;color:#17202b!important}
.body p{margin-bottom:25px!important;color:#3f4a57!important;font-size:16px!important;line-height:1.82!important}
.body h2{margin:72px 0 22px!important;font-size:clamp(34px,3.8vw,50px)!important;line-height:1.04!important;letter-spacing:-.05em!important}
blockquote{margin:54px 0!important;padding:0 0 0 24px!important;border-left:2px solid var(--blue)!important;font-size:clamp(25px,2.7vw,36px)!important;line-height:1.38!important;color:#15202a!important}
.article-note{margin:52px 0!important;padding:24px 0!important;border-color:#dfe5ea!important}
.article-note strong{color:var(--blue)!important;font-size:9px!important;letter-spacing:.11em!important}
.article-note p{font-size:14px!important;line-height:1.7!important;color:#5d6975!important}
.article-end{margin-top:88px!important;padding-top:28px!important;border-color:#dfe5ea!important}
.article-author-copy strong{font-size:17px!important}
.next{padding:84px var(--page)!important;background:#0b1117!important;color:#fff!important;border-top:0!important}
.next-inner{width:min(var(--article-max),100%)!important;grid-template-columns:220px 1fr!important;gap:72px!important}
.next-label{color:#7fb9ff!important}
.next-link{border-top-color:rgba(255,255,255,.16)!important}
.next-link small{color:#9eabb8!important}
.next-link h2{max-width:980px!important;color:#fff!important;font-size:clamp(42px,5vw,72px)!important;transition:color .2s ease,transform .2s ease}
.next-link:hover h2{color:#7fb9ff!important;transform:translateX(4px)}
.stack-reveal{opacity:0;transform:translateY(22px);transition:opacity .65s cubic-bezier(.2,.7,.2,1),transform .65s cubic-bezier(.2,.7,.2,1)}
.stack-reveal.is-visible{opacity:1;transform:none}
@media(max-width:980px){.article-grid{grid-template-columns:1fr!important;gap:28px!important}.article-aside{position:static!important;max-width:560px}.next-inner{grid-template-columns:1fr!important;gap:28px!important}}
@media(max-width:700px){.hero{padding:48px var(--page) 34px!important}.hero-top{margin-bottom:34px!important}.hero h1{font-size:clamp(46px,13vw,66px)!important}.deck{font-size:15px!important}.hero-media{width:100%!important;border-radius:0!important}.caption{width:auto!important;margin:10px var(--page) 0!important}.article{padding-top:64px!important;padding-bottom:84px!important}.body p{font-size:16px!important}.body h2{margin-top:56px!important}.next{padding:64px var(--page)!important}.next-link h2{font-size:38px!important}}
@media(prefers-reduced-motion:reduce){.stack-reveal{opacity:1!important;transform:none!important;transition:none!important}.next-link h2,.back{transition:none!important}}
</style>
'''

JS = r'''
<script id="stack-article-reveal">
(()=>{
  const items=[...document.querySelectorAll('.hero-top,.hero h1,.deck,.hero-media,.article-aside,.body > *,.article-end,.next-inner')];
  if(!items.length)return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  items.forEach(el=>el.classList.add('stack-reveal'));
  const io=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');io.unobserve(entry.target)}}),{threshold:.08,rootMargin:'0px 0px -5% 0px'});
  items.forEach(el=>io.observe(el));
})();
</script>
'''

for path in FILES:
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'<style id="stack-article-refresh-v\d+">.*?</style>\s*', '', text, flags=re.S)
    text = re.sub(r'<script id="stack-article-reveal">.*?</script>\s*', '', text, flags=re.S)
    text = text.replace('</head>', CSS + '</head>')
    text = text.replace('</body>', JS + '</body>')
    path.write_text(text, encoding='utf-8')
    print(f'refreshed {path}')
