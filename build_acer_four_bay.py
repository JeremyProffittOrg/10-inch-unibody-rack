"""Build, check and diagram the four-bay Acer shelves. Requires matplotlib."""
from pathlib import Path
import collections, json, math, os, struct, subprocess, sys
# Small geometric checks do not need a machine-wide BLAS thread pool.
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'/'acer-four-bay'
OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'acer-four-bay-shelves.scad'
OPENSCAD=Path('C:/Program Files/OpenSCAD/openscad.com') if os.name=='nt' else Path('openscad')
FLAGS=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0

def command(args,name):
    args=list(args);final_image=None
    if '-o' in args:
        index=args.index('-o')+1
        if str(args[index]).endswith('.png'):
            final_image=Path(args[index]);args[index]=final_image.with_name(final_image.stem+'-writing.png')
    result=subprocess.run([str(OPENSCAD),*map(str,args)],cwd=ROOT,text=True,capture_output=True,timeout=600,creationflags=FLAGS)
    (OUT/(name+'.log')).write_text(result.stdout+result.stderr,encoding='utf8')
    if result.returncode or 'ERROR:' in result.stderr:
        raise RuntimeError(name+': '+result.stdout+result.stderr)
    if final_image is not None:os.replace(args[index],final_image)
    return result.stdout+result.stderr

print('Building one-piece shelf assembly',flush=True)
stl=OUT/'acer-four-bay-shelves.stl'
log=command(['--export-format','binstl','-o',stl,SOURCE],'build')
metadata={}
for line in log.splitlines():
    if line.startswith('ECHO: ['):
        record=json.loads(line[6:]);metadata[record[0]]=record[1:]
W,H,D,pitch,gap=metadata['dimensions']
pw,pd,ph,dw,dd,dh,px,dx,front=metadata['devices']
gh,gt,fit,corner,cz,cw,cpw,cd=metadata['features']
fc,fy,fd,fp,sd,fm=metadata['fans']
assert abs(H-315)<1e-5 and abs(gap-22)<1e-5
assert abs(D-(front+dd+76.2))<1e-5
assert H<=325 and W<=320 and D<=325
assert front+pd+fit+gt+gh < cz-cd/2

# Independently validate the exported mesh, not only source assertions.
print('Checking STL manifold, component count and printer bounds',flush=True)
data=stl.read_bytes();count=struct.unpack_from('<I',data,80)[0]
assert len(data)==84+50*count
edges=collections.Counter();balance=collections.Counter();parents={}
lo=[float('inf')]*3;hi=[-float('inf')]*3;volume=0

def find(v):
    parents.setdefault(v,v)
    while parents[v]!=v:
        parents[v]=parents[parents[v]];v=parents[v]
    return v

def union(a,b):
    a,b=find(a),find(b)
    if a!=b:parents[a]=b

for i in range(count):
    pts=[struct.unpack_from('<fff',data,84+50*i+12+12*j) for j in range(3)]
    verts=[tuple(p) for p in pts]
    assert len(set(verts))==3,'Degenerate triangle'
    for p in pts:
        for j in range(3):lo[j]=min(lo[j],p[j]);hi[j]=max(hi[j],p[j])
    for a,b in zip(verts,verts[1:]+verts[:1]):
        key=tuple(sorted((a,b)));edges[key]+=1;balance[key]+=1 if a<b else -1;union(a,b)
    a,b,c=pts
    volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
assert all(n==2 for n in edges.values()),'Open/nonmanifold mesh edges'
assert all(n==0 for n in balance.values()),'Inconsistent face winding'
assert len({find(v) for v in parents})==1,'Disconnected geometry'
assert volume>0,'Inverted solid'
for measured,expected in zip([hi[i]-lo[i] for i in range(3)],[H,W,D]):assert abs(measured-expected)<.01
assert min(lo)>-.01
# Triangle/box separating-axis checks use the actual exported STL in use coordinates.
import numpy as np
raw=np.array([[struct.unpack_from('<fff',data,84+50*i+12+12*j) for j in range(3)] for i in range(count)])
tri=np.stack((raw[:,:,1],raw[:,:,0],D-raw[:,:,2]),axis=2)
def clear_box(low,high,label):
    centre=(np.array(low)+np.array(high))/2;half=(np.array(high)-np.array(low))/2
    v=tri-centre
    active=np.all(np.min(v,axis=1)<=half,axis=1)&np.all(np.max(v,axis=1)>=-half,axis=1)
    edges=[v[:,1]-v[:,0],v[:,2]-v[:,1],v[:,0]-v[:,2]]
    axes=[np.cross(edges[0],edges[1])]+[np.cross(e,b) for e in edges for b in np.eye(3)]
    for axis in axes:
        proj=np.einsum('nij,nj->ni',v,axis);radius=np.abs(axis)@half
        active &= (np.min(proj,axis=1)<=radius+1e-8)&(np.max(proj,axis=1)>=-radius-1e-8)
    assert not np.any(active),label+' intersects printed geometry'
for bay in range(4):
    base=5+bay*pitch
    for x,w,d,h,label in [(px,pw,pd,ph,'PSU'),(dx,dw,dd,dh,'DGX')]:
        clear_box([x+.05,base+.05,front+.05],[x+w-.05,base+h-.05,front+d-.05],label+' seated')
        lift=gh+fit
        clear_box([x+.05,base+lift+.05,-d],[x+w-.05,base+lift+h-.05,front+d-.05],label+' front insertion path')
clear_box([dx+dw/2-9,-1,cz-9],[dx+dw/2+9,H+1,cz+9],'DGX vertical cable path')
clear_box([px+pw/2-7,-1,cz-9],[px+pw/2+7,H+1,cz+9],'PSU vertical cable path')
print('PASS: eight nominal device fits, eight lifted insertion paths, two full-height cable paths',flush=True)

report={'device_fit_and_insertion_paths':True,'vertical_cable_paths':True,'passed':True,'triangle_count':count,'closed_manifold':True,'connected_components':1,'positive_volume_mm3':volume,'print_bounds_mm':[H,W,D],'assembly_bounds_mm':[W,H,D],'shelves':5,'retaining_pockets':8,'fan_mounts':12,'screw_holes':48,'cable_passages':10,'top_air_gap_mm':gap,'rear_extension_mm':76.2,'psu_model':'Delta ADP-240KB BA','psu_body_wdh_mm':[pw,pd,ph],'acer_oem_match':'UNCONFIRMED','support_free':'designed for rear-down print; slicer and physical test not yet performed','metadata':metadata}
(OUT/'validation.json').write_text(json.dumps(report,indent=2))

ink='#0f172a';steel='#64748b';blue='#0369a1';gold='#fcd34d'
def axes(title,xlim,ylim,size=(12,10)):
    fig,ax=plt.subplots(figsize=size,facecolor='white');fig.subplots_adjust(left=.08,right=.94,top=.86,bottom=.17)
    ax.set_aspect('equal');ax.set_xlim(*xlim);ax.set_ylim(*ylim);ax.axis('off')
    fig.suptitle(title,fontsize=19,weight='bold',x=.08,ha='left',y=.96,color=ink)
    return fig,ax

def dim(ax,a,b,label,offset=(0,0)):
    ax.annotate('',xy=a,xytext=b,arrowprops=dict(arrowstyle='<->',color=ink,lw=1))
    ax.text((a[0]+b[0])/2+offset[0],(a[1]+b[1])/2+offset[1],label,ha='center',va='center',fontsize=10,color=ink)

def save(fig,name,notes):
    for i,note in enumerate(notes):fig.text(.08,.115-i*.028,note,fontsize=10,color=ink)
    temporary=OUT/(name+'-writing.png')
    fig.savefig(temporary,dpi=170,facecolor='white');plt.close(fig)
    os.replace(temporary,OUT/(name+'.png'))

def frame(ax):
    for x in [0,W-5]:ax.add_patch(Rectangle((x,0),5,H,facecolor=steel))
    for i in range(5):ax.add_patch(Rectangle((0,i*pitch),W,5,facecolor=steel))

fig,ax=axes('Four Acer bays — front layout',(-25,W+25),(-10,H+25))
frame(ax)
for i in range(4):
    y=5+i*pitch
    for x,w,h,label,col in [(px,pw,ph,'PSU '+str(i+1),gold),(dx,dw,dh,'DGX '+str(i+1),'#cbd5e1')]:
        ax.add_patch(Rectangle((x,y),w,h,facecolor=col,edgecolor=ink))
        ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=11)
        for gx in [x-fit-gt,x+w+fit]:ax.add_patch(Rectangle((gx,y),gt,gh,facecolor='#0f766e'))
    ax.text(dx+dw/2,y+dh+gap/2,'22 mm above DGX',ha='center',va='center',fontsize=10,color=blue)
dim(ax,(0,H+12),(W,H+12),f'{W:g} mm wide',(0,6))
ax.text(-13,H/2,'315 mm high',rotation=90,va='center',ha='center')
save(fig,'front-layout',['Five 5 mm shelves; 5 mm outer walls; 22 mm device-to-wall and device-to-device spacing.',f'PSU envelope {pw:g} W × {pd:g} D × {ph:g} H mm: Delta ADP-240KB BA. Acer label match unconfirmed.','Green: 10 mm guides. Guide thickness and fitting clearance occupy part of each 22 mm side gap.'])

fig,ax=axes('Shelf plan — retainers, rear extension and cable passages',(-20,W+35),(-25,D+35))
ax.add_patch(Rectangle((0,0),W,D,facecolor='#e2e8f0',edgecolor=ink))
for x in [0,W-5]:ax.add_patch(Rectangle((x,0),5,D,facecolor=steel))
for x,w,d,label,col in [(px,pw,pd,'ACER PSU',gold),(dx,dw,dd,'DGX','#cbd5e1')]:
    ax.add_patch(Rectangle((x,front),w,d,facecolor=col,alpha=.6,edgecolor=ink,linestyle='--'))
    ax.text(x+w/2,front+d/2,label,ha='center',fontsize=11)
    back=front+d+fit
    for gx in [x-fit-gt,x+w+fit]:
        ax.add_patch(Rectangle((gx,0),gt,back+gt,facecolor='#0f766e'))
        ax.add_patch(Rectangle((gx,back+gt),gt,gh,facecolor='#99f6e4'))
    for ex in [x-fit,x+w-corner]:
        ax.add_patch(Rectangle((ex,0),corner+fit,gt,facecolor='#0f766e'))
        ax.add_patch(Rectangle((ex,back),corner+fit,gt,facecolor='#0f766e'))
        ax.add_patch(Rectangle((ex,back+gt),corner+fit,gh,facecolor='#99f6e4'))
for x,w in [(px+pw/2,cpw),(dx+dw/2,cw)]:
    ax.add_patch(Polygon([(x,cz-cd/2),(x+w/2,cz),(x,cz+cd/2),(x-w/2,cz)],facecolor='white',edgecolor=blue,lw=2))
    ax.text(x,cz,f'{w:g} × {cd:g}',ha='center',va='center',fontsize=9,color=blue)
for cx in fc:ax.add_patch(Rectangle((cx-fm/2,D-5),fm,5,facecolor=ink))
ax.axhline(D-50.8,color=blue,linestyle='--',lw=1)
ax.text(7,D-50.8+3,'Last 50.8 mm: cable zone',fontsize=9,color=blue)
dim(ax,(W+12,front+dd),(W+12,D),'76.2 mm',(0,0))
ax.text(W/2,-12,'FRONT — lift device over corner lips, then lower into guides',ha='center',fontsize=9)
ax.text(W/2,D+17,'REAR — three fan mounts; remaining rear is open',ha='center',fontsize=10)
save(fig,'shelf-plan',[f'Shelf depth {D:g} mm; exactly 76.2 mm (3 inches) beyond the DGX rear.',f'Two passages per shelf: {cw:g} × {cd:g} mm behind DGX; {cpw:g} × {cd:g} mm behind PSU (maximum diamond spans).','Dark green: retainers; pale green: 45° rear support ramps. White diamonds: through-holes.'])

fig,ax=axes('Rear layout — twelve 40 mm fan mounts',(-20,W+20),(-5,H+20))
frame(ax)
for i in range(4):
    y=5+i*pitch
    for j,cx in enumerate(fc):
        cy=y+fy
        for x in [cx-fm/2,cx+fm/2-3]:ax.add_patch(Rectangle((x,y),3,pitch-5,facecolor=steel))
        ax.add_patch(Rectangle((cx-fm/2,cy-fm/2),fm,fm,facecolor=steel,edgecolor=ink))
        ax.add_patch(Rectangle((cx-20,cy-20),40,40,fill=False,edgecolor='#fbbf24',linestyle='--'))
        ax.add_patch(Circle((cx,cy),fd/2,facecolor='white',edgecolor=ink))
        for xx in [-fp/2,fp/2]:
            for yy in [-fp/2,fp/2]:ax.add_patch(Circle((cx+xx,cy+yy),sd/2,facecolor='white'))
        ax.text(cx,cy,'PSU' if j==0 else 'DGX',ha='center',va='center',fontsize=8)
ax.text(W/2,H+10,'White areas around mounts stay open for rear cables',ha='center',fontsize=10,color=blue)
save(fig,'rear-fans',['Three fans per bay: two centred as a pair behind DGX, one centred behind PSU.',f'40 × 40 mm fan outline; {fd:g} mm airflow opening; {fp:g} mm screw pitch; {sd:g} mm M3 holes.', 'Fans attach outside the rear. Hardware depth and cable bend radius add to the printed dimensions.'])

fig,ax=axes('Retainer detail — 10 mm guides and 5 mm corner returns',(-15,190),(-20,185),(11,10))
x=15;w=150;d=150
ax.add_patch(Rectangle((x,front),w,d,facecolor='#e2e8f0',edgecolor=ink,linestyle='--'))
for gx in [x-fit-gt,x+w+fit]:ax.add_patch(Rectangle((gx,0),gt,front+d+fit+gt,facecolor='#0f766e'))
for ex in [x-fit,x+w-corner]:
    for z in [0,front+d+fit]:ax.add_patch(Rectangle((ex,z),corner+fit,gt,facecolor='#0f766e'))
ax.text(x+w/2,75,'DEVICE FOOTPRINT\nLift 10 mm to clear the lips',ha='center',va='center',fontsize=13)
ax.annotate('5 mm return onto each corner',xy=(x+3,1.5),xytext=(65,-12),arrowprops=dict(arrowstyle='->'),fontsize=10)
ax.text(x+w/2,172,'Front and rear centres stay open for connectors',ha='center',fontsize=10)
save(fig,'retainer-detail',['All guides and corner returns stand 10 mm above the shelf. Retainers are 3 mm thick.', '0.6 mm fitting clearance at each body edge; 45° ramps support rear edges during printing.', 'The PSU uses the same retainer layout, sized to its own 72 × 162 mm footprint.'])

# Upright views use the CAD renderer to avoid painter-order artifacts on deep bays.
upright=OUT/'upright-view.scad'
upright.write_text('use <'+SOURCE.as_posix()+'>\nrotate([90,0,0]) rack();\n')
for name,azimuth in [('assembly-front',225),('assembly-rear',45)]:
    command(['--render','-o',OUT/(name+'.png'),'--camera=0,0,0,55,0,'+str(azimuth)+',0','--autocenter','--viewall','--imgsize=1400,1200','--colorscheme=Tomorrow',upright],name)

print('Rendering front and rear 1024 PNG views',flush=True)
for name,azimuth in [('front',45),('rear',225)]:
    command(['--render','-o',OUT/('acer-four-bay-shelves_'+name+'.png'),'--camera=0,0,0,55,0,'+str(azimuth)+',0','--autocenter','--viewall','--imgsize=1024,1024','--colorscheme=Tomorrow',SOURCE],'render-'+name)
print('PASS: closed single-component STL; printer bounds; all diagrams generated',flush=True)
