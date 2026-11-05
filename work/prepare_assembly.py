from pathlib import Path
import hashlib,json,re
from PIL import Image,ImageOps,ImageDraw
R=Path(__file__).resolve().parent.parent
b=R/'work/src-20261105-assembly-ch8'
pdf=R/'raw/pdfs/1151 ch8.pdf'
sid='src-20261105-assembly-ch8'
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
meta=dict(source_id=sid,imported='2026-11-05',original_path='C:/Users/miu99/Downloads/1151 ch8.pdf',source_file='raw/pdfs/1151 ch8.pdf',sha256=sha,pages=51,title='Chapter 8: Advanced Procedures',authors=['Kip R. Irvine'],published=None,book_edition_year=2015,pdf_created='2023-10-31',version='7th Edition, Global Edition; mixed 5/e slides and course exercises',course='組合語言',unit='第八章',extraction='pypdf text; Poppler rendered all pages; visual review recorded separately')
(R/'raw/metadata'/f'{sid}.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
assets=R/'website/assets/assembly-ch8';assets.mkdir(parents=True,exist_ok=True)
imgs=sorted(b.glob('page-*.png'))
for i,p in enumerate(imgs,1):
    if i!=1: Image.open(p).convert('RGB').save(assets/f'{i:03}.webp',quality=88)
for start in range(0,len(imgs),9):
    sheet=Image.new('RGB',(1500,930),'#dddddd');draw=ImageDraw.Draw(sheet)
    for j,p in enumerate(imgs[start:start+9]):
        im=Image.open(p).convert('RGB');im.thumbnail((490,275))
        x=(j%3)*500;y=(j//3)*310
        sheet.paste(im,(x,y+25));draw.text((x+8,y+5),f'PDF p. {start+j+1}',fill='black')
    sheet.save(b/f'contact-{start+1:02}.jpg')
print('saved',len(imgs),'pages; SHA256',sha)
