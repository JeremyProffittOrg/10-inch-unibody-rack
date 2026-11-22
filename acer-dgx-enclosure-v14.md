# Curved fan-first DGX enclosure v14

One DGX sits above its power supply in a curved enclosure. The shelf, raised
retaining walls and seven-fan plate are permanently joined into one print.
The matching full-outline LCD cap is the only separate printed part. Historical
v13 and four-bay designs remain available.

## Dimensions and components

Use coordinates: X right, Y rearward, Z upward. Origin is the front fan plate.
Printing maps use Y to positive printer Z: the fan plate prints first.

| Parameter/component | Millimetres / position |
|---|---|
| Body bounding box | X -22..226, Y 0..281.85, Z -9..159 |
| Body print bounds | 248 x 168 x 281.85 |
| Cap bounding box | same X/Z outline, Y -57.7..0 |
| Cap print bounds | 248 x 168 x 57.7 |
| Assembled total depth | 339.55; two separate prints fit H2D |
| Side bow | 22 beyond nominal 204-wide outline |
| Side walls / roof / integral fan plate | 5 / 5 / 5 |
| Bottom | Z -9..6, thickness 15 |
| Integral shelf | Z 54.7..64.7, Y 5..240; joins both side walls |
| Troughs | 30 wide x 6 deep, X centres 77/127, Y 5..240 |
| Solid floor beneath troughs | 4 |
| DGX | 150 W x 150 D x 50.5 H; X 27, Y 77.05, Z 64.7 |
| Clear space above DGX | 38.8 |
| Power supply | 72 W x 162 D x 23 H; X 66, Y 77.05, Z 6 |
| Clear space over power supply | 25.7 to shelf underside |
| Retaining walls | 3 thick, 10 high, 0.6 fit clearance; Y 5..240 |
| Shelf rear cable opening | Y 240..281.85, full interior width |
| Seven fan frames | 40 x 40 x 20; bodies Y -20..0 |
| PSU fan X/Z centres | (77,26), (127,26) |
| Under-DGX fan X/Z centres | (77,70), (127,70) |
| Over-DGX fan X/Z centres | (52,125), (102,125), (152,125) |
| Fan apertures / screw pitch / screw bores | diameter 35 / 32 / diameter 3.4 |
| Cap face thickness | 4 |
| Cap mounting bores | diameter 3; body blind depth 15 |
| Cap screw X/Z centres | (0,18), (204,18), (0,138), (204,138) |
| LCD module envelope | 164.9 x 124.27 x 8.3, centred X 102 / Z 75 |
| LCD window | 156 x 89 |
| LCD mounting pitch / bores / standoffs | 156.9 x 114.96 / diameter 3.25 / 6.7 |
| LCD hardware to nearest fan face | 25.4 clear |
| Body side diamond vents | 24 long x 12 high |
| Cap side diamond vents | 20 long x 10 high |

The provisional PSU size comes from the latest four-bay design. Its match to
the supplied Acer adapter is not confirmed. LCD dimensions come from
[the retained Waveshare reference](waveshare-7inch-lcd-display-b.md).

## Cross-sections

Front view, LCD cap removed:

```text
          curved roof
       /  O   O   O  \       upper DGX fans
      (               )
      (    O     O    )       lower DGX fans
      ( ===U=====U=== )       fixed shelf, open troughs
      (    O     O    )       PSU fans
       \_____________/
```

Side view, front at left:

```text
LCD cap     fans | fixed plate              open rear
| LCD | 25.4 |20||============================== roof
|     | clear   ||   air above DGX --------->
|     |         ||       [ DGX ]
|     |         ||______ troughs __________   cable gap
|     |         ||       [ PSU ]
|_______________||_____________________________ floor
                 ^ print starts here, grows rearward
```

Top view through DGX shelf:

```text
FRONT: integral fan plate
+-----------------------------------------+
| wall | rail | trough | land | trough | rail | wall
|      |      |   air front to rear    |      |
|      |      |   DGX rests on lands   |      |
|------ fixed shelf ends at Y=240 ------------|
|              open cable space              |
+---------------- open rear -----------------+
```

## Assembly and printing

Build with `python build_acer_v14.py`, then
`node concept-v14/package_plates.cjs`. Open
`concept-v14/acer-dgx-enclosure-v14-separate-plates.3mf` in Bambu Studio.
Plate one is the body with the fan plate on the bed. Plate two is the cap with
its LCD face on the bed. Both use the existing H2D 0.20 mm profile.

Mount the seven fans on the front of the fixed plate; their bodies sit inside
the cap. Orient airflow toward the devices. The two lower DGX apertures open
directly into continuous channels beneath the device. The upper row opens
above it. Side diamonds in the cap supply intake air.

Install the LCD on its four existing-pattern standoffs. Attach the full-outline
cap through four aligned 3 mm holes. These are plain bores, not printed threads.
Choose plastic-compatible screws after a fit coupon; nominal M3 clearance can
be tight after printing. The cap has a 57.7 mm screw path before the body; select
screw length for that path plus engagement, without exceeding the 15 mm blind
depth. Device insertion is through the open rear. Longitudinal walls constrain
side movement; rearward retention requires an external strap if transported.

The face, shelf and guide walls grow from the first printed fan plate.
Thirty-degree transitions behind the fan bores avoid unsupported shelf and
guide starts. Diamond
vent ends grow at no more than 45 degrees. No removable shelf fasteners or
separate fan carrier are needed. Automatic support detection is checked with
`powershell -NoProfile -File concept-v14/run_support_audit.ps1`, followed by
`python concept-v14/check_support_audit.py`.

CAD checks cover single solids, device and fan fit, insertion from the rear,
uninterrupted troughs, trough floor, screw bores and the 25.4 mm gap. Export
checks require connected closed meshes and H2D bounds. Physical load, screw
fit and thermal performance are not measured by these checks.

## Changelog

- 2026-11-22: Combine curved v13 layout with permanent shelf retaining walls;
  add two continuous under-DGX channels and seven fan positions; integrate
  fan plate and shelf; print fan plate first; add matching screw-on LCD cap.
