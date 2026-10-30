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
    return max(faces, key=lambda f: f[2]*f[3] * max(.2, 1 - (((f[0]+f[2]/2-cx)**2 + (f[1]+f[3]/2-cy)**2) ** .5) / max(h,w)))


def hard_subject_window(shape, face, slug):
    h, w = shape
    if face is None:
        return np.ones((h, w), dtype=bool)
    x, y, fw, fh = face
    cx = x + fw/2
    top = max(0, int(y - 1.0*fh))
    env = np.zeros((h, w), dtype=bool)

    for yy in range(top, h):
        t = min(1.0, max(0.0, (yy-top)/max(1, h-top)))
        if slug == 'valentina-gran':
            left_mult = 0.82 + 0.18*t
            right_mult = 1.42 + 0.30*t
        elif slug == 'tamara-munoz':
            left_mult = 1.42 + 0.30*t
            right_mult = 0.72 + 0.14*t
        else:
            left_mult = right_mult = 1.55 + 0.25*t
        l = max(0, int(cx - fw*left_mult))
        r = min(w, int(cx + fw*right_mult))
        env[yy, l:r] = True

    Y, X = np.ogrid[:h, :w]
    if slug == 'valentina-gran':
        rx_l, rx_r = 1.05, 1.35
    elif slug == 'tamara-munoz':
        rx_l, rx_r = 1.35, 1.00
    else:
        rx_l = rx_r = 1.55

    head_y = y + .55*fh
    rx = np.where(X <= cx, fw*rx_l, fw*rx_r)
    head = ((X-cx)/rx)**2 + ((Y-head_y)/(fh*1.72))**2 <= 1
    env |= head
    return env


def refine_with_grabcut(img, rembg_alpha, face, slug):
    rgb = np.array(img.convert('RGB'))
    h, w = rgb.shape[:2]
    alpha = np.array(rembg_alpha)
    env = hard_subject_window((h, w), face, slug)

    if face is None:
        m = (alpha > 12) & env
        m = ndi.binary_closing(m, structure=np.ones((3,3)))
        return Image.fromarray((m*255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(1.5))

    x, y, fw, fh = face
    cx = int(x + fw/2)
    cy = int(y + fh/2)

    gc = np.full((h,w), cv2.GC_BGD, np.uint8)
    gc[(alpha > 12) & env] = cv2.GC_PR_FGD
    Y, X = np.ogrid[:h, :w]
    face_seed = ((X-cx)/(fw*.70))**2 + ((Y-cy)/(fh*.90))**2 <= 1
    gc[face_seed] = cv2.GC_FGD

    torso_l = max(0, int(cx - fw*.60))
    torso_r = min(w, int(cx + fw*.60))
    torso_t = min(h, int(y + fh*1.0))
    torso_b = min(h, int(y + fh*4.4))
    gc[torso_t:torso_b, torso_l:torso_r] = cv2.GC_FGD
    gc[~env] = cv2.GC_BGD
    gc[alpha < 3] = cv2.GC_BGD

    bgd = np.zeros((1,65), np.float64)
    fgd = np.zeros((1,65), np.float64)
    try:
        cv2.grabCut(rgb, gc, None, bgd, fgd, 8, cv2.GC_INIT_WITH_MASK)
        mask = (gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD)
    except cv2.error:
        mask = (alpha > 12) & env

    mask &= env

    if slug == 'valentina-gran':
        y0 = max(0, int(y - .15*fh))
        for yy in range(y0, h):
            t = min(1.0, max(0.0, (yy-y0)/max(1, h-y0)))
            keep_from = int(cx - fw*(.70 + .12*t))
            mask[yy, :max(0, keep_from)] = False
    elif slug == 'tamara-munoz':
        y0 = max(0, int(y - .10*fh))
        for yy in range(y0, h):
            t = min(1.0, max(0.0, (yy-y0)/max(1, h-y0)))
            keep_to = int(cx + fw*(.62 + .10*t))
            mask[yy, min(w, keep_to):] = False

    labels, n = ndi.label(mask)
    ids = labels[face_seed]
    ids = ids[ids > 0]
    if len(ids):
        chosen = int(np.bincount(ids).argmax())
        mask = labels == chosen

    mask = ndi.binary_closing(mask, structure=np.ones((3,3)))
    mask = ndi.binary_fill_holes(mask)
    out = Image.fromarray((mask*255).astype(np.uint8), 'L')
    return out.filter(ImageFilter.GaussianBlur(1.9))


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
        alpha = refine_with_grabcut(img, raw.getchannel('A'), face, slug)
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
        (max(1, round(subject.width*scale)), max(1, round(subject.height*scale))),
        Image.Resampling.LANCZOS,
    )

    canvas = Image.new('RGBA', CANVAS, BG)
    x = (CANVAS[0] - subject.width)//2
    y = CANVAS[1] - subject.height
    canvas.alpha_composite(subject, (x,y))
    canvas.convert('RGB').save(OUT / f'{slug}.png', 'PNG', optimize=True)
    print('processed', slug)


if __name__ == '__main__':
    session = new_session('u2net_human_seg')
    for slug, src in PEOPLE.items():
        process(slug, src, session)
