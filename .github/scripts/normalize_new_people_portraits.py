from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageOps, ImageFilter
from rembg import remove, new_session
from scipy import ndimage as ndi

ROOT = Path('.')
OUT = ROOT / 'images' / 'people'
OUT.mkdir(parents=True, exist_ok=True)

PEOPLE = {
    'valentina-gran': 'images/vgran.png',
    'tomas-recart': 'images/tomas.png',
    'tamara-munoz': 'images/tamara.png',
    'ignacio-lepe': 'images/lepe.png',
}

CANVAS = (720, 810)
BG = (241, 241, 241, 255)
TARGET_H = {k: 700 for k in PEOPLE}


def detect_face(img):
    rgb = np.array(img.convert('RGB'))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(45, 45))
    if len(faces) == 0:
        return None
    h, w = gray.shape
    cx, cy = w / 2, h / 2
    return max(
        faces,
        key=lambda f: f[2] * f[3] * max(.2, 1 - (((f[0] + f[2] / 2 - cx) ** 2 + (f[1] + f[3] / 2 - cy) ** 2) ** .5) / max(h, w)),
    )


def connected_to_face(mask, face):
    if face is None:
        return mask
    x, y, fw, fh = face
    h, w = mask.shape
    cx = int(x + fw / 2)
    cy = int(y + fh / 2)
    Y, X = np.ogrid[:h, :w]
    seed = ((X - cx) / max(1, fw * .78)) ** 2 + ((Y - cy) / max(1, fh * 1.00)) ** 2 <= 1
    labels, _ = ndi.label(mask)
    ids = labels[seed]
    ids = ids[ids > 0]
    if len(ids):
        chosen = int(np.bincount(ids).argmax())
        return labels == chosen
    return mask


def deterministic_subject_mask(rembg_alpha, face, slug):
    alpha = np.array(rembg_alpha)
    base = alpha > 10
    h, w = base.shape

    if face is None:
        base = ndi.binary_closing(base, structure=np.ones((3, 3)))
        base = ndi.binary_fill_holes(base)
        return Image.fromarray((base * 255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(1.25))

    x, y, fw, fh = [float(v) for v in face]
    cx = x + fw / 2
    top = max(0, int(y - .55 * fh))
    window = np.zeros((h, w), dtype=np.float32)

    for yy in range(top, h):
        t = min(1.0, max(0.0, (yy - top) / max(1, h - top)))
        if slug == 'valentina-gran':
            left_mult = .70 + .26 * t
            right_mult = 1.42 + .26 * t
        elif slug == 'tamara-munoz':
            left_mult = 1.36 + .22 * t
            right_mult = .66 + .20 * t
        else:
            left_mult = right_mult = 1.55 + .20 * t

        l = max(0, int(cx - fw * left_mult))
        r = min(w, int(cx + fw * right_mult))
        if r > l:
            window[yy, l:r] = 1.0

    Y, X = np.ogrid[:h, :w]
    head_y = y + .55 * fh
    if slug == 'valentina-gran':
        head = ((X - cx) / max(1, fw * 1.02)) ** 2 + ((Y - head_y) / max(1, fh * 1.70)) ** 2 <= 1
        y0 = max(0, int(y - .05 * fh))
        for yy in range(y0, h):
            t = min(1.0, max(0.0, (yy - y0) / max(1, h - y0)))
            cut = max(0, int(cx - fw * (.68 + .22 * t)))
            head[yy, :cut] = False
    elif slug == 'tamara-munoz':
        head = ((X - cx) / max(1, fw * .98)) ** 2 + ((Y - head_y) / max(1, fh * 1.70)) ** 2 <= 1
        y0 = max(0, int(y - .05 * fh))
        for yy in range(y0, h):
            t = min(1.0, max(0.0, (yy - y0) / max(1, h - y0)))
            cut = min(w, int(cx + fw * (.62 + .18 * t)))
            head[yy, cut:] = False
    else:
        head = ((X - cx) / max(1, fw * 1.55)) ** 2 + ((Y - head_y) / max(1, fh * 1.75)) ** 2 <= 1

    window = np.maximum(window, head.astype(np.float32))
    mask = base & (window > .5)
    mask = connected_to_face(mask, face)
    mask = ndi.binary_closing(mask, structure=np.ones((3, 3)))
    mask = ndi.binary_fill_holes(mask)

    out = Image.fromarray((mask * 255).astype(np.uint8), 'L')
    return out.filter(ImageFilter.GaussianBlur(1.35))


def smooth_ignacio(rembg_alpha):
    a = rembg_alpha.filter(ImageFilter.GaussianBlur(1.55))
    arr = np.array(a, dtype=np.float32)
    arr[arr < 5] = 0
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(.8))


def process(slug, src, session):
    img = Image.open(ROOT / src).convert('RGBA')
    raw = remove(
        img,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=228,
        alpha_matting_background_threshold=4,
        alpha_matting_erode_size=1,
    ).convert('RGBA')

    face = detect_face(img)
    if slug == 'ignacio-lepe':
        alpha = smooth_ignacio(raw.getchannel('A'))
    elif slug in ('valentina-gran', 'tamara-munoz'):
        alpha = deterministic_subject_mask(raw.getchannel('A'), face, slug)
    else:
        alpha = raw.getchannel('A').filter(ImageFilter.GaussianBlur(.8))

    raw.putalpha(alpha)
    bbox = alpha.getbbox()
    if not bbox:
        raise RuntimeError(f'No foreground for {slug}')

    subject = raw.crop(bbox)
    gray = ImageOps.grayscale(subject.convert('RGB')).convert('RGBA')
    gray.putalpha(subject.getchannel('A'))
    subject = gray

    scale = TARGET_H[slug] / subject.height
    max_w = int(CANVAS[0] * .84)
    if subject.width * scale > max_w:
        scale = max_w / subject.width

    subject = subject.resize(
        (max(1, round(subject.width * scale)), max(1, round(subject.height * scale))),
        Image.Resampling.LANCZOS,
    )

    canvas = Image.new('RGBA', CANVAS, BG)
    x = (CANVAS[0] - subject.width) // 2
    y = CANVAS[1] - subject.height
    canvas.alpha_composite(subject, (x, y))
    canvas.convert('RGB').save(OUT / f'{slug}.png', 'PNG', optimize=True)
    print('processed', slug)


if __name__ == '__main__':
    session = new_session('u2net_human_seg')
    for slug, src in PEOPLE.items():
        process(slug, src, session)
