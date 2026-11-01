from pathlib import Path
import re

STYLE = '''<style id="people-final-visual-v7">
.people-all img[alt="Alejandra Mustakis"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(.95) translateY(4%)!important}
.people-all img[alt="Domingo Errázuriz"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(.95) translateY(4%)!important}
.people-all img[alt="Javier Robledo"]{transform:scale(1.34) translateY(10%)!important}
.people-all img[alt="Jorge Muñoz"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(1.06) translateY(0)!important}
.people-all img[alt="Lía Morice"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(1.03) translateY(0)!important}
</style>'''

for filename in ["people.html", "es/people.html"]:
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<style id="people-final-visual-v\d+">.*?</style>\s*', '', text, flags=re.S)
    text = text.replace('</head>', STYLE + '\n</head>', 1)
    text = re.sub(r'<script src="/mobile-nav\.js(?:\?v=[^"]*)?" defer></script>', '<script src="/mobile-nav.js?v=20261101n" defer></script>', text)
    path.write_text(text, encoding="utf-8")

js = Path("mobile-nav.js")
text = js.read_text(encoding="utf-8")
text = text.replace("['José Espinosa','/images/jose-manual.png'", "['José Espinosa','/images/Jose-espinosa.png'")
text = re.sub(
    r"const tune=document\.createElement\('style'\);tune\.id='people-portrait-tuning-v\d+';tune\.textContent=`.*?`;document\.head\.appendChild\(tune\);",
    "const tune=document.createElement('style');tune.id='people-portrait-tuning-v7';tune.textContent=`.people-all img[alt=\"Alejandra Mustakis\"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(.95) translateY(4%)!important}.people-all img[alt=\"Domingo Errázuriz\"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(.95) translateY(4%)!important}.people-all img[alt=\"Javier Robledo\"]{transform:scale(1.34) translateY(10%)!important}.people-all img[alt=\"Jorge Muñoz\"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(1.06) translateY(0)!important}.people-all img[alt=\"Lía Morice\"]{object-fit:contain!important;object-position:center bottom!important;transform:scale(1.03) translateY(0)!important}`;document.head.appendChild(tune);",
    text,
    flags=re.S,
)
text = text.replace('20261101k', '20261101n').replace('20261101m', '20261101n')
js.write_text(text, encoding="utf-8")
