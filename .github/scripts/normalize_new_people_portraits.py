from pathlib import Path
import re
import numpy as np
import cv2
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

FACE_ENVELOPE = {
    'valentina-gran': (1.30, 2.15),
    'tomas-recart': (1.45, 2.45),
    'tamara-munoz': (1.20, 1.90),
    'ignacio-lepe': (1.35, 2.25),
}


def detect_main_face(img):
    rgb = np.array(img.convert('RGB'))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=5, minSize=(50, 50))
    if len(faces) == 0:
        return None
    h, w = gray.shape
    cx, cy = w / 2, h / 2
    best = None
    best_score = -1
    for x, y, fw, fh in faces:
        fx, fy = x + fw/2, y + fh/2
        dist = ((fx-cx)**2 + (fy-cy)**2) ** 0.5
        center_bonus = max(0.1, 1 - dist / max(h, w))
        score = fw * fh * center_bonus
        if score > best_score:
            best_score = score
            best = (x, y, fw, fh)
    return best


def face_guided_envelope(mask, face, slug):
    if face is None:
        return mask
    h, w = mask.shape
    x, y, fw, fh = face
    cx = x + fw / 2
    head_mult, body_mult = FACE_ENVELOPE.get(slug, (1.35, 2.2))

    env = np.zeros_like(mask, dtype=bool)
    top = max(0, int(y - 0.9 * fh))
    shoulder_y = min(h - 1, int(y + 2.2 * fh))

    for yy in range(top, h):
        if yy <= shoulder_y:
            t = (yy - top) / max(1, shoulder_y - top)
            half = fw * (head_mult + (1.55 - head_mult) * t)
        else:
            t = (yy - shoulder_y) / max(1, h - shoulder_y)
            half = fw * (1.55 + (body_mult - 1.55) * t)
        left = max(0, int(cx - half))
        right = min(w, int(cx + half))
        env[yy, left:right] = True

    # keep a generous ellipse around the head/upper hair so long hair is not clipped
    Y, X = np.ogrid[:h, :w]
    head_cy = y + 0.65 * fh
    rx = fw * 1.55
    ry = fh * 1.95
    head_ellipse = ((X - cx) / max(rx,1))**2 + ((Y - head_cy) / max(ry,1))**2 <= 1
    env |= head_ellipse
    return mask & env


def clean_mask(alpha_img, img, slug):
    alpha = np.array(alpha_img)
    mask = alpha > 28
    face = detect_main_face(img)
    mask = face_guided_envelope(mask, face, slug)

    # break thin bridges between main subject and background objects
    eroded = ndi.binary_erosion(mask, structure=np.ones((5,5)), iterations=1)
    labeled, num = ndi.label(eroded)
    if num > 0:
        if face is not None:
            x, y, fw, fh = face
            seed_x = int(x + fw/2)
            seed_y = int(y + fh*1.1)
            seed_y = max(0, min(eroded.shape[0]-1, seed_y))
            seed_x = max(0, min(eroded.shape[1]-1, seed_x))
            chosen = labeled[seed_y, seed_x]
        else:
            chosen = 0
        if chosen == 0:
            areas = ndi.sum(eroded, labeled, index=range(1, num+1))
            chosen = int(np.argmax(areas)) + 1
        core = labeled == chosen
        core = ndi.binary_dilation(core, structure=np.ones((5,5)), iterations=1)
        mask &= core

    mask = ndi.binary_closing(mask, structure=np.ones((5,5)))
    mask = ndi.binary_fill_holes(mask)
    mask = ndi.binary_opening(mask, structure=np.ones((3,3)))
    clean = (mask * 255).astype(np.uint8)
    return Image.fromarray(clean, mode='L').filter(ImageFilter.GaussianBlur(0.9))


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

    alpha = clean_mask(cut.getchannel('A'), img, slug)
    cut.putalpha(alpha)
    bbox = alpha.getbbox()
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
    subject = subject.resize((max(1, round(subject.width*scale)), max(1, round(subject.height*scale))), Image.Resampling.LANCZOS)

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
        f'<div class="portrait"><div class="portrait-inner"><img src="{image}?v=20261029-2318" alt="{name}" loading="lazy"></div></div>'
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
