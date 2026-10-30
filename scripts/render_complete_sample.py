"""Build all readable formats from the explicitly fictional ot_check_case fixture."""
from pathlib import Path
from html import escape as esc
from io import StringIO
import csv
import re
import zipfile
import ot_check_case as case

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
def p(t):return dict(type='p',text=t)
def h(t,id=None):return dict(type='h3',text=t,id=id)
def dl(items):return dict(type='dl',items=items)
def tbl(headers,rows,widths):return dict(type='table',headers=headers,rows=rows,widths=widths)
def refs(ids):return dict(type='sources',ids=ids)
sections=[]
def section(id,title,blocks):sections.append(dict(id=id,title=title,blocks=blocks))
section('decision','Decisión para gerencia',[
 p(case.PURPOSE),p(case.SUMMARY),
 tbl(['Orden y encargo','Responsable de cierre y plazo'],[[a['rank']+'. '+a['id']+' '+a['title'],a['owner']+'. '+a['due']+'.'] for a in case.actions],[.50,.50]),
 p('Compromiso solicitado: A03, unas 1,5 h internas; A01, 2 a 4 h para localizar y revisar; A02, 1 a 2 h de coordinación. Son estimaciones del escenario. Para A01, A02 y A04 se pide presupuesto técnico separado antes de autorizar cambios o ensayos.'),
 p('A02.0 es un paso propuesto al cliente del 26 al 30/10/2026, no iniciado, sin esperar presupuesto: confirmar habilitación y revisar los registros conservados de VPN, puesto de salto y cuenta local de todo el periodo disponible, como mínimo desde la última ventana autorizada, contrastando cada sesión con su ticket y ventana; si procede, aplicar el procedimiento vigente con soporte alternativo acordado. Un uso no autorizado se deriva al procedimiento de incidentes de la empresa, fuera de OT Check. El resto de A02 puede seguir después de conservar el paquete. La asignación es propuesta: gerencia debe designar una persona por rol. A03 puede avanzar en paralelo con A01 y A02. Si sólo se dispone de una franja de trabajo, se prepara la respuesta con plazo sin prometer que las mejoras estén terminadas.')])
section('compromiso','Recursos y condiciones de la decisión',[
 p(case.BUSINESS),p(case.OBJECTIVES),
 tbl(['Encargo','Recursos que se pide autorizar'],[[a['id'],a['resources']] for a in case.actions],[.14,.86]),
 p('Las estimaciones pertenecen a este escenario, no a una medición de Kalista ni a una tarifa de proveedor. Solicitar presupuesto no autoriza el trabajo técnico. Aplazar A01 mantiene incierta la reconstrucción; aplazar A02 deja sin resolver atribución y ventana; A04 depende de ambos y de producción.')])
section('perimetro','Proceso, dependencias y alcance',[
 p(case.SCOPE),p('Mapa funcional ficticio basado en E06. Describe dependencias de trabajo; no acredita una topología física o aislamiento efectivo.'),refs(['E06']),
 tbl(['Paso','Trabajo y dependencias','Consecuencia a considerar'],[[f[0],f[1]+' Activos: '+f[2]+'.',f[3]] for f in case.flow],[.18,.42,.40]),p(case.METHOD),p(case.EXCLUSIONS),
 p('La vía de soporte y transferencia se recoge como declaración en E13. Debe contrastarse con registros antes de aprobar una arquitectura o una sesión. El alcance documental y el alcance de una prueba técnica son distintos.')])
section('recuperacion','Catálogo de recuperación propuesto por MKDL',[
 p('El CSV Catálogo de recuperación contiene una fila por objeto con aplicabilidad, ubicación, custodia, evidencia y cierre pendiente. La tabla siguiente resume los seis activos. Por cada activo se concreta qué conservar y qué falta confirmar. El catálogo es la entrada de A01, no una lista que deba inventar el cliente. El mantenedor confirma qué objetos existen y qué procedimiento admite el fabricante.'),
 tbl(['Activo y contenido','Estado, responsable y siguiente comprobación'],[[r[0]+': '+r[1],r[2]+' Responsable: '+r[3]+'. '+r[4]+' Fuentes: '+r[5]+'.'] for r in case.recovery],[.45,.55])])
section('inventario','Funciones y dependencias del inventario',[
 tbl(['Activo y función','Dependencia y responsable'],[[a[0]+'. '+a[1]+': '+a[2],a[3]+' Responsable: '+a[4]+'.'] for a in case.assets],[.52,.48])])
b=[]
for c in case.checks:
 target=next(s['blocks'] for s in sections if s['id']=='perimetro') if c['id']=='C06' else b
 target.extend([h(c['id']+'. '+c['title'],c['id'].lower()),dl([('Estado',c['state']),('Método',c['method']),('Resultado del escenario',c['result']),('Límite',c['limit'])]),refs(c['sources'])])
b.insert(0,p('C01 integra la comparación del programa y la selección registrada que antes se separaba como C02. Se conserva la numeración restante para mantener la trazabilidad.'))
section('comprobaciones','Comprobaciones y resultados',b)
b=[p('El orden combina un compromiso de respuesta, conservación antes de cambios y dependencias de ejecución. Cada encargo tiene un único rol que responde del cierre y participantes distintos para realizar el trabajo. Se asignan personas antes de aprobarlo.')]
for a in case.actions:b.extend([h(a['id']+'. '+a['title'],'accion-'+a['id'].lower()),dl([
 ('Responsable de cierre propuesto',a['owner']),('Trabajo que encargar',a['task']),('Evidencia de cierre',a['proof']),('Estado',a['status'])]),refs(a['sources'])])
section('plan','Plan de trabajo y criterio de cierre',b)
b=[p('Borrador del escenario para aprobación de gerencia. No enviado ni aceptado por un comprador. Sólo se comunicarán fechas de pruebas o cambios después de acordarlas con quienes ejecutarán esos trabajos.')]
for title,text,ids in case.responses:b.extend([h(title),p(text),refs(ids)])
b.extend([h('Pendientes y responsables'),tbl(['Pendiente','Quién lo resuelve y con qué evidencia'],[[u[0]+'. '+u[1],u[2]+'. '+u[4]+' Acción: '+u[3]+'.'] for u in case.uncertainties],[.34,.66])])
section('respuesta','Respuesta externa para aprobación e incertidumbres internas',b)
section('seguimiento','Ejemplo de una revisión trimestral',[
 p('Continuación enteramente ficticia, tres meses después del diagnóstico. S01 a S04 son entradas inventadas para esta demostración, no hechos posteriores observados. No acreditan que el servicio se haya prestado.'),
 tbl(['Acción y cambio','Evidencia recibida y decisión'],[[r[0]+': '+r[1],r[2]+' '+r[3]+' Rol responsable: '+next(a['owner'].split(',')[0] for a in case.actions if a['id']==r[0])+'. Persona designada por gerencia en el escenario ficticio (nombre omitido). Fecha objetivo ficticia: 05/02/2027. Estado: abierto; pendiente de evidencia de cierre.'] for r in case.followup],[.48,.52]),
 p('La entrega trimestral distingue cambios, evidencias suficientes, pendientes y la siguiente decisión. Incluye preparar y analizar estos documentos, actualizar la matriz y la reunión de hasta 45 minutos. No equivale a soporte entre revisiones ni a una prueba técnica. La fecha de cierre sólo se cumplimenta al aceptar su evidencia.')])
b=[p('Fuentes del ejercicio en orden de identificación. Las fechas distinguen el documento, el cambio y la revisión: una copia reciente de un archivo antiguo no cambia su contenido.')]
for e in case.evidence:
 b.extend([h(e['id']+'. '+e['title'],'evidencia-'+e['id'].lower()),dl([('Tipo y procedencia',e['kind']+'. '+e['source']),('Fecha',e['date']),('Participante del escenario',e['author']),*e['fields'],('Conclusión respaldada',e['supports']),('Alcance de esta fuente',e['limit'])])])
 related=[a for a in case.actions if e['id'] in a['sources'] or any(e['id'] in c['sources'] for c in case.checks if c['id'] in a['checks'])]
 if related:b.append(dict(type='related',ids=[a['id'] for a in related]))
section('evidencias','Anexo de evidencias legibles',b)
section('aceptacion','Devolución y aceptación de la entrega',[p(case.DELIVERY),dict(type='list',items=case.acceptance)])

def text_values():
 yield from [case.VERSION,case.NOTICE,case.TITLE]
 for s in sections:
  yield s['title']
  for b in s['blocks']:
   if b['type'] in ['p','h3']:yield b['text']
   elif b['type']=='dl':
    for k,v in b['items']:yield k;yield v
   elif b['type']=='table':
    yield from b['headers']
    for row in b['rows']:yield from row
   elif b['type']=='list':yield from b['items']
def block_html(b):
 t=b['type']
 if t=='p':return '<p>'+esc(b['text'])+'</p>'
 if t=='h3':return '<h3'+(f' id="{b["id"]}"' if b.get('id') else '')+'>'+esc(b['text'])+'</h3>'
 if t=='dl':return '<dl>'+''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k,v in b['items'])+'</dl>'
 if t=='list':return '<ul>'+''.join('<li>'+esc(v)+'</li>' for v in b['items'])+'</ul>'
 if t=='sources':return '<p class="sample-source">Fuentes: '+', '.join(f'<a href="#evidencia-{e.lower()}">{esc(case.evidence_by_id[e]["title"])} ({e})</a>' for e in b['ids'])+'.</p>'
 if t=='related':return '<p class="sample-source">Volver al plan: '+', '.join('<a href="#accion-'+aid.lower()+'">'+aid+'</a>' for aid in b['ids'])+'.</p>'
 if t=='table':return '<div class="sample-table" role="region" tabindex="0" aria-label="Tabla: '+esc(b['headers'][0],quote=True)+'"><table role="table"><thead role="rowgroup"><tr role="row">'+''.join('<th scope="col" role="columnheader">'+esc(v)+'</th>' for v in b['headers'])+'</tr></thead><tbody role="rowgroup">'+''.join('<tr role="row">'+''.join('<td role="cell"><span class="cell-label" aria-hidden="true">'+esc(label)+'</span>'+esc(v)+'</td>' for label,v in zip(b['headers'],row))+'</tr>' for row in b['rows'])+'</tbody></table></div>'
 raise ValueError(t)

head='''<!doctype html><html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>Informe completo de ejemplo OT Check | MKDL</title><meta name="description" content="Caso ficticio completo: decisión para gerencia, proceso, activos, comprobaciones, encargos a proveedores y evidencias legibles."/><meta name="theme-color" content="#ecebea"/><meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self'; img-src 'self' data:; script-src 'none'; connect-src 'self'; base-uri 'self'; form-action 'none';"/><link rel="canonical" href="https://mkdl.jp/muestra-ot-check.html"/><link rel="icon" href="assets/mkdl-icon.svg" type="image/svg+xml"/><link rel="stylesheet" href="assets/site.css?v=20261030-legal-mobile"/><link rel="stylesheet" href="assets/sample.css?v=20261026-lectura"/></head><body><a class="skip-link" href="#contenido">Saltar al contenido</a>'''
header='''<header class="site-header"><a class="brand" href="index.html" aria-label="MKDL, inicio"><img src="assets/mkdl-logo.svg" alt="Mysthrala Kurogane Defense Labs" width="970" height="214"/></a><nav aria-label="Navegación principal"><a href="index.html#servicio">OT Check</a><a class="nav-contact" href="index.html#contacto">Contacto</a></nav></header>'''
footer='''<footer><div class="footer-brand"><img src="assets/mkdl-logo.svg" alt="" width="970" height="214"/></div><nav class="footer-links" aria-label="Información legal"><a href="aviso-legal.html">Aviso legal</a><a href="privacidad.html">Privacidad</a><a href="cookies.html">Cookies</a><a href="accesibilidad.html">Accesibilidad</a><a href="security-policy.html">Seguridad</a></nav><p class="copyright">© 2026 Mysthrala Kurogane Defense Labs</p></footer></body></html>'''
main='<main id="contenido" tabindex="-1" class="sample-report"><h1>'+esc(case.TITLE)+'</h1><p>'+esc(case.VERSION)+'</p><p class="sample-notice">'+esc(case.NOTICE)+'</p><p class="sample-downloads"><a href="assets/MKDL_Ejemplo_Informe_Gerencia.pdf" download>Descargar el informe completo en PDF</a><a href="assets/MKDL_Muestra_Sintetica.zip" download>Descargar la entrega para leer sin conexión</a></p>'
for s in sections:main+='<section aria-labelledby="'+s['id']+'"><h2 id="'+s['id']+'">'+esc(s['title'])+'</h2>'+''.join(block_html(b) for b in s['blocks'])+'</section>'
csv_labels={'MKDL_Matriz_Sintetica.csv':'Plan de actuaciones','MKDL_Inventario_Sintetico.csv':'Inventario y dependencias','MKDL_Comprobaciones_Sinteticas.csv':'Comprobaciones y límites','MKDL_Evidencias_Sinteticas.csv':'Registro de evidencias','MKDL_Encargos_Proveedor.csv':'Encargos a proveedores','MKDL_Catalogo_Recuperacion.csv':'Catálogo de recuperación','MKDL_Revision_Trimestral.csv':'Ejemplo de revisión trimestral','MKDL_Catalogo_Proveedor.csv':'Catálogo autónomo para proveedores'}
brief_names={a['id']:'MKDL_Pliego_'+a['id']+'.pdf' for a in case.actions if a['id'] in ['A01','A02','A04']}
main+='<p>Para compartir A01, descargar el <a href="assets/MKDL_Encargo_A01.zip" download>encargo A01 completo (ZIP con pliego y catálogo para proveedor)</a>. Para consultar los PDF: '+', '.join('<a href="assets/'+name+'" download>Pliego '+aid+' (PDF)</a>' for aid,name in brief_names.items())+'. A01 se comparte siempre junto con MKDL_Catalogo_Proveedor.csv, no como PDF suelto. A02 y A04 contienen su contexto y condiciones. No es necesario remitir el informe interno.</p>'
main+='<p><a href="assets/MKDL_Decisiones_y_Plan.pdf" download>Decisión y recursos para gerencia (dos páginas PDF)</a></p>'
main+='<p>Tablas editables para hoja de cálculo: '+', '.join('<a href="assets/'+name+'" download>'+label+' (CSV)</a>' for name,label in csv_labels.items())+'.</p></main>'
html=head+header+main+footer
assert not re.search('[\u2013\u2014]',html)
(ROOT/'muestra-ot-check.html').write_text(html,encoding='utf-8',newline='\n')

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate,Paragraph,PageBreak,KeepTogether,LongTable,TableStyle,Spacer
rl_config.invariant=True
# Fixed authoring timestamp for reproducibility, distinct from fictional evidence dates.
import os
os.environ['SOURCE_DATE_EPOCH']='1792969200'
styles={
 'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=23,leading=27,spaceAfter=14),
 'h2':ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=17,leading=21,spaceBefore=8,spaceAfter=12,keepWithNext=True,textColor=colors.HexColor('#3d3049')),
 'h3':ParagraphStyle('h3',fontName='Helvetica-Bold',fontSize=11.7,leading=15,spaceBefore=9,spaceAfter=5,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=13.3,spaceAfter=7),
 'field':ParagraphStyle('field',fontName='Helvetica',fontSize=9.6,leading=12.3,spaceAfter=4),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=9,leading=12.4,spaceAfter=8,textColor=colors.HexColor('#60636a')),
 'cell':ParagraphStyle('cell',fontName='Helvetica',fontSize=9.1,leading=12)}
def para(text,style='body'):return Paragraph(text,styles[style])
story=[para(esc(case.VERSION),'small'),para(esc(case.TITLE),'title'),para(esc(case.NOTICE),'small')]
for i,s in enumerate(sections):
 if s['id'] in ['compromiso','perimetro','seguimiento','evidencias']:story.append(PageBreak())
 story.append(para('<a name="'+s['id']+'"/>'+esc(s['title']),'h2'))
 last_record_parts=None
 for b in s['blocks']:
  t=b['type']
  if t not in ['sources','related']:last_record_parts=None
  if t=='p':story.append(para(esc(b['text'])))
  elif t=='h3':story.append(para(('<a name="'+b['id']+'"/>' if b.get('id') else '')+esc(b['text']),'h3'))
  elif t=='dl':
   paragraphs=[para('<b>'+esc(k)+'.</b> '+esc(v),'field') for k,v in b['items']]
   # Keep the record heading with its fields and sources, not on a preceding page.
   if story and isinstance(story[-1],Paragraph) and story[-1].style.name=='h3':paragraphs.insert(0,story.pop())
   if sum(len(k)+len(v) for k,v in b['items'])<1500:
    last_record_parts=paragraphs
    story.append(KeepTogether(paragraphs))
   else:story.extend(paragraphs)
  elif t=='list':story.extend(para('• '+esc(v)) for v in b['items'])
  elif t in ['sources','related']:
   if t=='sources':sources=para('Fuentes: '+', '.join('<link href="#evidencia-'+e.lower()+'" color="#3d3049">'+esc(case.evidence_by_id[e]['title'])+' ('+e+')</link>' for e in b['ids'])+'.','small')
   else:sources=para('Volver al plan: '+', '.join('<link href="#accion-'+a.lower()+'" color="#3d3049">'+a+'</link>' for a in b['ids'])+'.','small')
   if last_record_parts is not None:
    story.pop()
    story.append(KeepTogether(last_record_parts+[sources]))
   else:story.append(sources)
   last_record_parts=None
  elif t=='table':
   data=[[para('<b>'+esc(v)+'</b>','cell') for v in b['headers']]]+[[para(esc(v),'cell') for v in row] for row in b['rows']]
   tab=LongTable(data,colWidths=[w*(A4[0]-88) for w in b['widths']],repeatRows=1,hAlign='LEFT')
   tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#ecebea')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#c9c7c4')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
   story.extend([tab,Spacer(1,12)])
def frame(canvas,doc):
 canvas.saveState();canvas.drawImage(ImageReader(str(ASSETS/'mkdl-logo-print.png')),44,A4[1]-54,width=140,height=140*214/970,mask='auto')
 canvas.setStrokeColor(colors.HexColor('#c9c7c4'));canvas.line(44,A4[1]-65,A4[0]-44,A4[1]-65)
 canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#60636a'));canvas.drawString(44,27,'MKDL | Ejemplo ficticio | 26/10/2026');canvas.drawRightString(A4[0]-44,27,'Página '+str(doc.page));canvas.restoreState()
SimpleDocTemplate(str(ASSETS/'MKDL_Ejemplo_Informe_Gerencia.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=82,bottomMargin=48,title='OT Check: caso ficticio completo, proceso y encargos',author='MKDL').build(story,onFirstPage=frame,onLaterPages=frame)

# Supplier-facing requests stand alone; internal action tasks stay in the client matrix.
supplier_fields={
 'A01': [
  ('Destinatarios y reparto',case.supplier_repartition('A01')),
  ('Trabajo solicitado','Validar aplicabilidad del catálogo adjunto por objeto. Identificar lo ya conservado, resolver con mantenimiento e ingeniería la revisión válida de los parámetros CNC y presupuestar por separado la exportación o reconstrucción de lo que falte. Para cada objeto indicar paquete, versión, compatibilidad, procedimiento, custodia y evidencia de conservación; mantener abierto lo no resuelto.'),
  ('Punto de partida disponible','Se dispone de transcripciones ficticias de un programa P-204 revisión C y su copia coincidente. La copia de Parámetros CNC M-01 es revisión 1, anterior al cambio MNT-021 a revisión 2; otros dos extractos del mismo objeto llevan etiqueta revisión 2 pero distinto contenido. No seleccionar por nombre ni fecha. No se han aportado paquete CNC completo, imagen de puestos, proyecto CAM, licencias, configuración de red o procedimiento de reposición. El cliente facilitará las fuentes autorizadas por canal acordado, no credenciales.'),
  ('Resultado solicitado','Presupuesto desglosado por proveedor y objeto, separando validación, localización y generación de material. Adjuntar tabla de cobertura con estado, evidencia, pendientes y responsable de cada interfaz. Una copia documental no acredita restauración.'),
 ],
 'A02': [
  ('Destinatario',case.supplier_repartition('A02')),
  ('Trabajo solicitado','Paso propuesto al cliente del 26 al 30/10/2026, no iniciado y sin esperar al presupuesto: informática debe confirmar si la habilitación que muestra la exportación de cuentas corresponde a una ventana autorizada y pedir los registros conservados de VPN, puesto de salto y cuenta local de todo el periodo disponible, como mínimo desde la última ventana autorizada, contrastando cada sesión con su ticket y ventana para comprobar uso fuera de ventana sin presumir intrusión. Ante uso no autorizado, aplicar el procedimiento de incidentes de la empresa, fuera de OT Check. Al proveedor se solicita acordar de inmediato la alternativa de soporte para aplicar el procedimiento por ticket y ventana si procede. Cada proveedor cotiza sólo su parte: el proveedor informático cubre identidades remotas y puesto de salto; el mantenedor CNC confirma identidad técnica, necesidad y compatibilidad del acceso a máquina. No se duplica la conservación de configuración solicitada en A01. Conciliar técnico, identidad VPN, puesto de salto, acceso a ingeniería y cuenta local; documentar autorización, ventana y registro de cierre. Separar este paso inmediato del resto de cambios presupuestados.'),
  ('Punto de partida disponible','El procedimiento PR-SOP-02 exige aprobación de mantenimiento, identidad nominativa, ventana y registro de cierre. Una exportación ficticia muestra identidad genérica habilitada sin caducidad; no se aportan registros que vinculen esa identidad con VPN ni demuestren exposición, sesiones o MFA. El cliente facilitará procedimiento y extractos autorizados sin credenciales. Se requiere aclarar la discrepancia, no presumir una intrusión.'),
  ('Resultado solicitado','Propuesta de configuración y procedimiento compatibles con el fabricante, o excepción motivada para aprobación. Identificar permisos, ventana, alternativa de soporte y evidencias de habilitación y cierre. La eficacia sólo podrá revisarse con registros posteriores autorizados.'),
 ],
 'A04': [
  ('Destinatario',case.supplier_repartition('A04')),
  ('Trabajo solicitado','Presupuestar primero la definición de una prueba de recuperación aislada o en entorno aprobado por fabricante. Identificar servicio a recuperar, paquete de partida, licencias, recursos, entorno, pasos, autorizaciones, criterios de éxito y parada, conservación de evidencias y vuelta al estado anterior. Cotizar ejecución como fase separada, sin autorización implícita.'),
  ('Punto de partida y pendientes','Célula de seis activos: CNC, operación, ingeniería CAM, almacén de copias, acceso de soporte y conmutador. Producción propone recuperar preparación del siguiente trabajo en ocho horas y tolerar un cambio de turno; son objetivos por aprobar, no tiempos probados. Catálogo y paquetes aún deben validarse con sus proveedores. Calidad exige revisión aprobada y primera pieza antes de liberar producción.'),
  ('Resultado solicitado','Especificación y presupuesto por fases con alcance, dependencias y exclusiones. Un acta posterior deberá registrar entorno, pasos, resultados, incidencias y tiempos medidos frente a criterios aprobados y validación técnica y de producción. Un ensayo fallido no acredita recuperación; aceptar la especificación no acredita haber ejecutado la prueba.'),
 ]
}
for a in case.actions:
 if a['id'] not in brief_names:continue
 fields=[('Contacto del cliente','[Persona de contacto designada por el cliente]'),*supplier_fields[a['id']],('Condiciones antes de intervenir',a['change_safety']),('Siguiente paso','Proponer alcance, coste, plazo, interfaces, autorizaciones y exclusiones. Este documento solicita presupuesto y no autoriza una intervención. La persona de contacto debe confirmar alcance y destinatarios antes de utilizarlo.')]
 parts=[para('Petición de presupuesto | '+a['id'],'small'),para(esc(a['title']),'h2'),para('Ejercicio ficticio: proceso M-01. Sin cliente, instalación ni autorización reales.','small')]
 parts.extend(para('<b>'+esc(k)+'.</b> '+esc(v),'field') for k,v in fields)
 if a['id']=='A01':
  parts.extend([PageBreak(),para('Cobertura y reparto por proveedor','h2'),para('Resumen de seis activos. Compartir este PDF junto con MKDL_Catalogo_Proveedor.csv, incluidos en MKDL_Encargo_A01.zip. El catálogo tiene una fila por objeto; la columna Pliego correspondiente separa el alcance: los objetos A01 se cotizan aquí y OR24 se solicita sólo en A02. Para AS05, A01 conserva configuración de VPN y puesto de salto, mientras A02 concilia identidades, ticket y autorización. Ninguna fila autoriza intervenir.','small')])
  for r in case.recovery:
   providers=', '.join(dict.fromkeys(x['supplier'] for x in case.recovery_objects if x['asset']==r[0] and x['brief']=='A01'))
   selected=[x for x in case.recovery_objects if x['asset']==r[0] and x['brief']=='A01']
   content=('; '.join(x['object'] for x in selected).rstrip('.')+'.') if r[0]=='AS05' else r[1]
   coverage='; '.join(x['state'] for x in selected)+'. Identidad, ticket y autorización se solicitan sólo en el pliego A02.' if r[0]=='AS05' else r[2]
   parts.extend([para('<b>'+r[0]+'.</b> '+esc(content),'field'),para('Disponible y pendiente: '+esc(coverage)+' Proveedor a consultar: '+esc(providers)+'. Área del cliente: '+esc(r[3])+'.','small')])
 SimpleDocTemplate(str(ASSETS/brief_names[a['id']]),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=82,bottomMargin=48,title='OT Check: pliego '+a['id'],author='MKDL').build(parts,onFirstPage=frame,onLaterPages=frame)

from pypdf import PdfReader,PdfWriter
reader=PdfReader(ASSETS/'MKDL_Ejemplo_Informe_Gerencia.pdf')
assert 'Recursos y condiciones de la decisión' in reader.pages[1].extract_text()
assert 'Proceso, dependencias y alcance' in reader.pages[2].extract_text()
summary=PdfWriter()
for page in reader.pages[:2]:summary.add_page(page)
summary.add_metadata({'/Title':'OT Check: decisión y recursos, ejemplo ficticio','/Author':'MKDL','/CreationDate':'D:20261025230000Z','/ModDate':'D:20261025230000Z'})
with (ASSETS/'MKDL_Decisiones_y_Plan.pdf').open('wb') as f:summary.write(f)
import pypdfium2
from PIL import Image
preview=pypdfium2.PdfDocument(str(ASSETS/'MKDL_Decisiones_y_Plan.pdf'))
preview_image=preview[0].render(scale=1.8).to_pil().convert('RGB')
preview_image.save(ASSETS/'muestra-decision.png')
for width in [384,preview_image.width]:
 image=preview_image if width==preview_image.width else preview_image.resize((width,round(preview_image.height*width/preview_image.width)),Image.Resampling.LANCZOS)
 target=ASSETS/f'muestra-decision-{width}.webp'
 image.save(target,format='WEBP',lossless=True,method=6)
 with Image.open(target) as decoded:assert decoded.convert('RGB').tobytes()==image.tobytes()

def write_csv(name,headers,rows):
 b=StringIO(newline='');w=csv.writer(b,delimiter=';',lineterminator='\n');w.writerow(headers);w.writerows(rows);(ASSETS/name).write_text(b.getvalue(),encoding='utf-8-sig',newline='')
write_csv('MKDL_Matriz_Sintetica.csv',['Escenario','Orden','ID','Actuación','Prioridad','Motivo','Responsable de cierre propuesto','Participantes','Plazo o condición','Recursos estimados','Trabajo','Entradas','Dependencias','Condiciones previas','Aceptación','Evidencia de cierre','Cierre posterior de recuperación','Estado','Fuentes','Comprobaciones','Persona asignada','Fecha objetivo acordada','Fecha de cierre','Evidencia recibida','Próxima revisión'],[['FICTICIO',a['rank'],a['id'],a['title'],a['priority'],a['reason'],a['owner'],a['participants'],a['due'],a['resources'],a['task'],a['inputs'],a['dependency'],a['change_safety'],a['acceptance'],a['proof'],a.get('technical_success',''),a['status'],' '.join(a['sources']),' '.join(a['checks']),a['assigned_person'],a['target_date'],a['close_date'],a['received_evidence'],a['next_review']] for a in case.actions])
write_csv('MKDL_Inventario_Sintetico.csv',['ID','Activo','Función','Dependencias','Responsable del escenario','Límite'],case.assets)
write_csv('MKDL_Catalogo_Recuperacion.csv',['Escenario','ID objeto','Activo','Objeto','Aplicabilidad','Ubicación','Custodia propuesta','Estado de cobertura','Fuentes','Siguiente comprobación','Proveedor a consultar','Pliego correspondiente','Paquete identificado','Revisión confirmada','Procedimiento validado','Estado de cierre','Evidencia de cierre','Fecha de cierre'],[['FICTICIO']+[r[k] for k in ['id','asset','object','applicability','location','custodian','state','evidence','next','supplier','brief','package','revision','procedure','close_state','close_evidence','close_date']] for r in case.recovery_objects])
write_csv('MKDL_Catalogo_Proveedor.csv',['Escenario','ID objeto','Activo','Objeto','Aplicabilidad','Ubicación','Custodia propuesta','Estado de cobertura','Siguiente comprobación','Proveedor a consultar','Pliego correspondiente','Paquete identificado','Revisión confirmada','Procedimiento validado','Estado de cierre','Evidencia de cierre','Fecha de cierre'],[['FICTICIO']+[r[k] for k in ['id','asset','object','applicability','location','custodian','state','next','supplier','brief','package','revision','procedure','close_state','close_evidence','close_date']] for r in case.supplier_recovery])
write_csv('MKDL_Revision_Trimestral.csv',['Escenario','Acción','Cambio del escenario','Evidencia recibida','Siguiente decisión','Rol responsable propuesto','Persona asignada','Fecha objetivo ficticia','Estado','Fecha de cierre'],[['FICTICIO',*r,next(a['owner'].split(',')[0] for a in case.actions if a['id']==r[0]),'Designada por gerencia en el escenario ficticio (nombre omitido)','05/02/2027','Abierto: pendiente de evidencia de cierre',''] for r in case.followup])
write_csv('MKDL_Comprobaciones_Sinteticas.csv',['ID','Comprobación','Estado','Método','Resultado','Límite','Fuentes'],[[c[k] for k in ['id','title','state','method','result','limit']]+[' '.join(c['sources'])] for c in case.checks])
write_csv('MKDL_Evidencias_Sinteticas.csv',['ID','Título','Procedencia','Fecha','Participante ficticio','Tipo','Contenido','Qué respalda','Límite'],[[e[k] for k in ['id','title','source','date','author','kind']]+[' | '.join(k+': '+v for k,v in e['fields']),e['supports'],e['limit']] for e in case.evidence])
write_csv('MKDL_Encargos_Proveedor.csv',['Escenario','ID','Encargo','Destinatario o reparto','Trabajo solicitado','Punto de partida','Resultado solicitado','Autorizaciones y seguridad','Estado'],[['FICTICIO',a['id'],a['title'],supplier_fields[a['id']][0][1],supplier_fields[a['id']][1][1],supplier_fields[a['id']][2][1],supplier_fields[a['id']][3][1],a['change_safety'],'Solicitud de presupuesto; no autoriza intervención'] for a in case.actions if a['id'] in ['A01','A02','A04']])
with zipfile.ZipFile(ASSETS/'MKDL_Encargo_A01.zip','w') as bundle:
 for name in ['MKDL_Pliego_A01.pdf','MKDL_Catalogo_Proveedor.csv']:
  info=zipfile.ZipInfo(name,date_time=(2026,10,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;bundle.writestr(info,(ASSETS/name).read_bytes())
 info=zipfile.ZipInfo('LEEME.txt',date_time=(2026,10,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
 bundle.writestr(info,'Encargo ficticio A01: leer MKDL_Pliego_A01.pdf junto con MKDL_Catalogo_Proveedor.csv. Cada proveedor cotiza sólo su competencia. La columna Pliego correspondiente separa los objetos A01 del objeto OR24, que se solicita sólo en A02. No se autoriza intervención ni se acredita restauración.\n')

offline_header=re.sub(r'<nav.*?</nav>','',header.replace('href="index.html"','href="#contenido"'),flags=re.S)
offline=head+offline_header+re.sub(r'<p class="sample-downloads">.*?</p>','',main,flags=re.S)+'<footer><p>MKDL | Ejemplo ficticio. Informe y evidencias incluidos.</p></footer></body></html>'
with zipfile.ZipFile(ASSETS/'MKDL_Muestra_Sintetica.zip','w') as z:
 def add_file(name,data):
  info=zipfile.ZipInfo(name,date_time=(2026,10,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
 add_file('muestra-ot-check.html',offline)
 add_file('LEEME.txt','MKDL OT Check: ejemplo ficticio\n\nAbre muestra-ot-check.html o assets/MKDL_Ejemplo_Informe_Gerencia.pdf. Incluyen decisiones, proceso, catálogo por activo, plan, seguimiento y quince fichas legibles. Las dos primeras páginas del PDF resumen la decisión y los recursos. No necesitan Internet.\n\nConserva assets junto al HTML. Las tablas CSV se importan con punto y coma y UTF-8. Para A01, comparte MKDL_Encargo_A01.zip: contiene MKDL_Pliego_A01.pdf junto con MKDL_Catalogo_Proveedor.csv. No envíes A01 como PDF suelto. A02 y A04 son pliegos autónomos. El catálogo interno conserva trazabilidad al informe; la copia de proveedor elimina referencias internas no necesarias para presupuestar.\n\nCaso inventado. No se ha realizado una visita, cambio, seguimiento o restauración real.\n')
 for name in ['site.css','sample.css','mkdl-logo.svg','mkdl-icon.svg','MKDL_Ejemplo_Informe_Gerencia.pdf','MKDL_Decisiones_y_Plan.pdf',*brief_names.values(),*csv_labels,'MKDL_Encargo_A01.zip']:add_file('assets/'+name,(ASSETS/name).read_bytes())
print('Generado el ejemplo ficticio: catálogo por activo, quince fichas, cinco comprobaciones y cuatro acciones ordenadas.')
