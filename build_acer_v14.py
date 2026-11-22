"""Fan-first curved DGX enclosure. Dimensions mm; X right, Y rear, Z up.

Component bounds: shell X -22..226, Y 0..281.85, Z -9..159;
fixed shelf Z 54.7..64.7, Y 5..240; cap same X/Z outline, Y -57.7..0.
The two open troughs cross the shelf from the fan plate to its rear edge.
"""
from pathlib import Path
import json, math
from collections import Counter
import struct
from acer_four_bay_geometry import cq, box, normalize_stl

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output' / 'acer-v14'
width_mm, depth_mm = 204., 281.85
bottom_mm, top_mm, bow_mm = -9., 159., 22.
wall_mm, plate_mm = 5., 5.
floor_mm, roof_mm = 6., 154.
shelf_bottom_mm, shelf_top_mm, shelf_end_mm = 54.7, 64.7, 240.
dgx_x_mm, device_front_mm = 27., 77.05
dgx_width_mm, dgx_depth_mm, dgx_height_mm = 150., 150., 50.5
psu_width_mm, psu_depth_mm, psu_height_mm = 72., 162., 23.
psu_x_mm = (width_mm-psu_width_mm)/2
fit_mm, guide_mm, guide_height_mm = .6, 3., 10.
trough_width_mm, trough_depth_mm = 30., 6.
trough_centres_mm = [77., 127.]
fan_frame_mm, fan_thickness_mm, fan_bore_mm = 40., 20., 35.
fan_pitch_mm, fan_screw_mm = 32., 3.4
transition_degrees = 30.
fan_centres_mm = [(77.,26.),(127.,26.),(77.,70.),(127.,70.),
                  (52.,125.),(102.,125.),(152.,125.)]
front_screw_mm, screw_depth_mm = 3., 15.
front_points_mm = [(x,z) for x in [0.,204.] for z in [18.,138.]]
lcd_width_mm, lcd_height_mm, lcd_depth_mm = 164.9,124.27,8.3
lcd_pitch_x_mm, lcd_pitch_z_mm = 156.9,114.96
lcd_window_width_mm, lcd_window_height_mm = 156.,89.
lcd_centre_z_mm, lcd_plate_mm, lcd_standoff_mm = 75.,4.,6.7
fan_clearance_mm = 25.4
cap_back_mm = -fan_thickness_mm-fan_clearance_mm-lcd_depth_mm
cap_front_mm = cap_back_mm-lcd_plate_mm
overlap_mm = 1.


def log(message):
    print(message,flush=True)


def outline(inset=0):
    """Closed bowed X/Z perimeter; inset shifts the side arcs inward."""
    return (cq.Workplane('XZ').moveTo(inset,bottom_mm)
        .lineTo(width_mm-inset,bottom_mm)
        .threePointArc((width_mm+bow_mm-inset,(bottom_mm+top_mm)/2),(width_mm-inset,top_mm))
        .lineTo(inset,top_mm)
        .threePointArc((-bow_mm+inset,(bottom_mm+top_mm)/2),(inset,bottom_mm)).close())


def envelope(start,end,inset=0):
    """Bowed prism, X/Z outline above; Y start..end."""
    return outline(inset).extrude(-(end-start)).val().translate((0,start,0))


def cyl(x,y,z,r,length):
    return cq.Solid.makeCylinder(r,length,cq.Vector(x,y,z),cq.Vector(0,1,0))


def slab(z,height,start=0,end=depth_mm):
    return envelope(start,end).intersect(box(-bow_mm,start,z,width_mm+2*bow_mm,end-start,height))


def rail(x,z):
    """Longitudinal retaining wall; joined to fan plate and shelf, open rear."""
    return box(x,plate_mm,z,guide_mm,shelf_end_mm-plate_mm,guide_height_mm)


def diamond_side(y,z,length=24.,height=12.):
    """Side vent with 45-degree-or-steeper leading/trailing slopes in print Y."""
    return (cq.Workplane('YZ',origin=(-bow_mm-overlap_mm,0,0))
        .polyline([(y-length/2,z),(y,z-height/2),(y+length/2,z),(y,z+height/2)])
        .close().extrude(width_mm+2*bow_mm+2*overlap_mm).val())


def print_pose(s):
    """Fan/front first: Y depth becomes positive printer Z, preserving handedness."""
    s=s.rotate((0,0,0),(1,0,0),90)
    b=s.BoundingBox()
    return s.translate((-b.xmin,-b.ymin,-b.zmin))


def mesh_check(path):
    data=path.read_bytes(); n=struct.unpack_from('<I',data,80)[0]
    assert len(data)==84+50*n
    edges=Counter(); adjacency={}
    for i in range(n):
        vertices=[struct.unpack_from('<fff',data,84+50*i+12+12*j) for j in range(3)]
        for a,b in zip(vertices,vertices[1:]+vertices[:1]):
            edges[tuple(sorted((a,b)))]+=1
            adjacency.setdefault(a,set()).add(b); adjacency.setdefault(b,set()).add(a)
    assert all(c==2 for c in edges.values()), 'Non-manifold mesh: '+str(Counter(edges.values()))
    todo=[next(iter(adjacency))]; seen=set(todo)
    while todo:
        for v in adjacency[todo.pop()]:
            if v not in seen:seen.add(v);todo.append(v)
    assert len(seen)==len(adjacency),'Disconnected mesh'
    return {'triangles':n,'closed_manifold':True,'connected':True}


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    log('Building fixed shelf and curved fan-first shell')
    outer=envelope(0,depth_mm)
    cavity=envelope(plate_mm,depth_mm+overlap_mm,wall_mm).intersect(
        box(-bow_mm,plate_mm,floor_mm,width_mm+2*bow_mm,depth_mm,roof_mm-floor_mm))
    shell=outer.cut(cavity)
    shelf=slab(shelf_bottom_mm,shelf_top_mm-shelf_bottom_mm,plate_mm,shelf_end_mm)
    rails=[rail(dgx_x_mm-fit_mm-guide_mm,shelf_top_mm),
           rail(dgx_x_mm+dgx_width_mm+fit_mm,shelf_top_mm),
           rail(psu_x_mm-fit_mm-guide_mm,floor_mm),
           rail(psu_x_mm+psu_width_mm+fit_mm,floor_mm)]
    shell=shell.fuse(shelf,*rails).clean()
    # Open channels retain four millimetres of shelf floor and open at both ends.
    troughs=[box(x-trough_width_mm/2,plate_mm,shelf_top_mm-trough_depth_mm,
                 trough_width_mm,shelf_end_mm-plate_mm+overlap_mm,trough_depth_mm+overlap_mm)
             for x in trough_centres_mm]
    cuts=list(troughs)
    for x,z in fan_centres_mm:
        cuts.append(cyl(x,-overlap_mm,z,fan_bore_mm/2,plate_mm+overlap_mm))
        # 30-degree transitions let shelf/guide material grow into the opening
        # behind the first plate without starting a wide unsupported bridge.
        cuts.append(cq.Solid.makeCone(fan_bore_mm/2,0,fan_bore_mm/2/math.tan(math.radians(transition_degrees)),
                    cq.Vector(x,plate_mm,z),cq.Vector(0,1,0)))
        for dx in [-fan_pitch_mm/2,fan_pitch_mm/2]:
            for dz in [-fan_pitch_mm/2,fan_pitch_mm/2]:
                cuts.append(cyl(x+dx,-overlap_mm,z+dz,fan_screw_mm/2,plate_mm+overlap_mm))
                cuts.append(cq.Solid.makeCone(fan_screw_mm/2,0,fan_screw_mm/2/math.tan(math.radians(transition_degrees)),
                            cq.Vector(x+dx,plate_mm,z+dz),cq.Vector(0,1,0)))
    # Front screw lands grow from the fan plate and taper into the side walls.
    lands=[]
    for x,z in front_points_mm:
        lands.append(box(x-5,0,z-5,10,screw_depth_mm+wall_mm,10))
    shell=shell.fuse(*lands).clean()
    cuts.extend(cyl(x,-overlap_mm,z,front_screw_mm/2,screw_depth_mm+overlap_mm) for x,z in front_points_mm)
    # Side diamonds are beyond the fan bodies; their leading ends grow from the wall.
    for y in [55.,95.,135.,175.,215.,255.]:
        for z in [35.,105.,135.]:cuts.append(diamond_side(y,z))
    shell=shell.cut(*cuts).clean()

    log('Building matching screw-on LCD cap with one-inch fan clearance')
    cap=envelope(cap_front_mm,0).cut(
        envelope(cap_back_mm,overlap_mm,wall_mm).intersect(
            box(-bow_mm,cap_back_mm,bottom_mm+wall_mm,width_mm+2*bow_mm,
                -cap_back_mm+overlap_mm,top_mm-bottom_mm-2*wall_mm)))
    lcd_points=[(width_mm/2+dx,lcd_centre_z_mm+dz)
        for dx in [-lcd_pitch_x_mm/2,lcd_pitch_x_mm/2]
        for dz in [-lcd_pitch_z_mm/2,lcd_pitch_z_mm/2]]
    cap=cap.fuse(*[cyl(x,cap_back_mm-overlap_mm,z,4.,lcd_standoff_mm+overlap_mm) for x,z in lcd_points],
                 *[box(x-5,cap_back_mm,z-5,10,-cap_back_mm,10) for x,z in front_points_mm]).clean()
    cap_cuts=[box((width_mm-lcd_window_width_mm)/2,cap_front_mm-overlap_mm,
                   lcd_centre_z_mm-lcd_window_height_mm/2,lcd_window_width_mm,
                   lcd_plate_mm+2*overlap_mm,lcd_window_height_mm)]
    cap_cuts.extend(cyl(x,cap_front_mm-overlap_mm,z,front_screw_mm/2,-cap_front_mm+2*overlap_mm) for x,z in front_points_mm)
    cap_cuts.extend(cyl(x,cap_front_mm-overlap_mm,z,3.25/2,lcd_plate_mm+lcd_standoff_mm+2*overlap_mm) for x,z in lcd_points)
    for z in [25.,50.,75.,100.,125.]:cap_cuts.append(diamond_side(-16.,z,20.,10.))
    cap=cap.cut(*cap_cuts).clean()

    log('Checking device fit, uninterrupted airflow, screw bores and fan envelopes')
    dgx=box(dgx_x_mm,device_front_mm,shelf_top_mm,dgx_width_mm,dgx_depth_mm,dgx_height_mm)
    psu=box(psu_x_mm,device_front_mm,floor_mm,psu_width_mm,psu_depth_mm,psu_height_mm)
    module=box((width_mm-lcd_width_mm)/2,cap_back_mm,lcd_centre_z_mm-lcd_height_mm/2,
               lcd_width_mm,lcd_depth_mm,lcd_height_mm)
    for name,part in [('shell',shell),('lcd',cap)]:
        assert part.isValid() and len(part.Solids())==1,name
        for device in [dgx,psu]:assert part.intersect(device).Volume()<1e-5,name+' device collision'
    assert shell.intersect(cap).Volume()<1e-5
    for x,z in fan_centres_mm:
        fan=box(x-fan_frame_mm/2,-fan_thickness_mm,z-fan_frame_mm/2,fan_frame_mm,fan_thickness_mm,fan_frame_mm)
        assert shell.intersect(fan).Volume()<1e-5,('fan collision',x,z)
        assert cap.intersect(fan).Volume()<1e-5
        assert abs(fan.BoundingBox().ymin-module.BoundingBox().ymax-fan_clearance_mm)<1e-6
    for trough in troughs:assert shell.intersect(trough).Volume()<1e-5,'Blocked trough'
    for x in trough_centres_mm:
        assert shell.isInside(cq.Vector(x,device_front_mm+50,shelf_bottom_mm+2)), 'Missing trough floor'
        # Air enters through lower-DGX fan aperture and reaches the rear below DGX.
        airway=box(x-5,0,shelf_top_mm-4,10,shelf_end_mm,3)
        assert shell.intersect(airway).Volume()<1e-5,'Blocked under-DGX airflow'
    for x,z in fan_centres_mm[-3:]:
        airway=box(x-5,0,shelf_top_mm+dgx_height_mm+5,10,depth_mm,5)
        assert shell.intersect(airway).Volume()<1e-5,'Blocked over-DGX airflow'
    for x,z in front_points_mm:
        bore=cyl(x,cap_front_mm,z,front_screw_mm/2-.01,screw_depth_mm-cap_front_mm)
        assert shell.intersect(bore).Volume()<1e-5 and cap.intersect(bore).Volume()<1e-5
    # Both devices insert from the open rear without passing the fan plate.
    for device in [dgx,psu]:
        for offset in range(0,241,20):assert shell.intersect(device.translate((0,offset,0))).Volume()<1e-5
    report={'passed':True,'integral_shelf':True,'integral_fan_plate':True,
        'fan_count':len(fan_centres_mm),'body_print_orientation':'fan plate first',
        'fan_clearance_mm':fan_clearance_mm,'front_screw_diameter_mm':front_screw_mm,
        'trough_width_depth_mm':[trough_width_mm,trough_depth_mm],
        'DGX_clearance_above_mm':roof_mm-shelf_top_mm-dgx_height_mm,
        'power_brick_envelope_mm':[psu_width_mm,psu_depth_mm,psu_height_mm],
        'parts':{}}
    for name,part in [('shell',shell),('lcd',cap)]:
        cq.exporters.export(part,str(OUT/(name+'.step')))
        cq.exporters.export(part,str(OUT/(name+'-assembly.stl')),tolerance=.08,angularTolerance=.05)
        posed=print_pose(part); b=posed.BoundingBox()
        assert b.xlen<=325 and b.ylen<=320 and b.zlen<=325
        path=OUT/(name+'.stl')
        cq.exporters.export(posed,str(path),tolerance=.08,angularTolerance=.05)
        normalize_stl(path)
        report['parts'][name]={'print_bounds_mm':[b.xlen,b.ylen,b.zlen],**mesh_check(path)}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2))
    log('PASS: single solids, fit, troughs, 25.4 mm fan clearance, bores, insertion and manifold meshes')
    return report


if __name__=='__main__':build()
