"""Read actual Bambu slicing results, including generated support toolpaths."""
from pathlib import Path
from zipfile import ZipFile
import json, re, xml.etree.ElementTree as ET

root=Path(__file__).parent
project=root/'support-audit-sliced.3mf'
with ZipFile(project) as z:
    profile=json.loads(z.read('Metadata/project_settings.config'))
    assert str(profile['enable_support'])=='1', 'Audit must run with supports enabled'
    assert profile['support_type']=='normal(auto)'
    assert str(profile['support_threshold_angle'])=='45'
    assert str(profile['support_on_build_plate_only'])=='0'
    result={'settings':{k:profile.get(k) for k in ['enable_support','support_type',
        'support_threshold_angle','bridge_no_support','max_bridge_length']},'plates':[]}
    for plate in ET.fromstring(z.read('Metadata/slice_info.config')).findall('plate'):
        meta={m.attrib['key']:m.attrib['value'] for m in plate.findall('metadata')}
        number=int(meta['index'])
        record={'plate':number,'support_used':meta.get('support_used'),'weight_g':meta.get('weight'),
                'prediction_seconds':meta.get('prediction'),'outside':meta.get('outside')}
        filaments=plate.findall('filament')
        assert filaments, 'Missing filament usage metadata'
        record['filament_used_for_support']=[f.attrib.get('used_for_support') for f in filaments]
        support=False; layer=0.; x=y=0.; samples=[]; extrusions=0; features=0; support_sections=0
        with z.open(f'Metadata/plate_{number}.gcode') as g:
            for raw in g:
                line=raw.decode('utf-8',errors='replace').strip()
                if line.startswith('; FEATURE:') or line.startswith(';TYPE:'):
                    features+=1
                    support='support' in line.lower()
                    support_sections+=int(support)
                if line.startswith(('G0 ','G1 ')):
                    fields={k:float(v) for k,v in re.findall(r'([XYZE])(-?[\d.]+)',line)}
                    x=fields.get('X',x);y=fields.get('Y',y);layer=fields.get('Z',layer)
                    if support and 'E' in fields and fields['E']>0 and ('X' in fields or 'Y' in fields):
                        extrusions+=1
                        if extrusions%100==0:samples.append([round(x,2),round(y,2),round(layer,2)])
        assert features>0, 'G-code feature markers missing; cannot classify supports'
        record.update(support_extrusion_moves=extrusions,support_feature_sections=support_sections,support_samples=samples)
        result['plates'].append(record)
(root/'support-audit-report.json').write_text(json.dumps(result,indent=2))
print(json.dumps([{k:v for k,v in r.items() if k!='support_samples'} for r in result['plates']],indent=2))
assert len(result['plates'])==2, 'Expected two sliced plates'
assert all(r['outside']=='false' for r in result['plates'])
# Bambu PrintApply.cpp assigns m_support_used from enable_support, even with
# no generated support. Check actual toolpaths AND per-filament consumption.
# https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintApply.cpp
assert all(r['support_extrusion_moves']==0 and r['support_feature_sections']==0
           and all(v=='false' for v in r['filament_used_for_support'])
           for r in result['plates']), 'Generated support needs review'
print('PASS: automatic support detection generated no support on any of the two plates.')
