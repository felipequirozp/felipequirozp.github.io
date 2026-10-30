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
Y_SHIFT = {'valentina-gran': 6, 'tomas-recart': 8, 'tamara-munoz': 10, 'ignacio-lepe': 8}


def central_seed(mask, iterations=12):
    eroded = ndi.binary_erosion(mask, iterations=iterations)
    labels, count = ndi.label(eroded)
    if count == 0:
        return None

    h, w = mask.shape
    best_label = 0
    best_score = -1
    for lab in range(1, count + 1):
        comp = labels == lab
        area = int(comp.sum())
        if area == 0:
            continue
        ys, xs = np.nonzero(comp)
        cx = xs.mean() / w
        cy = ys.mean() / h
        # Strongly prefer a sizeable component around the face/torso center.
        center = max(0.0, 1.0 - abs(cx - .5) * 2.8)
        upper = max(0.0, 1.0 - abs(cy - .42) * 1.8)
        score = area * (1.0 + center * 2.5 + upper * 1.2)
        if score > best_score:
            best_score = score
            best_label = lab
    return labels == best_label if best_label else None


def refine_alpha(alpha_img, slug):
    alpha = np.array(alpha_img)
    original = alpha > 28

    # Break thin bridges between the subject and stubborn background objects,
    # then reconstruct only the region connected to the central person seed.
    seed = central_seed(original, iterations=14)
    if seed is None:
        seed = central_seed(original, iterations=8)
    if seed is not None:
        mask = ndi.binary_propagation(seed, mask=original)
    else:
        mask = original

    # Remove tiny islands and close pinholes without regrowing removed background.
    labels, n = ndi.label(mask)
    if n:
        sizes = ndi.sum(mask, labels, index=range(1, n + 1))
        keep = [i + 1 for i, s in enumerate(sizes) if s >= 900]
        mask = np.isin(labels, keep)

    mask = ndi.binary_fill_holes(mask)
    mask = ndi.binary_closing(mask, structure=np.ones((5, 5)))

    # Per-photo guard rails for the two images where rembg repeatedly kept
    # obvious side-background people/shapes. These only trim outer zones.
    h, w = mask.shape
    if slug == 'tamara-munoz':
        mask[:, int(w * .86):] = False
    elif slug == 'valentina-gran':
        # remove the far-left circular backdrop while preserving hair/shoulder
        yy, xx = np.ogrid[:h, :w]
        forbidden = (xx < w * .13) & (yy > h * .22)
        mask[forbidden] = False

    clean = (mask * 255).astype(np.uint8)
    clean = Image.fromarray(clean, mode='L').filter(ImageFilter.GaussianBlur(1.35))
    return clean


def process(slug, src_path, session):
    img = Image.open(ROOT / src_path).convert('RGBA')
    cut = remove(
        img,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=245,
        alpha_matting_background_threshold=8,
        alpha_matting_erode_size=10,
    ).convert('RGBA')

    clean_alpha = refine_alpha(cut.getchannel('A'), slug)
    cut.putalpha(clean_alpha)
    bbox = clean_alpha.getbbox()
    if not bbox:
        raise RuntimeError(f'No foreground detected for {slug}')

    subject = cut.crop(bbox)
    gray = ImageOps.grayscale(subject.convert('RGB')).convert('RGBA')
    gray.putalpha(subject.getchannel('A'))
    subject = gray

    scale = TARGET_HEIGHT / subject.height
    max_w = int(CANVAS[0] * .88)
    if subject.width * scale > max_w:
        scale = max_w / subject.width
    subject = subject.resize((max(1, round(subject.width * scale)), max(1, round(subject.height * scale))), Image.Resampling.LANCZOS)

    canvas = Image.new('RGBA', CANVAS, BG)
    x = (CANVAS[0] - subject.width) // 2
    y = CANVAS[1] - subject.height + Y_SHIFT.get(slug, 0)
    canvas.alpha_composite(subject, (x, y))

    out = OUT / f'{slug}.png'
    canvas.convert('RGB').save(out, 'PNG', optimize=True)
    print(f'Processed {src_path} -> {out}')


def card(name, image, linkedin):
    return (
        f'<article class="person"><a class="card-link" href="{linkedin}" target="_blank" rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a>'
        f'<div class="portrait"><div class="portrait-inner"><img src="{image}?v=20261029-2315" alt="{name}" loading="lazy"></div></div>'
        f'<div class="person-copy"><h3>{name}</h3></div></article>'
    )


def patch_html(path):
    text = path.read_text(encoding='utf-8')
    for slug, (_, name, linkedin) in PEOPLE.items():
        pattern = re.compile(r'<article class="person">(?:(?!</article>).)*?<h3>' + re.escape(name) + r'</h3>(?:(?!</article>).)*?</article>', re.S)
        text, n = pattern.subn(card(name, f'/images/people/{slug}.png', linkedin), text, count=1)
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
