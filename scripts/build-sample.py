#!/usr/bin/env python3
"""Build the human-readable synthetic sample. Authoring dependency: reportlab.

The website itself remains static and has no runtime dependencies.
Run from any directory with Python 3.11+ and reportlab installed.
"""
from pathlib import Path
from html import escape
from io import StringIO
import csv
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SOURCES = ASSETS / 'muestra-ot-check-evidencias'
raw = {json.loads(p.read_text(encoding='utf-8'))['id']: json.loads(p.read_text(encoding='utf-8')) for p in SOURCES.glob('E*.json')}
assert set(raw) == {'E01', 'E02', 'E03', 'E04', 'E05'}
assert raw['E02']['contenido']['registro_restauracion'] is None
assert raw['E04']['contenido']['autorizador'] is None

INTRO = 'Informe de ejemplo sobre una célula de mecanizado ficticia. Todos los documentos y declaraciones son simulados. No corresponde a un cliente, una visita ni una prueba realizada.'
SCOPE = 'Preparación y ejecución de trabajos en una célula de mecanizado. Se dispone de una lista de seis componentes y de cuatro fichas sobre copias, recuperación, accesos y una petición de un comprador. La revisión se limita a esa información.'
METHOD = 'Se contrastan documentos y una declaración del ejercicio. No hay observación en planta, entrevista real, escaneo, cambio de configuración ni restauración. La lista de componentes no permite confirmar conexiones, versiones ni cobertura de las copias.'
DECISION = 'Preparar una respuesta al comprador que separe lo documentado de lo pendiente. En paralelo, aclarar la cobertura de las copias y quién autoriza el soporte. Decidir después si encargar una prueba de recuperación con alcance propio.'
ORDER = 'El plazo de diez días laborables de la petición ficticia marca la preparación de la respuesta. Las aclaraciones sobre copias y accesos la alimentan y pueden iniciarse en paralelo. No se propone modificar sistemas sin confirmación ni sustituir una prueba técnica por una revisión documental.'
LIMIT = 'No puede concluirse que las copias fallen, que el acceso esté activo o sea inseguro, ni que se incumpla una norma. Tampoco se conoce un tiempo de recuperación ni se garantiza la aceptación del comprador.'
OWNER_NOTE = 'Las responsables indicadas son propuestas para que la organización las valide y asigne. MKDL entrega el análisis y el plan; las modificaciones y pruebas posteriores requieren su propio alcance y autorización.'
actions = [
    dict(id='A01', title='Aclarar qué cubren las copias y decidir si preparar una prueba',
         fact='Hay un calendario semanal de programas CNC y se recuerda una prueba anterior sin fecha ni registro. No se ha demostrado la recuperación.',
         sources=['E02', 'E03'], owner='Mantenimiento e informática, con validación de la responsable del proceso.',
         work='Relacionar los programas necesarios para el proceso con las copias disponibles. Solicitar el procedimiento y el registro de la prueba recordada. Si no aparecen, registrar la incertidumbre y proponer las condiciones de una prueba separada.',
         close='Cobertura y carencias documentadas, con responsable asignada y decisión registrada sobre la prueba. Este cierre documental no equivale a una recuperación comprobada.',
         when='Iniciar la aclaración mientras se prepara la respuesta al comprador. La fecha de una prueba se acuerda por separado.',
         dependency='Participación de mantenimiento e informática. Si se plantea una restauración: entorno, ventana, criterio de parada y autorización propios.'),
    dict(id='A02', title='Confirmar quién autoriza el soporte del proveedor',
         fact='La ficha recibida indica proveedor y finalidad de soporte, pero no identifica quién autoriza el acceso. No demuestra que exista un acceso activo.',
         sources=['E04'], owner='Mantenimiento e informática, con la persona que tenga autoridad sobre ese acceso.',
         work='Confirmar con las áreas implicadas si el acceso se utiliza, para qué alcance, quién lo aprueba y cuándo debe revisarse. Registrar la respuesta y las evidencias que la respalden.',
         close='Validación fechada con autorizador, finalidad, alcance y próxima revisión. Si un dato no puede confirmarse, permanece identificado como pendiente.',
         when='En paralelo con A01 y antes de contestar sobre autorizaciones o proponer un cambio de acceso.',
         dependency='Confirmación de la organización y del proveedor habitual. No deshabilitar ni modificar accesos sin coordinación y autorización.'),
    dict(id='A03', title='Responder al comprador con evidencias y pendientes explícitos',
         fact='La petición ficticia solicita información sobre copias, recuperación y autorizadores, con un plazo de diez días laborables.',
         sources=['E05', 'E02', 'E03', 'E04'], owner='Calidad o comercial prepara la respuesta; gerencia la revisa y aprueba.',
         work='Vincular cada pregunta con su respaldo disponible. Explicar las comprobaciones pendientes y quién las coordinará. Evitar afirmar una restauración realizada o una autorización que no constan.',
         close='Respuesta revisada y aprobada por gerencia, con los documentos de respaldo y los pendientes asociados. La aceptación externa sólo se registra cuando el comprador la comunique.',
         when='Preparar y aprobar la respuesta dentro de los diez días laborables del escenario; no esperar a una prueba aún no acordada.',
         dependency='Resultados disponibles de A01 y A02, o sus incertidumbres expresas. El comprador decide si acepta la respuesta.'),
]
evidence = [
    dict(id='E01', title='Descripción del proceso', kind='Documento del ejercicio',
         rows=[('Proceso', raw['E01']['contenido']['proceso'].capitalize()), ('Componentes enumerados', ', '.join(raw['E01']['contenido']['activos']))],
         meaning='Permite delimitar el ejemplo a un proceso y seis componentes.',
         limit='No aporta topología, configuración, versiones, conexiones ni relación confirmada entre cada componente y sus copias.'),
    dict(id='E02', title='Calendario de copias', kind='Documento del ejercicio',
         rows=[('Objeto', raw['E02']['contenido']['objeto']), ('Frecuencia prevista', raw['E02']['contenido']['frecuencia']), ('Registro de restauración', 'No aportado en esta ficha')],
         meaning='Documenta una frecuencia prevista para programas CNC.',
         limit='Un calendario no demuestra que las copias se ejecuten, sean íntegras, cubran todo lo necesario o permitan recuperar en un tiempo concreto.'),
    dict(id='E03', title='Declaración de mantenimiento', kind='Declaración simulada',
         rows=[('Declaración', raw['E03']['contenido']['declaracion']), ('Fecha y resultado de aquella prueba', 'No aportados')],
         meaning='Señala una prueba que conviene localizar y contrastar.',
         limit='El recuerdo no confirma el resultado, la vigencia ni la repetibilidad de una prueba. No se ha entrevistado a una persona real.'),
    dict(id='E04', title='Ficha de acceso del proveedor', kind='Documento del ejercicio',
         rows=[('Proveedor', raw['E04']['contenido']['proveedor']), ('Finalidad indicada', raw['E04']['contenido']['finalidad']), ('Autorizador', 'No identificado en la ficha')],
         meaning='Permite solicitar la confirmación de finalidad, alcance y autoridad de aprobación.',
         limit='La ausencia de autorizador en esta ficha no demuestra que no exista, que el acceso esté activo ni que sea inseguro.'),
    dict(id='E05', title='Petición del comprador', kind='Solicitud simulada',
         rows=[('Petición', raw['E05']['contenido']['solicitud'].capitalize()), ('Plazo del escenario', 'Diez días laborables'), ('Naturaleza', 'Requisito contractual supuesto para el ejercicio')],
         meaning='Justifica preparar una respuesta con respaldo y pendientes antes del plazo del escenario.',
         limit='No acredita una obligación legal, un requisito real de una empresa ni que el comprador acepte la respuesta.'),
]
labels = {e['id']: e['title'] for e in evidence}
uncertainties = [
    ('Cobertura e integridad de las copias', 'Mantenimiento e informática contrastan inventario, procedimiento y registros; una prueba posterior necesitaría otro alcance.', 'A01'),
    ('Resultado y vigencia de la prueba recordada', 'Localizar su registro. Si no aparece, conservar el estado no comprobado.', 'A01'),
    ('Estado y autorización del acceso de soporte', 'Confirmación de las áreas con autoridad y del proveedor, con respaldo fechado.', 'A02'),
    ('Aceptación de la respuesta por el comprador', 'Esperar su comunicación. La aprobación interna de gerencia no es aceptación externa.', 'A03'),
]
responses = [
    ('Copias de programas', 'Consta un calendario semanal de copias de programas CNC. No se han contrastado la ejecución, integridad ni cobertura de las copias.', ['E02']),
    ('Recuperación', 'Se recuerda una prueba anterior, pero no se han aportado su fecha ni su registro. No podemos acreditar su resultado ni un tiempo de recuperación.', ['E03']),
    ('Autorización del soporte', 'La ficha identifica un mantenedor y una finalidad de soporte. Falta confirmar quién autoriza el acceso y cuál es su alcance. Esta ficha no demuestra que el acceso esté activo.', ['E04']),
]

def p(text): return f'<p>{escape(text)}</p>'
def links(ids): return ', '.join(f'<a href="#evidencia-{eid.lower()}">{escape(labels[eid])} ({eid})</a>' for eid in ids)
def field(label, text): return f'<dt>{escape(label)}</dt><dd>{escape(text)}</dd>'

main = '<main id="contenido" tabindex="-1" class="sample-report">'
main += '<h1>Qué decidir sobre las copias y los accesos de una célula de mecanizado</h1>'
main += f'<p class="sample-notice">{escape(INTRO)}</p>'
main += '<p class="sample-downloads"><a href="assets/MKDL_Ejemplo_Informe_Gerencia.pdf" download>Descargar el informe completo en PDF</a><a href="assets/MKDL_Muestra_Sintetica.zip" download>Descargar informe y anexos para leer sin conexión</a></p>'
main += '<section aria-labelledby="decision"><h2 id="decision">Decisión que permite tomar esta revisión</h2>' + p(DECISION) + p(SCOPE) + f'<p>Perímetro descrito en {links(["E01"])}.</p>' + p(METHOD) + p(ORDER) + '</section>'
main += '<section aria-labelledby="plan"><h2 id="plan">Actuaciones propuestas</h2>' + p(OWNER_NOTE)
for a in actions:
    main += f'<article class="sample-action" id="accion-{a["id"].lower()}"><h3>{a["id"]}. {escape(a["title"])}</h3>'
    main += p(a['fact']) + f'<p class="sample-source">Respaldo: {links(a["sources"])}.</p><dl>'
    main += ''.join(field(label, a[key]) for label,key in [('Trabajo que encargar', 'work'),('Responsable propuesta', 'owner'),('Cuándo', 'when'),('Dependencias', 'dependency'),('Cómo darlo por cerrado', 'close')])
    main += '</dl></article>'
main += '</section><section aria-labelledby="respuesta"><h2 id="respuesta">Borrador de respuesta al comprador</h2>' + p('Texto del escenario para revisión y aprobación de gerencia. No es una respuesta enviada ni aceptada por un comprador.') + '<dl>'
for subject, text, refs in responses:
    main += f'<dt>{escape(subject)}</dt><dd>{escape(text)} Respaldo: {links(refs)}.</dd>'
main += '</dl>' + p('Las comprobaciones pendientes se asignan según A01 y A02. Sólo se comunicarán fechas de pruebas o cambios cuando estén acordadas y autorizadas.') + '</section><section aria-labelledby="evidencias"><h2 id="evidencias">Evidencias del ejercicio</h2>'
main += p('Estas son las cinco fichas completas utilizadas para el ejemplo, fechadas el 25 de octubre de 2026. Los datos ausentes se indican como no aportados; no se sustituyen por supuestos. Puedes volver desde cada ficha a las actuaciones que respalda.')
for e in evidence:
    main += f'<article class="sample-evidence" id="evidencia-{e["id"].lower()}"><h3>{e["id"]}. {escape(e["title"])}</h3><dl>'
    main += field('Tipo', e['kind']) + ''.join(field(label, value) for label,value in e['rows'])
    main += field('Qué permite afirmar', e['meaning']) + field('Qué no demuestra', e['limit']) + '</dl>'
    related = [a for a in actions if e['id'] in a['sources']]
    if related:
        main += '<p>Actuaciones relacionadas: ' + ', '.join(f'<a href="#accion-{a["id"].lower()}">{a["id"]}: {escape(a["title"])}</a>' for a in related) + '.</p>'
    main += '</article>'
main += '</section><section aria-labelledby="pendientes"><h2 id="pendientes">Qué sigue pendiente de comprobar</h2>' + p(LIMIT) + '<dl class="sample-uncertainties">'
for subject, check, action in uncertainties: main += field(subject, check)
main += '</dl>' + p('Esta muestra ilustra el análisis y la entrega documental. No acredita la ejecución de mejoras. La devolución sirve para validar el alcance, resolver dudas y asignar las siguientes decisiones, sin dar por cerrados los pendientes técnicos.')
main += '<p><a href="assets/MKDL_Matriz_Sintetica.csv" download>Descargar el plan editable para trabajar en una hoja de cálculo (CSV)</a></p></section></main>'

head = '''<!doctype html>
<html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Ejemplo de informe OT Check | MKDL</title><meta name="description" content="Informe ficticio completo: decisiones, actuaciones, responsables, criterios de cierre y cinco evidencias legibles."/>
<meta name="theme-color" content="#ecebea"/><meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self'; img-src 'self' data:; script-src 'none'; connect-src 'self'; base-uri 'self'; form-action 'none';"/>
<link rel="canonical" href="https://mkdl.jp/muestra-ot-check.html"/><link rel="icon" href="assets/mkdl-icon.svg" type="image/svg+xml"/>
<link rel="stylesheet" href="assets/site.css"/><link rel="stylesheet" href="assets/sample.css"/></head><body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>'''
header = '''<header class="site-header"><a class="brand" href="index.html" aria-label="MKDL, inicio"><img src="assets/mkdl-logo.svg" alt="Mysthrala Kurogane Defense Labs" width="970" height="214"/></a><nav aria-label="Navegación principal"><a href="index.html#servicio">OT Check</a><a class="nav-contact" href="index.html#contacto">Contacto</a></nav></header>'''
footer = '''<footer><div class="footer-brand"><img src="assets/mkdl-logo.svg" alt="" width="970" height="214"/></div><nav class="footer-links" aria-label="Información legal"><a href="aviso-legal.html">Aviso legal</a><a href="privacidad.html">Privacidad</a><a href="cookies.html">Cookies</a><a href="accesibilidad.html">Accesibilidad</a></nav><p class="copyright">© 2026 Mysthrala Kurogane Defense Labs</p></footer></body></html>'''
html = head + header + main + footer
assert not re.search('[\u2013\u2014]', html)
(ROOT / 'muestra-ot-check.html').write_text(html, encoding='utf-8', newline='\n')

# One content model supplies the full PDF, HTML and editable plan.
from reportlab.lib import colors
from reportlab import rl_config
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.utils import ImageReader
rl_config.invariant = True

styles = {
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=23, leading=27, textColor=colors.HexColor('#202227'), spaceAfter=16),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=17, leading=21, spaceBefore=8, spaceAfter=12, textColor=colors.HexColor('#3d3049'), keepWithNext=True),
    'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=12, leading=16, spaceBefore=10, spaceAfter=7, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10.3, leading=14.5, spaceAfter=9),
    'small': ParagraphStyle('small', fontName='Helvetica', fontSize=9, leading=12.5, spaceAfter=8, textColor=colors.HexColor('#60636a')),
}
story = []
def para(text, kind='body'): return Paragraph(text, styles[kind])
def add(text, kind='body'): story.append(para(escape(text), kind))
def pdf_field(label, text): story.append(para(f'<b>{escape(label)}.</b> {escape(text)}'))
def page_title(text, anchor): story.append(para(f'<a name="{anchor}"/>{escape(text)}', 'h2'))

add('OT Check | Informe de ejemplo', 'small')
add('Copias y accesos de una célula de mecanizado', 'title')
add(INTRO, 'small')
page_title('Decisión que permite tomar esta revisión', 'decision')
add(DECISION)
pdf_field('Alcance', SCOPE)
story.append(para('<link href="#e01" color="#3d3049">Descripción del proceso (E01)</link>.', 'small'))
pdf_field('Método y profundidad', METHOD)
pdf_field('Orden propuesto', ORDER)
pdf_field('Límite de las conclusiones', LIMIT)
add('El plan de las páginas siguientes enlaza con las cinco fichas del anexo. El documento contiene toda la información necesaria para leer el ejemplo sin conexión.', 'small')
page_title('Qué sigue pendiente de comprobar', 'pendientes')
for subject,check,action in uncertainties: pdf_field(subject,check)
story.append(PageBreak())
page_title('Actuaciones propuestas', 'plan')
add(OWNER_NOTE, 'small')
for a in actions:
    block_start = len(story)
    story.append(para(f'<a name="{a["id"].lower()}"/>{a["id"]}. {escape(a["title"])}', 'h3'))
    add(a['fact'])
    refs = ', '.join(f'<link href="#{eid.lower()}" color="#3d3049">{escape(labels[eid])} ({eid})</link>' for eid in a['sources'])
    story.append(para('Respaldo: ' + refs + '.', 'small'))
    for label,key in [('Trabajo que encargar','work'),('Responsable propuesta','owner'),('Cuándo','when'),('Dependencias','dependency'),('Cómo darlo por cerrado','close')]: pdf_field(label,a[key])
    story.append(Spacer(1,8))
    block = story[block_start:]
    del story[block_start:]
    story.append(KeepTogether(block))
page_title('Borrador de respuesta al comprador', 'respuesta')
add('Texto del escenario para revisión y aprobación de gerencia. No es una respuesta enviada ni aceptada por un comprador.', 'small')
for subject,text,refs in responses:
    pdf_field(subject,text)
add('Las comprobaciones pendientes se asignan según A01 y A02. Sólo se comunicarán fechas de pruebas o cambios cuando estén acordadas y autorizadas.', 'small')
story.append(PageBreak())
page_title('Evidencias del ejercicio', 'evidencias')
add('Fichas completas del 25 de octubre de 2026. Todos los datos son sintéticos. No aportado significa ausente en la información de este ejercicio, sin atribuir por ello un fallo técnico.', 'small')
for e in evidence:
    block = [para(f'<a name="{e["id"].lower()}"/>{e["id"]}. {escape(e["title"])}', 'h3')]
    for label,value in [('Tipo', e['kind']), *e['rows'], ('Qué permite afirmar',e['meaning']), ('Qué no demuestra',e['limit'])]:
        block.append(para(f'<b>{escape(label)}.</b> {escape(value)}'))
    related = [a['id'] for a in actions if e['id'] in a['sources']]
    if related:
        block.append(para('Actuaciones relacionadas: ' + ', '.join(f'<link href="#{aid.lower()}" color="#3d3049">{aid}</link>' for aid in related) + '.', 'small'))
    story.append(KeepTogether(block))

logo = ASSETS / 'mkdl-logo-print.png'
assert logo.exists(), 'Render the unchanged original SVG to mkdl-logo-print.png before building the PDF.'
def frame(canvas, doc):
    canvas.saveState()
    canvas.drawImage(ImageReader(str(logo)), 44, A4[1]-54, width=140, height=140*214/970, mask='auto')
    canvas.setStrokeColor(colors.HexColor('#c9c7c4'))
    canvas.line(44, A4[1]-65, A4[0]-44, A4[1]-65)
    canvas.setFont('Helvetica',8)
    canvas.setFillColor(colors.HexColor('#60636a'))
    canvas.drawString(44,27,'MKDL | Ejemplo ficticio | 25 de octubre de 2026')
    canvas.drawRightString(A4[0]-44,27,f'Página {doc.page}')
    canvas.restoreState()
pdf_path = ASSETS / 'MKDL_Ejemplo_Informe_Gerencia.pdf'
doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=44,leftMargin=44,topMargin=82,bottomMargin=48,title='OT Check: informe de ejemplo y evidencias',author='MKDL',pageCompression=1)
doc.build(story,onFirstPage=frame,onLaterPages=frame)

buffer=StringIO(newline='')
w=csv.writer(buffer,delimiter=';',lineterminator='\n')
w.writerow(['Escenario','ID','Actuación','Fundamento','Fuentes','Trabajo que encargar','Responsable propuesta','Cuándo','Dependencias','Comprobación de cierre','Estado de ejecución'])
for a in actions: w.writerow(['SIMULADO',a['id'],a['title'],a['fact'],' '.join(a['sources']),a['work'],a['owner'],a['when'],a['dependency'],a['close'],'No ejecutado; propuesta del ejercicio'])
(ASSETS/'MKDL_Matriz_Sintetica.csv').write_text(buffer.getvalue(),encoding='utf-8-sig',newline='')

offline_header = header.replace('href="index.html"','href="#contenido"')
offline_header = re.sub(r'<nav.*?</nav>','',offline_header,flags=re.S)
offline_main = re.sub(r'<p class="sample-downloads">.*?</p>','',main,flags=re.S)
offline = head + offline_header + offline_main + '<footer><p>MKDL | Ejemplo ficticio. Informe y evidencias incluidos en este paquete.</p></footer></body></html>'
with zipfile.ZipFile(ASSETS/'MKDL_Muestra_Sintetica.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    def add_file(name, data):
        info = zipfile.ZipInfo(name, date_time=(2026,10,25,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, data)
    add_file('muestra-ot-check.html',offline)
    add_file('LEEME.txt','MKDL OT Check: ejemplo ficticio\n\nAbre muestra-ot-check.html para leer el informe y las cinco evidencias sin conexión, o assets/MKDL_Ejemplo_Informe_Gerencia.pdf para imprimirlos. Mantén la carpeta assets junto al HTML.\n\nEl plan editable está en assets/MKDL_Matriz_Sintetica.csv, separado por punto y coma y codificado en UTF-8.\n\nTodo el contenido es simulado. No describe a un cliente ni una prueba ejecutada. No se necesita interpretar archivos JSON.\n')
    for name in ['site.css','sample.css','mkdl-logo.svg','mkdl-icon.svg','MKDL_Ejemplo_Informe_Gerencia.pdf','MKDL_Matriz_Sintetica.csv']:
        add_file('assets/'+name,(ASSETS/name).read_bytes())
print('Generados HTML, PDF completo, plan editable y paquete sin conexión desde el mismo contenido.')
