from pathlib import Path
import re
import numpy as np
from PIL import Image, ImageOps, ImageFilter
from rembg import remove, new_session
from scipy import ndimage as ndi

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
TARGET_HEIGHT = 735
BG = (241, 241, 241, 255)

Y_SHIFT = {
    'valentina-gran': 6,
    'tomas-recart': 8,
    'tamara-munoz': 10,
    'ignacio-lepe': 8,
}


def choose_best_component(mask):
    labeled, num = ndi.label(mask)
    if num == 0:
        return mask

    h, w = mask.shape
    cy, cx = h / 2, w / 2
    best_label = None
    best_score = -1e18

    for label_id in range(1, num + 1):
        comp = labeled == label_id
        area = comp.sum()
        if area < 1500:
            continue

        ys, xs = np.nonzero(comp)
        y0, y1 = ys.min(), ys.max()
        x0, x1 = xs.min(), xs.max()
        comp_cy = ys.mean()
        comp_cx = xs.mean()

        dist = ((comp_cx - cx) ** 2 + (comp_cy - cy) ** 2) ** 0.5
        center_bonus = max(0, 1 - dist / max(h, w))
        bbox_h = y1 - y0 + 1
        bbox_w = x1 - x0 + 1
        tall_bonus = bbox_h / max(1, bbox_w)

        score = area * 1.0 + center_bonus * 30000 + tall_bonus * 12000

        if score > best_score:
            best_score = score
            best_label = label_id

    if best_label is None:
        areas = ndi.sum(mask, labeled, index=range(1, num + 1))
        best_label = int(np.argmax(areas)) + 1

    return labeled == best_label


def refine_alpha(alpha_img):
    alpha = np.array(alpha_img)
    mask = alpha > 20
    mask = choose_best_component(mask)
    mask = ndi.binary_closing(mask, structure=np.ones((7, 7)))
    mask = ndi.binary_fill_holes(mask)
    mask = ndi.binary_opening(mask, structure=np.ones((3, 3)))
    mask = ndi.binary_dilation(mask, structure=np.ones((3, 3)), iterations=1)

    clean = (mask * 255).astype(np.uint8)
    return Image.fromarray(clean, mode='L').filter(ImageFilter.GaussianBlur(1.1))


def process(slug, src_path, session):
    img = Image.open(ROOT / src_path).convert('RGBA')

    cut = remove(
        img,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=6,
    ).convert('RGBA')

    clean_alpha = refine_alpha(cut.getchannel('A'))
    cut.putalpha(clean_alpha)

    bbox = clean_alpha.getbbox()
    if not bbox:
        raise RuntimeError(f'No foreground detected for {slug}')

    subject = cut.crop(bbox)
    gray = ImageOps.grayscale(subject.convert('RGB')).convert('RGBA')
    gray.putalpha(subject.getchannel('A'))
    subject = gray

    scale = TARGET_HEIGHT / subject.height
    max_w = int(CANVAS[0] * 0.88)
    if subject.width * scale > max_w:
        scale = max_w / subject.width

    new_size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(new_size, Image.Resampling.LANCZOS)

    canvas = Image.new('RGBA', CANVAS, BG)
    x = (CANVAS[0] - subject.width) // 2
    y = CANVAS[1] - subject.height + Y_SHIFT.get(slug, 0)
    canvas.alpha_composite(subject, (x, y))

    out = OUT / f'{slug}.png'
    canvas.convert('RGB').save(out, 'PNG', optimize=True)
    print(f'Processed {src_path} -> {out}')


def card(name, image, linkedin):
    return (
        f'<article class="person"><a class="card-link" href="{linkedin}" target="_blank" '
        f'rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a>'
        f'<div class="portrait"><div class="portrait-inner"><img src="{image}?v=20261029-2305" '
        f'alt="{name}" loading="lazy"></div></div>'
        f'<div class="person-copy"><h3>{name}</h3></div></article>'
    )


def patch_html(path):
    text = path.read_text(encoding='utf-8')
    for slug, (_, name, linkedin) in PEOPLE.items():
        pattern = re.compile(
            r'<article class="person">(?:(?!</article>).)*?<h3>'
            + re.escape(name)
            + r'</h3>(?:(?!</article>).)*?</article>',
            re.S,
        )
        replacement = card(name, f'/images/people/{slug}.png', linkedin)
        text, n = pattern.subn(replacement, text, count=1)
        if n != 1:
            raise RuntimeError(f'Could not replace card for {name} in {path}')

    expected = ['Christopher Neilson','Zack Tseng','Nicolás Muñoz','Leidy Gómez','Rodrigo Lewit','Karen Radonich','Valentina Gran','Tomás Recart','Tamara Muñoz','Ignacio Lepe','Valentina Wagenreld','Damián Aldunate','Matías Bussinger','Lía Morice','Martín Alvarado','Jorge Muñoz','Francisca Astudillo','Juan Yuz','Javier Robledo']
    for name in expected:
        if text.count(f'<h3>{name}</h3>') != 1:
            raise RuntimeError(f'{path}: invalid count for {name}')

    path.write_text(text, encoding='utf-8')


if __name__ == '__main__':
    session = new_session('u2net_human_seg')
    for slug, (src, _, _) in PEOPLE.items():
        process(slug, src, session)

    patch_html(Path('people.html'))
    patch_html(Path('es/people.html'))
