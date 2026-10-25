# Web corporativa de MKDL

Sitio estático de servicio y contacto para Mysthrala Kurogane Defense Labs. Esta rama prepara la oferta OT Check; editarla o comprobarla en local no cambia lo publicado en mkdl.jp. Kurogane Hub tiene otro repositorio y una superficie pública propia; no forma parte de OT Check.

OT Check revisa un proceso industrial delimitado para entregar decisiones, prioridades, responsables propuestos y comprobaciones con las que encargar mejoras. Euskadi es la base operativa; el público incluye industria de distintos tamaños y unidades de grupos. Alcance, profundidad, calendario, desplazamiento y precio se acuerdan por encargo. No se publica una tarifa firme ni se insinúan clientes o pilotos.

Kalista realiza personalmente el servicio. Consultoría, documentación y formación son la actividad ordinaria. No se incluyen por defecto implementación, integración, operación, incidentes ni disponibilidad permanente. La actividad sigue en preparación y no se declara alta, seguro o certificaciones Cisco efectivos.

## Editar y comprobar

La web no requiere JavaScript, instalación de paquetes ni servicios externos. Usa la marca y el logotipo originales. Antes de preparar publicación deben pasar ambos empaquetados:

```powershell
py -3 scripts/package-site.py --target github
py -3 scripts/package-site.py --target cloudflare
```

Se exportan únicamente archivos públicos a `_site` y `_site-cloudflare`. Cada operación recrea sólo su directorio fijo, validando enlaces y fragmentos locales. No publicar la raíz completa del repositorio.

Vista local del exportado:

```powershell
py -3 -m http.server 4174 --bind 127.0.0.1 --directory _site
```

Abrir `http://127.0.0.1:4174/` y cerrar el servidor con Ctrl+C. Comprobar escritorio, móvil, teclado, enlaces, descargas, legibilidad y avisos legales. En Linux, sustituir `py -3` por `python3`.

## Modelo de entrega sintético

`scripts/ot_check_case.py` contiene los datos de un ejercicio enteramente ficticio: seis activos, catálogo de recuperación por activo y 26 objetos trazables, quince fichas, cinco comprobaciones y cuatro acciones ordenadas. No acredita visita, cliente, seguimiento ni recuperación real. No es un procedimiento de intervención en un control CNC.

`scripts/render_complete_sample.py`, invocado mediante `scripts/build-sample.py`, genera HTML legible, informe PDF, resumen de dos páginas para gerencia, tres pliegos separados, siete CSV editables y ZIP sin conexión. A01 incluye su catálogo para que el proveedor no necesite recibir el informe interno. Los archivos de texto de las muestras son no ejecutables. Las cinco fuentes antiguas se conservan en Git como antecedente sintético, excluidas de los dos exports públicos. El CSV de catálogo tiene una fila por objeto, estado de cobertura, proveedor competente y campos de cierre; no se marca cerrado por incluirlo en la lista. Los pliegos son solicitudes autónomas para los proveedores de cada parte del proceso. A01 debe acompañarse del catálogo CSV, como indica su segunda página.

La generación requiere Python3.11 o superior y las dependencias de autoría `reportlab`, `pypdf` y `pypdfium2`. No son dependencias de ejecución del sitio ni del empaquetado para publicar. Usar un entorno de autoría que ya las tenga o uno aislado aprobado:

```powershell
py -3 scripts/build-sample.py
```

El generador conserva salida determinista. No editar los derivados como una segunda fuente. El PNG de vista previa se obtiene automáticamente de la primera página del PDF vigente. Los CSV usan UTF-8 con BOM y punto y coma. `assets/mkdl-logo-print.png` deriva del SVG original.

## Archivos y límites

- `index.html`, `index.md` y `llms.txt`: explicación y descubrimiento de la oferta.
- `muestra-ot-check.html` y `assets/MKDL_*`: ejercicio, documentos y tablas.
- `assets/site.css` y `assets/mkdl-logo.svg`: identidad original conservada.
- `assets/ot-check.css`, `assets/sample.css`, `assets/commercial.css`: ajustes de portada, informe y lectura de avisos.
- Avisos legales, privacidad, cookies y accesibilidad: textos que requieren revisión contra actividad y proveedores reales antes de publicar.
- `.well-known/security.txt` y `security.txt`: contacto y vigencia idénticos.
- `CNAME`, metadatos, `sitemap.xml` y `robots.txt`: dominio previsto mkdl.jp.

La ausencia de formularios, analítica o almacenamiento programado en las fuentes no acredita la configuración del alojamiento, CDN o correo. La identidad jurídica necesaria no se sustituye por el nombre profesional ni se rellena por inferencia. No introducir expedientes, radar, datos económicos personales, secretos ni documentos de cliente en este repositorio público.

Revisión local, ensayo humano, revisión contractual, CI, publicación y comprobación pública son puertas distintas. Esta rama no autoriza push, PR, merge, despliegue o cambio de dominio. El workflow existente mantiene sus condiciones de publicación. La preparación de Cloudflare se describe en [su guía](cloudflare/README.md); no acredita un cambio de alojamiento ya ejecutado.

Usar exclusivamente información sintética en incidencias. Documentación y contenido visual conservan los términos de [LICENSE](LICENSE).
