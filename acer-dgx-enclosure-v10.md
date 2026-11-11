# Acer enclosure v10: notched fan plate and recessed seats

Two variants share the same removable panels and device layout:

- **v10 / A:** sides bow outward along the front-to-back direction.
- **v10b / B:** side rounding rotated 90 degrees, bowing outward bottom-to-top.

Both fan panels have rounded corner notches around the LCD mounts. Lower fan
attachment screws move inward; upper screws attach to mounts beneath the roof.
The front extraction path is checked in 5 mm increments through 65 mm travel,
with the LCD panel removed first.

| Feature | Dimension |
|---|---|
| Bottom nominal thickness | 18 mm, doubled from 9 |
| DGX shelf nominal thickness | 10 mm, doubled from 5 |
| Device locating pockets | 3 mm deep |
| Remaining material under brick / DGX pockets | 15 / 7 mm |
| Brick pocket | 74 x 164 mm for provisional 70 x 160 mm brick |
| DGX pocket | 154 x 154 mm for 150 x 150 mm device |
| Maximum outside width / depth / height | 228 / 262.8 / 171 mm |
| Brick bottom / DGX bottom elevation | 6 / 61.7 mm |
| Clearance above power brick | 12.7 mm |
| Reserved rear DGX cable space | 50.8 mm |
| Fan panel | 164 x 139.75 x 4 mm |
| LCD panel face | 186 x 134 x 4 mm |

The bottom grows downward, keeping the equipment compact. A 3 mm recessed
front fan/insertion area keeps the two lower fan bottoms level with the seated
brick. The underside strap channels remain 3 mm deep and their through-slots
are moved away from the locating-pocket edges. The LCD lower edge and screw
positions follow the lowered front recess to retain the nominal 5 mm intake.
The upper fans follow the new seated DGX elevation. M3 pilot holes still need
tapping before assembly; both panels use four M3 x 12 screws.

Build both with:

```powershell
python build_acer_v10.py
python build_acer_v10.py --side-bow-vertical
node concept-v10/package_plates.cjs
node concept-v10b/package_plates.cjs
node concept-v10/package_compare.cjs
```

The comparison project is
`concept-v10/acer-dgx-v10-both-versions-six-plates.3mf`.
Plates 1-3 contain variant A's enclosure, LCD and fan panels; plates 4-6
contain variant B's matching parts. Separate three-plate projects are also
available in each variant's output directory. Projects are unsliced; choose
supports and material settings before printing. CAD fit and rounding checks
pass, but physical fit and the provisional brick dimensions still need checking.
