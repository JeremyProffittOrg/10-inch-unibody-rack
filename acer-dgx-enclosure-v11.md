# Acer enclosure v11: matched LCD outline and extended front

Based on the vertical-bow v10b case. The LCD panel's left and right edges now
follow the same circular side profile as the body, with a nominal 5 mm intake
gap. Its screen mounting surface remains flat for the existing LCD module.
The rectangular filler bezel has been removed to expose the curved intake.

The case is 19.05 mm (3/4 inch) longer, entirely in front of the fan and device
layout. With the front face as Y0, internal equipment and the fan carrier move
rearward by 19.05 mm. This preserves the 50.8 mm rear DGX cable allowance while
increasing LCD-to-fan separation by 19.05 mm. Overall dimensions are
228 x 281.85 x 171 mm. LCD back face is Y4; fan plate front is Y47.05.

The thicker bottom and shelf, 3 mm device pockets, underside strap recesses,
notched removable fan carrier, five fan patterns, four LCD screws and M3
body pilot mounts carry over from v10b. The same provisional 70 x 160 x 36 mm
power brick envelope applies. Tap the 2.5 mm body pilot holes M3 before fitting
M3 x 12 screws. Material and support settings remain to be selected.

Build and package:

```powershell
python build_acer_v11.py
node concept-v11/package_plates.cjs
```

Open `concept-v11/acer-dgx-enclosure-v11-separate-plates.3mf` in Bambu Studio.
The enclosure, bowed-outline LCD panel and fan carrier occupy separate plates.
CAD checks cover solid validity, rounded edges, equipment fit, stacking and
fan-panel withdrawal after removing the LCD. Physical fit remains untested.

![Front preview](concept-v11/preview-front.png)
