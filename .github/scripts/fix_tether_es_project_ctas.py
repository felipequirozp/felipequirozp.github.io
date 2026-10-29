from pathlib import Path

p = Path('es/tethereducation.html')
s = p.read_text(encoding='utf-8')

old1 = '<article class="program"><small>Elección escolar</small><h3>Explorador Virtual de Colegios</h3><p>Experiencias digitales de descubrimiento escolar en LATAM, Estados Unidos y Europa.</p></article>'
new1 = '<a class="program" href="/es/tethered/explorador-virtual-colegios"><small>Elección escolar</small><h3>Explorador Virtual de Colegios</h3><p>Experiencias digitales de descubrimiento escolar en LATAM, Estados Unidos y Europa.</p><span class="program-link">Ver proyecto ↗</span></a>'

old2 = '<article class="program"><small>Ecosistema de producto</small><h3>Tether Studio</h3><p>Trabajo de producto y experimentación habilitado por IA dentro del ecosistema Tether.</p></article>'
new2 = '<a class="program" href="/es/tethered/tether-studio"><small>Ecosistema de producto</small><h3>Tether Studio</h3><p>Trabajo de producto y experimentación habilitado por IA dentro del ecosistema Tether.</p><span class="program-link">Ver proyecto ↗</span></a>'

s = s.replace(old1, new1).replace(old2, new2)
p.write_text(s, encoding='utf-8')
