from pathlib import Path
import sys, importlib, json
sys.modules['vtk']=importlib.import_module('vtkmodules.vtkCommonDataModel')
import cadquery as cq
root=Path(__file__).parent
parts={n:cq.importers.importStep(str(root/(n+'.step'))).val() for n in ['shell','lid','lcd','rear-fan-carrier']}
report={}
for angle in [5,15,30,45,60,75]:
    panel=parts['lcd'].rotate((0,19,182),(1,19,182),5-angle)
    hits={n:panel.intersect(parts[n]).Volume() for n in ['shell','lid','rear-fan-carrier']}
    report[angle]=hits
    print('LCD angle',angle,hits,flush=True)
    assert all(v<.1 for v in hits.values()),(angle,hits)
(root/'hinge-clearance.json').write_text(json.dumps(report,indent=2))
