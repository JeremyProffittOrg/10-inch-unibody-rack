# Four-bay Acer GN100 shelves

A one-piece, open-front four-bay rack. Each bay holds an Acer GN100 on the right and its external power brick on the left. Five shelves and both outside walls are 5 mm thick. The back is open except for twelve fan mounts and their support posts. All CAD edges have 0.5 mm fillets; cable-window plan corners have 3 mm radii.

## Hardware basis and remaining uncertainty

The GN100 body envelope is 150 W x 150 D x 50.5 H mm. The previous enclosure's 70 x 160 x 36 mm power brick was explicitly provisional and is not reused here.

The candidate power brick is the Delta ADP-240KB BA, 72 W x 162 D x 23 H mm. Those dimensions are published by Delta in its [manufacturer specification](https://filecenter.deltaww.com/Products/download/02/0201/Products-202310190855436362.pdf). Acer confirms a [240 W USB-C adapter](https://community.acer.com/en/en/kb/articles/19556-getting-started-with-the-acer-veriton-gn100-ai-workstation), but does not identify the exact brick model there. The match to the operator's supplied Acer adapter remains UNCONFIRMED. Read its label or measure it before printing tight retainers. No physical fit or cooling test has been performed.

## Dimensions

| Parameter | mm |
|---|---:|
| Overall width / height / printed depth | 298 / 315 / 229.8 |
| Rear shelf extension beyond DGX body | 76.2 (3 inches) |
| DGX front offset from rack front | 3.6 |
| Shelf and outer wall thickness | 5 |
| Shelf pitch / bay clear height | 77.5 / 72.5 |
| Clearance over each DGX | 22 |
| Nominal outer and inter-device side gaps | 22 |
| PSU body W / D / H | 72 / 162 / 23 |
| DGX body W / D / H | 150 / 150 / 50.5 |
| Device fitting clearance, per edge | 0.6 |
| Retainer height / thickness | 10 / 3 |
| Front/rear corner return onto body width | 5 |
| Rear guide ramp run | 10 |
| Cable opening start behind each device | 12.7 (0.5 inch) |
| Cable opening end before rack rear | 25.4 (1 inch) |
| DGX cable opening, throat | 120 W x 38.1 D |
| PSU cable opening, throat | 57.6 W x 26.1 D |
| Cable-window inside corner / all-edge radius | 3 / 0.5 |
| Fan body outline / mount outline | 40 x 40 / 44 x 44 |
| Fan airflow aperture / screw clearance | diameter 35 / diameter 3.4 |
| Fan screw pitch / DGX fan-pair centre spacing | 32 / 154 |
| Rear mount thickness / supporting post width | 5 / 3 |

The 22 mm side gaps are measured from device bodies to walls or the other device body. The retaining rails occupy part of these gaps at the bottom 10 mm. This is deliberate: the rails are inside the established overall envelope. With the corrected PSU width, overall width is 5 + 22 + 72 + 22 + 150 + 22 + 5 = 298 mm.

## Coordinates and component positions

Use coordinates: X = width, Y = height, Z = depth toward rear. Origin is front-bottom-left. Printing rotates the rack so the rear sits on the bed: [X,Y,Z] maps to [Y,X,229.8-Z]. The print bounds are 315 x 298 x 229.8 mm, within the project's 325 x 320 x 325 mm single-nozzle H2D limits.

| Component | Position / bounding box |
|---|---|
| Five shelves | X 0..298, Y 77.5i..77.5i+5, Z 0..229.8; i=0..4 |
| Left/right walls | X 0..5 / 293..298, Y 0..315, Z 0..229.8 |
| PSU body, each bay | X 27..99, Y 5+77.5i..28+77.5i, Z 3.6..165.6 |
| DGX body, each bay | X 121..271, Y 5+77.5i..55.5+77.5i, Z 3.6..153.6 |
| Retainers | 0.6 mm from body edges; 3 mm thick; Y shelf top..top+10 |
| Rear fan centres | X 63,119,273; Y 41.25+77.5i; Z 224.8..229.8 |
| Cable passage centres | X 63 and 196; Z 178.3..204.4 for PSU, 166.3..204.4 for DGX; through all five shelves |

### Front section

~~~text
    5 | 22 | PSU 72 | 22 | DGX 150 | 22 | 5   = 298
  +------------------------------------------------+
  |          air       |       22 mm air            |
  | PSU (23 high)      |       DGX (50.5 high)       |
  +================ 5 mm shelf ====================+
  |                   repeat four bays             | 315
  +================================================+
~~~

### Top section of a shelf

~~~text
REAR: +--open--[PSU FAN]--open--[DGX FAN][DGX FAN]--open--+
      |          rounded            rounded             |
      |          cable hole         cable hole          | last 50.8
      |                                                 |
      |   rear corner stops       rear corner stops     | 76.2 past DGX
      |  +----------------+     +-------------------+   |
      |  |   PSU 72x162   |     |    DGX 150x150    |   |
      |  +----------------+     +-------------------+   |
FRONT +---5 mm corner returns; middle edges stay open----+
~~~

### Side section of a bay

~~~text
            top shelf
  +------------------------------------------------------+
  |                  22 mm above DGX                     |
  | +-----------------------+                 [rear fan] |
  | |       DGX 50.5        |                            |
  | +-----------------------+  cables                    |
  +--- shelf --- retainer ---\--- rounded opening --------+
     front       10 mm       45 degree guide ramp
                  <---76.2 mm beyond DGX rear----------->
~~~

## Fan and cable details

There are three fan mounts in every bay: two at the far edges of the DGX lane including both 22 mm side gaps and one aligned to the centre of the PSU. Each mount supports a standard 40 x 40 mm frame with 32 mm mounting-hole pitch. A 35 mm circular opening preserves the screw pads; a full 40 x 40 mm through-cut would remove those pads. There are 48 M3 clearance holes in total. Screws/nuts and fans are separate hardware. Fans sit outside the rear mounting face; choose screw length for the actual fan thickness plus the 5 mm mount and nut.

Outside the three rings and their posts, the rear is open. The outer wall directly supports the far-right fan, so no redundant thin post is used there. The DGX 40 mm fan bodies span X=99..139 and X=253..293, aligned with the outer edges of its two side gaps.

Each shelf has two rounded rectangular cable windows. Widths are 80% of the respective body widths: 120 mm for DGX and 57.6 mm for PSU. Each begins 12.7 mm behind its device and ends 25.4 mm before the rack rear. Thus DGX depth is 38.1 mm and PSU depth is 26.1 mm. Corners are R3 in plan. Nominal dimensions are at the straight throat; R0.5 edge lips flare the openings by up to 0.5 mm at each surface.

The device retainers have full side guides and short front/rear corner returns. The middle of both front and rear ends remains open for connectors and strain relief. Insert a device from the front above the 10 mm lips, then lower it into the pocket. The 22 mm space above a DGX permits the 10 mm lift. Do not force a device into an unverified pocket.

## Print and validation

The STL retains its rear-face-down orientation and 315 x 298 x 229.8 mm print bounds. The new wide rounded cable windows replace the tapered diamond openings. Their closing edges can require support in this orientation. Support-free printing is not claimed for this revision; review support placement and layer preview before printing.

The generator reuses the repository's CadQuery dependency for true three-dimensional fillets. Every geometric surface discontinuity is filleted at R0.5 mm, including outer shell, guides, fan mounts, screw bores and window lips. Native CAD validation requires one valid solid with zero remaining sharp edges. Mesh checks require a closed, consistently oriented, connected STL and unchanged printer bounds. Device-envelope, insertion-path and cable-path intersection checks protect fit. No physical fit, structural load or cooling test has been performed.

Build from the repository root:

~~~text
C:/Users/Jeremy/.local/bin/uv.exe run --python 3.13 --with cadquery==2.8.0 --with matplotlib python build_acer_four_bay.py
~~~

OpenSCAD must be installed. Linux uses openscad from PATH. This generator writes STL, validation JSON, logs, front/rear 1024 PNGs, and four annotated diagrams under output/acer-four-bay/.

The geometry source is acer_four_bay_geometry.py. The SCAD file is a mesh viewer, not a second implementation. Its view selector supports print (default), assembly, colored, xray, and shelf. The shelf inspection view includes one bay; the delivered STL is the complete connected rack.

## Diagrams

- [Assembly front](output/acer-four-bay/assembly-front.png)
- [Assembly rear](output/acer-four-bay/assembly-rear.png)

- [Front layout](output/acer-four-bay/front-layout.png)
- [Shelf plan and cable passages](output/acer-four-bay/shelf-plan.png)
- [Rear fan mounts](output/acer-four-bay/rear-fans.png)
- [Retainer detail](output/acer-four-bay/retainer-detail.png)

## Changelog

- 2026-11-16: Added four-bay shelves, left PSU pockets, 76.2 mm rear extension, twelve fan mounts, ten cable passages and 10 mm corner retainers. Replaced the previous provisional brick envelope with published Delta ADP-240KB BA dimensions; exact Acer OEM identity remains unconfirmed.

- 2026-11-16: Moved DGX fans outward across the full 194 mm lane; enlarged cable windows to 80% body width with the requested front/rear lands; rounded all edges at R0.5 and window plan corners at R3. The separate 2 mm-base fit-test coupon remains unchanged.
