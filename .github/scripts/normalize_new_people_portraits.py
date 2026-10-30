from pathlib import Path
import re
from PIL import Image, ImageOps, ImageFilter
from rembg import remove, new_session

ROOT = Path('.')
OUT = ROOT / 'images' / 'people'
OUT.mkdir(parents=True, exist_ok=True)

PEOPLE = {
    'valentina-gran': ('images/vgran.png', 'Valentina Gran', 'https://www.linkedin.com/in/valentina-gran-koch-0b945325/'),
    'tomas-recart': ('images/tomas.png', 'Tomás Recart', 'https://www.linkedin.com/in/tomas-recart-balze-a9957918a/'),
    'tamara-munoz': ('images/tamara.png', 'Tamara Muñoz', 'https://www.linkedin.com/in/tamara-munoz-ojeda/'),
    'ignacio-lepe': ('images/lepe.png', 'Ignacio Lepe', 'https://www.linkedin.com/in/ignacio-lepe-6026b4215/'),
}

CANVAS = (720, 810)
TARGET_HEIGHT = 740
Y_SHIFT = {'valentina-gran': 12, 'tomas-recart': 12, 'tamara-munoz': 8, 'ignacio-lepe': 8}


def process(slug, src_path, session):
    img = Image.open(ROOT / src_path).convert('RGBA')
    cut = remove(img, session=session, alpha_matting=True,
                 alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=12,
                 alpha_matting_erode_size=8).convert('RGBA')
    alpha = cut.getchannel('A').filter(ImageFilter.GaussianBlur(0.45))
    cut.putalpha(alpha)
    bbox = alpha.getbbox()
    if not bbox:
        raise RuntimeError(f'No foreground detected for {slug}')
    subject = cut.crop(bbox)
    gray = ImageOps.grayscale(subject.convert('RGB')).convert('RGBA')
    gray.putalpha(subject.getchannel('A'))
    subject = gray
    scale = TARGET_HEIGHT / subject.height
    max_w = int(CANVAS[0] * 0.96)
    if subject.width * scale > max_w:
        scale = max_w / subject.width
    new_size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(new_size, Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', CANVAS, (255, 255, 255, 0))
    x = (CANVAS[0] - subject.width) // 2
    y = CANVAS[1] - subject.height + Y_SHIFT.get(slug, 0)
    canvas.alpha_composite(subject, (x, y))
    out = OUT / f'{slug}.png'
    canvas.save(out, 'PNG', optimize=True)
    print(f'Processed {src_path} -> {out}')


def card(name, image, linkedin):
    return (
        f'<article class="person"><a class="card-link" href="{linkedin}" target="_blank" '
        f'rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a>'
        f'<div class="portrait"><div class="portrait-inner"><img src="{image}?v=20261029-2205" '
        f'alt="{name}" loading="lazy" style="transform:none!important"></div></div>'
        f'<div class="person-copy"><h3>{name}</h3></div></article>'
    )


def patch_html(path):
    text = path.read_text(encoding='utf-8')
    for slug, (_, name, linkedin) in PEOPLE.items():
        pattern = rf'<article class="person">.*?<h3>{re.escape(name)}</h3>.*?</article>'
        replacement = card(name, f'/images/people/{slug}.png', linkedin)
        text, n = re.subn(pattern, replacement, text, count=1, flags=re.S)
        if n != 1:
            raise RuntimeError(f'Could not replace card for {name} in {path}')
    path.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    session = new_session('u2net_human_seg')
    for slug, (src, _, _) in PEOPLE.items():
        process(slug, src, session)
    patch_html(Path('people.html'))
    patch_html(Path('es/people.html'))
