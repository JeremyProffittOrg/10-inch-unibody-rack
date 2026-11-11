// Native Bambu three-plate package using only Node standard-library file tools.
const fs=require('fs'),path=require('path'),zlib=require('zlib');
const root=__dirname;
const table=new Uint32Array(256);
for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=(c&1)?0xedb88320^(c>>>1):c>>>1;table[n]=c>>>0;}
function crc(data){let c=0xffffffff;for(const b of data)c=table[(c^b)&255]^(c>>>8);return (c^0xffffffff)>>>0;}
function readZip(file,name){
 const b=fs.readFileSync(file);let e=b.length-22;while(e>=0&&b.readUInt32LE(e)!==0x06054b50)e--;
 if(e<0)throw Error('Invalid ZIP');let p=b.readUInt32LE(e+16);
 for(let i=0;i<b.readUInt16LE(e+10);i++){
  if(b.readUInt32LE(p)!==0x02014b50)throw Error('Invalid directory');
  const nl=b.readUInt16LE(p+28),el=b.readUInt16LE(p+30),cl=b.readUInt16LE(p+32);
  if(b.toString('utf8',p+46,p+46+nl)===name){
   const off=b.readUInt32LE(p+42),start=off+30+b.readUInt16LE(off+26)+b.readUInt16LE(off+28);
   const raw=b.subarray(start,start+b.readUInt32LE(p+20));
   const out=b.readUInt16LE(p+10)===8?zlib.inflateRawSync(raw):Buffer.from(raw);
   if(crc(out)!==b.readUInt32LE(p+16))throw Error('CRC mismatch');return out;
  }p+=46+nl+el+cl;
 }throw Error('Missing member '+name);
}
function writeZip(file,entries){
 const fd=fs.openSync(file,'w'),central=[];let offset=0;
 for(const [name,value] of entries){
  const raw=Buffer.isBuffer(value)?value:Buffer.from(value),packed=zlib.deflateRawSync(raw,{level:5});
  const nb=Buffer.from(name),sum=crc(raw),h=Buffer.alloc(30);
  h.writeUInt32LE(0x04034b50,0);h.writeUInt16LE(20,4);h.writeUInt16LE(2048,6);h.writeUInt16LE(8,8);
  h.writeUInt32LE(sum,14);h.writeUInt32LE(packed.length,18);h.writeUInt32LE(raw.length,22);h.writeUInt16LE(nb.length,26);
  fs.writeSync(fd,h);fs.writeSync(fd,nb);fs.writeSync(fd,packed);
  const c=Buffer.alloc(46);c.writeUInt32LE(0x02014b50,0);c.writeUInt16LE(20,4);c.writeUInt16LE(20,6);c.writeUInt16LE(2048,8);c.writeUInt16LE(8,10);
  c.writeUInt32LE(sum,16);c.writeUInt32LE(packed.length,20);c.writeUInt32LE(raw.length,24);c.writeUInt16LE(nb.length,28);c.writeUInt32LE(offset,42);
  central.push(c,nb);offset+=30+nb.length+packed.length;
 }
 const directory=Buffer.concat(central);fs.writeSync(fd,directory);
 const end=Buffer.alloc(22);end.writeUInt32LE(0x06054b50,0);end.writeUInt16LE(entries.length,8);end.writeUInt16LE(entries.length,10);end.writeUInt32LE(directory.length,12);end.writeUInt32LE(offset,16);
 fs.writeSync(fd,end);fs.closeSync(fd);
}
const profile=fs.readFileSync(path.join(root,'../cad-config/h2d-project-settings.json'));
const validation=JSON.parse(fs.readFileSync(path.join(root,'validation.json')));
if(!validation.top_integral)throw Error('Wrong revision');


const parts=[['shell','Bowed enclosure - power below DGX'],['lcd','Four-screw LCD panel - 5 mm intake gap'],['fan-plate','Internal removable five-fan plate']];
const centres=[[175,160],[595,160],[175,-224]],records=[];
const xml=['<?xml version="1.0" encoding="UTF-8"?><model xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xml:lang="en-US" unit="millimeter"><metadata name="Application">BambuStudio-02.00.02.01</metadata><metadata name="BambuStudio:3mfVersion">1</metadata><metadata name="Title">Acer enclosure v10b - separate plates</metadata><resources>'];
const config=['<?xml version="1.0" encoding="UTF-8"?><config>'];
for(let part=0;part<parts.length;part++){
 const [name,label]=parts[part],id=part+1,data=fs.readFileSync(path.join(root,name+'.stl')),count=data.readUInt32LE(80);
 if(data.length!==84+50*count)throw Error('Bad STL');
 const unique=new Map(),verts=[],tri=new Uint32Array(count*3),lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
 for(let i=0;i<count;i++)for(let j=0;j<3;j++){
  const at=84+i*50+12+j*12,v=[data.readFloatLE(at),data.readFloatLE(at+4),data.readFloatLE(at+8)],key=v.join(',');
  let index=unique.get(key);
  if(index===undefined){
   index=verts.length;unique.set(key,index);

   if(name==='fan-plate'||name==='lcd'){const oldY=v[1];v[1]=-v[2];v[2]=oldY;}
   for(let k=0;k<3;k++){lo[k]=Math.min(lo[k],v[k]);hi[k]=Math.max(hi[k],v[k]);}verts.push(v);
  }tri[i*3+j]=index;
 }
 const size=hi.map((n,i)=>n-lo[i]),shift=[-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]];
 if(size[0]>=325||size[1]>=320||size[2]>=320)throw Error('Plate bounds exceeded');
 xml.push(`<object id="${id}" name="${label}" type="model"><mesh><vertices>`);
 for(const v of verts)xml.push(`<vertex x="${(v[0]+shift[0]).toFixed(7)}" y="${(v[1]+shift[1]).toFixed(7)}" z="${(v[2]+shift[2]).toFixed(7)}"/>`);
 xml.push('</vertices><triangles>');
 for(let i=0;i<tri.length;i+=3)xml.push(`<triangle v1="${tri[i]}" v2="${tri[i+1]}" v3="${tri[i+2]}"/>`);
 xml.push('</triangles></mesh></object>');
 config.push(`<object id="${id}"><metadata key="name" value="${label}"/><metadata key="extruder" value="1"/><metadata face_count="${count}"/><part id="${id}" subtype="normal_part"><metadata key="name" value="${label}"/><metadata key="source_file" value="${name}.stl"/><mesh_stat face_count="${count}" edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/></part></object><plate><metadata key="plater_id" value="${id}"/><metadata key="plater_name" value="${label}"/><metadata key="locked" value="false"/><model_instance><metadata key="object_id" value="${id}"/><metadata key="instance_id" value="0"/><metadata key="identify_id" value="${id}"/></model_instance></plate>`);
 records.push({plate:id,part:name,size_mm:size,centre_xy:centres[part],bed_z:0,triangles:count});console.log(records.at(-1));
}
xml.push('</resources><build>');centres.forEach(([x,y],i)=>xml.push(`<item objectid="${i+1}" transform="1 0 0 0 1 0 0 0 1 ${x} ${y} 0" printable="1"/>`));xml.push('</build></model>');config.push('</config>');
const out=path.join(root,'acer-dgx-enclosure-v10b-separate-plates.3mf');
writeZip(out,[['3D/3dmodel.model',xml.join('')],['Metadata/model_settings.config',config.join('')],['Metadata/project_settings.config',profile],['[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/><Default Extension="config" ContentType="application/octet-stream"/></Types>'],['_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>']]);
const verified=readZip(out,'Metadata/model_settings.config').toString();if((verified.match(/<plate>/g)||[]).length!==3)throw Error('Plate count mismatch');
readZip(out,'3D/3dmodel.model');fs.writeFileSync(path.join(root,'plate-layout.json'),JSON.stringify(records,null,2));console.log('Three-plate project validated:',out);
