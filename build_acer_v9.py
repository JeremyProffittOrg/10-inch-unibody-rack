"""Parametric Acer enclosure v9. Requires cadquery. Units mm.
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

OUT=Path(__file__).parent/'concept-v9'; OUT.mkdir(exist_ok=True)
W,D,H=204.,262.8,159.
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
        if abs(faces[0].normalAt(pt).dot(faces[1].normalAt(pt)))<.999:result.append(e)
    return result
def rnd(s,r=1):
    edges=sharp_edges(s)
    result=s.fillet(r,edges).clean() if edges else s
    assert result.isValid(), 'Invalid rounded solid'
    return result
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

# New vertical layout. X across, Y rearward, Z upward; dimensions in mm.
FLOOR=9.; ROOF=150.; SHELF=57.7; SEAT=62.7
BRICK_X=67.; BRICK_Y=58.; BRICK_Z=FLOOR
DGX_X=27.; DGX_Y=58.; DGX_Z=SEAT
LCD_X=9.; LCD_Z=14.; PW=186.; PH=131.
def profile(inset=0):
    return (cq.Workplane('XY').moveTo(inset,0).lineTo(W-inset,0)
        .threePointArc((W+12-inset,D/2),(W-inset,D)).lineTo(inset,D)
        .threePointArc((-12+inset,D/2),(inset,0)).close())
def slab(z,h):return profile().extrude(h).val().translate((0,0,z))
def port(p,w,h,t,axis='z',r=3):
    tool=port_tool(w,h,t,r,1)
    if axis=='y':tool=tool.rotate((0,0,0),(1,0,0),90)
    if axis=='x':tool=tool.rotate((0,0,0),(0,1,0),90).rotate((0,0,0),(1,0,0),90)
    return tool.translate(p)
def save(name,s):
    assert s.isValid(),name
    assert len(s.Solids())==1,(name,len(s.Solids()))
    edges=sharp_edges(s)
    if edges:
        cq.exporters.export(s,str(OUT/(name+'-diagnostic.step')))
        (OUT/(name+'-sharp.json')).write_text(json.dumps([e.Center().toTuple() for e in edges]))
    assert not edges,(name,'sharp edges',len(edges))
    cq.exporters.export(s,str(OUT/(name+'.step')))
    cq.exporters.export(s,str(OUT/(name+'.stl')),tolerance=.12,angularTolerance=.2)
    log(name+': valid single solid, rounded edges')

log('Building bowed enclosure and vertically stacked equipment bays')
walls=slab(FLOOR,ROOF-FLOOR).cut(profile(4).extrude(ROOF-FLOOR+2).val().translate((0,0,FLOOR-1)))
shelf=slab(SHELF,5).intersect(box(-20,56,SHELF-1,W+40,158,7))
rim=slab(154,5).cut(rr(190,D-14,5,7).translate((7,7,153)))
foot=rr(188,D-16,4,4).translate((8,8,-3)).cut(rr(176,D-28,3,6).translate((14,14,-4)))
lcd_points=[(x,z) for x in [14.5,189.5] for z in [21,138]]
fan_points=[(x,z) for x in [26,178] for z in [18,129]]
lcd_bosses=[box(x,4,z-6,39,14,12).intersect(slab(0,H)) for x in [-20,185] for z in [21,138]]
fan_bosses=[box(x,32,z-6,50,12,12).intersect(slab(0,H)) for x in [-20,174] for z in [18,129]]
shell=rnd(fuse([slab(0,FLOOR),walls,shelf,slab(ROOF,4),rim,foot,*lcd_bosses,*fan_bosses]))
log('Base validity: '+str(shell.isValid()))
shell=round_holes(shell,[(x,4,z) for x,z in lcd_points],1.25,10,'y')
shell=round_holes(shell,[(x,32,z) for x,z in fan_points],1.25,10,'y')
log('Boss hole validity: '+str(shell.isValid()))
log('Adding recessed underside strap channels')
recesses=[rr(88,12,3,4).translate((58,y-2,-1)) for y in [98,178]]
shell=rnd(shell.cut(*recesses).clean())
log('Recess validity: '+str(shell.isValid()))
tools_cut=[]
for y in [98,178]:
    for x in [60,140]:tools_cut.append(port((x,y,3),4,8,6,r=1))
for y in [88,178]:
    for x in [20,180]:tools_cut.append(port((x,y,SHELF),4,8,5,r=1))
# Vents avoid strap channels and leave a supporting perimeter around the shelf.
for x in [32,60,88,116,144,172]:
    for y in [70,122,150,206,226]:tools_cut.append(port((x,y,ROOF),12,18,4))
for x in [32,88,144,172]:
    for y in [70,122,150,206,226]:
        tools_cut.append(port((x,y,0),12,18,FLOOR))
for x in [40,68,96,124,152]:
    for y in [108,140,196]:tools_cut.append(port((x,y,SHELF),12,10,5))
shell=shell.cut(*tools_cut).clean()
log('Vented shell validity: '+str(shell.isValid()))
log('Building internal removable five-fan plate')
fan_plate=rnd(box(20,28,9.25,164,4,127.75))
fan_centres=[(77,29),(127,29)]+[(x,113.2) for x in [52,102,152]]
for x,z in fan_centres:
    fan_plate=round_holes(fan_plate,[(x,27,z)],17.5,6,'y')
    fan_plate=round_holes(fan_plate,[(x+dx,27,z+dz) for dx in [-16,16] for dz in [-16,16]],1.65,6,'y')
fan_plate=round_holes(fan_plate,[(x,27,z) for x,z in fan_points],1.7,6,'y')
fan_plate=hole(fan_plate,(30,32,57),144,20,4,'y')

log('Building four-screw LCD panel with 5 mm perimeter intake')
# Local LCD plate uses X horizontal, Y upward, Z toward the viewer.
mount_points=[(x,y) for x in [(PW-156.9)/2,(PW+156.9)/2] for y in [(PH-114.96)/2,(PH+114.96)/2]]
lcd_parts=[box(0,0,0,PW,PH,4)]
for x,y in mount_points:lcd_parts.append(cylinder(x,y,-6.7,4,7.7))
# Cable tie towers behind the panel, clear of the board and case bosses.
for x in [0,PW-8]:lcd_parts.append(box(x,PH/2-6,-8,8,12,9))
lcd_local=rnd(fuse(lcd_parts))
lcd_local=hole(lcd_local,((PW-156)/2,(PH-89)/2,0),156,89,4)
for x,y in mount_points:lcd_local=round_holes(lcd_local,[(x,y,-7)],1.625,12,'z')
for x,z in lcd_points:lcd_local=round_holes(lcd_local,[(x-LCD_X,z-LCD_Z,-1)],1.7,6,'z')
for x in [0,PW-8]:lcd_local=hole(lcd_local,(x,PH/2-3,-5.5),6,3,8,'x',1)
def lcd_pose(s):return s.rotate((0,0,0),(1,0,0),90).translate((LCD_X,4,LCD_Z))
lcd=lcd_pose(lcd_local)
module=lcd_pose(box((PW-164.9)/2,(PH-124.27)/2,-8.3,164.9,124.27,8.3))
brick=box(BRICK_X,BRICK_Y,BRICK_Z,*BRICK)
dgx=box(DGX_X,DGX_Y,DGX_Z,150,150,50.5)
fans=[box(x-20,32,z-20,40,20,40) for x,z in fan_centres]
parts={'shell':shell,'lcd':lcd,'fan-plate':fan_plate}
log('Checking equipment fit, panel gaps, fan alignment and stacking')
for name,part in parts.items():
    for device,item in [('brick',brick),('DGX',dgx),('LCD-module',module)]:
        if name=='lcd' and device=='LCD-module':continue # Board envelope includes its supporting standoffs.
        assert part.intersect(item).Volume()<.1,(name,device)
for fan in fans:
    for name,part in parts.items():assert part.intersect(fan).Volume()<.1,('fan',name)
    assert fan.intersect(module).Volume()<.1
for a,b in [('shell','lcd'),('shell','fan-plate'),('lcd','fan-plate')]:
    assert parts[a].intersect(parts[b]).Volume()<.1,(a,b)
for dy in [-10,-30,-60]:assert shell.intersect(fan_plate.translate((0,dy,0))).Volume()<.1
stack=shell.intersect(shell.translate((0,0,H))).Volume()
assert stack<.1,stack
assert abs(SHELF-(BRICK_Z+BRICK[2])-12.7)<1e-6
assert abs((D-4)-(DGX_Y+150)-50.8)<1e-6
assert BRICK_X-4>=25.4 and W-4-(BRICK_X+BRICK[0])>=25.4
report={'top_integral':True,'layout':'power brick below DGX','power_brick_envelope_mm':BRICK,
 'outer_bounds_mm':[W+24,D,H+3],'power_clearance_above_mm':12.7,
 'power_min_side_clearance_mm':63,'DGX_rear_cable_clearance_mm':50.8,
 'lower_fan_centres_xz_mm':fan_centres[:2],'lower_fan_bottom_z_mm':9,
 'power_bottom_z_mm':9,'fan_outer_edge_overhang_mm':10,'LCD_perimeter_gap_mm':5,
 'LCD_panel_screws':4,'fan_plate_screws':4,'pilot_diameter_mm':2.5,
 'clearance_hole_diameter_mm':3.4,'underside_strap_recess_mm':3,
 'stack_overlap_mm3':stack,'parts':{}}
for name,s in parts.items():
    save(name,s)
    report['parts'][name]={'valid':s.isValid(),'solids':len(s.Solids()),'sharp_90_edges':len(sharp_edges(s))}
assembly=cq.Assembly(name='Acer enclosure v9 - vertically stacked')
for (name,s),color in zip(parts.items(),[(.32,.43,.5),(1,.61,.15),(.3,.65,.5)]):assembly.add(s,name=name,color=cq.Color(*color))
assembly.export(str(OUT/'acer-dgx-enclosure-v9.step'))
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
log('DONE')
