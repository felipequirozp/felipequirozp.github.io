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
    'valentina-gran': 690,
    'tomas-recart': 690,
    'tamara-munoz': 690,
    'ignacio-lepe': 690,
}


def detect_face(img):
    rgb = np.array(img.convert('RGB'))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = cascade.detectMultiScale(gray, scaleFactor=1.06, minNeighbors=5, minSize=(45, 45))
    if len(faces) == 0:
        return None
    h, w = gray.shape
    cx, cy = w / 2, h / 2
    return max(faces, key=lambda f: f[2]*f[3] * max(.2, 1 - (((f[0]+f[2]/2-cx)**2 + (f[1]+f[3]/2-cy)**2) ** .5) / max(h,w)))


def envelope(shape, face, slug):
    h, w = shape
    if face is None:
        return np.ones((h, w), dtype=bool)
    x, y, fw, fh = face
    cx = x + fw/2
    env = np.zeros((h, w), dtype=bool)
    top = max(0, int(y - 1.0*fh))
    shoulder = min(h-1, int(y + 2.0*fh))

    # Asymmetric widths are deliberate: Valentina's artifact is on the left;
    # Tamara's secondary person/background is on the right.
    if slug == 'valentina-gran':
        left_top, right_top, left_bottom, right_bottom = 1.25, 1.55, 1.55, 2.05
    elif slug == 'tamara-munoz':
        left_top, right_top, left_bottom, right_bottom = 1.55, 1.20, 2.00, 1.45
    else:
        left_top = right_top = 1.55
        left_bottom = right_bottom = 2.10

    for yy in range(top, h):
        t = min(1.0, max(0.0, (yy-top)/max(1, h-top)))
        lm = left_top + (left_bottom-left_top)*t
        rm = right_top + (right_bottom-right_top)*t
        l = max(0, int(cx-fw*lm))
        r = min(w, int(cx+fw*rm))
        env[yy, l:r] = True

    # generous head ellipse so hair is preserved
    Y, X = np.ogrid[:h, :w]
    head = ((X-cx)/(fw*1.6))**2 + ((Y-(y+0.55*fh))/(fh*1.9))**2 <= 1
    env |= head
    return env


def grabcut_refine(img, rembg_alpha, face, slug):
    rgb = np.array(img.convert('RGB'))
    h, w = rgb.shape[:2]
    alpha = np.array(rembg_alpha)

    if face is None:
        # Safe fallback: preserve rembg edges, only smooth tiny speckles.
        m = alpha > 18
        m = ndi.binary_closing(m, structure=np.ones((3,3)))
        return Image.fromarray((m*255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(1.25))

    env = envelope((h,w), face, slug)
    x, y, fw, fh = face
    cx = int(x + fw/2)
    cy = int(y + fh/2)

    gc = np.full((h,w), cv2.GC_BGD, np.uint8)
    # rembg foreground inside our person envelope is probable foreground
    gc[(alpha > 18) & env] = cv2.GC_PR_FGD
    # high-confidence face / central torso seeds
    Y, X = np.ogrid[:h, :w]
    face_seed = ((X-cx)/(fw*.72))**2 + ((Y-cy)/(fh*.90))**2 <= 1
    gc[face_seed] = cv2.GC_FGD
    torso_l = max(0, int(cx - fw*.75))
    torso_r = min(w, int(cx + fw*.75))
    torso_t = min(h, int(y + fh*1.15))
    torso_b = min(h, int(y + fh*4.6))
    gc[torso_t:torso_b, torso_l:torso_r] = cv2.GC_FGD
    # anything outside the person envelope is definite background
    gc[~env] = cv2.GC_BGD
    gc[alpha < 4] = cv2.GC_BGD

    bgd = np.zeros((1,65), np.float64)
    fgd = np.zeros((1,65), np.float64)
    try:
        cv2.grabCut(rgb, gc, None, bgd, fgd, 6, cv2.GC_INIT_WITH_MASK)
        mask = (gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD)
    except cv2.error:
        mask = (alpha > 18) & env

    # Keep only components connected to the face seed after a very light opening.
    # This removes the black side shape/person behind without creating jagged shoulders.
    soft = ndi.binary_opening(mask, structure=np.ones((2,2)))
    labels, n = ndi.label(soft)
    ids = labels[face_seed]
    ids = ids[ids > 0]
    if len(ids):
        chosen = int(np.bincount(ids).argmax())
        mask = labels == chosen
        mask = ndi.binary_dilation(mask, structure=np.ones((3,3)), iterations=1)

    mask &= env
    mask = ndi.binary_closing(mask, structure=np.ones((3,3)))
    mask = ndi.binary_fill_holes(mask)
    out = Image.fromarray((mask*255).astype(np.uint8), 'L')
    return out.filter(ImageFilter.GaussianBlur(1.35))


def smooth_ignacio(rembg_alpha):
    # Ignacio was already isolated; the old erosion/envelope caused the pixelated edge.
    # Preserve the model's original alpha and only soften tiny noise.
    a = rembg_alpha.filter(ImageFilter.GaussianBlur(1.15))
    arr = np.array(a)
    arr[arr < 8] = 0
    return Image.fromarray(arr.astype(np.uint8), 'L')


def process(slug, src, session):
    img = Image.open(ROOT / src).convert('RGBA')
    raw = remove(
        img,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=235,
        alpha_matting_background_threshold=8,
        alpha_matting_erode_size=3,
    ).convert('RGBA')

    face = detect_face(img)
    if slug == 'ignacio-lepe':
        alpha = smooth_ignacio(raw.getchannel('A'))
    else:
        alpha = grabcut_refine(img, raw.getchannel('A'), face, slug)

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
    max_w = int(CANVAS[0] * .86)
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
