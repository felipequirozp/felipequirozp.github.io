from pathlib import Path
import re
import numpy as np
from PIL import Image, ImageOps, ImageFilter
from rembg import remove, new_session
from scipy import ndimage

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
TARGET_HEIGHT = 755


def keep_main_subject(alpha_img):
    a = np.array(alpha_img)
    binary = a > 40
    labels, count = ndimage.label(binary)
    if count <= 1:
        return alpha_img

    h, w = binary.shape
    # Prefer the connected component that occupies the central portrait zone.
    cx = w // 2
    probe_points = [
        (int(h * .32), cx),
        (int(h * .42), cx),
        (int(h * .52), cx),
    ]
    chosen = 0
    for y, x in probe_points:
        lab = labels[y, x]
        if lab:
            chosen = int(lab)
            break

    if not chosen:
        # Otherwise choose the largest component that intersects the central 60%.
        best = (0, 0)
        for lab in range(1, count + 1):
            mask = labels == lab
            ys, xs = np.where(mask)
            if not len(xs):
                continue
            central = np.any((xs >= int(w*.2)) & (xs <= int(w*.8)))
            score = int(mask.sum()) if central else 0
            if score > best[1]:
                best = (lab, score)
        chosen = best[0] or 1

    clean = np.where(labels == chosen, a, 0).astype(np.uint8)
    clean = Image.fromarray(clean, 'L').filter(ImageFilter.GaussianBlur(0.7))
    return clean


def process(slug, src_path, session):
    img = Image.open(ROOT / src_path).convert('RGBA')
    cut = remove(
        img,
        session=session,
        alpha_matting=False,
        post_process_mask=True,
    ).convert('RGBA')

    alpha = keep_main_subject(cut.getchannel('A'))
    cut.putalpha(alpha)
    bbox = alpha.getbbox()
    if not bbox:
        raise RuntimeError(f'No foreground detected for {slug}')

    subject = cut.crop(bbox)
    gray = ImageOps.grayscale(subject.convert('RGB')).convert('RGBA')
    gray.putalpha(subject.getchannel('A'))
    subject = gray

    scale = TARGET_HEIGHT / subject.height
    max_w = int(CANVAS[0] * 0.97)
    if subject.width * scale > max_w:
        scale = max_w / subject.width
    new_size = (max(1, round(subject.width * scale)), max(1, round(subject.height * scale)))
    subject = subject.resize(new_size, Image.Resampling.LANCZOS)

    canvas = Image.new('RGBA', CANVAS, (255, 255, 255, 0))
    x = (CANVAS[0] - subject.width) // 2
    y = CANVAS[1] - subject.height
    canvas.alpha_composite(subject, (x, y))

    out = OUT / f'{slug}.png'
    canvas.save(out, 'PNG', optimize=True)
    print(f'Processed {src_path} -> {out}')


def patch_html(path):
    text = path.read_text(encoding='utf-8')
    for slug, (_, name, _) in PEOPLE.items():
        pat = re.compile(
            r'(<article class="person">(?:(?!</article>).)*?<h3>' + re.escape(name) + r'</h3>(?:(?!</article>).)*?</article>)',
            re.S,
        )
        m = pat.search(text)
        if not m:
            raise RuntimeError(f'Missing card {name} in {path}')
        card = m.group(1)
        card = re.sub(
            r'src="[^"]+"',
            f'src="/images/people/{slug}.png?v=20261029-2220"',
            card,
            count=1,
        )
        text = text[:m.start()] + card + text[m.end():]

    expected = ['Christopher Neilson','Zack Tseng','Nicolás Muñoz','Leidy Gómez','Rodrigo Lewit','Karen Radonich','Valentina Gran','Tomás Recart','Tamara Muñoz','Ignacio Lepe','Damián Aldunate','Matías Bussinger','Lía Morice','Martín Alvarado','Jorge Muñoz','Francisca Astudillo','Juan Yuz','Javier Robledo','Valentina Wagenreld']
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
