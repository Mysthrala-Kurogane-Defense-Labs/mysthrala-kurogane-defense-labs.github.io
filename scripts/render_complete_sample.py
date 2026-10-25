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
 tbl(['Encargo','Cuándo y por qué'],[[a['id']+'. '+a['title'],a['priority']+'. '+a['reason']] for a in case.actions],[.38,.62]),p(case.BUSINESS),p(case.OBJECTIVES),
 p('Se conservan dos controles respaldados para las muestras: coincidencia del programa con su copia y de la revisión liberada con dos registros. No se propone sustituirlos ni comprar una herramienta por defecto.')])
section('perimetro','Proceso, dependencias y alcance',[
 p(case.SCOPE),p('Mapa funcional ficticio basado en E06. Describe dependencias de trabajo; no acredita una topología física o aislamiento efectivo.'),refs(['E06']),
 tbl(['Paso','Trabajo y dependencias','Consecuencia a considerar'],[[f[0],f[1]+' Activos: '+f[2]+'.',f[3]] for f in case.flow],[.18,.42,.40]),p(case.METHOD),p(case.EXCLUSIONS),
 p('Cobertura documental: once fichas y muestras explícitas. Sin muestreo estadístico ni observación de ejecución. No representa una revisión de toda la planta.')])
b=[]
for a in case.assets:b.extend([h(a[0]+'. '+a[1],a[0].lower()),dl([('Función',a[2]),('Dependencias',a[3]),('Responsable del escenario',a[4]),('Límite de revisión',a[5])])])
section('inventario','Activos del proceso revisado',b)
b=[]
for c in case.checks:
 target=sections[1]['blocks'] if c['id']=='C06' else b
 target.extend([h(c['id']+'. '+c['title'],c['id'].lower()),dl([('Estado',c['state']),('Método',c['method']),('Resultado del escenario',c['result']),('Límite',c['limit'])]),refs(c['sources'])])
section('comprobaciones','Comprobaciones y resultados',b)
b=[p('El orden responde al plazo del comprador, a las diferencias constatadas en las muestras y a la dependencia del mantenedor. No asigna probabilidades o ahorros no medidos. La organización debe validar y asignar las responsables propuestas.')]
for a in case.actions:b.extend([h(a['id']+'. '+a['title'],'accion-'+a['id'].lower()),dl([
 ('Prioridad y motivo',a['priority']+'. '+a['reason']),('Responsable propuesta',a['owner']),('Trabajo que encargar',a['task']),('Información de entrada',a['inputs']),
  ('Dependencias',a['dependency']),('Condiciones antes de intervenir',a['change_safety']),('Aceptación del encargo',a['acceptance']),('Evidencia de cierre',a['proof']),*([('Cierre posterior de la recuperación',a['technical_success'])] if 'technical_success' in a else []),('Estado',a['status'])]),refs(a['sources'])])
section('plan','Plan y especificaciones para proveedores',b)
b=[p('Borrador del escenario para aprobación de gerencia. No enviado ni aceptado por un comprador. Sólo se comunicarán fechas de pruebas o cambios después de acordarlas con quienes ejecutarán esos trabajos.')]
for title,text,ids in case.responses:b.extend([h(title),p(text),refs(ids)])
b.extend([h('Pendientes y responsables'),tbl(['Pendiente','Quién lo resuelve y con qué evidencia'],[[u[0]+'. '+u[1],u[2]+'. '+u[4]+' Acción: '+u[3]+'.'] for u in case.uncertainties],[.34,.66])])
section('respuesta','Respuesta al comprador e incertidumbres',b)
b=[p('Once fichas ficticias del caso v4. E01 a E05 conservan las fuentes del extracto anterior; E06 a E11 amplían explícitamente el ejercicio. No son documentos recibidos de una empresa ni evidencias de una visita real.')]
for e in case.evidence:
 b.extend([h(e['id']+'. '+e['title'],'evidencia-'+e['id'].lower()),dl([('Tipo y procedencia',e['kind']+'. '+e['source']),('Fecha',e['date']),('Participante del escenario',e['author']),*e['fields'],('Qué respalda',e['supports']),('Qué no demuestra',e['limit'])])])
 related=[a for a in case.actions if e['id'] in a['sources'] or any(e['id'] in c['sources'] for c in case.checks if c['id'] in a['checks'])]
 if related:b.append(dict(type='related',ids=[a['id'] for a in related]))
section('evidencias','Anexo de evidencias legibles',b)
section('aceptacion','Devolución y aceptación de la entrega',[p(case.DELIVERY),dict(type='list',items=case.acceptance),p('La versión, el alcance firmado y las interlocutoras se identifican en un encargo real. Kalista realiza la revisión humana y la devolución. Los reparos sobre cobertura o coherencia se corrigen dentro del alcance. La aceptación del informe no cierra las actuaciones técnicas ni equivale a homologación del comprador.')])

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

head='''<!doctype html><html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>Informe completo de ejemplo OT Check | MKDL</title><meta name="description" content="Caso ficticio completo: decisión para gerencia, proceso, activos, comprobaciones, encargos a proveedores y evidencias legibles."/><meta name="theme-color" content="#ecebea"/><meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self'; img-src 'self' data:; script-src 'none'; connect-src 'self'; base-uri 'self'; form-action 'none';"/><link rel="canonical" href="https://mkdl.jp/muestra-ot-check.html"/><link rel="icon" href="assets/mkdl-icon.svg" type="image/svg+xml"/><link rel="stylesheet" href="assets/site.css"/><link rel="stylesheet" href="assets/sample.css"/></head><body><a class="skip-link" href="#contenido">Saltar al contenido</a>'''
header='''<header class="site-header"><a class="brand" href="index.html" aria-label="MKDL, inicio"><img src="assets/mkdl-logo.svg" alt="Mysthrala Kurogane Defense Labs" width="970" height="214"/></a><nav aria-label="Navegación principal"><a href="index.html#servicio">OT Check</a><a class="nav-contact" href="index.html#contacto">Contacto</a></nav></header>'''
footer='''<footer><div class="footer-brand"><img src="assets/mkdl-logo.svg" alt="" width="970" height="214"/></div><nav class="footer-links" aria-label="Información legal"><a href="aviso-legal.html">Aviso legal</a><a href="privacidad.html">Privacidad</a><a href="cookies.html">Cookies</a><a href="accesibilidad.html">Accesibilidad</a></nav><p class="copyright">© 2026 Mysthrala Kurogane Defense Labs</p></footer></body></html>'''
main='<main id="contenido" tabindex="-1" class="sample-report"><h1>'+esc(case.TITLE)+'</h1><p>'+esc(case.VERSION)+'</p><p class="sample-notice">'+esc(case.NOTICE)+'</p><p class="sample-downloads"><a href="assets/MKDL_Ejemplo_Informe_Gerencia.pdf" download>Descargar el informe completo en PDF</a><a href="assets/MKDL_Muestra_Sintetica.zip" download>Descargar la entrega para leer sin conexión</a></p>'
for s in sections:main+='<section aria-labelledby="'+s['id']+'"><h2 id="'+s['id']+'">'+esc(s['title'])+'</h2>'+''.join(block_html(b) for b in s['blocks'])+'</section>'
csv_labels={'MKDL_Matriz_Sintetica.csv':'Plan de actuaciones','MKDL_Inventario_Sintetico.csv':'Inventario y dependencias','MKDL_Comprobaciones_Sinteticas.csv':'Comprobaciones y límites','MKDL_Evidencias_Sinteticas.csv':'Registro de evidencias','MKDL_Encargos_Proveedor.csv':'Encargos a proveedores'}
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
styles={
 'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=23,leading=27,spaceAfter=14),
 'h2':ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=17,leading=21,spaceBefore=8,spaceAfter=12,keepWithNext=True,textColor=colors.HexColor('#3d3049')),
 'h3':ParagraphStyle('h3',fontName='Helvetica-Bold',fontSize=11.7,leading=15,spaceBefore=9,spaceAfter=5,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10.2,leading=14,spaceAfter=8),
 'field':ParagraphStyle('field',fontName='Helvetica',fontSize=10.2,leading=14,spaceAfter=4),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=9,leading=12.4,spaceAfter=8,textColor=colors.HexColor('#60636a')),
 'cell':ParagraphStyle('cell',fontName='Helvetica',fontSize=9.1,leading=12)}
def para(text,style='body'):return Paragraph(text,styles[style])
story=[para(esc(case.VERSION),'small'),para(esc(case.TITLE),'title'),para(esc(case.NOTICE),'small')]
for i,s in enumerate(sections):
 if i:story.append(PageBreak())
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
   if sum(len(k)+len(v) for k,v in b['items'])<3500:
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
 canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#60636a'));canvas.drawString(44,27,'MKDL | Caso ficticio v4 | 25/10/2026');canvas.drawRightString(A4[0]-44,27,'Página '+str(doc.page));canvas.restoreState()
SimpleDocTemplate(str(ASSETS/'MKDL_Ejemplo_Informe_Gerencia.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=82,bottomMargin=48,title='OT Check: caso ficticio completo, proceso y encargos',author='MKDL').build(story,onFirstPage=frame,onLaterPages=frame)

def write_csv(name,headers,rows):
 b=StringIO(newline='');w=csv.writer(b,delimiter=';',lineterminator='\n');w.writerow(headers);w.writerows(rows);(ASSETS/name).write_text(b.getvalue(),encoding='utf-8-sig',newline='')
write_csv('MKDL_Matriz_Sintetica.csv',['Escenario','ID','Actuación','Prioridad','Motivo','Responsable propuesta','Trabajo','Entradas','Dependencias','Condiciones previas','Aceptación','Evidencia de cierre','Cierre posterior de recuperación','Estado','Fuentes','Comprobaciones'],[['FICTICIO v4',a['id'],a['title'],a['priority'],a['reason'],a['owner'],a['task'],a['inputs'],a['dependency'],a['change_safety'],a['acceptance'],a['proof'],a.get('technical_success',''),a['status'],' '.join(a['sources']),' '.join(a['checks'])] for a in case.actions])
write_csv('MKDL_Inventario_Sintetico.csv',['ID','Activo','Función','Dependencias','Responsable del escenario','Límite'],case.assets)
write_csv('MKDL_Comprobaciones_Sinteticas.csv',['ID','Comprobación','Estado','Método','Resultado','Límite','Fuentes'],[[c[k] for k in ['id','title','state','method','result','limit']]+[' '.join(c['sources'])] for c in case.checks])
write_csv('MKDL_Evidencias_Sinteticas.csv',['ID','Título','Procedencia','Fecha','Participante ficticio','Tipo','Contenido','Qué respalda','Límite'],[[e[k] for k in ['id','title','source','date','author','kind']]+[' | '.join(k+': '+v for k,v in e['fields']),e['supports'],e['limit']] for e in case.evidence])
write_csv('MKDL_Encargos_Proveedor.csv',['ID','Encargo','Entradas','Trabajo solicitado','Autorizaciones y seguridad','Dependencias','Criterio de aceptación','Evidencia de cierre','Cierre posterior de recuperación','Estado'],[[a['id'],a['title'],a['inputs'],a['task'],a['change_safety'],a['dependency'],a['acceptance'],a['proof'],a.get('technical_success',''),a['status']] for a in case.actions if a['id'] in ['A01','A02','A04']])
offline_header=re.sub(r'<nav.*?</nav>','',header.replace('href="index.html"','href="#contenido"'),flags=re.S)
offline=head+offline_header+re.sub(r'<p class="sample-downloads">.*?</p>','',main,flags=re.S)+'<footer><p>MKDL | Caso ficticio v4. Informe y evidencias incluidos.</p></footer></body></html>'
with zipfile.ZipFile(ASSETS/'MKDL_Muestra_Sintetica.zip','w') as z:
 def add_file(name,data):
  info=zipfile.ZipInfo(name,date_time=(2026,10,25,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
 add_file('muestra-ot-check.html',offline)
 add_file('LEEME.txt','MKDL OT Check: caso ficticio v4\n\nAbre muestra-ot-check.html o assets/MKDL_Ejemplo_Informe_Gerencia.pdf. Ambos contienen el caso completo, proceso, resultados, encargos y once fichas legibles. No necesitan Internet.\n\nConserva la carpeta assets junto al HTML. Las cinco tablas CSV se importan con separador punto y coma y UTF-8. Son editables; no hace falta abrirlas para entender el informe.\n\nCaso inventado. No representa a ninguna empresa real. No se ha realizado ninguna visita, cambio o restauración real.\n')
 for name in ['site.css','sample.css','mkdl-logo.svg','mkdl-icon.svg','MKDL_Ejemplo_Informe_Gerencia.pdf',*csv_labels]:add_file('assets/'+name,(ASSETS/name).read_bytes())
print('Generada la entrega ficticia v4: once fichas, seis comprobaciones, cuatro actuaciones y cinco tablas editables.')
