# Acer enclosure v9: power supply below DGX

This new layout preserves v8 separately. Build using CadQuery with
`python build_acer_v9.py`, then package using `node concept-v9/package_plates.cjs`.
The resulting three-plate project is `concept-v9/acer-dgx-enclosure-v9-separate-plates.3mf`.

| Feature | Millimetres |
|---|---|
| Overall maximum width / depth / height | 228 / 262.8 / 162 |
| Side-wall outward bow | 12 per side |
| Provisional power brick | 70 x 160 x 36 |
| Clearance above brick | 12.7 |
| Minimum clear aisle beside brick | 63 per side |
| Reserved cable space behind DGX | 50.8 |
| Lower fans | Two 40 x 40 x 20 |
| Lower fan overhang beyond brick edges | 10 per outer edge |
| LCD panel face / perimeter gap | 186 x 131 / 5 |
| Underside strap-channel recess | 3 |

```
FRONT                 SIDE (front left)
  [  LCD panel  ]       LCD | fans |  DGX       | cables
  [fan fan fan  ]           |      |-----------|
  [ fan   fan   ]           | fans | brick     |
                           |______|___________|
                                  recessed straps
```

The power-brick and lower-fan bottoms share Z9. The DGX shelf underside is
Z57.7, giving exactly 12.7 mm above the 36 mm high brick. Brick and DGX start
at Y58, behind the fan envelopes at Y32..52. Two brick straps pass through
the floor into recessed underside channels; two DGX straps pass through
paired slots in its shelf. Keep strap heads inside the equipment bays.

The internal fan plate carries two lower brick fans and three upper DGX fans.
The LCD panel is fixed using four screws and replaces the previous hinged
arrangement. Both removable panels use four M3 x 12 screws with 3.4 mm
clearance holes. Tap the body's 2.5 mm pilot holes M3 before assembly.
Remove the LCD panel before withdrawing the fan plate through the front.

Plate 1 is the upright enclosure; plates 2 and 3 place the LCD and fan panels
front-face down. The project is unsliced: tune supports and material settings.
The CAD checks cover validity, sharp edges, equipment fit, fan envelopes,
part collisions, stacking, and sampled fan-plate extraction positions.
Physical fit has not been tested; verify the actual brick dimensions.

Local preview with the LCD removed:

![Internal front layout](concept-v9/preview-front.png)

See [design notes](concept-v9/DESIGN-NOTES.txt) for attachment and print details.
