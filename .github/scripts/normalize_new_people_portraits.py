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
TARGET_H = {
    'valentina-gran': 700,
    'tomas-recart': 700,
    'tamara-munoz': 700,
    'ignacio-lepe': 700,
}


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


def base_envelope(shape, face, slug):
    h, w = shape
    if face is None:
        return np.ones((h, w), dtype=bool)
    x, y, fw, fh = face
    cx = x + fw/2
    env = np.zeros((h, w), dtype=bool)
    top = max(0, int(y - 1.05*fh))

    if slug == 'valentina-gran':
        left_top, right_top, left_bottom, right_bottom = 1.18, 1.42, 1.48, 1.82
    elif slug == 'tamara-munoz':
        left_top, right_top, left_bottom, right_bottom = 1.45, 1.12, 1.82, 1.38
    else:
        left_top = right_top = 1.48
        left_bottom = right_bottom = 1.90

    for yy in range(top, h):
        t = min(1.0, max(0.0, (yy-top)/max(1, h-top)))
        lm = left_top + (left_bottom-left_top)*t
        rm = right_top + (right_bottom-right_top)*t
        l = max(0, int(cx-fw*lm))
        r = min(w, int(cx+fw*rm))
        env[yy, l:r] = True

    Y, X = np.ogrid[:h, :w]
    head = ((X-cx)/(fw*1.48))**2 + ((Y-(y+0.55*fh))/(fh*1.82))**2 <= 1
    env |= head
    return env


def manual_background_cuts(mask, face, slug):
    if face is None:
        return mask
    h, w = mask.shape
    x, y, fw, fh = face
    cx = x + fw/2

    # These are deliberate manual exclusions for the two source photos whose
    # background touches the subject. Prefer a clean portrait over retaining
    # a stray background/person at the edge.
    if slug == 'valentina-gran':
        # Remove the dark block on the LEFT, while leaving face/hair untouched.
        y0 = max(0, int(y + 0.05*fh))
        for yy in range(y0, h):
            t = min(1.0, max(0.0, (yy-y0)/max(1, h-y0)))
            left_keep = int(cx - fw*(1.02 + .32*t))
            mask[yy, :max(0, left_keep)] = False
    elif slug == 'tamara-munoz':
        # Remove the secondary person/background on the RIGHT.
        y0 = max(0, int(y + 0.05*fh))
        for yy in range(y0, h):
            t = min(1.0, max(0.0, (yy-y0)/max(1, h-y0)))
            right_keep = int(cx + fw*(1.00 + .28*t))
            mask[yy, min(w, right_keep):] = False
    return mask


def refined_alpha(img, rembg_alpha, face, slug):
    rgb = np.array(img.convert('RGB'))
    h, w = rgb.shape[:2]
    alpha = np.array(rembg_alpha)

    if face is None:
        m = alpha > 12
        m = ndi.binary_closing(m, structure=np.ones((3,3)))
        out = Image.fromarray((m*255).astype(np.uint8), 'L')
        return out.filter(ImageFilter.GaussianBlur(1.5))

    env = base_envelope((h,w), face, slug)
    x, y, fw, fh = face
    cx = int(x + fw/2)
    cy = int(y + fh/2)

    gc = np.full((h,w), cv2.GC_BGD, np.uint8)
    gc[(alpha > 12) & env] = cv2.GC_PR_FGD

    Y, X = np.ogrid[:h, :w]
    face_seed = ((X-cx)/(fw*.74))**2 + ((Y-cy)/(fh*.92))**2 <= 1
    gc[face_seed] = cv2.GC_FGD

    torso_l = max(0, int(cx - fw*.70))
    torso_r = min(w, int(cx + fw*.70))
    torso_t = min(h, int(y + fh*1.0))
    torso_b = min(h, int(y + fh*4.5))
    gc[torso_t:torso_b, torso_l:torso_r] = cv2.GC_FGD
    gc[~env] = cv2.GC_BGD
    gc[alpha < 3] = cv2.GC_BGD

    bgd = np.zeros((1,65), np.float64)
    fgd = np.zeros((1,65), np.float64)
    try:
        cv2.grabCut(rgb, gc, None, bgd, fgd, 7, cv2.GC_INIT_WITH_MASK)
        mask = (gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD)
    except cv2.error:
        mask = (alpha > 12) & env

    mask &= env
    mask = manual_background_cuts(mask, face, slug)
    mask = ndi.binary_closing(mask, structure=np.ones((3,3)))
    mask = ndi.binary_fill_holes(mask)

    # Keep only the component that intersects the face seed.
    labels, n = ndi.label(mask)
    ids = labels[face_seed]
    ids = ids[ids > 0]
    if len(ids):
        chosen = int(np.bincount(ids).argmax())
        mask = labels == chosen

    out = Image.fromarray((mask*255).astype(np.uint8), 'L')
    return out.filter(ImageFilter.GaussianBlur(1.6))


def smooth_ignacio(rembg_alpha):
    # Keep the original segmentation edge; do not erode/dilate it.
    # Two-stage blur removes the staircase/pixel look without eating shoulders.
    a = rembg_alpha.filter(ImageFilter.GaussianBlur(1.35))
    arr = np.array(a, dtype=np.float32)
    arr[arr < 5] = 0
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, 'L').filter(ImageFilter.GaussianBlur(.65))


def process(slug, src, session):
    img = Image.open(ROOT / src).convert('RGBA')
    raw = remove(
        img,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=230,
        alpha_matting_background_threshold=5,
        alpha_matting_erode_size=1,
    ).convert('RGBA')

    face = detect_face(img)
    if slug == 'ignacio-lepe':
        alpha = smooth_ignacio(raw.getchannel('A'))
    elif slug in ('valentina-gran', 'tamara-munoz'):
        alpha = refined_alpha(img, raw.getchannel('A'), face, slug)
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

    target_h = TARGET_H[slug]
    scale = target_h / subject.height
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
