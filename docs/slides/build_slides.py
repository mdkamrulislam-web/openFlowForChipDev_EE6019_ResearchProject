#!/usr/bin/env python3
"""Build the editable Tiny Tapeout beginner lecture; see README.md.

The deck uses local images and lecture-notes.json. No network calls are made.
"""
from pathlib import Path
import argparse
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.xmlchemy import OxmlElement
from lxml import etree

HERE = Path(__file__).resolve().parent
PAPER, NAVY, TEAL, FIRE = 'F8F4EB', '152B39', '007F83', 'F05B3E'
PALE, WHITE, GREY, RULE = 'DDEDEC', 'FFFFFF', '536974', 'CBD1CD'
FONT, DISPLAY, MONO = 'Aptos', 'Aptos Display', 'Consolas'
REPO = 'https://github.com/mdkamrulislam-web/tt-sky130-counter'
SHA = '61ef06bed008e76000f9ae46d65182e476d15dd6'
GDS_RUN = REPO + '/actions/runs/37693100748'
VIEWER = 'https://mdkamrulislam-web.github.io/tt-sky130-counter/'
TEMPLATES = 'https://tinytapeout.com/hdl/templates/'
notes = json.loads((HERE / 'lecture-notes.json').read_text(encoding='utf-8'))
source_index = []


def C(value):
    return RGBColor.from_string(value)


def shape(s, x, y, w, h, fill=WHITE, line=None, kind=MSO_SHAPE.RECTANGLE):
    q = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    q.fill.solid()
    q.fill.fore_color.rgb = C(fill)
    if line:
        q.line.color.rgb = C(line)
        q.line.width = Pt(1.2)
    else:
        q.line.fill.background()
    # Override theme effects, so every diagram remains flat and editable.
    q._element.spPr.append(OxmlElement('a:effectLst'))
    return q


def text(s, x, y, w, h, value, size=24, colour=NAVY, bold=False,
         font=FONT, align=PP_ALIGN.LEFT, link=None, spacing=1.08):
    q = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = q.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.015)
    tf.margin_top = tf.margin_bottom = Inches(0.015)
    for i, line in enumerate(value.split('\n')):
        p = tf.paragraphs[0] if not i else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(0)
        r = p.add_run()
        r.text = line
        r.font.name = font
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = C(colour)
        if link:
            r.hyperlink.address = link
    return q


def rule(s, x, y, w, colour=RULE):
    shape(s, x, y, w, 0.015, colour)


def arrow(s, x1, y1, x2, y2, colour=TEAL, width=2.3):
    q = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                              Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    q.line.color.rgb = C(colour)
    q.line.width = Pt(width)
    q._element.spPr.append(OxmlElement('a:effectLst'))
    tail = OxmlElement('a:tailEnd')
    tail.set('type', 'triangle')
    q.line._get_or_add_ln().append(tail)
    return q


def dot(s, x, y, d, fill=TEAL):
    return shape(s, x, y, d, d, fill, kind=MSO_SHAPE.OVAL)


def label(s, x, y, value, w=11.8, colour=TEAL):
    return text(s, x, y, w, 0.30, value.upper(), 12, colour, True)


def code(s, x, y, w, h, value, size=20):
    assert len(value.splitlines()) <= 12
    shape(s, x, y, w, h, NAVY)
    shape(s, x, y, 0.08, h, FIRE)
    return text(s, x + .25, y + .22, w - .50, h - .42,
                value, size, PAPER, font=MONO, spacing=1.15)


def strip(s, value, x=.65, y=6.27, w=12.0, size=24, fill=PALE):
    shape(s, x, y, w, .55, fill)
    text(s, x + .16, y + .08, w - .32, .40, value, size, TEAL, True)


def counter(s, x, y, value, w=1.32, colour=TEAL, size=48):
    shape(s, x, y, w, 1.00, colour)
    text(s, x + .05, y + .16, w - .10, .73, str(value), size, PAPER, True,
         font=DISPLAY, align=PP_ALIGN.CENTER)


def chip(s, x, y, w=4.6, h=3.2, active=(1,2)):
    shape(s, x, y, w, h, NAVY)
    for r in range(3):
        for c in range(4):
            shape(s, x + .17 + c * (w-.34)/4, y+.17+r*(h-.34)/3,
                  (w-.56)/4, (h-.52)/3, FIRE if (r,c)==active else PALE)
    for i in range(7):
        shape(s, x-.15, y+.31+i*(h-.62)/6, .15, .07, TEAL)
        shape(s, x+w, y+.31+i*(h-.62)/6, .15, .07, TEAL)


def pending(s, x, y, w, h, marker, title, detail):
    shape(s, x, y, w, h, PAPER, TEAL)
    text(s, x+.16, y+.15, w-.32, .34, marker+' • CAPTURE PENDING', 20, TEAL, True)
    if h < 2.4:
        text(s, x+.16, y+.66, w-.32, .49, title, 26, NAVY, True)
        text(s, x+.16, y+1.25, w-.32, .39, detail, 20, GREY)
    else:
        text(s, x+.16, y+.70, w-.32, .69, title, 26, NAVY, True)
        text(s, x+.16, y+1.48, w-.32, h-1.60, detail, 22, GREY)


def picture(s, name, x, y, w=None, h=None):
    kwargs = {}
    if w: kwargs['width'] = Inches(w)
    if h: kwargs['height'] = Inches(h)
    return s.shapes.add_picture(str(HERE/'img'/name), Inches(x), Inches(y), **kwargs)


def slide(prs, title, section, step=None, extra='', urls=()):
    number = len(prs.slides)+1
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = C(PAPER)
    label(s, .65, .34, section)
    if step is not None:
        text(s, .56, .76, 1.18, 1.00, f'{step:02d}', 70, FIRE, True, DISPLAY)
        text(s, 1.98, .85, 10.68, 1.10, title, 40, NAVY, True, DISPLAY)
    else:
        text(s, .65, .87, 12.02, 1.01, title, 42, NAVY, True, DISPLAY)
    rule(s, .65, 7.02, 12.02)
    text(s, .65, 7.14, 10.4, .18,
         'EE6019 • Tiny Tapeout • 8 October 2026 • Sources and teaching notes in PowerPoint', 10, GREY)
    text(s, 12.01, 7.12, .64, .21, f'{number:02d}', 11, TEAL, True, align=PP_ALIGN.RIGHT)
    original = notes[number-1]
    sources = list(dict.fromkeys(original['sources']+list(urls)))
    prose = original['notes'] + ('\n\nBEGINNER EXAMPLE / REVIEW NOTES\n'+extra if extra else '')
    s.notes_slide.notes_text_frame.text = (
        'LECTURER NOTES\n'+prose+'\n\nSOURCES (checked 7 October 2026)\n'+'\n'.join(sources))
    source_index.append({'slide':number,'title':title,'sources':sources})
    return s


def build(output):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333333), Inches(7.5)
    prs.core_properties.title = 'Make your own chip: the Tiny Tapeout flow, step by step'
    prs.core_properties.author = 'EE6019 teaching project'
    # Match hyperlinks to the two intentional diagram colours.
    for part in prs.part.package.iter_parts():
        if part.content_type == 'application/vnd.openxmlformats-officedocument.theme+xml':
            root = etree.fromstring(part.blob)
            ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
            for key in ('hlink','folHlink'):
                node=root.find('.//a:clrScheme/a:'+key,ns)
                for child in list(node): node.remove(child)
                etree.SubElement(node,'{'+ns['a']+'}srgbClr').set('val',TEAL)
            part._blob=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)

    # 01 — a distinctive opening, with the running example already visible.
    s=slide(prs,'Make your own chip.','Tiny Tapeout flow • step by step')
    # Replace standard title with a generous two-line opening.
    s.shapes[1].text_frame.clear()
    text(s,.62,1.13,7.20,2.01,'Make your\nown chip.',58,NAVY,True,DISPLAY,spacing=.96)
    text(s,.68,3.61,6.4,1.11,'From an 8-bit counter\nto a real ASIC.',30)
    text(s,.68,5.20,6.4,.88,'ASIC = a chip made for a specific job.\nOur job: count from 0 to 255.',24)
    chip(s,8.05,1.66,4.53,3.46)
    label(s,8.05,5.44,'One shared chip. Your own tile.',4.6)
    for i,v in enumerate([0,1,2]):
        counter(s,8.12+i*1.55,5.91,v,1.17,size=36)
        if i<2: arrow(s,9.32+i*1.55,6.38,9.61+i*1.55,6.38)

    # 02 — one circuit selected from many, and the cost-sharing idea.
    s=slide(prs,'Many designs. One shared chip.','Why a student chip is affordable')
    chip(s,.84,2.00,5.12,3.30)
    arrow(s,6.16,3.62,7.09,3.62)
    shape(s,7.20,2.87,1.84,1.42,TEAL)
    text(s,7.34,3.09,1.56,1.00,'Select\none tile',26,PAPER,True,align=PP_ALIGN.CENTER)
    arrow(s,9.18,3.62,10.00,3.62)
    text(s,10.11,3.03,2.47,1.42,'Your\nboard pins',30,NAVY,True)
    rule(s,.84,5.66,11.64)
    text(s,.84,5.95,3.64,.67,'Shared fabrication',26,TEAL,True)
    text(s,4.86,5.95,3.44,.67,'Open design tools',26,TEAL,True)
    text(s,8.70,5.87,3.78,.93,'Open PDK:\nprocess rules + cells',24,TEAL,True)

    # 03 — a visible workflow with a continuous example, not eight small cards.
    s=slide(prs,'The path from an idea to silicon','Keep this map beside the lab')
    stages=[('Idea','Count 0–255'),('RTL','Verilog: registers + logic'),('Test','Check its behaviour'),('Template','Connect fixed pins'),
            ('Actions','Tools build + check'),('GDS','Layout geometry'),('Fab','Manufacture'),('Board','Select + test')]
    for i,(name,detail) in enumerate(stages):
        r,c=divmod(i,4); x=.82+c*3.18; y=2.18+r*2.29
        dot(s,x,y,.50,FIRE if i<4 else TEAL)
        text(s,x+.06,y+.07,.38,.35,str(i+1),20,PAPER,True,align=PP_ALIGN.CENTER)
        text(s,x,y+.71,2.70,.52,name,30,NAVY,True)
        text(s,x,y+1.30,2.72,.73,detail,24)
        if c<3: arrow(s,x+.58,y+.25,x+3.04,y+.25)
    label(s,.82,6.76,'You design and verify • Actions build • fabrication follows an approved submission')

    # 04 — typographic foundry comparison plus a delivery timeline.
    s=slide(prs,'Choose the process with your template','Three fabrication routes')
    data=[('IHP','130','SG13G2','IHP MPW'),('SkyWater','130','SKY130','ChipFoundry'),('GlobalFoundries','180','GF180','wafer.space')]
    for i,(fab,node,pdk,route) in enumerate(data):
        x=.72+i*4.18
        text(s,x,2.15,3.82,.62,fab,30,NAVY,True)
        text(s,x,2.99,2.83,1.20,node,80,TEAL,True,DISPLAY)
        text(s,x+2.64,3.74,1.13,.46,'nm',24,TEAL)
        text(s,x,4.56,3.77,1.04,pdk+'\n'+route,26)
        if i<2: shape(s,x+3.90,2.08,.015,3.65,RULE)
    strip(s,'Allow months for fabrication, assembly and delivery: typically 6–12 months.')

    # 05 — counter bits are connected to real shared pins.
    s=slide(prs,'Eight bits become eight output pins','The fixed Tiny Tapeout interface',extra='Visible worked example: count 5 is binary 00000101, so uo_out[2] and uo_out[0] are high. clk and rst_n are external pins; ena is internal selection. In this actual example uio_oe[0]=1 drives wrap and the remaining uio pins are inputs. The enable input is assumed synchronous in the minimal example.',urls=[REPO+'/blob/'+SHA+'/src/project.v'])
    shape(s,4.79,2.10,3.11,1.56,NAVY)
    text(s,5.04,2.34,2.62,1.03,'8-bit\ncounter',32,PAPER,True,align=PP_ALIGN.CENTER)
    text(s,.77,2.21,3.36,1.15,'ui_in[0] → enable\nclk → clock\nrst_n = 0 → reset',24)
    arrow(s,4.05,2.87,4.65,2.87)
    arrow(s,8.02,2.87,8.61,2.87)
    text(s,8.76,2.19,3.92,1.25,'uo_out[7:0] → count\nuio[0] → wrap\nuio_oe[0] = 1',24)
    label(s,.79,4.10,'Example: count = 5 → binary 00000101')
    for i,v in enumerate('00000101'):
        x=.86+i*1.51
        text(s,x,4.52,1.10,.35,f'uo[{7-i}]',20,GREY,align=PP_ALIGN.CENTER)
        shape(s,x,5.02,1.10,.67,FIRE if v=='1' else PALE)
        text(s,x,5.12,1.10,.45,v,28,PAPER if v=='1' else NAVY,True,align=PP_ALIGN.CENTER)
    strip(s,'1x1: SKY / IHP ≈ 167 × 108 µm • GF180 ≈ 340 × 160 µm',size=24)

    # 06 — measured utilisation, visibly distinct from a gate-count limit.
    s=slide(prs,'Our counter: 4.96% reported core utilisation','Measured Tiny Tapeout result',extra='The 10-by-10 diagram is an editable illustration of area utilisation, not a cell floorplan. Exact utilisation is 4.96131% of core area, including non-fill physical cells. All gds jobs, including precheck, passed at 61ef06b. Lint warnings are TIMESCALEMOD and are not a zero-warning result.',urls=[GDS_RUN])
    text(s,.78,2.02,6.20,1.40,'4.96%',88,FIRE,True,DISPLAY)
    text(s,.83,3.61,5.54,.84,'Utilisation = occupied cell area\nas a fraction of available core area.',24)
    for i,(a,b) in enumerate([('47','cells after synthesis'),('50 MHz','clock target'),('+8.643 ns','worst setup slack')]):
        y=4.77+i*.62
        text(s,.83,y,2.34,.46,a,26,TEAL,True)
        text(s,3.28,y,3.68,.46,b,24)
    for r in range(10):
        for c in range(10):
            shape(s,8.18+c*.42,2.14+r*.42,.35,.35,FIRE if r==0 and c<5 else PALE)
    text(s,8.14,6.43,4.31,.36,'SKY130 • 1x1 • commit 61ef06b',20,TEAL,True)

    # 07 — two entry routes; simple equivalent examples.
    s=slide(prs,'Draw gates, or write their behaviour','Two ways into the same flow',extra='The visible AND example has A=1 and B=0, so its output is 0. This illustrates the same logic expressed as a gate drawing and an HDL assignment; the running counter lesson uses the HDL route.')
    shape(s,6.55,2.04,.015,4.61,RULE)
    label(s,.83,2.13,'Wokwi • gates in a browser',5.20)
    text(s,.82,2.71,5.10,.81,'A picture of the circuit',30,NAVY,True)
    text(s,.85,4.13,1.27,1.27,'A = 1\nB = 0',28)
    shape(s,2.49,4.13,1.83,1.11,TEAL)
    text(s,2.53,4.40,1.75,.55,'AND',30,PAPER,True,align=PP_ALIGN.CENTER)
    arrow(s,2.07,4.68,2.42,4.68)
    arrow(s,4.43,4.68,4.89,4.68)
    text(s,5.00,4.42,1.00,.68,'0',40,FIRE,True)
    label(s,7.05,2.13,'Verilog • this lesson',5.15)
    text(s,7.04,2.71,5.32,.81,'A description of the circuit',30,NAVY,True)
    code(s,7.06,4.12,5.52,1.16,'assign y = a & b;',24)
    text(s,7.06,5.81,5.41,.67,'An IHP Chisel template also exists.',24)

    # 08 — first large lab step and exact setup instructions.
    s=slide(prs,'Copy the template for your class shuttle','Start with the correct fab',1)
    for i,(fab,name,pin) in enumerate([('SKY130','ttsky-verilog-template','ttsky26d'),('IHP','ttihp-verilog-template','ttihp26b • closed'),('GF180','ttgf-verilog-template','ttgf26c')]):
        y=2.13+i*.85
        text(s,.83,y,1.67,.55,fab,26,TEAL,True)
        text(s,2.79,y,5.65,.55,name,26)
        text(s,8.75,y,3.89,.55,pin,24,GREY)
        rule(s,.83,y+.68,11.67)
    pending(s,.82,4.91,5.63,1.79,'P1','Use this template','Signed-in template menu capture.')
    pending(s,6.82,4.91,5.63,1.79,'P2','Pages → GitHub Actions','Capture the repo Pages setting.')

    # 09 — an editable file tree linked to the actual example.
    s=slide(prs,'Know which file you are changing','Your project is a small set of files',2,extra='The actual counter has project.v plus counter.v. Both must appear in info.yaml source_files and test/Makefile PROJECT_SOURCES. The docs artifact shown on slide26 was built by docs at 61ef06b.',urls=[REPO+'/tree/'+SHA])
    code(s,.82,2.13,5.27,4.56,'src/\n  project.v\n  counter.v\ninfo.yaml\ntest/\n  test.py\n  tb.v\n  Makefile\ndocs/info.md',24)
    pairs=[('Circuit','src/: wrapper + counter RTL'),('Build description','info.yaml: name, sources, clock, tiles'),('Tests','test/: stimulus, checks and instance'),('Datasheet','docs/info.md: behaviour + testing')]
    for i,(head,detail) in enumerate(pairs):
        y=2.23+i*1.06
        text(s,6.65,y,5.70,.52,head,28,TEAL,True)
        text(s,6.65,y+.55,5.72,.77,detail,24)

    # 10 — actual wrapper excerpt beside the port contract.
    s=slide(prs,'Connect the counter to the shared pins','Keep every template port unchanged',3,extra='This visible code is the real wrapper excerpt at 61ef06b. The top name is tt_um_mdkamrulislam_counter. Ports are exactly ui_in, uo_out, uio_in, uio_out, uio_oe, ena, clk and rst_n; do not add ports. Reset is inverted because the underlying counter uses active-high rst.',urls=[REPO+'/blob/'+SHA+'/src/project.v'])
    text(s,.82,2.18,4.06,.72,'The port contract',30,TEAL,True)
    text(s,.82,3.06,4.03,2.55,'8 inputs: ui_in\n8 outputs: uo_out\n8 bidirectional: uio_*\nControl: ena, clk, rst_n',24,spacing=1.40)
    text(s,.82,5.73,4.05,.87,'uio_oe: 0 = input\nuio_oe: 1 = output',24,NAVY,True)
    code(s,5.25,2.12,7.24,3.70,'counter #(.WIDTH(8)) counter_inst (\n  .clk(clk), .rst(~rst_n),\n  .en(ui_in[0]),\n  .count(uo_out),\n  .wrap(uio_out[0])\n);\nassign uio_out[7:1] = 7\'b0;\nassign uio_oe = 8\'b0000_0001;',20)
    text(s,5.29,6.06,7.17,.58,'Same top name in RTL, info.yaml and tb.v.',24,TEAL,True)

    # 11 — continuous counter behaviour, with a real short RTL example.
    s=slide(prs,'Describe what happens on a clock edge','Write the counter; define reset and hold',4,extra='The snippet is an 8-bit teaching form of the existing WIDTH-parameterised counter, with declarations omitted. rst is active high inside the core; the wrapper derives it from ~rst_n. Counting is modulo256. wrap is combinational: high when count255 and en1, before the overflow edge. Formative question answer: count stays7 when en0. Reset wins over enable.',urls=[REPO+'/blob/'+SHA+'/src/counter.v'])
    code(s,.82,2.12,6.57,2.80,'always @(posedge clk) begin\n  if (rst) count <= 8\'b0;\n  else if (en) count <= count + 1\'b1;\nend\nassign wrap = en && (&count);',20)
    text(s,7.94,2.28,4.50,2.72,'rst_n = 0 → 0 at next ↑clk\nEnable = 1 → increment\nEnable = 0 → hold\nwrap = 1 at 255, if enabled',24,spacing=1.40)
    for i,v in enumerate([0,1,2,255,0]):
        x=.83+i*2.49
        counter(s,x,5.19,v,1.73,size=42)
        if i==2: text(s,x+1.84,5.39,.56,.48,'…',32,TEAL,True,align=PP_ALIGN.CENTER)
        elif i<4: arrow(s,x+1.84,5.69,x+2.28,5.69)
    text(s,.84,6.55,11.60,.36,'Try it: count = 7, enable = 0. Next count?  7 — it holds.',24,TEAL,True)

    # 12 — code stimulus and expected result are side by side.
    s=slide(prs,'A test says what should happen','cocotb = Python driving your Verilog simulator',5,extra='The example uses the real test helper step(), which waits for the falling edge, drives inputs, waits for the rising edge, updates the model and samples outputs after8ns. The excerpt is original pedagogical code using this helper. It is not a standalone test file. Run cd test; install the pinned requirements; make -B; python -m cocotb_tools.check_results results.xml. This last check prevents make-success hiding failed tests. Waveform P8 remains pending a real GTKWave/Surfer view.',urls=[REPO+'/blob/'+SHA+'/test/test.py'])
    text(s,.84,2.08,7.20,.36,'Excerpt using step() from the real test',20,TEAL,True)
    code(s,.82,2.55,7.20,2.63,'await step(reset=True)\nawait step(enable=1)\nassert int(dut.uo_out.value) == 1\nawait step(enable=0)\nassert int(dut.uo_out.value) == 1',20)
    text(s,8.60,2.36,3.83,.80,'RESET → 0',30,TEAL,True)
    text(s,8.60,3.39,3.83,.80,'COUNT → 1',30,TEAL,True)
    text(s,8.60,4.42,3.83,.80,'HOLD → 1',30,TEAL,True)
    text(s,.84,5.34,7.26,.38,'Needs Python + make + Icarus Verilog',22,GREY)
    code(s,.82,5.81,7.20,1.10,'cd test && make -B\npython -m cocotb_tools.check_results results.xml',18)
    text(s,8.59,5.62,3.87,1.01,'step() applies inputs\nand samples after the edge.',24)

    # 13 — real passing Actions screenshot, cropped using editable picture fields.
    s=slide(prs,'Push once. Check three green workflows.','A reproducible result on GitHub',6,extra='P3 is captured from the real public Actions list filtered to branch worked-example. It shows docs, test and gds all successful at 61ef06b. The optional fpga workflow has not run. Native PowerPoint crop magnifies the three workflow rows, retaining the real workflow labels and commit; it does not alter the results. Each pass label describes a genuine workflow result.',urls=[REPO+'/actions?query=branch%3Aworked-example'])
    text(s,.84,2.12,11.67,.83,'A commit starts three automated jobs: test checks behaviour,\ngds builds and checks layout, docs writes the datasheet.',24)
    q=picture(s,'counter-actions-green.png',.82,3.37,w=7.25,h=2.35)
    q.crop_left=.225
    q.crop_right=.365
    q.crop_top=.302
    q.crop_bottom=.485
    for i,(name,detail) in enumerate([('docs  PASS','Datasheet generated'),('test  PASS','Reset, count, hold, wrap'),('gds  PASS','All four jobs succeeded')]):
        y=3.37+i*.88
        text(s,8.75,y,3.73,.47,name,28,TEAL,True)
        text(s,8.75,y+.49,3.73,.38,detail,20)
    text(s,.84,6.27,11.67,.45,'Worked example: tt-sky130-counter • commit 61ef06b',24,TEAL,True,link=REPO+'/tree/'+SHA)
    label(s,.84,6.76,'Actual GitHub evidence • fpga is optional and was not run')

    # 14 — large actual layout; cell taxonomy and honest pending captures.
    s=slide(prs,'A layout is geometry, not a photograph','GDS = the file that describes the chip layers',7,extra='All actual counter jobs passed. P5 is a genuine loaded browser 3D viewer capture of the published OAS from run 37693100748. The viewer\'s native Filler cells checkbox is off, so the useful logic is easier to find. The viewer refits the camera when visibility changes: do not use the screenshots as a pixel-area comparison. The original 2D gds_render and full-filler viewer capture remain as source assets. P4 still needs the metrics/cell-table view; the run summary itself has been captured.',urls=[VIEWER,GDS_RUN,'https://gds-viewer.tinytapeout.com/?pdk=sky130A&model=https%3A%2F%2Fmdkamrulislam-web.github.io%2Ftt-sky130-counter%2Ftinytapeout.oas'])
    picture(s,'counter-viewer-no-fill.png',.81,2.08,w=6.53,h=4.49)
    text(s,8.75,2.19,3.83,.64,'Look for three things',28,TEAL,True)
    for i,caption in enumerate(['1  Logic + wiring','2  Warnings + timing','3  Precheck + gl_test']):
        text(s,8.75,3.04+i*.72,3.81,.62,caption,24)
    text(s,8.75,5.34,3.82,.57,'Open the actual viewer ↗',24,TEAL,True,link=VIEWER)
    text(s,8.75,6.06,3.82,.75,'Filler cells hidden.\nP4 metrics capture pending.',20,GREY)

    # 15 — editable synthesis/placement/routing metaphor.
    s=slide(prs,'Tools turn behaviour into cells and wires','Inside the automated gds flow')
    for i,(head,tool) in enumerate([('Map logic','Yosys + ABC'),('Place + route','OpenROAD'),('Check','Timing + DRC + LVS')]):
        x=.83+i*4.17
        text(s,x,2.10,3.74,.58,head,30,TEAL,True)
        text(s,x,5.56,3.78,1.08,tool,26,NAVY,True)
    for x,y,l in [(1.04,3.22,'AND'),(2.61,3.22,'DFF'),(1.82,4.40,'OR')]:
        shape(s,x,y,1.19,.74,NAVY); text(s,x,y+.17,1.19,.43,l,24,PAPER,True,align=PP_ALIGN.CENTER)
    arrow(s,2.27,3.57,2.53,3.57)
    arrow(s,2.97,4.07,2.97,4.35)
    arrow(s,4.01,3.90,4.60,3.90,FIRE,3)
    for r in range(3):
        for c in range(5): shape(s,5.12+c*.62,3.06+r*.68,.48,.45,TEAL if (r+c)%3==0 else PALE)
    for y in [3.57,4.24,4.91]: rule(s,5.06,y,3.11,FIRE)
    arrow(s,8.40,3.90,8.92,3.90,FIRE,3)
    for i,(a,b) in enumerate([('Timing','Before next edge?'),('DRC','Wire spacing okay?'),('LVS','Same connections?')]):
        y=3.05+i*.75
        dot(s,9.08,y+.04,.29,TEAL)
        text(s,9.51,y,2.91,.56,a+'\n'+b,22)

    # 16 — two representations, exactly the same test expectations.
    s=slide(prs,'Check the synthesised circuit too','Run the same functional tests on gates',8,extra='The actual counter RTL and gl_test both passed at61ef06b. Functional gate-level simulation uses PDK cell models and power connections. It does not replace static timing analysis or SDF timing simulation. The statement on the slide distinguishes function from speed without presenting gl_test as timing sign-off.',urls=[REPO+'/blob/'+SHA+'/test/Makefile',GDS_RUN])
    shape(s,.83,3.05,3.24,1.50,NAVY)
    text(s,.99,3.28,2.90,1.04,'One testbench\nSame outputs',26,PAPER,True,align=PP_ALIGN.CENTER)
    arrow(s,4.22,3.49,5.40,2.92)
    arrow(s,4.22,4.08,5.40,4.82)
    text(s,5.60,2.44,6.55,.64,'RTL: your Verilog description',30,TEAL,True)
    text(s,5.60,3.20,6.55,.60,'0 → 1 → hold 1 → reset 0',26)
    text(s,5.60,4.41,6.55,.64,'Gates: the mapped cell netlist',30,TEAL,True)
    text(s,5.60,5.17,6.55,.60,'0 → 1 → hold 1 → reset 0',26)
    strip(s,'In test/: make -B GATES=yes • needs gate_level_netlist.v and PDK_ROOT.',size=22)

    # 17 — one genuine failure, plus a focused debug sequence.
    s=slide(prs,'A real first failure: empty project information','Read the first useful error',extra='The initial template gds run37693066241 genuinely failed because project title, author and description were empty. This is metadata validation, not a failed RTL assertion. The worked-example commit filled these fields and all workflows passed. P6 is optional future assertion-failure evidence; no counter assertion failed. Do not invent a failed test. The contrasting snippets are teaching excerpts of metadata, not screenshots.',urls=[REPO+'/actions/runs/37693066241',REPO+'/blob/'+SHA+'/info.yaml'])
    label(s,.83,2.10,'Before • template defaults',5.44,colour=FIRE)
    code(s,.83,2.64,5.46,1.91,'title: ""\nauthor: ""\ndescription: ""',24)
    label(s,6.80,2.10,'After • describe the counter',5.47)
    code(s,6.80,2.64,5.67,1.91,'title: "8-bit counter"\nauthor: "Your name"\ndescription: "Count, hold, reset"',20)
    text(s,.84,4.69,11.53,.36,'YAML excerpts: these fields belong inside project:',20,GREY)
    text(s,.84,5.14,11.53,.74,'Fix one cause → commit → rerun → read the new result.',30,NAVY,True)
    text(s,.84,5.98,11.53,.78,'Then check: top name • source files • assertions • tile area • timing.\nNo counter assertion failed; this genuine example is a metadata error.',22,GREY)

    # 18 — approved submission is a revision, not the latest uncontrolled push.
    s=slide(prs,'Choose the revision for fabrication','Explained only • no reservation or payment',9)
    seq=[('Sign in','GitHub account'),('Choose shuttle','Correct fab'),('Add repo','Public source'),('Review price','Payment / coupon'),('Submit revision','Verified commit')]
    for i,(a,b) in enumerate(seq):
        x=.83+i*2.50
        dot(s,x,2.30,.54,FIRE)
        text(s,x+.07,2.36,.40,.35,str(i+1),22,PAPER,True,align=PP_ALIGN.CENTER)
        text(s,x,3.12,2.10,1.00,a,28,NAVY,True)
        text(s,x,4.32,2.12,1.20,b,24)
        if i<4: arrow(s,x+.61,2.57,x+2.34,2.57)
    strip(s,'A new GitHub push needs a new submitted revision before the deadline.',size=24)

    # 19 — board diagram + actual counter interaction.
    s=slide(prs,'On the board, test the same behaviour','After fabrication • choose your tile',extra='Begin at a slow clock or single-step while watching count. The current ETR board uses RP2350B; older boards use RP2040. Mode and pin ownership matter when using switches versus controller-driven inputs. A real switch enable needs synchronisation/debounce; the minimal worked example assumes stable synchronous enable.')
    shape(s,.83,2.08,7.03,4.10,PALE)
    shape(s,1.14,2.47,2.54,1.17,NAVY)
    text(s,1.27,2.71,2.28,.71,'Controller',28,PAPER,True,align=PP_ALIGN.CENTER)
    shape(s,4.85,2.47,2.54,1.17,TEAL)
    text(s,4.98,2.71,2.28,.71,'ASIC tile',28,PAPER,True,align=PP_ALIGN.CENTER)
    arrow(s,3.82,3.02,4.70,3.02)
    text(s,1.12,4.11,2.60,.72,'Switch / PMOD\nInputs',24)
    text(s,4.83,4.11,2.60,1.14,'Binary pins\nRead back count',24)
    arrow(s,3.41,4.24,4.76,3.37)
    arrow(s,6.12,3.82,6.12,4.00)
    text(s,1.12,5.31,6.29,.56,'No seven-segment decoder is included.',20,GREY)
    text(s,8.52,2.25,3.96,3.94,'Select your project.\nSet a slow clock.\nrst_n = 0 until ↑clk:\ncount becomes 0.\nEnable: 0 → 1 → 2.\nDisable: count holds.',24,spacing=1.28)
    strip(s,'Synchronous enable assumed: synchronise and debounce a real switch.',size=24)

    # 20 — a checklist tied to an example, rather than six generic cards.
    s=slide(prs,'Show your evidence before a submission review','Your six checkpoints')
    checks=['Behaviour and pins are written down.','RTL, metadata and test setup agree.','Reset, count, hold and wrap tests pass.',
            'test, gds and docs pass at one commit.','Area, timing, warnings and datasheet are reviewed.','Teacher approves shuttle, terms, budget and revision.']
    for i,c in enumerate(checks):
        y=2.06+i*.72
        dot(s,.84,y+.04,.30,TEAL)
        text(s,1.43,y,10.96,.61,c,26)
        if i<5: rule(s,1.43,y+.59,10.92)

    # 21 — a concrete change with predicted output before running tools.
    s=slide(prs,'Lab: make the counter count down','Predict the output before you change the RTL',extra='At reset the8-bit counter is0. A modulo256 count-down counter goes0,255,254 when enabled. Its terminal flag must be defined afresh: the existing wrap indicates count255 with enable1 for count-up. For count-down a logical underflow condition would usually be count0 with enable1. Students must specify and test this choice, not merely swap plus for minus. Expected quiz answer:0−1 modulo256 is255.',urls=[REPO+'/blob/'+SHA+'/src/counter.v',REPO+'/blob/'+SHA+'/test/test.py'])
    label(s,.83,2.15,'Expected count-down sequence')
    for i,v in enumerate([0,255,254]):
        counter(s,.83+i*2.44,2.75,v,1.94,size=44)
        if i<2: arrow(s,2.89+i*2.44,3.25,3.16+i*2.44,3.25)
    code(s,8.50,2.72,3.98,1.40,'count <= count - 1\'b1;',18)
    text(s,.85,4.45,6.78,1.73,'1  Define the new wrap / underflow rule.\n2  Change RTL + expected test values.\n3  Push; compare area and timing.',26,spacing=1.37)
    text(s,8.53,4.62,3.93,1.65,'Unsigned 8-bit count:\nwhat is 0 − 1?\n255 (it wraps).',26,TEAL,True)
    strip(s,'Submit a commit with evidence; no shuttle booking during this exercise.',size=24)

    # 22 — a typography-led reading map, with clickable official links.
    s=slide(prs,'Learn one layer deeper','Official references to keep open')
    resources=[('Start','Templates','https://tinytapeout.com/hdl/templates/'),('Connect','HDL interface rules','https://tinytapeout.com/hdl/important/'),
               ('Verify','Testing guide','https://tinytapeout.com/hdl/testing/'),('Understand','Making ASICs + factory tour','https://tinytapeout.com/making_asics/'),
               ('Check limits','Technical specs','https://tinytapeout.com/specs/'),('Plan','Shuttles + FAQ','https://tinytapeout.com/chips/')]
    for i,(a,b,url) in enumerate(resources):
        y=2.03+i*.74
        text(s,.84,y,2.89,.53,a,26,TEAL,True)
        text(s,4.05,y,8.38,.53,b+' ↗',28,NAVY,link=url)
        rule(s,.84,y+.60,11.64)

    # 23 — clear procurement comparison, no student-confusing commitment.
    s=slide(prs,'Staff: budget projects and shared hardware','Appendix A • starting prices, not a quote')
    for i,(projects,kits,price) in enumerate([('5','1 PCB kit','€565'),('25','3 PCB kits','€2,195'),('75','5 PCB kits','€5,325')]):
        x=.83+i*4.17
        text(s,x,2.16,3.73,1.34,projects,84,TEAL,True,DISPLAY)
        text(s,x,3.55,3.74,.61,'projects, up to',26)
        text(s,x,4.52,3.74,.60,kits,26)
        text(s,x,5.28,3.74,.70,price,38,NAVY,True)
        if i<2: shape(s,x+3.90,2.12,.015,3.91,RULE)
    strip(s,'75 one-tile projects can cover a class of about 70; five kits are shared.',size=24)

    # 24 — pinned template and open deadline are visibly different.
    s=slide(prs,'Staff: a template pin is not an open booking','Appendix B • 7 October 2026 snapshot')
    rows=[('SKY','ttsky26d','30 Nov 2026'),('GF','ttgf26c','7 Dec 2026'),('IHP','ttihp26b','Closed 21 Sep 2026')]
    label(s,.83,2.02,'Template',2.0); label(s,3.31,2.02,'Action pin',4.0); label(s,7.31,2.02,'Submission deadline',5.0)
    for i,(a,b,c) in enumerate(rows):
        y=2.62+i*.94
        text(s,.83,y,2.12,.60,a,30,TEAL,True)
        text(s,3.31,y,3.47,.60,b,28)
        text(s,7.31,y,5.07,.60,c,28,FIRE if i==2 else NAVY)
        rule(s,.83,y+.74,11.66)
    text(s,.84,5.71,11.58,1.10,'Next IHP: March 2027 planned; exact day unpublished.\nEstimated shipping: Q1 2028. Re-check before committing.',26,TEAL,True)

    # 25 — procurement terms are explicit about what has not been verified.
    s=slide(prs,'Staff: verify the exact IHP loan agreement','Appendix C • current shuttle terms still required')
    shape(s,6.60,2.04,.015,4.61,RULE)
    label(s,.83,2.17,'Reported in prior programme material',5.43,colour=FIRE)
    text(s,.83,2.84,5.26,3.31,'IHP retains chip ownership.\nDefault loan: two years.\nNo resale or transfer.\nEU + Switzerland shipping.',26,spacing=1.40)
    label(s,7.12,2.17,'Confirm for the chosen shuttle',5.29)
    text(s,7.12,2.84,5.21,3.49,'Read the current agreement.\nCheck student ownership.\nCheck duration and returns.\nRecord terms before payment.',26,spacing=1.40)
    strip(s,'These historical restrictions need official confirmation for the selected run.',size=22)

    # 26 — evidence already obtained plus an exact list of remaining captures.
    s=slide(prs,'Staff: finish the evidence pack','Appendix D • actual artifacts and remaining captures',extra='P3, P5 and P7 are captured from genuine public CI/browser artifacts. P4 run overview is captured but its metrics/cell table remains pending. The old 150-by-150 µm custom LibreLane render remains in img/counter-sky130-background.png for provenance only and is not used as Tiny Tapeout evidence. Pending P1 requires signed-in template menu; P2 requires repo settings; P4 is the metrics/cell table; P6 is optional future assertion-failure evidence; P8 is the real FST waveform view. README gives exact routes.',urls=[GDS_RUN,REPO+'/actions/runs/37693100755'])
    picture(s,'counter-datasheet-page-1.png',.87,2.01,h=4.71)
    text(s,4.69,2.10,7.70,1.09,'Captured: Actions, datasheet,\nGDS render and real 3D viewer.',26,TEAL,True)
    text(s,4.70,3.41,7.72,2.83,'P1  Signed-in template menu\nP2  Pages source setting\nP4  gds metrics + cell table\nP8  Reset / count / hold / wrap waveform\nP6  Optional future assertion-failure example',24,spacing=1.32)
    text(s,4.70,6.45,7.74,.41,'Capture instructions: docs/slides/README.md',22,GREY)

    output.parent.mkdir(parents=True,exist_ok=True)
    prs.save(output)
    (output.parent/'slide-sources.json').write_text(json.dumps(source_index,indent=2)+'\n',encoding='utf-8')
    print(f'Built {len(prs.slides)} redesigned slides: {output}')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=HERE/'tiny-tapeout-flow-v1.pptx')
    build(p.parse_args().output)
