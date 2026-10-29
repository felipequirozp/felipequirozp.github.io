from pathlib import Path

# Keep GeoVictoria EN/ES on the same redesigned structure.
# Triggered to align both languages with the current redesign.
en = Path('geovictoria.html')
s = en.read_text(encoding='utf-8')

# Keep role current, per portfolio preference.
s = s.replace('July — September 2026', 'July 2026 — Present')
s = s.replace('As Product Manager, I worked across scheduling and shift operations, taking products from discovery and validation into pilots, production and commercial use.', 'As Product Manager, I work across scheduling and shift operations, taking products from discovery and validation into pilots, production and commercial use.')
s = s.replace('I worked across product discovery, roadmap definition, prioritization, validation, enterprise pilots, adoption and commercial feedback.', 'I work across product discovery, roadmap definition, prioritization, validation, enterprise pilots, adoption and commercial feedback.')

# Let the GeoVictoria mark sit directly on the hero instead of inside a dark capsule.
s = s.replace('.geo-logo{display:inline-flex;align-items:center;justify-content:center;padding:10px 16px;border-radius:14px;background:#0d1724}.geo-logo img{height:26px;width:auto}', '.geo-logo{display:inline-flex;align-items:center;justify-content:flex-start;padding:0;background:transparent}.geo-logo img{height:38px;width:auto;max-width:260px;object-fit:contain;object-position:left center}')

en.write_text(s, encoding='utf-8')

es = s
repls = [
    ('<html lang="en">','<html lang="es">'),
    ('GeoVictoria case study by Felipe Quiroz — product strategy, workforce management and B2B SaaS.','Caso GeoVictoria de Felipe Quiroz — estrategia de producto, workforce management y B2B SaaS.'),
    ('href="https://felipequirozp.cl/geovictoria"><link rel="alternate" hreflang="en"','href="https://felipequirozp.cl/es/geovictoria"><link rel="alternate" hreflang="en"'),
    ('<a class="brand" href="/">Felipe Quiroz</a>','<a class="brand" href="/es/">Felipe Quiroz</a>'),
    ('<a href="/#work">Work</a><a href="/about">About</a><a href="/projects">Projects</a><a href="/initiatives">Initiatives</a><a href="/blog">Blog</a>','<a href="/es/#work">Trabajo</a><a href="/es/about">Sobre mí</a><a href="/es/projects">Proyectos</a><a href="/es/initiatives">Iniciativas</a><a href="/es/blog">Blog</a>'),
    ('<a class="lang" href="/es/geovictoria">ES</a>','<a class="lang" href="/geovictoria">EN</a>'),
    ('Product systems for <span>real-world operations.</span>','Sistemas de producto para <span>operaciones reales.</span>'),
    ('GeoVictoria is a Latin American workforce management SaaS company serving 10,000+ customers. As Product Manager, I work across scheduling and shift operations, taking products from discovery and validation into pilots, production and commercial use.','GeoVictoria es una compañía latinoamericana de Workforce Management SaaS que atiende a 10.000+ clientes. Como Product Manager, trabajo en planificación y operación de turnos, llevando productos desde discovery y validación hacia pilotos, producción y uso comercial.'),
    ('July 2026 — Present','Julio 2026 — Presente'),
    ('workforce products led','productos de workforce liderados'),
    ('validations and pilots','validaciones y pilotos'),
    ('core LATAM markets','mercados principales en LATAM'),
    ('Scope','Alcance'),
    ('Connecting customer problems, product decisions and execution.','Conectando problemas de clientes, decisiones de producto y ejecución.'),
    ('I work across product discovery, roadmap definition, prioritization, validation, enterprise pilots, adoption and commercial feedback. The job sat close to customers and internal teams, translating operational complexity into rules, workflows and product decisions.','Trabajo en product discovery, definición de roadmap, priorización, validación, pilotos enterprise, adopción y feedback comercial. El rol está muy cerca de clientes y equipos internos, traduciendo complejidad operativa en reglas, workflows y decisiones de producto.'),
    ('My scope covered Chile, Argentina, Colombia, Peru and Mexico, with additional pilot work in Costa Rica.','Mi alcance cubre Chile, Argentina, Colombia, Perú y México, además de trabajo de pilotos en Costa Rica.'),
    ('Enterprise pilots','Pilotos enterprise'),
    ('Commercial feedback','Feedback comercial'),
    ('Product portfolio','Portafolio de producto'),
    ('Three products across planning, optimization and employee workflows.','Tres productos entre planificación, optimización y workflows de colaboradores.'),
    ('Each product addressed a different layer of workforce operations, from planning coverage to optimizing shifts and enabling controlled employee changes.','Cada producto aborda una capa distinta de la operación de workforce: desde planificar cobertura hasta optimizar turnos y habilitar cambios controlados entre colaboradores.'),
    ('Shift and staffing planning for complex operations, connecting coverage, rules, absences and workforce needs.','Planificación de turnos y dotación para operaciones complejas, conectando cobertura, reglas, ausencias y necesidades de personal.'),
    ('My contribution','Mi contribución'),
    ('I helped define priorities and operating rules, coordinating validation with customers and internal teams before scaling changes.','Ayudo a definir prioridades y reglas operativas, coordinando validación con clientes y equipos internos antes de escalar cambios.'),
    ('An optimization product combining demand, availability and operational constraints to support better staffing decisions.','Un producto de optimización que combina demanda, disponibilidad y restricciones operativas para apoyar mejores decisiones de dotación.'),
    ('I led its evolution from MVP toward production and enterprise pilots, validating rules, usability and commercial value with real customers.','Lideré su evolución desde MVP hacia producción y pilotos enterprise, validando reglas, usabilidad y valor comercial con clientes reales.'),
    ('View project ↗','Ver proyecto ↗'),
    ('A 0→1 workflow for employee shift changes, operational rules, approvals and automation.','Un workflow 0→1 para cambios de turno entre colaboradores, reglas operativas, aprobaciones y automatización.'),
    ('I led the product from early definition through rules, validation and pilot design across multiple markets.','Lideré el producto desde su definición inicial hasta reglas, validación y diseño de pilotos en múltiples mercados.'),
    ('In the field','En terreno'),
    ('Built close to customers, pilots and commercial reality.','Construido cerca de clientes, pilotos y realidad comercial.'),
    ('The work depended on constant feedback from customers, sales and implementation teams. Pilots helped test operational rules, usability and value before moving products toward broader adoption.','El trabajo depende de feedback constante de clientes, ventas y equipos de implementación. Los pilotos permiten probar reglas operativas, usabilidad y valor antes de llevar los productos hacia una adopción más amplia.'),
    ('GeoVictoria team and customer work','Trabajo con equipo y clientes de GeoVictoria'),
    ('See the product work in detail.','Mira el trabajo de producto en detalle.'),
    ('Explore the individual GeoVictoria product cases and the decisions behind them.','Explora los casos individuales de producto de GeoVictoria y las decisiones detrás de ellos.'),
    ('href="/projects">View projects ↗','href="/es/projects">Ver proyectos ↗'),
    ('Product · Growth · Operations · Company building','Producto · Growth · Operaciones · Company building'),
    ('Building products, growth systems and companies across technology and business.','Construyendo productos, sistemas de crecimiento y compañías entre tecnología y negocio.'),
    ('<strong>Explore</strong>','<strong>Explorar</strong>'),
    ('<strong>Contact</strong>','<strong>Contacto</strong>'),
]
for a,b in repls:
    es = es.replace(a,b)

# Translate internal case-study links.
es = es.replace('href="/geovictoria/shift-optimizer"','href="/es/geovictoria/shift-optimizer"')
es = es.replace('href="/geovictoria/shift-change-workflow"','href="/es/geovictoria/shift-change-workflow"')

Path('es/geovictoria.html').write_text(es, encoding='utf-8')
