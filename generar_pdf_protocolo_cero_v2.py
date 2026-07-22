#!/usr/bin/env python3
# Genera descargas/n2n-protocolo-cero.pdf con WeasyPrint
# Lenguaje visual alineado a n2n-mvp-start.pdf
# Ejecutar desde la raiz del repo: /home/dflorida/GITHUB/n2n/n2n-site

import os
import sys
from weasyprint import HTML as WHTML

SALIDA = "descargas/n2n-protocolo-cero.pdf"

if not os.path.isfile("css/main.css"):
    print("ERROR: no parece la raiz del repo n2n-site. Abortado.")
    sys.exit(1)

for req in ("fonts/Outfit-Variable.woff2", "img/logo.png"):
    if not os.path.isfile(req):
        print(f"ERROR: falta {req}. Abortado.")
        sys.exit(1)

DOC = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<style>
@font-face {
  font-family: 'Outfit';
  src: url('fonts/Outfit-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
}
@page { size: A4; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Outfit', sans-serif;
  color: #1a1a2e;
  font-size: 8pt;
  line-height: 1.4;
}
.band { height: 4mm; background: linear-gradient(90deg, #ff6600 0 22%, #000055 22% 100%); }
.page { padding: 5mm 13mm 6mm 13mm; }

.masthead { display: flex; justify-content: space-between; align-items: flex-start; }
.masthead img { height: 10mm; }
.eyebrow {
  text-align: right;
  font-size: 7.2pt;
  font-weight: 700;
  letter-spacing: .17em;
  text-transform: uppercase;
  color: #52526a;
  line-height: 1.75;
}
.eyebrow .url { color: #ff6600; }

.kicker {
  margin-top: 4mm;
  font-size: 7.4pt;
  font-weight: 700;
  letter-spacing: .22em;
  text-transform: uppercase;
  color: #ff6600;
}
h1 {
  font-size: 24pt;
  font-weight: 800;
  letter-spacing: -.025em;
  color: #000055;
  line-height: 1.02;
  margin-top: 1.5mm;
}
.sub {
  font-size: 11pt;
  font-weight: 600;
  color: #000055;
  margin-top: 1.4mm;
}
.intro { margin-top: 2.5mm; color: #1a1a2e; }
.intro strong { color: #000055; }

.callout {
  margin-top: 3.5mm;
  background: #ebebef;
  border-left: 3pt solid #ff6600;
  padding: 3.5mm 4.5mm;
}
.callout .quote {
  font-size: 9pt;
  font-weight: 700;
  color: #000055;
  line-height: 1.22;
  margin-bottom: 2.6mm;
}
.ctitle {
  font-size: 7.4pt;
  font-weight: 700;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: #000055;
  margin-bottom: 2.2mm;
}

h2 {
  font-size: 7.4pt;
  font-weight: 700;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: #ff6600;
  padding-bottom: 1.2mm;
  border-bottom: .75pt solid #000055;
  margin-bottom: 2.2mm;
}

table { width: 100%; border-collapse: collapse; }
td { vertical-align: top; padding: 0; }
.gap { width: 7mm; }
.cols { margin-top: 3.5mm; }

ul { list-style: none; }
li { position: relative; padding-left: 4mm; margin-bottom: 1.6mm; line-height: 1.28; }
li:last-child { margin-bottom: 0; }
li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 1.05mm;
  width: 1.5mm;
  height: 1.5mm;
  background: #ff6600;
  transform: rotate(45deg);
}
li b { display: block; color: #000055; font-weight: 700; font-size: 8.2pt; }
li span { color: #52526a; font-size: 7.4pt; }

.step { margin-bottom: 1.5mm; }
.step:last-child { margin-bottom: 0; }
.step .n {
  font-style: normal;
  font-size: 7pt;
  font-weight: 800;
  color: #ff6600;
  letter-spacing: .08em;
  margin-right: 1.4mm;
}
.step b { display: block; color: #000055; font-weight: 700; font-size: 8.2pt; line-height: 1.18; }
.step span { color: #52526a; font-size: 7.4pt; line-height: 1.26; }

.scope p { color: #52526a; font-size: 7.4pt; line-height: 1.34; margin-bottom: 2mm; }
.scope p:last-child { margin-bottom: 0; }
.scope b { color: #000055; }

.navy {
  margin-top: 4mm;
  background: #000055;
  color: #fff;
  padding: 4mm 4.5mm;
  position: relative;
}
.navy::after {
  content: "";
  position: absolute;
  top: 0; right: 0; bottom: 0;
  width: 3pt;
  background: #ff6600;
}
.navy .lab {
  font-size: 7.2pt;
  font-weight: 700;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: #ff6600;
  margin-bottom: 1.6mm;
}
.navy .big { font-size: 14pt; font-weight: 800; line-height: 1.05; }
.navy .med { font-size: 11pt; font-weight: 800; line-height: 1.1; }
.navy .cap { font-size: 7.4pt; color: rgba(255,255,255,.72); margin-top: 1.2mm; line-height: 1.35; }
.navy .div { width: 7mm; border-left: .75pt solid rgba(255,255,255,.28); }
.navy .fine {
  margin-top: 3mm;
  padding-top: 2.4mm;
  border-top: .75pt solid rgba(255,255,255,.2);
  font-size: 7.6pt;
  color: rgba(255,255,255,.85);
}
.navy .fine strong { color: #fff; }
.navy .fine .tiny { display: block; margin-top: 1.4mm; font-size: 7.2pt; color: rgba(255,255,255,.55); }

.foot {
  margin-top: 3.5mm;
  padding-top: 2.6mm;
  border-top: .75pt solid #d8d8e8;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.foot .l { font-size: 8.6pt; color: #1a1a2e; }
.foot .l a { color: #ff6600; font-weight: 700; text-decoration: none; }
.foot .l .path { display: block; margin-top: 1.4mm; font-size: 7.4pt; color: #52526a; text-decoration: none; }
.foot .r { text-align: right; }
.foot .r .lab {
  font-size: 7.2pt;
  font-weight: 700;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: #52526a;
  margin-bottom: 1.2mm;
}
.foot .r a { display: block; font-size: 8.6pt; font-weight: 700; color: #000055; text-decoration: none; }
</style>
</head>
<body>

<div class="band"></div>
<div class="page">

<div class="masthead">
  <img src="img/logo.png" alt="N2N">
  <div class="eyebrow">
    CONTROL OPERATIVO<br>
    CADENA DE FRÍO · B2B<br>
    <span class="url">N2N.COM.AR</span>
  </div>
</div>

<p class="kicker">Método de control de pérdidas</p>
<h1>Protocolo CERO</h1>
<p class="sub">Control de pérdidas en cadena de frío</p>

<p class="intro">En operaciones de alto volumen la pérdida no aparece con nombre propio: aparece como diferencia de inventario, merma, rotura de cadena de frío y rechazo de cliente. Se distribuye entre planillas, turnos y depósitos hasta que nadie puede señalar dónde ocurrió, y termina asumida como costo fijo. <strong>No es costo fijo: es ausencia de control en los puntos exactos donde la mercadería cambia de manos.</strong></p>

<div class="callout">
  <p class="quote">El control no se pide. Se hace estructuralmente inevitable.</p>
  <p class="ctitle">Los cinco pilares</p>
  <table>
    <tr>
      <td>
        <ul>
          <li><b>Puntos de custodia</b><span>Cada instancia en que la mercadería cambia de manos: recepción, cámara, carga, reparto, devolución.</span></li>
          <li><b>Segregación de funciones</b><span>Quien pesa no es quien registra, y quien registra no es quien despacha.</span></li>
          <li><b>Evidencia obligatoria</b><span>Peso, foto, geolocalización, usuario y marca de tiempo en cada movimiento.</span></li>
        </ul>
      </td>
      <td class="gap"></td>
      <td>
        <ul>
          <li><b>Control inevitable</b><span>La operación no avanza sin registro: el paso siguiente no existe sin el dato del anterior.</span></li>
          <li><b>Verificación permanente</b><span>Revisión periódica de anomalías. Un control que no se verifica se degrada.</span></li>
        </ul>
      </td>
    </tr>
  </table>
</div>

<table class="cols">
  <tr>
    <td>
      <h2>Las seis fases</h2>
      <div class="step"><b><i class="n">01</i>Relevamiento</b><span>Circuito real, no el del manual: quién toca qué y dónde no queda rastro.</span></div>
      <div class="step"><b><i class="n">02</i>Cuantificación</b><span>Brecha entre lo que entra, lo que se registra y lo que sale.</span></div>
      <div class="step"><b><i class="n">03</i>Diseño de controles</b><span>Segregación y evidencia en cada punto de custodia.</span></div>
      <div class="step"><b><i class="n">04</i>Implantación técnica</b><span>El sistema que vuelve el control inevitable.</span></div>
      <div class="step"><b><i class="n">05</i>Verificación 60 días</b><span>Ajuste en el período en que el circuito puede volver atrás.</span></div>
      <div class="step"><b><i class="n">06</i>Control continuo</b><span>Auditoría periódica e informe de anomalías.</span></div>
    </td>
    <td class="gap"></td>
    <td>
      <h2>Alcance</h2>
      <div class="scope">
        <p><b>Aplica a:</b> distribuidoras de lácteos, pescados, congelados, avícola y fiambres, y operadores logísticos refrigerados. Más de un punto de almacenamiento, flota propia o tercerizada, y volumen que no se puede contar a mano.</p>
        <p><b>No aplica a:</b> operaciones de un solo punto sin traslado interno, retail, y quien busca únicamente un software de stock.</p>
        <p>El Protocolo CERO no audita personas: audita estructura. Interviene sobre el circuito físico y sobre el sistema que lo registra. Cuando el registro deja de ser un pedido y pasa a ser una condición, la oportunidad desaparece sola.</p>
      </div>
    </td>
  </tr>
</table>

<div class="navy">
  <table>
    <tr>
      <td style="width:33%">
        <p class="lab">Diagnóstico</p>
        <p class="big">USD 1.500</p>
        <p class="cap">2 a 3 semanas. Informe con puntos de fuga, magnitud estimada y controles faltantes.</p>
      </td>
      <td class="div"></td>
      <td style="width:33%">
        <p class="lab">Implantación</p>
        <p class="med">Según operación</p>
        <p class="cap">6 a 10 semanas. Diseño de controles y sistema que los ejecuta.</p>
      </td>
      <td class="div"></td>
      <td>
        <p class="lab">Control continuo</p>
        <p class="med">Abono mensual</p>
        <p class="cap">Auditoría mensual e informe de anomalías.</p>
      </td>
    </tr>
  </table>
  <div class="fine">
    <strong>El diagnóstico es tuyo:</strong> te sirve aunque no avances con N2N.
    <span class="tiny">(Valores en dólares, no incluyen impuestos.)</span>
  </div>
</div>

<div class="foot">
  <div class="l">
    El método completo está en <a href="https://n2n.com.ar/control/protocolo-cero/">n2n.com.ar</a>
    <a class="path" href="https://n2n.com.ar/control/protocolo-cero/">n2n.com.ar/control/protocolo-cero/</a>
  </div>
  <div class="r">
    <p class="lab">Contacto</p>
    <a href="mailto:contacto@n2n.com.ar">contacto@n2n.com.ar</a>
  </div>
</div>

</div>
</body>
</html>
'''

os.makedirs("descargas", exist_ok=True)

doc = WHTML(string=DOC, base_url=os.getcwd()).render()
paginas = len(doc.pages)

if paginas != 1:
    print(f"ERROR: el PDF salio en {paginas} paginas. Debe ser 1. No se escribio el archivo.")
    sys.exit(1)

doc.write_pdf(SALIDA)

print(f"OK  {SALIDA}")
print(f"Paginas: {paginas}")
print(f"Bytes: {os.path.getsize(SALIDA)}")
