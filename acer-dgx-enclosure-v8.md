# Stackable Acer enclosure v8

Parametric source: `build_acer_v8.py`. Dimensions are millimetres, with X across
the case, Y toward the rear, and Z upward. Earlier numbered files preserve the
design iterations; v8 is the current design.

| Feature | Dimension |
|---|---|
| Outer width / depth / total height | 280 / 251.6 / 166.9 |
| Acer seat elevation | 36.4 |
| Power brick seat elevation | 49.1 |
| Provisional brick envelope | 70 x 160 x 36 |
| Fan envelope, four positions | 40 x 40 x 20 |
| Removable fan plate | 271.2 x 101.5 x 4 |
| Plate attachment | Four M3 x 12 screws |
| Plate holes / body pilots | Diameter 3.4 / 2.5 |
| Body pilot depth | 10 |
| Front cable opening width | 112.5 |
| Divider passage length | 151.2 |
| LCD pivot Y / Z | 11 / 145.53235 |

Top view:
```
                  REAR
  +----------------+------------------------+
  | power brick    | Acer                   |
  | left shelf    : : right shelf           |
  |              : :                       |
  +-----------------------------------------+
  | fan           fan       fan       fan   |
  |              hinged LCD                 |
                  FRONT
```

Side view:
```
  +---------- integral ventilated roof -----+
  | LCD hinge                               |
  | /       fans       equipment            |
  |/             raised shelves             |
  |              cable space                |
  +---------- filled vented floor -----------+
       nesting foot below / recess above
```

Front view: the power fan is on the left; three Acer fans span the right.
The LCD swings outward in front of the removable fan plate.

## Build and assembly

Install CadQuery in a Python environment, then run `python build_acer_v8.py`.
Run `node concept-v8/package_plates.cjs` to package the generated meshes using
the checked-in H2D configuration in `cad-config/h2d-project-settings.json`.
Open the generated three-plate 3MF in Bambu Studio. Plate 1 contains the upright
enclosure; plates 2 and 3 contain the face-down LCD and fan mounts.

Tap the four body pilot holes M3 before fitting four M3 x 12 screws. Printed
threads and heat-set inserts are not modeled. Open the LCD to 75 degrees to
withdraw the fan plate forward. Mount the fans behind the plate, Y29 through
Y49. Measure the actual power brick before production.

The generator checks solid validity, rounded edges, device fit, LCD movement,
fan envelopes, stacking, and sampled fan-plate removal positions. These are
CAD checks, not a physical fit test. The project is unsliced; supports and
material settings need to be chosen before printing.

## Changelog

- v8: removable fan plate, four M3 mounts and three print plates.
- v7: enlarged cable passages and forward LCD pivot.
- v6: filled ventilated bottom, raised brick shelf and reduced overall height.
- v5: integral roof, raised Acer shelf and full-height LCD reinforcement.
- v1-v4: initial enclosure and LCD concepts.
