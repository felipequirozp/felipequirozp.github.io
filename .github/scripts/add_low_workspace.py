from pathlib import Path

CSS = r'''
<style id="low-workspace-feature">
.low-workspace-feature{padding:88px var(--page) 92px;background:#f5f6f8}
.low-workspace-feature__inner{width:min(var(--max),100%);margin:0 auto;display:grid;grid-template-columns:minmax(300px,.72fr) minmax(0,1.28fr);gap:clamp(40px,7vw,96px);align-items:center}
.low-workspace-feature .section-label{color:var(--blue)}
.low-workspace-feature h2{margin:16px 0 18px;max-width:520px;font-family:Manrope,sans-serif;font-size:clamp(42px,4.4vw,62px);line-height:1.03;letter-spacing:-.055em;font-weight:500;color:var(--ink)}
.low-workspace-feature h2 span{display:block;color:#273253}
.low-workspace-feature p{margin:0;max-width:560px;color:var(--muted);font-size:15px;line-height:1.75}
.low-workspace-feature__tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px}
.low-workspace-feature__tags span{padding:8px 10px;border:1px solid #d7dde5;border-radius:999px;background:#fff;color:#667281;font-size:9px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.low-workspace-feature__link{display:inline-flex;align-items:center;gap:9px;margin-top:28px;color:var(--blue);font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.low-workspace-feature__link svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;transition:transform .2s ease}
.low-workspace-feature__link:hover svg{transform:translate(2px,-2px)}
.low-workspace-feature__visual{display:block;overflow:hidden;border:1px solid #dfe3e9;background:#fff;box-shadow:0 24px 60px rgba(21,26,44,.10)}
.low-workspace-feature__visual img{display:block;width:100%;height:auto}
@media(max-width:860px){.low-workspace-feature__inner{grid-template-columns:1fr;gap:34px}.low-workspace-feature__copy{max-width:700px}}
@media(max-width:640px){.low-workspace-feature{padding:64px var(--page) 68px}.low-workspace-feature h2{font-size:clamp(38px,9vw,48px)}.low-workspace-feature p{font-size:14px}.low-workspace-feature__visual{box-shadow:0 16px 40px rgba(21,26,44,.09)}}
</style>
'''

EN = r'''
  <section class="low-workspace-feature" id="low-workspace">
    <div class="low-workspace-feature__inner">
      <div class="low-workspace-feature__copy">
        <div class="section-label">Built at lowsignal</div>
        <h2>Low Workspace<span>One workspace to run the company.</span></h2>
        <p>I designed and built Low Workspace, an internal operating platform that brings client management, revenue visibility, tasks and team operations into one place.</p>
        <div class="low-workspace-feature__tags"><span>Product</span><span>Operations</span><span>AI-assisted development</span></div>
        <a class="low-workspace-feature__link" href="/low-workspace">View project <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 12.5 12.5 3.5M5 3.5h7.5V11"/></svg></a>
      </div>
      <a class="low-workspace-feature__visual" href="/low-workspace" aria-label="View Low Workspace project"><img src="/images/panel-demo.png" alt="Low Workspace operations dashboard" loading="lazy" decoding="async"></a>
    </div>
  </section>

'''

ES = r'''
  <section class="low-workspace-feature" id="low-workspace">
    <div class="low-workspace-feature__inner">
      <div class="low-workspace-feature__copy">
        <div class="section-label">Construido en lowsignal</div>
        <h2>Low Workspace<span>Un workspace para operar la compañía.</span></h2>
        <p>Diseñé y desarrollé Low Workspace, una plataforma interna que centraliza la gestión de clientes, la visibilidad de ingresos, las tareas y la operación del equipo en un solo lugar.</p>
        <div class="low-workspace-feature__tags"><span>Producto</span><span>Operaciones</span><span>Desarrollo asistido por IA</span></div>
        <a class="low-workspace-feature__link" href="/es/low-workspace">Ver proyecto <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 12.5 12.5 3.5M5 3.5h7.5V11"/></svg></a>
      </div>
      <a class="low-workspace-feature__visual" href="/es/low-workspace" aria-label="Ver proyecto Low Workspace"><img src="/images/panel-demo.png" alt="Panel de operaciones de Low Workspace" loading="lazy" decoding="async"></a>
    </div>
  </section>

'''

def patch(path: str, block: str):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if 'id="low-workspace-feature"' not in text:
        text = text.replace("</head>", CSS + "\n</head>", 1)
    if 'class="low-workspace-feature"' not in text:
        marker = '  <section class="testimonial">'
        if marker not in text:
            raise RuntimeError(f"testimonial marker not found in {path}")
        text = text.replace(marker, block + marker, 1)
    p.write_text(text, encoding="utf-8")

patch("lowsignal.html", EN)
patch("es/lowsignal.html", ES)
