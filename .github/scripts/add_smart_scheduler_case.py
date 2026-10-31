from pathlib import Path
import re

ROOT = Path('.')


def transform_en(s: str) -> str:
    r = {
        '<title>Shift Optimizer | Felipe Quiroz</title>': '<title>Smart Scheduler | Felipe Quiroz</title>',
        'Shift Optimizer case study by Felipe Quiroz — B2B SaaS product work across workforce planning, optimization, enterprise pilots and product validation.': 'Smart Scheduler case study by Felipe Quiroz — workforce planning, Chilean labor-rule validation, customer discovery and B2B SaaS product work.',
        '/geovictoria/shift-optimizer': '/geovictoria/smart-scheduler',
        '/es/geovictoria/shift-optimizer': '/es/geovictoria/smart-scheduler',
        'Taking workforce optimization from MVP to production.': 'Making complex shift planning easier to build, validate and publish.',
        'An optimization product for complex workforce operations, combining demand, availability and operational constraints to support better staffing decisions.': 'A smart planning experience for building weekly and monthly rotating schedules in one calendar, with real-time checks for Chilean working-time rules before shifts are published.',
        '<strong>MVP → Production</strong><span>Product stage</span>': '<strong>Scheduling · Compliance</strong><span>Product scope</span>',
        '<strong>Enterprise pilots</strong><span>Validation model</span>': '<strong>Customer discovery</strong><span>Validation model</span>',
        '<strong>LATAM</strong><span>Operational context</span>': '<strong>Chile</strong><span>Legal context</span>',
        'Shift planning is a constraint problem, not a calendar problem.': 'Planning shifts means catching problems before they reach operations.',
        'Operations teams need to balance demand, employee availability, labor rules, coverage requirements and real-world exceptions at the same time. A planner that ignores any of those layers quickly creates conflicts, manual corrections or staffing gaps.': 'Teams building rotating schedules need speed, but also confidence that what they publish can actually be operated. Weekly limits, consecutive days, rest periods and recurring shift patterns all add friction to what looks like a simple calendar.',
        'The product challenge was to turn that complexity into a decision-support experience that felt understandable to planners and robust enough for enterprise operations.': 'The product challenge was to keep planning flexible while surfacing inconsistencies in real time, so planners could fix issues before publishing the schedule.',
        'Three inputs shaped the optimization model.': 'The planner brings the core scheduling workflow into one place.',
        '<span>01 / Demand</span><h3>What the operation needs.</h3><p>Coverage and staffing requirements by day, shift and operational context.</p>': '<span>01 / Calendar</span><h3>Weekly and monthly planning.</h3><p>Build and edit rotating schedules directly in the grid, including drag-and-drop changes.</p>',
        '<span>02 / Availability</span><h3>Who can actually work.</h3><p>Employee availability, absences and practical constraints around assignments.</p>': '<span>02 / Alerts</span><h3>Catch inconsistencies early.</h3><p>Surface excessive hours and consecutive-day issues before the schedule is saved or published.</p>',
        '<span>03 / Constraints</span><h3>What cannot be broken.</h3><p>Operational rules, rest requirements and other conditions that make a schedule valid.</p>': '<span>03 / Templates</span><h3>Reuse rotating patterns.</h3><p>Apply recurring schemes such as 4x4, 7x7 and 5x2 to one or many employees.</p>',
        'Connecting product decisions with operational reality.': 'Bringing customer reality directly into product decisions.',
        'I work across discovery, rule definition, prioritization, usability validation and engineering coordination to move Shift Optimizer from MVP toward production and broader commercial use.': 'I worked directly with customers through discovery and validation sessions, mapping how teams planned shifts, where errors appeared and which rules created the most operational friction. I translated that feedback into product requirements, validations and priorities with Product and Engineering.',
        '<strong>Discovery</strong><span>Understanding customer workflows, pain points and planning constraints.</span>': '<strong>Customer discovery</strong><span>Running conversations with customers to understand planning workflows, edge cases and pain points.</span>',
        '<strong>Rule definition</strong><span>Translating operational conditions into product logic and validations.</span>': '<strong>Business rules</strong><span>Turning labor and operational conditions into product logic and real-time validations.</span>',
        '<strong>Prioritization</strong><span>Balancing customer value, business impact and technical feasibility.</span>': '<strong>Product definition</strong><span>Prioritizing improvements across customer value, business impact and technical feasibility.</span>',
        '<strong>Validation</strong><span>Testing usability and product value through real enterprise pilots.</span>': '<strong>Validation</strong><span>Testing flows and product behavior with real customer scenarios before broader rollout.</span>',
        '/images/geo-shift-optimizer.webp': '/images/planificador.png',
        'Shift Optimizer product validation': 'Smart Scheduler interface',
        'Enterprise pilots were part of the product loop.': 'Customer conversations were part of the product loop.',
        'The product was validated with real operational teams, using pilots to test rules, usability and whether the optimizer actually supported better planning decisions in practice.': 'I met with customers and operational teams to review real scheduling cases, validate rules and understand where the planner needed to be clearer, faster or more flexible.',
        'That feedback informed the transition from an MVP toward a production-ready product and helped connect product decisions with commercial value.': 'That feedback fed directly into the roadmap and helped connect product decisions with usability, operational reliability and commercial adoption.',
        '<span>Enterprise pilots</span><span>Customer validation</span><span>Operational rules</span><span>Usability</span><span>Commercial value</span>': '<span>Customer discovery</span><span>Customer validation</span><span>Chilean labor rules</span><span>Usability</span><span>Product delivery</span>',
    }
    for a, b in r.items():
        s = s.replace(a, b)
    return s


def transform_es(s: str) -> str:
    r = {
        '<title>Optimizador de Turnos | Felipe Quiroz</title>': '<title>Planificador Inteligente | Felipe Quiroz</title>',
        '/es/geovictoria/shift-optimizer': '/es/geovictoria/smart-scheduler',
        '/geovictoria/shift-optimizer': '/geovictoria/smart-scheduler',
        'Llevando la optimización de turnos desde MVP a producción.': 'Haciendo más simple planificar, validar y publicar turnos complejos.',
        'Un producto de optimización para operaciones complejas de workforce, combinando demanda, disponibilidad y restricciones operativas para apoyar mejores decisiones de dotación.': 'Una experiencia de planificación para construir mallas de turnos rotativos semanales y mensuales en un solo calendario, con validaciones en tiempo real de la jornada legal chilena antes de publicar.',
        '<strong>MVP → Producción</strong><span>Etapa de producto</span>': '<strong>Planificación · Cumplimiento</strong><span>Alcance del producto</span>',
        '<strong>Pilotos enterprise</strong><span>Modelo de validación</span>': '<strong>Discovery con clientes</strong><span>Modelo de validación</span>',
        '<strong>LATAM</strong><span>Contexto operacional</span>': '<strong>Chile</strong><span>Contexto legal</span>',
        'Planificar turnos es un problema de restricciones, no de calendario.': 'Planificar turnos también significa detectar problemas antes de llegar a la operación.',
        'Los equipos operativos deben equilibrar al mismo tiempo demanda, disponibilidad de colaboradores, reglas laborales, requerimientos de cobertura y excepciones del mundo real. Un planificador que ignore cualquiera de esas capas rápidamente genera conflictos, correcciones manuales o brechas de dotación.': 'Los equipos que construyen turnos rotativos necesitan velocidad, pero también confianza en que lo que publican puede operarse. Límites de jornada, días consecutivos, descansos y patrones recurrentes agregan complejidad a lo que parece ser solo un calendario.',
        'El desafío de producto era convertir esa complejidad en una experiencia de apoyo a decisiones que fuera entendible para planificadores y suficientemente robusta para operaciones enterprise.': 'El desafío de producto era mantener la planificación flexible y, al mismo tiempo, mostrar inconsistencias en tiempo real para corregirlas antes de publicar la malla.',
        'Tres inputs estructuran el modelo de optimización.': 'El planificador reúne el flujo central de turnos en un solo lugar.',
        '<span>01 / Demanda</span><h3>Lo que necesita la operación.</h3><p>Cobertura y requerimientos de dotación por día, turno y contexto operativo.</p>': '<span>01 / Calendario</span><h3>Planificación semanal y mensual.</h3><p>Construcción y edición de turnos rotativos directamente en la malla, incluyendo cambios con drag & drop.</p>',
        '<span>02 / Disponibilidad</span><h3>Quién realmente puede trabajar.</h3><p>Disponibilidad de colaboradores, ausencias y restricciones prácticas sobre asignaciones.</p>': '<span>02 / Alertas</span><h3>Detectar inconsistencias antes.</h3><p>Alertas por exceso de jornada y días consecutivos antes de guardar o publicar la planificación.</p>',
        '<span>03 / Restricciones</span><h3>Lo que no se puede romper.</h3><p>Reglas operativas, requerimientos de descanso y otras condiciones que hacen válido un turno.</p>': '<span>03 / Plantillas</span><h3>Reutilizar patrones rotativos.</h3><p>Aplicación de esquemas como 4x4, 7x7 y 5x2 a uno o múltiples colaboradores.</p>',
        'Conectando decisiones de producto con la realidad operacional.': 'Llevando la realidad de los clientes directamente a las decisiones de producto.',
        'Trabajo entre discovery, definición de reglas, priorización, validación de usabilidad y coordinación con ingeniería para llevar Optimizador de Turnos desde MVP hacia producción y un uso comercial más amplio.': 'Trabajé directamente con clientes mediante reuniones de discovery y validación, entendiendo cómo planificaban sus turnos, dónde aparecían errores y qué reglas generaban mayor fricción. Ese feedback se transformaba en requerimientos, validaciones y prioridades junto a Producto e Ingeniería.',
        '<strong>Discovery</strong><span>Entender workflows de clientes, dolores y restricciones de planificación.</span>': '<strong>Discovery con clientes</strong><span>Conversaciones con clientes para entender workflows, casos borde y fricciones de planificación.</span>',
        '<strong>Definición de reglas</strong><span>Traducir condiciones operativas en lógica de producto y validaciones.</span>': '<strong>Reglas de negocio</strong><span>Traducir condiciones laborales y operativas en lógica de producto y validaciones en tiempo real.</span>',
        '<strong>Priorización</strong><span>Equilibrar valor para clientes, impacto de negocio y factibilidad técnica.</span>': '<strong>Definición de producto</strong><span>Priorizar mejoras equilibrando valor para clientes, impacto de negocio y factibilidad técnica.</span>',
        '<strong>Validación</strong><span>Probar usabilidad y valor del producto mediante pilotos enterprise reales.</span>': '<strong>Validación</strong><span>Probar flujos y comportamiento del producto con escenarios reales antes de escalar.</span>',
        '/images/geo-shift-optimizer.webp': '/images/planificador.png',
        'Validación de producto de Optimizador de Turnos': 'Interfaz de Planificador Inteligente',
        'Los pilotos enterprise son parte del loop de producto.': 'Las conversaciones con clientes son parte del loop de producto.',
        'El producto se valida con equipos operativos reales, usando pilotos para probar reglas, usabilidad y si el optimizador efectivamente apoya mejores decisiones de planificación en la práctica.': 'Me reunía con clientes y equipos operativos para revisar casos reales de planificación, validar reglas y entender dónde el producto debía ser más claro, rápido o flexible.',
        'Ese feedback alimenta la transición desde MVP hacia un producto listo para producción y ayuda a conectar decisiones de producto con valor comercial.': 'Ese feedback alimentaba directamente el roadmap y ayudaba a conectar decisiones de producto con usabilidad, confiabilidad operacional y adopción comercial.',
        '<span>Pilotos enterprise</span><span>Validación con clientes</span><span>Reglas operativas</span><span>Usabilidad</span><span>Valor comercial</span>': '<span>Discovery con clientes</span><span>Validación con clientes</span><span>Jornada legal chilena</span><span>Usabilidad</span><span>Product delivery</span>',
    }
    for a, b in r.items():
        s = s.replace(a, b)
    return s


def add_card(path: Path, es=False):
    s = path.read_text(encoding='utf-8')
    href = '/es/geovictoria/smart-scheduler' if es else '/geovictoria/smart-scheduler'
    if href in s:
        return
    opt_href = '/es/geovictoria/shift-optimizer' if es else '/geovictoria/shift-optimizer'
    pattern = re.compile(r'(<a class="card reveal" data-cat="saas product" href="' + re.escape(opt_href) + r'">.*?</a>)', re.S)
    title = 'Planificador Inteligente' if es else 'Smart Scheduler'
    desc = ('Malla semanal y mensual con validaciones de jornada legal chilena antes de publicar.' if es else 'Weekly and monthly shift planning with real-time Chilean working-time validations before publishing.')
    cta = 'Ver proyecto ↗' if es else 'View project ↗'
    card = f'<a class="card reveal" data-cat="saas product" href="{href}"><div class="visual geo"><img src="/images/planificador.png" alt="{title}"></div><div class="body"><div class="meta"><span>GeoVictoria</span><span>2026</span></div><h3>{title}</h3><p>{desc}</p><div class="impact"><span>Customer discovery</span><span>Workforce planning</span><span>B2B</span></div><span class="cta">{cta}</span></div></a>'
    s2, n = pattern.subn(r'\1\n' + card, s, count=1)
    if n != 1:
        raise RuntimeError(f'Could not find optimizer card in {path}')
    path.write_text(s2, encoding='utf-8')


en = Path('geovictoria/shift-optimizer.html').read_text(encoding='utf-8')
es = Path('es/geovictoria/shift-optimizer.html').read_text(encoding='utf-8')
Path('geovictoria/smart-scheduler.html').write_text(transform_en(en), encoding='utf-8')
Path('es/geovictoria/smart-scheduler.html').write_text(transform_es(es), encoding='utf-8')
add_card(Path('projects.html'), False)
add_card(Path('es/projects.html'), True)
