from pathlib import Path
from io import BytesIO
import requests
from PIL import Image, ImageFilter
from rembg import remove, new_session

ROOT = Path('.')
OUT = ROOT / 'images' / 'people'
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    'christopher-neilson': 'images/christopher-neilson.jpg',
    'zack-tseng': 'images/zack-tseng.jpg',
    'nicolas-munoz': 'https://lowsignal.cl/assets/nicolas-munoz.jpg',
    'damian-aldunate': 'images/team_damian-1.png',
    'matias-bussinger': 'images/team-matias.png',
    'lia-morice': 'images/team_lia-1.png',
    'martin-alvarado': 'images/team_martin-1.png',
    'jorge-munoz': 'images/team_jorge-1.png',
    'francisca-astudillo': 'images/francisca-astudillo.jpg',
    'rodrigo-lewit': 'images/rodrigo-lewit.jpg',
    'juan-yuz': 'images/yuz-rector.png',
    'karen-radonich': 'images/karen-radonich.jpg',
    'javier-robledo': 'images/javier-robledo.jpg',
}

OLD_TO_NEW = {
    '/images/christopher-neilson.jpg': '/images/people/christopher-neilson.webp',
    '/images/zack-tseng.jpg': '/images/people/zack-tseng.webp',
    'https://lowsignal.cl/assets/nicolas-munoz.jpg': '/images/people/nicolas-munoz.webp',
    '/images/team_damian-1.png': '/images/people/damian-aldunate.webp',
    '/images/team-matias.png': '/images/people/matias-bussinger.webp',
    '/images/team_lia-1.png': '/images/people/lia-morice.webp',
    '/images/team_martin-1.png': '/images/people/martin-alvarado.webp',
    '/images/team_jorge-1.png': '/images/people/jorge-munoz.webp',
    '/images/francisca-astudillo.jpg': '/images/people/francisca-astudillo.webp',
    '/images/rodrigo-lewit.jpg': '/images/people/rodrigo-lewit.webp',
    '/images/yuz-rector.png': '/images/people/juan-yuz.webp',
    '/images/karen-radonich.jpg': '/images/people/karen-radonich.webp',
    '/images/javier-robledo.jpg': '/images/people/javier-robledo.webp',
}

CANVAS = (720, 840)
TOP = (242, 246, 248)
BOTTOM = (226, 234, 239)
FLAT = (241, 241, 241)

def load_image(source: str) -> Image.Image:
    if source.startswith('http'):
        r = requests.get(source, timeout=30)
        r.raise_for_status()
        return Image.open(BytesIO(r.content)).convert('RGBA')
    return Image.open(ROOT / source).convert('RGBA')


def gradient_bg(size):
    w, h = size
    bg = Image.new('RGB', size)
    px = bg.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(round(TOP[i] * (1-t) + BOTTOM[i] * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return bg.convert('RGBA')


def process_one(slug: str, source: str, session):
    src = load_image(source)
    cut = remove(src, session=session, alpha_matting=True,
                 alpha_matting_foreground_threshold=235,
                 alpha_matting_background_threshold=15,
                 alpha_matting_erode_size=8)
    cut = cut.convert('RGBA')
    alpha = cut.getchannel('A').filter(ImageFilter.GaussianBlur(0.45))
    cut.putalpha(alpha)
    bbox = alpha.getbbox()
    if not bbox:
        raise RuntimeError(f'No foreground detected for {slug}')
    subject = cut.crop(bbox)
    max_w = int(CANVAS[0] * 0.82)
    max_h = int(CANVAS[1] * 0.90)
    scale = min(max_w / subject.width, max_h / subject.height)
    new_size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(new_size, Image.Resampling.LANCZOS)

    if slug == 'damian-aldunate':
        bg = Image.new('RGBA', CANVAS, FLAT + (255,))
    else:
        bg = gradient_bg(CANVAS)

    x = (CANVAS[0] - subject.width) // 2
    y = CANVAS[1] - subject.height - 22
    if slug == 'damian-aldunate':
        # Bake the lower framing into the bitmap itself so CSS never exposes
        # a second background tone above the image.
        y += 72
    if y < 16:
        y = 16
    bg.alpha_composite(subject, (x, y))
    out = OUT / f'{slug}.webp'
    bg.convert('RGB').save(out, 'WEBP', quality=92, method=6)
    print(f'processed {slug} -> {out}')


def patch_references():
    for path in [Path('people.html'), Path('es/people.html'), Path('.github/scripts/unify_people_grid.py')]:
        text = path.read_text(encoding='utf-8')
        for old, new in OLD_TO_NEW.items():
            text = text.replace(old, new)
        text = text.replace('filter:grayscale(100%) saturate(.45) contrast(.93) brightness(1.05)!important;mix-blend-mode:multiply',
                            'filter:grayscale(100%) contrast(.96) brightness(1.02)!important;mix-blend-mode:normal')
        path.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    session = new_session('u2net_human_seg')
    for slug, source in SOURCES.items():
        process_one(slug, source, session)
    patch_references()
