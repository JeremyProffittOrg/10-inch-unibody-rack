# Acer enclosure v12: stronger bow and printing ramps

The vertical side bow increases from 12 to 22 mm per side. The LCD outline
follows the new profile and retains its nominal 5 mm intake gap. Overall
maximum size is 248 x 281.85 x 171 mm.

Low 3 mm thick guides define a 12.7 mm air channel beside each side of the
150 mm DGX. Their inward faces are X14.3 and X189.7; the DGX occupies X27..177.
The guides reach 8 mm above the seated device base and leave the upper side
vents unobstructed. Their rear ends taper into the shelf.

LCD and fan body mounts now taper into the side walls or roof behind their
screw faces. The ramps are **30 degrees from the rear-to-front print axis**
(60 degrees to the build plate). The enclosure is placed rear-face-down on
plate 1, with the LCD and fan carrier separately face-down on plates 2 and 3.

Both device pockets retain 3 mm depth but now have a front lead-in rising
3 mm over 3 mm: a 45-degree ramp. Pocket fronts extend 2 mm forward so the
ramp clears the seated device corners. The shelf front extends accordingly.
The first roof vent row moves behind the upper mounting-ramp tails.

Existing thicker floors, recessed strap paths, notched fan carrier, M3 pilot
holes, device/fan elevations and 50.8 mm rear cable allocation remain.
Tap the body pilots M3 for M3 x 12 screws. The brick envelope remains
provisional at 70 x 160 x 36 mm.

```powershell
python build_acer_v12.py
node concept-v12/package_plates.cjs
```

Open `concept-v12/acer-dgx-enclosure-v12-separate-plates.3mf` in Bambu Studio.
The project is unsliced. These ramps address the specified mount backs and
pocket fronts; the entire enclosure has not been validated as support-free.
Review remaining shelf bridges and overhangs in the slicer before printing.
CAD checks include solid validity, rounded edges, device fit, fan envelopes,
stacking and fan-panel extraction. Physical fit has not been tested.
