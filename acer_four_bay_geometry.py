"""Rounded four-bay geometry. CadQuery is already used by the Acer enclosure generators."""
from pathlib import Path
import importlib,json,os,sys
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
if sys.platform=='win32':
    sys.modules['vtk']=importlib.import_module('vtkmodules.vtkCommonDataModel')
import cadquery as cq

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'/'acer-four-bay'
wall_mm=25.;shelf_mm=5.;height_mm=315.;bay_count=4
psu_width_mm=72.;psu_depth_mm=162.;psu_height_mm=23.
dgx_width_mm=150.;dgx_depth_mm=150.;dgx_height_mm=50.5
side_gap_mm=22.;outer_gap_mm=2.;rear_extension_mm=76.2;front_extension_mm=25.4
psu_rear_open_ratio=.5
fit_mm=.6;guide_thickness_mm=3.;guide_height_mm=10.;corner_return_mm=5.
edge_radius_mm=.5;cable_corner_radius_mm=3.
cable_width_ratio=.8;cable_device_gap_mm=12.7;cable_rear_land_mm=25.4
fan_frame_mm=40.;fan_mount_mm=44.;fan_bore_mm=35.;fan_pitch_mm=32.;fan_screw_mm=3.4;fan_post_mm=3.;fan_depth_mm=5.
psu_x_mm=wall_mm+outer_gap_mm
dgx_x_mm=psu_x_mm+psu_width_mm+side_gap_mm
width_mm=dgx_x_mm+dgx_width_mm+outer_gap_mm+wall_mm
front_mm=front_extension_mm+guide_thickness_mm+fit_mm
depth_mm=front_mm+dgx_depth_mm+rear_extension_mm
pitch_mm=(height_mm-shelf_mm)/bay_count
bay_height_mm=pitch_mm-shelf_mm
fan_centres_mm=[psu_x_mm+psu_width_mm/2,
    dgx_x_mm-outer_gap_mm+fan_frame_mm/2,
    dgx_x_mm+dgx_width_mm+outer_gap_mm-fan_frame_mm/2]


def box(x,y,z,w,h,d):
    return cq.Solid.makeBox(w,h,d,cq.Vector(x,y,z))


def guide(x,width,z0,z1,y):
    """10 mm rail and 45-degree rear ramp; extruded along X."""
    return (cq.Workplane('YZ',origin=(x,y,0))
        .polyline([(0,z0),(guide_height_mm,z0),(guide_height_mm,z1),(0,z1+guide_height_mm)])
        .close().extrude(width).val())


def retainer(x,w,d,y,rear_open_ratio=None):
    """Side guides and full front stop; PSU rear stops leave the middle half open.

    Bounds: X x-fit-guide_thickness .. x+w+fit+guide_thickness,
    Y y .. y+guide_height, Z 0 .. front+d+fit+guide_thickness+guide_height.
    Side rails merge into the thick outer shell; all stops join the shelf top.
    """
    back=front_mm+d+fit_mm;parts=[]
    for rail_x in [x-fit_mm-guide_thickness_mm,x+w+fit_mm]:
        parts.append(guide(rail_x,guide_thickness_mm,0,back+guide_thickness_mm,y))
    parts.append(box(x-fit_mm,y,0,w+2*fit_mm,guide_height_mm,guide_thickness_mm))
    if rear_open_ratio is None:
        for end_x in [x-fit_mm,x+w-corner_return_mm]:
            parts.append(guide(end_x,corner_return_mm+fit_mm,back,back+guide_thickness_mm,y))
    else:
        stop_width=(w+2*fit_mm)*(1-rear_open_ratio)/2
        for end_x in [x-fit_mm,x+w+fit_mm-stop_width]:
            parts.append(box(end_x,y,back,stop_width,guide_height_mm,guide_thickness_mm))
    return parts


def cable_window(cx,body_width,body_depth,y):
    """Rounded rectangular throat: 80% width, 12.7 mm behind body to 25.4 mm from rear."""
    w=cable_width_ratio*body_width
    start=front_mm+body_depth+cable_device_gap_mm
    end=depth_mm-cable_rear_land_mm
    return (cq.Workplane('XY').box(w,shelf_mm+2,end-start,centered=(False,False,False))
        .edges('|Y').fillet(cable_corner_radius_mm).val().translate((cx-w/2,y-1,start)))


def sharp_edges(shape):
    """Find true surface discontinuities; tangent fillet boundaries are excluded."""
    adjacent={}
    for face in shape.Faces():
        for edge in face.Edges():adjacent.setdefault(edge.hashCode(),[]).append(face)
    result=[]
    for edge in shape.Edges():
        faces=adjacent.get(edge.hashCode(),[])
        if len(faces)==2:
            point=edge.positionAt(.5)
            if abs(faces[0].normalAt(point).dot(faces[1].normalAt(point)))<.999:
                result.append(edge)
    return result


def metadata():
    dgx_start=front_mm+dgx_depth_mm+cable_device_gap_mm
    psu_start=front_mm+psu_depth_mm+cable_device_gap_mm
    end=depth_mm-cable_rear_land_mm
    return {
        'revision':{'front_extension_mm':front_extension_mm,'outer_wall_mm':wall_mm,
                    'outer_gap_mm':outer_gap_mm,'psu_rear_open_ratio':psu_rear_open_ratio,
                    'psu_rear_open_mm':(psu_width_mm+2*fit_mm)*psu_rear_open_ratio},
        'dimensions':[width_mm,height_mm,depth_mm,pitch_mm,bay_height_mm-dgx_height_mm],
        'devices':[psu_width_mm,psu_depth_mm,psu_height_mm,dgx_width_mm,dgx_depth_mm,dgx_height_mm,psu_x_mm,dgx_x_mm,front_mm],
        'features':[guide_height_mm,guide_thickness_mm,fit_mm,corner_return_mm,(dgx_start+end)/2,.8*dgx_width_mm,.8*psu_width_mm,end-dgx_start],
        'fans':[fan_centres_mm,bay_height_mm/2,fan_bore_mm,fan_pitch_mm,fan_screw_mm,fan_mount_mm],
        'windows':{'dgx':[.8*dgx_width_mm,dgx_start,end],'psu':[.8*psu_width_mm,psu_start,end],
                   'plan_radius_mm':cable_corner_radius_mm,'edge_radius_mm':edge_radius_mm},
    }


def normalize_stl(path):
    """Drop only facets that collapse during STL float32 encoding; retain all finite-area faces."""
    import struct
    blob=path.read_bytes();count=struct.unpack_from('<I',blob,80)[0]
    assert len(blob)==84+50*count
    kept=[]
    for i in range(count):
        record=blob[84+50*i:84+50*(i+1)]
        a,b,c=[struct.unpack_from('<fff',record,12+12*j) for j in range(3)]
        u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
        cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
        if any(cross):kept.append(record)
    path.write_bytes(blob[:80]+struct.pack('<I',len(kept))+b''.join(kept))
    return count-len(kept)


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    assert height_mm<=325 and width_mm<=320 and depth_mm<=325
    assert side_gap_mm>2*(fit_mm+guide_thickness_mm)
    assert edge_radius_mm<fit_mm and 2*edge_radius_mm<guide_thickness_mm
    parts=[box(0,0,0,wall_mm,height_mm,depth_mm),box(width_mm-wall_mm,0,0,wall_mm,height_mm,depth_mm)]
    cuts=[]
    for i in range(bay_count+1):
        y=i*pitch_mm;parts.append(box(0,y,0,width_mm,shelf_mm,depth_mm))
        cuts.extend([cable_window(dgx_x_mm+dgx_width_mm/2,dgx_width_mm,dgx_depth_mm,y),
                     cable_window(psu_x_mm+psu_width_mm/2,psu_width_mm,psu_depth_mm,y)])
    for i in range(bay_count):
        y=shelf_mm+i*pitch_mm
        parts.extend(retainer(dgx_x_mm,dgx_width_mm,dgx_depth_mm,y))
        parts.extend(retainer(psu_x_mm,psu_width_mm,psu_depth_mm,y,psu_rear_open_ratio))
        for cx in fan_centres_mm:
            cy=y+bay_height_mm/2
            parts.append(box(cx-fan_mount_mm/2,cy-fan_mount_mm/2,depth_mm-fan_depth_mm,fan_mount_mm,fan_mount_mm,fan_depth_mm))
            for x in [cx-fan_mount_mm/2,cx+fan_mount_mm/2-fan_post_mm]:
                # The outer wall directly carries the far-right fan. Avoid a redundant 1 mm lip.
                if x+fan_post_mm<=width_mm-wall_mm:
                    parts.append(box(x,y,depth_mm-fan_depth_mm,fan_post_mm,bay_height_mm,fan_depth_mm))
            cuts.append(cq.Solid.makeCylinder(fan_bore_mm/2,fan_depth_mm+2,cq.Vector(cx,cy,depth_mm-fan_depth_mm-1),cq.Vector(0,0,1)))
            for xx in [-fan_pitch_mm/2,fan_pitch_mm/2]:
                for yy in [-fan_pitch_mm/2,fan_pitch_mm/2]:
                    cuts.append(cq.Solid.makeCylinder(fan_screw_mm/2,fan_depth_mm+2,cq.Vector(cx+xx,cy+yy,depth_mm-fan_depth_mm-1),cq.Vector(0,0,1)))
    print('Fusing rounded shelf construction',flush=True)
    shape=parts[0].fuse(*parts[1:]).clean().cut(*cuts).clean()
    assert shape.isValid() and len(shape.Solids())==1
    edges=sharp_edges(shape)
    print('Filleting '+str(len(edges))+' edges at R0.5 mm',flush=True)
    shape=shape.fillet(edge_radius_mm,edges).clean()
    assert shape.isValid() and len(shape.Solids())==1
    assert not sharp_edges(shape),'Sharp CAD edges remain'
    # Acceptance checks on the final rounded solid, before exporting or opening it.
    for i in range(bay_count):
        y=shelf_mm+i*pitch_mm
        for x,w in [(psu_x_mm,psu_width_mm),(dgx_x_mm,dgx_width_mm)]:
            for fraction in [.1,.5,.9]:
                assert shape.isInside(cq.Vector(x+w*fraction,y+guide_height_mm/2,guide_thickness_mm/2)),'Missing full front wall'
        back=front_mm+psu_depth_mm+fit_mm
        stop=(psu_width_mm+2*fit_mm)*(1-psu_rear_open_ratio)/2
        for x in [psu_x_mm-fit_mm+stop/2,psu_x_mm+psu_width_mm+fit_mm-stop/2]:
            assert shape.isInside(cq.Vector(x,y+guide_height_mm/2,back+guide_thickness_mm/2)),'Missing PSU rear stop'
        for x,inside in [(wall_mm-.5,True),(wall_mm+.5,False),(width_mm-wall_mm+.5,True),(width_mm-wall_mm-.5,False)]:
            assert shape.isInside(cq.Vector(x,y+bay_height_mm/2,front_mm+dgx_depth_mm/2))==inside,'Outer wall thickness mismatch'
    print_shape=shape.rotate((0,0,0),(1,1,0),180).translate((0,0,depth_mm))
    cq.exporters.export(shape,str(OUT/'acer-four-bay-shelves.step'))
    removed={}
    for name,item in [('acer-four-bay-shelves-assembly',shape),('acer-four-bay-shelves',print_shape)]:
        temp=OUT/(name+'-writing.stl')
        cq.exporters.export(item,str(temp),tolerance=.15,angularTolerance=.35)
        removed[name]=normalize_stl(temp)
        os.replace(temp,OUT/(name+'.stl'))
    result=metadata()
    result['cad_validation']={'collapsed_float32_facets_removed':removed,'valid':True,'solids':1,'sharp_edges':0,'edge_radius_mm':edge_radius_mm}
    (OUT/'geometry.json').write_text(json.dumps(result,indent=2))
    print('PASS: one valid CAD solid, all edges rounded',flush=True)
    return result

if __name__=='__main__':build()
