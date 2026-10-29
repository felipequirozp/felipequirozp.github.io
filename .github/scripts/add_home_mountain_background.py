from pathlib import Path

files = [Path('index.html'), Path('es/index.html')]
style = '''<style id="home-mountain-closing">
.closing{position:relative;isolation:isolate;background:#0b1117!important;overflow:hidden}
.closing::before{content:"";position:absolute;inset:0;z-index:-2;background:url('/images/edificios.jpg') center 48%/cover no-repeat;filter:grayscale(100%);transform:scale(1.01)}
.closing::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(5,11,17,.93) 0%,rgba(5,11,17,.88) 45%,rgba(5,11,17,.80) 100%)}
.closing-inner{position:relative;z-index:1}
@media(max-width:700px){.closing::before{background-position:62% center}.closing::after{background:linear-gradient(180deg,rgba(5,11,17,.91),rgba(5,11,17,.86))}}
</style>'''

for path in files:
    s = path.read_text()
    if 'id="home-mountain-closing"' not in s:
        s = s.replace('</head>', style + '</head>')
    path.write_text(s)

print('Applied mountain closing background to EN/ES home')