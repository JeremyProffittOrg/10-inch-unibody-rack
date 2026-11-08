"""Parametric Acer enclosure v5. Requires cadquery. Units mm.
Native CAD fillets provide R1 edges and R3 vent corners with R1 lips.
Exports separate components, assembly STEP, STL, 3MF, and OpenSCAD viewer.
"""
from pathlib import Path
import math, json
from functools import lru_cache
# Headless CAD: avoid loading unrelated VTK reader plug-ins on Windows.
import sys, importlib
if sys.platform == "win32":
    sys.modules["vtk"] = importlib.import_module("vtkmodules.vtkCommonDataModel")
import cadquery as cq

OUT=Path(__file__).parent/'concept-v5'; OUT.mkdir(exist_ok=True)
W,D,H=280.,251.6,174.6
BRICK=(70.,160.,36.) # UNVERIFIED: measure user's brick before production.
PIVOT=(19.,182.) # recalculated below
ANGLE=5.
def box(x,y,z,w,d,h):
    return cq.Solid.makeBox(w,d,h,cq.Vector(x,y,z))
def fuse(parts):
    return parts[0].fuse(*parts[1:]).clean()
def sharp_edges(s):
    adjacent={}
    for face in s.Faces():
        for edge in face.Edges():adjacent.setdefault(edge.hashCode(),[]).append(face)
    result=[]
    for e in s.Edges():
        faces=adjacent.get(e.hashCode(),[])
        if len(faces)!=2:continue
        pt=e.positionAt(.5)
        if abs(faces[0].normalAt(pt).dot(faces[1].normalAt(pt)))<.01:result.append(e)
    return result
def rnd(s,r=1):
    edges=sharp_edges(s)
    return s.fillet(r,edges).clean() if edges else s
def cylinder(x,y,z,r,h,axis=(0,0,1)):
    return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(*axis))
def rr(w,h,r,depth):
    return cq.Workplane('XY').box(w,h,depth,centered=(False,False,False)).edges('|Z').fillet(r).val()
def orient(s,p,axis):
    if axis=='x': s=s.rotate((0,0,0),(0,1,0),90).rotate((0,0,0),(1,0,0),90)
    if axis=='y': s=s.rotate((0,0,0),(1,0,0),90).rotate((0,0,0),(0,1,0),180)
    return s.translate(p)
@lru_cache(maxsize=None)
def port_tool(w,h,t,r=3,lip=1):
    blank=box(-4,-4,0,w+8,h+8,t)
    coupon=blank.cut(rr(w,h,r,t+2).translate((0,0,-1))).clean()
    if lip:
        edges=[]
        for e in coupon.Edges():
            b=e.BoundingBox()
            if b.xmin>=-.01 and b.xmax<=w+.01 and b.ymin>=-.01 and b.ymax<=h+.01:
                if any(abs(b.zmin-z)<.01 and abs(b.zmax-z)<.01 for z in [0,t]):edges.append(e)
        coupon=coupon.fillet(lip,edges).clean()
    return box(-3,-3,0,w+6,h+6,t).cut(coupon).fuse(rr(w,h,r,t+2).translate((0,0,-1))).clean()
def hole(s,p,w,h,t,axis='z',r=3,lip=1):
    cutter=port_tool(w,h,t,r,lip)
    if axis=='x':cutter=cutter.rotate((0,0,0),(0,1,0),90).rotate((0,0,0),(1,0,0),90)
    elif axis=='y':cutter=cutter.rotate((0,0,0),(1,0,0),90)
    return s.cut(cutter.translate(p)).clean()
def round_holes(s,points,r,t,axis):
    vec={'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}[axis]
    ax={'x':0,'y':1,'z':2}[axis]
    s=s.cut(*[cylinder(*p,r,t,vec) for p in points]).clean()
    edges=[]
    for e in s.Edges():
        if e.geomType()!='CIRCLE' or abs(e.radius()-r)>.001:continue
        c=e.Center().toTuple()
        if any(all(abs(c[j]-p[j])<.001 for j in range(3) if j!=ax) and p[ax]-.001<=c[ax]<=p[ax]+t+.001 for p in points):edges.append(e)
    return s.fillet(1,edges).clean() if edges else s
def log(msg):print(msg,flush=True)

FLOOR=6.
CABLE_CLEAR=12.7
SHELF=FLOOR+CABLE_CLEAR
SEAT=SHELF+5
DGX_RISE=12.7
DGX_SHELF=SHELF+DGX_RISE
DGX_SEAT=SEAT+DGX_RISE
LID_Z=H-10
GAP=10.
PW=W-8-2*GAP
sn=math.sin(math.radians(ANGLE));cs=math.cos(math.radians(ANGLE))
# R1 rounded panel projected bounds, including its 5mm thickness.
PROJECTED_HEIGHT=LID_Z-FLOOR-2*GAP
PH=(PROJECTED_HEIGHT-5*sn+2*(cs+sn-1))/cs
AXIS_Y=PH+4
PIVOT=(19.,LID_Z-GAP+4*cs-5*sn+(cs+sn-1))
PX=4+GAP
def pose(s,angle=ANGLE):
    return s.translate((0,-AXIS_Y,0)).rotate((0,0,0),(1,0,0),90-angle).translate((PX,*PIVOT))
def save(name,s):
    assert s.isValid(),name+' invalid'
    assert len(s.Solids())==1,(name,len(s.Solids()))
    sharp=len(sharp_edges(s));assert sharp==0,(name,'sharp edges',sharp)
    cq.exporters.export(s,str(OUT/(name+'.step')))
    cq.exporters.export(s,str(OUT/(name+'.stl')),tolerance=.12,angularTolerance=.2)
    log(name+' exported: valid single solid, all right-angle edges rounded')

log('Building shorter shell with 12.7mm lower cable space')
floor=box(0,0,0,W,D,FLOOR)
walls=[box(0,0,0,4,D,H),box(W-4,0,0,4,D,H),box(0,D-4,0,W,4,H)]
rim=box(0,0,LID_Z,W,D,10).cut(box(8,8,LID_Z-1,W-16,D-16,12))
# Local hinge reliefs retain the outer wall and the stacking registration.
rim=rim.cut(box(4,8,LID_Z-1,5,22,12)).cut(box(W-9,8,LID_Z-1,5,22,12))
foot=box(8.5,8.5,-5,W-17,D-17,6).cut(box(14.5,14.5,-6,W-29,D-29,8))
brick_shelf=box(0,46,SHELF,106,D-46,8).cut(rr(74,164,3,4).translate((18,48.8,SEAT)))
acer_shelf=box(102,46,DGX_SHELF,W-102,D-46,8).cut(rr(154,154,3,4).translate((110,48.8,DGX_SEAT)))
divider=box(102,46,FLOOR,4,D-46,LID_Z-FLOOR)
front=box(4,25,FLOOR,W-8,4,DGX_SEAT+50.5+21-FLOOR)
roof=box(8,8,LID_Z,W-16,D-16,4)
pivot_lands=[cylinder(x,*PIVOT,5,7,(1,0,0)) for x in [4,269]]
shell=rnd(fuse([floor,*walls,rim,foot,brick_shelf,acer_shelf,divider,front,roof,*pivot_lands]))
log('Base shell rounded')

log('Building enlarged panel and longer pivot tabs')
lcd_parts=[box(0,0,0,PW,PH,5)]
mount_points=[(x,y) for x in [(PW-156.9)/2,(PW+156.9)/2] for y in [(PH-114.96)/2,(PH+114.96)/2]]
for x,y in mount_points:lcd_parts.append(cylinder(x,y,-6.7,4,7.7))
tie_x=[16,PW-28];tie_y=[24,PH-23.35]
for x in tie_x:
    for y in tie_y:lcd_parts.append(box(x,y,-8,12,12,9))
tab_x=[0,PW-12]
for x in tab_x:
    lcd_parts += [box(x,0,-5,12,AXIS_Y,10),cylinder(x,AXIS_Y,0,5,12,(1,0,0))]
lcd=rnd(fuse(lcd_parts))
lcd=hole(lcd,((PW-156)/2+1,(PH-89)/2+4,0),156,89,5,'z')
for x,y in mount_points:lcd=round_holes(lcd,[(x,y,-7)],1.625,13,'z')
for x in tie_x:
    for y in tie_y:lcd=hole(lcd,(x,y+3,-5.5),6,3,12,'x',1,1)
for x in tab_x:lcd=round_holes(lcd,[(x-1,AXIS_Y,0)],2.2,14,'x')
lcd_local=lcd
lcd=pose(lcd)

module_local=box((PW-164.9)/2,(PH-124.27)/2,-8.3,164.9,124.27,8.3)
report={'shell_height_mm':H,'clear_cable_height_mm':CABLE_CLEAR,'panel_width_mm':PW,'panel_height_mm':PH,'pivot_yz_mm':PIVOT,'fan_count_front':4,'fan_count_rear':0,'pivot_tab_width_mm':12,'top_integral':True,'dgx_shelf_rise_mm':DGX_RISE,'dgx_clear_cable_height_mm':CABLE_CLEAR+DGX_RISE,'brick_clear_cable_height_mm':CABLE_CLEAR,'dgx_seat_z_mm':DGX_SEAT,'brick_seat_z_mm':SEAT}
body=pose(rnd(box(0,0,0,PW,PH,5))).BoundingBox()
gaps={'left':body.xmin-4,'right':W-4-body.xmax,'bottom':body.zmin-FLOOR,'top':LID_Z-body.zmax}
report['panel_face_gaps_mm']=gaps
assert all(abs(v-10)<.001 for v in gaps.values()),gaps
log('Panel face clearances: '+str(gaps))
for angle in [5,15,30,45,60,75]:
    frame=pose(lcd_local,angle);module=pose(module_local,angle)
    overlaps={'frame_shell':shell.intersect(frame).Volume(),'module_shell':shell.intersect(module).Volume()}
    log('Preflight angle '+str(angle)+': '+str(overlaps))
    assert all(v<.1 for v in overlaps.values()),(angle,overlaps)
    report['angle_'+str(angle)]=overlaps
for name,x,w,d,h in [('Acer',112,150,150,50.5),('brick',20,*BRICK)]:
    volume=shell.intersect(box(x,50.8,DGX_SEAT if name=='Acer' else SEAT,w,d,h)).Volume()
    assert volume<.1,(name,volume)
    report[name+'_seated_overlap_mm3']=volume
log('Preflight passed')
if '--preflight' in sys.argv:
    (OUT/'preflight.json').write_text(json.dumps(report,indent=2));sys.exit(0)

log('Cutting rounded loading openings and vents')
for x,w,seat in [(14,82,SEAT),(109,158,DGX_SEAT)]:shell=hole(shell,(x,D,seat+5.5),w,H-55-seat-5.5,4,'y')
shell=hole(shell,(14,D,8.35),80,8,4,'y')
shell=hole(shell,(110,D,8.7),158,20,4,'y')
for x in [0,W-4]:
    for y in range(62,230,28):
        for z in [SEAT+19,SEAT+57,H-44]:shell=hole(shell,(x,y,z),14,25,4,'x')
shell=hole(shell,(102,124,8.35),42,8,4,'x')
for y in [78,92,188,202]:shell=hole(shell,(102,y,10.35),10,4,4,'x',1)
log('Adding strap slots, shelf vents and video passage')
for x in [36,59,130,156,182,208,234]:
    for y in [77,111,145,179]:shell=hole(shell,(x,y,SHELF if x<100 else DGX_SHELF),10,16,5,'z')
for y in [87,179]:
    for x in [10,95]:shell=hole(shell,(x,y,SHELF),4,12,8,'z',1)
for x in [40,170]:shell=hole(shell,(x,219,SHELF if x<100 else DGX_SHELF),32,18,8,'z')
shell=hole(shell,(168,29,8.5),32,14,4,'y')
front_centres=[(55,SEAT+36)]+[(x,DGX_SEAT+50.5) for x in [136,186,236]]
for x,z in front_centres:
    shell=round_holes(shell,[(x,24,z)],18.5,6,'y')
    shell=round_holes(shell,[(x+dx,24,z+dz) for dx in [-16,16] for dz in [-16,16]],1.65,6,'y')
for x in [-1,268]:shell=round_holes(shell,[(x,*PIVOT)],2.2,13,'x')
log('Perforating integral roof')
for x in [24,50,76,118,144,170,196,222,248]:
    for y in range(60,226,32):shell=hole(shell,(x,y,LID_Z),14,20,4,'z')
save('shell',shell)
save('lcd',lcd)
cq.exporters.export(lcd_local,str(OUT/'lcd-flat.step'))
parts={'shell':shell,'lcd':lcd}
for a,b in [('shell','lcd')]:
    vol=parts[a].intersect(parts[b]).Volume();assert vol<.1,(a,b,vol)
    report[a+'/'+b]=vol
stack_overlap=shell.intersect(shell.translate((0,0,H))).Volume()
assert stack_overlap<.1,stack_overlap
report['stack_overlap_mm3']=stack_overlap
report['parts']={n:{'valid':s.isValid(),'solids':len(s.Solids()),'sharp_90_edges':len(sharp_edges(s))} for n,s in parts.items()}
assembly=cq.Assembly(name='Acer enclosure v5')
for (name,s),color in zip(parts.items(),[(.32,.43,.5),(1,.61,.15)]):assembly.add(s,name=name,color=cq.Color(*color))
assembly.export(str(OUT/'acer-dgx-enclosure-v5.step'))
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
log('DONE')
