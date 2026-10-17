"""Extract traceable source images. Input directory holds user's original PDFs."""
import fitz,hashlib,json,sys,pathlib
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[2]
dest=root/'docs/component_atlas_v001/assets/sources';dest.mkdir(parents=True,exist_ok=True)
inp=pathlib.Path(sys.argv[1]);manifest=[]
pages={'A1':sorted(set([49,50,51,58,60,62,64,67,70,71,72,73,77,81,82,83,84,85,86,87,88,89,90,91,93,94,95,96,97,98,99,100,104,106,109,110,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,336,344,345])),
       'A2':[10,24,28,31,36,39,41,44,46,49,50,56],
       'A3':[1,3,7,8,9,10]}
rotated={283,284,285,286,287,288,291,292,293,294,299,300,301}
for name,ns in pages.items():
    source=inp/(name+'.pdf');d=fitz.open(source);sha=hashlib.sha256(source.read_bytes()).hexdigest()
    for n in ns:
        p=d[n-1];scale=2000/p.rect.width
        pix=p.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False)
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        rotation=90 if name=='A1' and n in rotated else 0
        if rotation:im=im.rotate(-90,expand=True)
        file=f'{name}-p{n:03}.jpg';im.save(dest/file,quality=88,optimize=True)
        manifest.append(dict(file=file,source=name,pdf_page=n,printed_page=n-15 if name=='A1' else None,source_sha256=sha,rotation_clockwise_deg=rotation,operation='FULL_PAGE_RASTER_NO_GEOMETRY_REDRAW',sha256=hashlib.sha256((dest/file).read_bytes()).hexdigest()))
    # Photo-only crops use original page rectangles; no invented outlines.
    if name=='A1':
        crops={
          'beam-six':(82,(.17,.55,.87,.85)), 'beam-upper':(82,(.17,.05,.87,.34)),
          'pingliang':(83,(.16,.68,.87,.91)), 'rufu':(84,(.16,.05,.88,.36)),
          'lane':(87,(.15,.41,.88,.67)), 'youe':(88,(.15,.40,.88,.71)),
          'tuojiao':(90,(.16,.54,.9,.81)), 'chashou':(83,(.16,.68,.87,.91)),
          'purlin':(97,(.15,.06,.89,.45)), 'corner':(98,(.15,.58,.87,.86)),
          'roof':(99,(.15,.63,.89,.90)), 'floor':(133,(.15,.67,.89,.91)),
          'platform':(132,(.55,.69,.91,.91)), 'wall':(136,(.14,.08,.9,.34)),
          'door':(136,(.14,.08,.9,.34)), 'window':(136,(.14,.08,.9,.34)),
          'vent':(137,(.13,.64,.9,.9)), 'chiwen':(140,(.14,.09,.9,.43)),
          'chuishou':(141,(.14,.09,.9,.39)), 'ridge-corner':(142,(.14,.16,.89,.47)),
          'figure':(143,(.14,.47,.91,.89)), 'taoshou':(144,(.14,.09,.9,.44)),
          'eave-tile':(144,(.14,.56,.92,.83)), 'huagong':(73,(.14,.08,.9,.36)),
          'dou':(70,(.16,.04,.89,.33)), 'inner':(94,(.14,.25,.89,.58))}
        for key,(n,box) in crops.items():
            p=d[n-1];r=p.rect;clip=fitz.Rect(box[0]*r.width,box[1]*r.height,box[2]*r.width,box[3]*r.height)
            pix=p.get_pixmap(matrix=fitz.Matrix(2.7,2.7),clip=clip,alpha=False)
            im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);file='A1-crop-'+key+'.jpg';im.save(dest/file,quality=91,optimize=True)
            manifest.append(dict(file=file,source=name,pdf_page=n,printed_page=n-15,source_sha256=sha,normalized_crop=list(box),operation='RECTANGLE_CROP_NO_REDRAW',sha256=hashlib.sha256((dest/file).read_bytes()).hexdigest()))
(dest/'SOURCE_IMAGE_PROVENANCE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(len(manifest),'source images extracted')
