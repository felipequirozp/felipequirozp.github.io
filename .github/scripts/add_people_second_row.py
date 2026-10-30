from pathlib import Path
import re

PEOPLE = [
    ("Valentina Gran", "/images/vgran.png", "https://www.linkedin.com/in/valentina-gran-koch-0b945325/"),
    ("Tomás Recart", "/images/tomas.png", "https://www.linkedin.com/in/tomas-recart-balze-a9957918a/"),
    ("Tamara Muñoz", "/images/tamara.png", "https://www.linkedin.com/in/tamara-munoz-ojeda/"),
    ("Ignacio Lepe", "/images/lepe.png", "https://www.linkedin.com/in/ignacio-lepe-6026b4215/"),
]


def card(name, image, linkedin):
    return (
        f'<article class="person"><a class="card-link" href="{linkedin}" target="_blank" '
        f'rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a>'
        f'<div class="portrait"><div class="portrait-inner"><img src="{image}" alt="{name}" loading="lazy" '
        f'style="transform:none!important"></div></div>'
        f'<div class="person-copy"><h3>{name}</h3></div></article>'
    )


def patch(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(r'(<div class="people-grid">)(.*?)(</div></div></section>\s*<section class="closing">)', text, re.S)
    if not match:
        raise RuntimeError(f"People grid not found in {path}")

    blocks = re.findall(r'<article class="person"[^>]*>.*?</article>', match.group(2), re.S)
    if len(blocks) < 6:
        raise RuntimeError(f"Expected at least 6 people cards in {path}")

    new_names = {name for name, _, _ in PEOPLE}
    cleaned = []
    for block in blocks:
        m = re.search(r'<h3>(.*?)</h3>', block, re.S)
        name = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''
        if name not in new_names:
            cleaned.append(block)

    additions = [card(*person) for person in PEOPLE]
    ordered = cleaned[:6] + additions + cleaned[6:]
    replacement = match.group(1) + ''.join(ordered) + match.group(3)
    text = text[:match.start()] + replacement + text[match.end():]
    path.write_text(text, encoding="utf-8")


for file in [Path("people.html"), Path("es/people.html")]:
    patch(file)
