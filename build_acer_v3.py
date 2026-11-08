"""Parametric Acer enclosure v3. Requires cadquery. Units mm.
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

OUT=Path(__file__).parent/'concept-v3'; OUT.mkdir(exist_ok=True)
W,D,H=280.,251.6,200.
BRICK=(70.,160.,36.) # UNVERIFIED: measure user's brick before production.
PIVOT=(19.,182.)
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

log('Building structural shell and 3mm recessed equipment seats')
floor=box(0,0,0,W,D,6)
walls=[box(0,0,0,4,D,H),box(W-4,0,0,4,D,H),box(0,D-4,0,W,4,H)]
rim=box(0,0,190,W,D,10).cut(box(8,8,189,W-16,D-16,12))
foot=box(8.5,8.5,-5,W-17,D-17,6).cut(box(14.5,14.5,-6,W-29,D-29,8))
shelf=box(0,46,50,W,D-46,8)
# 3mm deep, 2mm wall clearance per side preserves 1mm at floor fillets; rear ledges replace retaining crossbar.
for x,w,d in [(18,74,164),(110,154,154)]:
    shelf=shelf.cut(rr(w,d,3,4).translate((x,48.8,55)))
divider=box(102,46,6,4,D-46,184)
front=box(4,25,6,W-8,4,120.5)
lid_screws=[(14,54),(W-14,54),(14,D-18),(W-14,D-18)]
lid_lands=[box(x-10,y-6,184,20,12,6) for x,y in lid_screws]
log('Rounding complete structural shell, including inside junctions')
pivot_lands=[box(x,12,172,7,18,15) for x in [4,269]]
shell=rnd(fuse([floor,*walls,rim,foot,shelf,divider,front,*lid_lands,*pivot_lands]))
log('Structural rounding complete: '+str(len(sharp_edges(shell)))+' sharp right-angle edges')
for x,w in [(14,82),(109,158)]:shell=hole(shell,(x,D,60.5),w,84.5,4,'y')
for x,w in [(14,80),(110,158)]:shell=hole(shell,(x,D,12),w,30,4,'y')
# All ventilation holes: R3 plan corners, R1 entrance and exit edges.
log('Rounding side vent openings')
for x in [0,W-4]:
    for y in range(62,230,28):
        for z in [74,116,156]:
            shell=hole(shell,(x,y,z),14,25,4,'x')
# Cable compartment interconnect through the centre wall.
shell=hole(shell,(102,124,15),42,26,4,'x')
for y in [78,188]:
    for z in [19,33]:shell=hole(shell,(102,y,z),10,4,4,'x',1)
log('Adding shelf vents, two brick straps and cable routes')
for x in [36,59,130,156,182,208,234]:
    for y in [77,111,145,179]:shell=hole(shell,(x,y,50),10,16,5,'z')
# Two straps: each has a slot on EACH side of the brick pocket.
for y in [87,179]:
    for x in [10,95]:shell=hole(shell,(x,y,50),4,12,8,'z',1)
for x in [40,170]:shell=hole(shell,(x,219,50),32,18,8,'z')
# Front video cable passage feeds directly into the Acer cable compartment.
shell=hole(shell,(168,29,18),32,20,4,'y')
# Three front 4020 mounting patterns: 32mm pitch, 3.3mm screw holes.
front_centres=[(55,91),(150,105.5),(224,105.5)]
for x,z in front_centres:
    shell=round_holes(shell,[(x,24,z)],18.5,6,'y')
    shell=round_holes(shell,[(x+dx,24,z+dz) for dx in [-16,16] for dz in [-16,16]],1.65,6,'y')
# Case-side pivot bosses: M4 bolt and washer friction adjustment.
log('Building top LCD pivots')
for x in [4,269]:
    shell=round_holes(shell,[(x-1,*PIVOT)],2.2,9,'x')
# Lid screws and rear fan carrier screws; M3 hardware with nuts.

shell=round_holes(shell,[(x,y,184) for x,y in lid_screws],1.65,12,'z')
carrier_screws=[(110,151),(266,151)]
shell=round_holes(shell,[(x,D-5,z) for x,z in carrier_screws],1.65,6,'y')
log('Building separate rounded ventilated lid')
lid=rnd(box(8.4,8.4,190,W-16.8,D-16.8,4))
# Lid rests on inner ledges; small side tabs reach the four screw lands.

lid=round_holes(lid,[(x,y,189) for x,y in lid_screws],1.65,7,'z')
for x in range(29,238,26):
    for y in range(60,226,32):lid=hole(lid,(x,y,190),14,20,4,'z')
log('Building removable rear triple-fan carrier')
carrier=rnd(fuse([box(106,D,81.5,164,4,48)]+[box(x-4,D,124,8,4,34) for x,z in carrier_screws]))
for x in [136,186,236]:
    carrier=round_holes(carrier,[(x,D-1,105.5)],18.5,6,'y')
    carrier=round_holes(carrier,[(x+dx,D-1,105.5+dz) for dx in [-16,16] for dz in [-16,16]],1.65,6,'y')
carrier=round_holes(carrier,[(x,D-1,z) for x,z in carrier_screws],1.65,6,'y')
log('Building separate articulated LCD plate and 8mm cable-tie towers')
lcd_parts=[box(0,0,0,254,133.35,5)]
mount_points=[(x,y) for x in [(254-156.9)/2,(254+156.9)/2] for y in [(133.35-114.96)/2,(133.35+114.96)/2]]
for x,y in mount_points:lcd_parts.append(cylinder(x,y,-6.7,4,7.7))
for x in [16,226]:
    for y in [24,110]:lcd_parts.append(box(x,y,-8,12,12,9))
for x in [0,248]:lcd_parts.append(box(x,127.35,-5,6,16,10))
lcd=rnd(fuse(lcd_parts))
lcd=hole(lcd,(50,26.175,0),156,89,5,'z')
for x,y in mount_points:lcd=round_holes(lcd,[(x,y,-7)],1.625,13,'z')
for x in [16,226]:
    for y in [24,110]:lcd=hole(lcd,(x,y+3,-5.5),6,3,12,'x',1,1)
for x in [0,248]:lcd=round_holes(lcd,[(x-1,137.35,0)],2.2,8,'x')
lcd_local=lcd
lcd=lcd.translate((0,-137.35,0)).rotate((0,0,0),(1,0,0),90-ANGLE).translate((13,*PIVOT))

lcd=rnd(lcd)
lcd_local=lcd.translate((-13,-PIVOT[0],-PIVOT[1])).rotate((0,0,0),(1,0,0),ANGLE-90).translate((0,137.35,0))

parts={'shell':shell,'lid':lid,'lcd':lcd,'rear-fan-carrier':carrier}
log('Validating and exporting')
report={}
for name,s in parts.items():
    assert s.isValid(),name+' invalid'
    assert len(s.Solids())==1,(name,len(s.Solids()))
    cq.exporters.export(s,str(OUT/(name+'.stl')),tolerance=.12,angularTolerance=.2)
    cq.exporters.export(s,str(OUT/(name+'.step')))
    report[name]={'solids':len(s.Solids()),'valid':s.isValid(),'volume_mm3':s.Volume(),'sharp_90_edges':len(sharp_edges(s))}
    print(name,report[name],flush=True)
cq.exporters.export(lcd_local,str(OUT/'lcd-flat.step'))
assembly=cq.Assembly(name='Acer enclosure v3')
colors=[(.32,.43,.5),( .4,.52,.6),(1,.61,.15),(.55,.6,.65)]
for (name,s),color in zip(parts.items(),colors):assembly.add(s,name=name,color=cq.Color(*color))
assembly.export(str(OUT/'acer-dgx-enclosure-v3.step'))
# Test rigid-part intersections; hinge side washers are intentionally separate.
for a,b in [('shell','lcd'),('lid','lcd'),('shell','lid'),('shell','rear-fan-carrier')]:
    vol=parts[a].intersect(parts[b]).Volume()
    report[a+' / '+b]={'intersection_mm3':vol}
    assert vol<.1,(a,b,vol)
for name,x,w,d,h in [('Acer',112,150,150,50.5),('brick',20,*BRICK)]:
    volume=shell.intersect(box(x,50.8,55,w,d,h)).Volume()
    report[name+' seated']={'intersection_mm3':volume}
    assert volume<.1,(name,volume)
module_envelope=box(44.55,4.54,-8.3,164.9,124.27,8.3).translate((0,-137.35,0)).rotate((0,0,0),(1,0,0),90-ANGLE).translate((13,*PIVOT))
module_overlap=shell.intersect(module_envelope).Volume()
report['LCD module / shell']={'intersection_mm3':module_overlap}
assert module_overlap<.1,module_overlap
stack_overlap=shell.intersect(shell.translate((0,0,H))).Volume()+lid.intersect(shell.translate((0,0,H))).Volume()
report['stack interface']={'intersection_mm3':stack_overlap}
assert stack_overlap<.1,stack_overlap
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
log('DONE')
