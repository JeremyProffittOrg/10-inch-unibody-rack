# Acer enclosure v13: diamond ventilation and support review

Side, roof, bottom and shelf vents now use pointed diamonds with their long
points along the front-to-back axis. Vent mouths use 1 mm chamfers. The pointed ends replace the earlier R3
rounding because automatic slicing found supports under those rounded ends. Small strap slots and fan/screw patterns remain
functional slots and circular holes.

## Geometry changes from the support review

- The DGX shelf is a separate part, printed flat. This removes its former wide,
  unsupported rear-edge span when printing the case rear-face-down.
- Four integral ramped ledges support the shelf. Use four M3 x 16 screws through
  3.4 mm shelf holes into 2.5 mm body pilots tapped M3. Roof access openings
  allow a driver to reach the screws with the integral top in place.
- Four ramped corner feet replace the continuous bottom nesting ring. They
  locate inside the stacking recess without creating wide transverse starts.
- The front of the top stacking recess and the new roof access collars have
  ramps that build progressively from the rear.
- Underside strap channels have ramped front ends. Their slots have been moved
  clear of those slopes and the device-pocket edges.
- LCD cable-tie tower openings are 4 x 5 mm diamonds with tapered mouths,
  sized for 2.5 mm cable ties, to avoid a horizontal slot ceiling.
- The previous 30-degree mount ramps, 45-degree device-pocket lead-ins, bowed
  LCD panel, recessed seats and 12.7 mm DGX side channels are retained.

The print project has four plates: enclosure rear-face-down; LCD face-down;
fan carrier face-down; and DGX shelf bottom-down. The shelf is inserted through
the rear before the devices, then secured using the roof access holes. Remove
the LCD before withdrawing the fan plate through the front.

## Dimensions and layout

| Feature | Millimetres |
|---|---:|
| Maximum outside width / depth / overall height | 248 / 281.85 / 171 |
| Nominal bottom / shelf thickness | 18 / 10 |
| Device locating recesses | 3 |
| DGX envelope | 150 x 150 x 50.5 |
| Power brick envelope (provisional) | 70 x 160 x 36 |
| Clearance above power brick | 12.7 |
| DGX side channels / rear cable clearance | 12.7 / 50.8 |
| LCD perimeter intake | 5 |

Side view, front at left:

```text
 LCD   fan plate    integral vented roof
  |       |      +----------------------+
  |      O O O   |        DGX           | rear cables
  |       |      +-- removable shelf ---+
  |      O O     |    power brick       |
  +--------------+----------------------+
                recessed underside straps
```

Front view: bowed walls enclose the LCD, with three upper fans and two lower
fans behind it. Top view: the DGX sits between two low guides defining its
side air channels; its tie slots pass through the removable shelf.

## Build and verification

```powershell
python build_acer_v13.py
node concept-v13/package_plates.cjs
./concept-v13/run_support_audit.ps1
python concept-v13/check_support_audit.py
```

The packager writes the large mesh XML incrementally to avoid retaining
millions of XML strings in memory. The OpenSCAD viewer imports the generated
meshes; build them before opening `acer-dgx-enclosure-v13.scad`.

The support audit enables normal automatic supports at a 45-degree threshold,
including internal regions, using the inherited H2D 0.20 mm PLA profile.
Anchored bridges up to 10 mm are allowed. The checker reads Bambu's actual
`support_used` results and scans generated G-code for support extrusion paths;
turning supports off alone is not considered a passing audit.

CAD validation checks each part's solid validity, rounding, device fit,
fan envelopes, assembly collisions, stacking, and fan-carrier extraction.
Small low-angle OCCT fillet-transition seams are distinguished from sharp
structural edges. Physical fit and printer-specific cooling still need checking.
The power brick envelope remains provisional at 70 x 160 x 36 mm.

The generated project is
`concept-v13/acer-dgx-enclosure-v13-separate-plates.3mf`. Generated STEP/STL/3MF
files and audit reports stay local under this repository's artifact policy.
