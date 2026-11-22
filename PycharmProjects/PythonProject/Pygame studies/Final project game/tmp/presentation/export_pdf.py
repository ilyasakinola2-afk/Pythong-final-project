import io
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader

root = Path(__file__).resolve().parents[2]
deck = json.loads((root / 'tmp/presentation/deck-export.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
images = {i['id']: ImageReader(io.BytesIO(bytes(i['data']))) for i in deck['images']}
dest = root / 'output/presentation/Tank_Shooters.pdf'
c = canvas.Canvas(str(dest), pagesize=(960, 540))
c.setTitle('Tank Shooters - Pygame Final Project')
c.setAuthor('Ilyas Akinola')
for slide in deck['slides']:
    width = slide['widthEmu'] / 12700
    height = slide['heightEmu'] / 12700
    c.setPageSize((width, height))
    c.setFillColor(HexColor('#' + slide['background']['fill']['color']['value']))
    c.rect(0, 0, width, height, stroke=0, fill=1)
    for e in slide['elements']:
        b = e['bbox']
        x, top, w, h = [b[k] / 12700 for k in ('xEmu', 'yEmu', 'widthEmu', 'heightEmu')]
        if e.get('imageReference'):
            c.saveState()
            c.translate(x+w/2, height-top-h/2)
            c.rotate(-b.get('rotation', 0)/60000)
            c.drawImage(images[e['imageReference']['id']], -w/2, -h/2, width=w, height=h, mask='auto')
            c.restoreState()
            continue
        style = e.get('textStyle', {})
        font = 'Arial-Bold' if style.get('bold') else 'Arial'
        size = style.get('fontSize', 1800) / 100
        c.setFont(font, size)
        c.setFillColor(HexColor('#' + style['fill']['color']['value']))
        lines = []
        for para in e.get('paragraphs', []):
            lines.extend(''.join(r.get('text', '') for r in para.get('runs', [])).split('\n'))
        y = height-top-size
        for line in lines:
            if style.get('alignment') == 2:
                c.drawCentredString(x+w/2, y, line)
            else:
                c.drawString(x, y, line)
            y -= size*1.2
    c.showPage()
c.save()
reader = PdfReader(str(dest))
assert len(reader.pages) == 6
print(f'Created {dest} with {len(reader.pages)} pages.')
for i,p in enumerate(reader.pages,1):
    print(i, p.extract_text()[:100].replace('\n',' / '))
