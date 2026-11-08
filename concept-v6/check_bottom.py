import sys, importlib, json
from pathlib import Path
sys.modules['vtk'] = importlib.import_module('vtkmodules.vtkCommonDataModel')
import cadquery as cq
p=Path(__file__).parent
s=cq.importers.importStep(str(p/'shell.step')).val()
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.TopAbs import TopAbs_IN
classifier=BRepClass3d_SolidClassifier(s.wrapped)
def inside(point):
    classifier.Perform(point.toPnt(),1e-6)
    return classifier.State()==TopAbs_IN
# Check the new bottom contains material between vents, down to the foot level.
for z in [-4, 0, 5]:
    assert inside(cq.Vector(45,85,z)), ('bottom material missing',z)
# Every roof vent has a matching through-hole at the bottom.
for x in [24,50,76,118,144,170,196,222,248]:
    for y in range(60,226,32):
        for z in [-4,0,5,153.9]:
            assert not inside(cq.Vector(x+7,y+10,z)), (x,y,z)
v=json.loads((p/'validation.json').read_text())
assert abs(v['dgx_seat_z_mm']-36.4)<1e-6
assert abs(v['brick_seat_z_mm']-49.1)<1e-6
assert abs(s.BoundingBox().zlen-166.9)<1e-6
print('Verified filled bottom, 54 matching through-vents, shelf elevations and overall height.')
