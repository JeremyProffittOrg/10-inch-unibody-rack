"""Build native Bambu multi-plate project without driving the application UI."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from array import array
import struct,math,json,xml.etree.ElementTree as E
from xml.sax.saxutils import escape

root=Path(__file__).parent
template=Path(r'C:\dev\automatica\cases\ir\concepts\end-window\exports\compact-ir-cases-eight-plates.3mf')
with ZipFile(template) as z:
    profile=z.read('Metadata/project_settings.config')
    settings=json.loads(profile)
assert settings['printer_model']=='Bambu Lab H2D'
validation=json.loads((root/'validation.json').read_text())
py,pz=validation['pivot_yz_mm'];ph=validation['panel_height_mm'];pw=validation['panel_width_mm']
px=(280-pw)/2;axis_y=ph+4
cs=math.cos(math.radians(85));sn=math.sin(math.radians(85))
parts=[('shell','Enclosure frame'),('lcd','LCD mount - face down'),('lid','Removable lid')]
centres=[(175,160),(595,160),(175,-224)]
cfg=E.Element('config');report=[]
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
def meta(parent,key,value):E.SubElement(parent,'metadata',key=key,value=str(value))
def transform(v,name):
    x,y,z=v
    if name=='lcd':
        dy=y-py;dz=z-pz
        return x-px,-(dy*cs+dz*sn+axis_y),-(-dy*sn+dz*cs)
    return v
output=root/'acer-dgx-enclosure-v4-separate-plates.3mf'
with ZipFile(output,'w',ZIP_DEFLATED,compresslevel=5) as archive:
    with archive.open('3D/3dmodel.model','w') as xml:
        def put(s):xml.write(s.encode('utf-8'))
        put(f'<?xml version="1.0" encoding="UTF-8"?><model xmlns="{ns}" xml:lang="en-US" unit="millimeter">')
        put('<metadata name="Application">BambuStudio-02.00.02.01</metadata><metadata name="BambuStudio:3mfVersion">1</metadata>')
        put('<metadata name="Title">Acer enclosure v4 - separate plates</metadata><metadata name="Description">Unsliced layout: enclosure frame, LCD mount, and lid on separate H2D plates.</metadata><resources>')
        for idx,(name,label) in enumerate(parts,1):
            data=(root/(name+'.stl')).read_bytes();count=struct.unpack_from('<I',data,80)[0]
            assert len(data)==84+50*count
            unique={};verts=[];tris=array('I')
            for row in struct.iter_unpack('<12fH',data[84:]):
                for v in [row[3:6],row[6:9],row[9:12]]:
                    found=unique.get(v)
                    if found is None:
                        found=len(verts);unique[v]=found;verts.append(transform(v,name))
                    tris.append(found)
            lo=[min(v[a] for v in verts) for a in range(3)];hi=[max(v[a] for v in verts) for a in range(3)]
            shift=[-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]]
            size=[hi[a]-lo[a] for a in range(3)]
            assert size[0]<325 and size[1]<320 and size[2]<320,(name,size)
            put(f'<object id="{idx}" name="{escape(label)}" type="model"><mesh><vertices>')
            for start in range(0,len(verts),5000):
                put(''.join('<vertex x="%.7f" y="%.7f" z="%.7f"/>'%(v[0]+shift[0],v[1]+shift[1],v[2]+shift[2]) for v in verts[start:start+5000]))
            put('</vertices><triangles>')
            for start in range(0,len(tris),15000):
                put(''.join(f'<triangle v1="{tris[j]}" v2="{tris[j+1]}" v3="{tris[j+2]}"/>' for j in range(start,min(start+15000,len(tris)),3)))
            put('</triangles></mesh></object>')
            obj=E.SubElement(cfg,'object',id=str(idx));meta(obj,'name',label);meta(obj,'extruder','1')
            E.SubElement(obj,'metadata',face_count=str(count))
            part=E.SubElement(obj,'part',id=str(idx),subtype='normal_part');meta(part,'name',label);meta(part,'source_file',name+'.stl')
            E.SubElement(part,'mesh_stat',face_count=str(count),edges_fixed='0',degenerate_facets='0',facets_removed='0',facets_reversed='0',backwards_edges='0')
            plate=E.SubElement(cfg,'plate');meta(plate,'plater_id',idx);meta(plate,'plater_name',label);meta(plate,'locked','false')
            inst=E.SubElement(plate,'model_instance');meta(inst,'object_id',idx);meta(inst,'instance_id',0);meta(inst,'identify_id',idx)
            report.append({'plate':idx,'part':name,'size_mm':size,'centre_xy':centres[idx-1],'bed_z':0,'triangles':count})
            print(report[-1],flush=True)
        put('</resources><build>')
        for idx,(x,y) in enumerate(centres,1):put(f'<item objectid="{idx}" transform="1 0 0 0 1 0 0 0 1 {x} {y} 0" printable="1"/>')
        put('</build></model>')
    archive.writestr('Metadata/model_settings.config',E.tostring(cfg,encoding='utf-8',xml_declaration=True))
    archive.writestr('Metadata/project_settings.config',profile)
    archive.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/><Default Extension="config" ContentType="application/octet-stream"/></Types>')
    archive.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
with ZipFile(output) as archive:
    assert archive.testzip() is None
    metadata=E.fromstring(archive.read('Metadata/model_settings.config'))
    assert len(metadata.findall('plate'))==3
    assert [p.find('model_instance/metadata').get('value') for p in metadata.findall('plate')]==['1','2','3']
(root/'plate-layout.json').write_text(json.dumps(report,indent=2))
print('Three-plate project validated:',output,flush=True)
