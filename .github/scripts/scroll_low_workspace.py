from pathlib import Path

paths = [Path('lowsignal/low-workspace.html'), Path('es/lowsignal/low-workspace.html')]

css = '''\n<style id="low-workspace-scroll-reveal">\n  .reveal-on-scroll{opacity:0;transform:translateY(28px);transition:opacity .7s cubic-bezier(.2,.65,.3,1),transform .7s cubic-bezier(.2,.65,.3,1)}\n  .reveal-on-scroll.is-visible{opacity:1;transform:none}\n  .reveal-on-scroll[data-delay="1"]{transition-delay:.08s}\n  .reveal-on-scroll[data-delay="2"]{transition-delay:.16s}\n  .reveal-on-scroll[data-delay="3"]{transition-delay:.24s}\n  @media(prefers-reduced-motion:reduce){.reveal-on-scroll{opacity:1!important;transform:none!important;transition:none!important}}\n</style>\n'''

js = '''\n<script id="low-workspace-scroll-reveal-script">\n(()=>{\n  if(!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;\n  const selectors=['.section-grid','.feature-grid','.build-grid','.showcase-head','.product-shot','.login-story','.principle','.project-nav-inner','.footer-grid'];\n  const targets=[];\n  selectors.forEach(sel=>document.querySelectorAll(sel).forEach(el=>targets.push(el)));\n  targets.forEach((el,i)=>{\n    el.classList.add('reveal-on-scroll');\n    if(i%4) el.dataset.delay=String(i%4);\n  });\n  const io=new IntersectionObserver(entries=>{\n    entries.forEach(entry=>{\n      if(entry.isIntersecting){\n        entry.target.classList.add('is-visible');\n        io.unobserve(entry.target);\n      }\n    });\n  },{threshold:.12,rootMargin:'0px 0px -6% 0px'});\n  targets.forEach(el=>io.observe(el));\n})();\n</script>\n'''

for path in paths:
    text = path.read_text(encoding='utf-8')
    if 'low-workspace-scroll-reveal' in text:
        continue
    text = text.replace('</head>', css + '\n</head>', 1)
    text = text.replace('</body>', js + '\n</body>', 1)
    path.write_text(text, encoding='utf-8')
