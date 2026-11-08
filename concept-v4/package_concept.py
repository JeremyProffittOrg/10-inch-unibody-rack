"""Package OpenSCAD STL parts as one assembly, preserving positions and names."""
from pathlib import Path
import struct, zipfile, xml.etree.ElementTree as E
root=Path(__file__).parent
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
E.register_namespace('',ns)
def el(tag, **attrs): return E.Element('{'+ns+'}'+tag,{k:str(v) for k,v in attrs.items()})
model=el('model',unit='millimeter'); resources=el('resources'); model.append(resources)
names=['Shorter shell - 3 Acer fans plus brick fan','Rounded ventilated lid','Extended articulating LCD panel - 10mm perimeter clearance']
files=['shell','lid','lcd']
materials=el('basematerials',id=10)
for name,color in zip(names,['#667D8AFF','#F3A438FF','#AAB3BDFF','#354451FF']): materials.append(el('base',name=name,displaycolor=color))
resources.append(materials)
for idx,name in enumerate(names,1):
 data=(root/(files[idx-1]+'.stl')).read_bytes(); verts=[]
 if data[:5]==b'solid':
  for line in data.decode().splitlines():
   if line.strip().startswith('vertex '): verts.append(tuple(map(float,line.split()[1:])))
 else:
  count=struct.unpack_from('<I',data,80)[0]
  for t in range(count):
   vals=struct.unpack_from('<12fH',data,84+50*t)
   verts.extend([vals[3:6],vals[6:9],vals[9:12]])
 assert verts and len(verts)%3==0
 obj=el('object',id=idx,type='model',name=name,pid=10,pindex=idx-1)
 mesh=el('mesh'); vs=el('vertices'); ts=el('triangles'); unique={}; triangles=[]
 for v in verts:
  if v not in unique: unique[v]=len(unique); vs.append(el('vertex',x=v[0],y=v[1],z=v[2]))
  triangles.append(unique[v])
 for t in range(0,len(triangles),3): ts.append(el('triangle',v1=triangles[t],v2=triangles[t+1],v4=triangles[t+2]))
 mesh.extend([vs,ts]);obj.append(mesh);resources.append(obj)
 print(name,len(unique),'vertices',len(triangles)//3,'triangles', 'bounds',[(min(v[i] for v in unique),max(v[i] for v in unique)) for i in range(3)])
assembly=el('object',id=5,type='model',name='ACER V4 - ASSEMBLED REVIEW - NOT PRINT LAYOUT')
components=el('components')
for i in range(1,4): components.append(el('component',objectid=i))
assembly.append(components);resources.append(assembly)
build=el('build');build.append(el('item',objectid=5));model.append(build)
with zipfile.ZipFile(root/'acer-dgx-enclosure-v4.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True))
 z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
