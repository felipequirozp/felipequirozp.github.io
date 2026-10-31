from pathlib import Path

FILES = [Path('people.html'), Path('es/people.html')]

old_card = '<article class="person"><div class="portrait"><div class="portrait-inner"><img src="/images/alfonso.png?v=20261031" alt="Alfonso" loading="lazy"></div></div><div class="person-copy"><h3>Alfonso</h3></div></article>'
new_card = '<article class="person"><a class="card-link" href="https://www.linkedin.com/in/alfonso-irarrazaval/" target="_blank" rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a><div class="portrait"><div class="portrait-inner"><img src="/images/alfonso.png?v=20261031-2" alt="Alfonso Irarrázabal" loading="lazy"></div></div><div class="person-copy"><h3>Alfonso Irarrázabal</h3></div></article>'

for path in FILES:
    text = path.read_text(encoding='utf-8')
    if old_card in text:
        text = text.replace(old_card, new_card, 1)
    else:
        text = text.replace('<h3>Alfonso</h3>', '<h3>Alfonso Irarrázabal</h3>', 1)
        text = text.replace('alt="Alfonso"', 'alt="Alfonso Irarrázabal"', 1)
        if 'href="https://www.linkedin.com/in/alfonso-irarrazaval/"' not in text:
            marker = '<article class="person"><div class="portrait"><div class="portrait-inner"><img src="/images/alfonso.png?v=20261031" alt="Alfonso Irarrázabal" loading="lazy"></div></div><div class="person-copy"><h3>Alfonso Irarrázabal</h3></div></article>'
            replacement = '<article class="person"><a class="card-link" href="https://www.linkedin.com/in/alfonso-irarrazaval/" target="_blank" rel="noopener noreferrer" aria-label="Open LinkedIn profile"></a><div class="portrait"><div class="portrait-inner"><img src="/images/alfonso.png?v=20261031-2" alt="Alfonso Irarrázabal" loading="lazy"></div></div><div class="person-copy"><h3>Alfonso Irarrázabal</h3></div></article>'
            text = text.replace(marker, replacement, 1)

    css_rule = '.people-all img[alt="Alfonso Irarrázabal"]{transform:scale(1.04) translateY(7%)!important}\n'
    if css_rule not in text:
        anchor = '.people-all img[alt="Ignacio Lepe"]{transform:scale(1.10) translateY(2%)!important}\n'
        text = text.replace(anchor, anchor + css_rule, 1)
    path.write_text(text, encoding='utf-8')
