# Four-bay Acer GN100 shelves

A one-piece, open-front four-bay rack. Each bay holds an Acer GN100 on the right and its external power brick on the left. Five shelves are 3 mm thick; both outside walls are 25 mm thick. The shelves extend 25.4 mm farther forward, with full front retaining walls. The back is open except for twelve fan mounts and their support posts. All CAD edges have 0.5 mm fillets; cable-window plan corners have 3 mm radii.

## Hardware basis and remaining uncertainty

The GN100 body envelope is 150 W x 150 D x 50.5 H mm. The previous enclosure's 70 x 160 x 36 mm power brick was explicitly provisional and is not reused here.

The candidate power brick is the Delta ADP-240KB BA, 72 W x 162 D x 23 H mm. Those dimensions are published by Delta in its [manufacturer specification](https://filecenter.deltaww.com/Products/download/02/0201/Products-202310190855436362.pdf). Acer confirms a [240 W USB-C adapter](https://community.acer.com/en/en/kb/articles/19556-getting-started-with-the-acer-veriton-gn100-ai-workstation), but does not identify the exact brick model there. The match to the operator's supplied Acer adapter remains UNCONFIRMED. Read its label or measure it before printing tight retainers. No physical fit or cooling test has been performed.

## Dimensions

| Parameter | mm |
|---|---:|
| Overall width / height / printed depth | 298 / 297 / 255.2 |
| Rear shelf extension beyond DGX body | 76.2 (3 inches) |
| Added front shelf length | 25.4 (1 inch) |
| DGX front offset from rack front | 29 |
| Shelf / outer wall thickness | 3 / 25 |
| Shelf pitch / bay clear height | 73.5 / 70.5 |
| Clearance over each DGX | 20 |
| Nominal outer / inter-device side gaps | 2 / 22 |
| PSU body W / D / H | 72 / 162 / 23 |
| DGX body W / D / H | 150 / 150 / 50.5 |
| Device fitting clearance, per edge | 0.6 |
| Retainer height / ordinary wall thickness | 10 / 3 |
| Shared divider width / full-height depth | 20.8 / 194.6 |
| Front retaining wall | full pocket width |
| DGX rear corner return onto body width | 5 |
| PSU rear opening / clear pocket width | 36.6 / 73.2 (50%) |
| Rear guide ramp run | 10 |
| Cable opening start behind each device | 12.7 (0.5 inch) |
| Cable opening end before rack rear | 25.4 (1 inch) |
| DGX cable opening, throat | 120 W x 38.1 D |
| PSU cable opening, throat | 57.6 W x 26.1 D |
| Cable-window inside corner / all-edge radius | 3 / 0.5 |
| Fan body outline / mount outline | 40 x 40 / 44 x 44 |
| Fan airflow aperture / screw clearance | diameter 35 / diameter 3.4 |
| Fan screw pitch / DGX fan-pair centre spacing | 32 / 114 |
| Rear mount thickness / supporting post width | 5 / 3 |
| Front screw-hole throat diameter / depth | 3 / 15 |
| Front screw-hole vertical pitch / count per side | 15 / 18 |
| Front screw-hole row X positions | 12.5 / 285.5 |
| Front screw-hole first / last Y centres | 21 / 276 |
| Minimum hole-mouth clearance from outside top/bottom | 19 (required minimum 15) |

The device positions in X remain unchanged. The thicker shell leaves 2 mm between each outer device body and its wall; the body-to-body separation remains 22 mm. A solid 20.8 mm-wide divider now fills that separation except for 0.6 mm fitting clearance beside each device. The outside guides merge into the shell. Width is 25 + 2 + 72 + 22 + 150 + 2 + 25 = 298 mm. The devices and rear features move 25.4 mm rearward in the new front-origin coordinates. The new front retaining walls sit at the extended front edge; each pocket gains 25.4 mm of front-to-back space.

## Coordinates and component positions

Use coordinates: X = width, Y = height, Z = depth toward rear. Origin is front-bottom-left. Printing rotates the rack so the rear sits on the bed: [X,Y,Z] maps to [Y,X,255.2-Z]. The print bounds are 297 x 298 x 255.2 mm, within the project's 325 x 320 x 325 mm single-nozzle H2D limits.

| Component | Position / bounding box |
|---|---|
| Five shelves | X 0..298, Y 73.5i..73.5i+3, Z 0..255.2; i=0..4 |
| Left/right walls | X 0..25 / 273..298, Y 0..297, Z 0..255.2 |
| PSU body, each bay | X 27..99, Y 3+73.5i..26+73.5i, Z 29..191 |
| DGX body, each bay | X 121..271, Y 3+73.5i..53.5+73.5i, Z 29..179 |
| Front screw holes | X centres 12.5/285.5; Y 21+15i, i=0..17; Z 0..15 |
| Ordinary retainers | 0.6 mm from body edges; 3 mm thick; Y shelf top..top+10 |
| Shared divider, each bay | X 99.6..120.4; Y shelf top..top+10; Z 0..194.6 at full height, ramp to Z=204.6 |
| Rear fan centres | X 63,139,253; Y 38.25+73.5i; Z 250.2..255.2 |
| Cable passage centres | X 63 and 196; Z 203.7..229.8 for PSU, 191.7..229.8 for DGX; through all five shelves |

### Front section

~~~text
   25 | 2 | PSU 72 | 22 | DGX 150 | 2 | 25   = 298
  +------------------------------------------------+
  o          air       |       20 mm air            o
  o PSU (23 high)      |       DGX (50.5 high)       o
  +================ 3 mm shelf ====================+
  |                   repeat four bays             | 297
  +================================================+
~~~

### Top section of a shelf

~~~text
REAR: +--open--[PSU FAN]--open--[DGX FAN][DGX FAN]--open--+
      |          rounded            rounded             |
      |          cable hole         cable hole          |
      |                                                 |
      |   50% rear opening        rear corner stops     | 76.2 past DGX
      |  +----------------+     +-------------------+   |
      |  |   PSU 72x162   |#####|    DGX 150x150    |   |
      |  +----------------+#####+-------------------+   |
      |         # = continuous shared divider          |
      |           25.4 mm added front space             |
FRONT +---full PSU front wall-----full DGX front wall----+
~~~

### Side section of a bay

~~~text
            top shelf
  +------------------------------------------------------+
  |                  20 mm above DGX                     |
  | +-----------------------+                 [rear fan] |
  | |       DGX 50.5        |                            |
  | +-----------------------+  cables                    |
  +--- shelf --- retainer ---\--- rounded opening --------+
     full front wall (10 mm high); 25.4 mm extra front shelf
                  <---76.2 mm beyond DGX rear----------->
~~~

## Front screw holes

Each outside front wall has eighteen unthreaded blind holes, centred in its 25 mm thickness. The two rows lie at X=12.5 and X=285.5 mm. Hole centres run from Y=21 to Y=276 mm at exactly 15 mm intervals. Each hole has a 3 mm cylindrical throat and extends 15 mm from the front face toward the rear. R0.5 mouth rounding flares the opening to 4 mm at the face; the blind floor edge is also rounded. The nearest rounded mouth edge is 19 mm from each outside top/bottom edge, exceeding the required 15 mm minimum. No threaded geometry or screw hardware is included.

~~~text
Front view:                     Side cut through one hole:
X=12.5             X=285.5       front Z=0          Z=15
  o                    o         ---> (3 mm bore) ---| solid wall
  | 15 mm pitch        |
  o                    o         Hole stops inside the side wall.
Y=21,36,...,276 on both sides.
~~~

## Fan and cable details

There are three fan mounts in every bay: two moved inward to clear the thicker outer walls and one aligned to the centre of the PSU. Each mount supports a standard 40 x 40 mm frame with 32 mm mounting-hole pitch. A 35 mm circular opening preserves the screw pads; a full 40 x 40 mm through-cut would remove those pads. There are 48 M3 clearance holes in total. Screws/nuts and fans are separate hardware. Fans sit outside the rear mounting face; choose screw length for the actual fan thickness plus the 5 mm mount and nut.

Outside the three rings and their posts, the rear is open. The outer wall directly supports the far-right fan, so no redundant thin post is used there. The DGX 40 mm fan bodies span X=119..159 and X=233..273. Fan centres are X=139 and X=253; their 35 mm airflow bores clear the thick outside walls.

Each shelf has two rounded rectangular cable windows. Widths are 80% of the respective body widths: 120 mm for DGX and 57.6 mm for PSU. Each begins 12.7 mm behind its device and ends 25.4 mm before the rack rear. Thus DGX depth is 38.1 mm and PSU depth is 26.1 mm. Corners are R3 in plan. Nominal dimensions are at the straight throat; R0.5 edge lips flare the openings by up to 0.5 mm at each surface.

The device retainers have outer side guides and full-width front walls at the extended shelf edge. The two former inner guides and their gap are replaced by one solid shared divider, 20.8 mm wide and 10 mm high. It runs continuously from the front to Z=194.6, then slopes down to the shelf by Z=204.6. The divider connects both front walls and preserves the 0.6 mm clearance to each device. DGX rear corners retain their 5 mm stops. Each PSU rear wall leaves a centered 36.6 mm opening, exactly half the 73.2 mm clear pocket width. Its remaining end sections are vertical, without ramps into the cable windows. The outer guides, shared divider and DGX rear stops retain 45-degree rear ramps. All retainers are 10 mm high. Ordinary retaining walls are 3 mm thick; the shared divider is 20.8 mm wide. Insert devices from the front above the walls, then lower them into their pockets; the 20 mm clearance above each DGX permits this lift. Connector and physical PSU fit remain unverified.

## Print and validation

The STL retains its rear-face-down orientation and 297 x 298 x 255.2 mm print bounds. The new wide rounded cable windows replace the tapered diamond openings. Their closing edges can require support in this orientation. Support-free printing is not claimed for this revision; review support placement and layer preview before printing.

The generator reuses the repository's CadQuery dependency for true three-dimensional fillets. Every geometric surface discontinuity is filleted at R0.5 mm, including outer shell, guides, fan mounts, screw bores and window lips. Native CAD validation requires one valid solid with zero remaining sharp edges. Mesh checks require a closed, consistently oriented, connected STL and the revised printer bounds. Native checks verify all five 3 mm shelf sections and the thirty-six screw-hole diameters and blind floors. Exported STL checks verify all thirty-six open bore paths. Each divider must contain its entire interior test volume without gaps. Hole checks include the rounded-mouth top/bottom clearance. Device-envelope, insertion-path and cable-path intersection checks protect fit. No physical fit, structural load or cooling test has been performed.

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

- 2026-11-20: Extended the shelves 25.4 mm at the front, added full front retaining walls, left the centered 50% of each PSU rear wall open, and thickened outside walls to 25 mm while retaining 298 mm overall width. Moved DGX fans inward; preserved 5 mm fan-mount depth, device sizes, and bay height.

- 2026-11-21: Reduced each bay clear height by 2 mm and all five shelves by 2 mm, including top and bottom. Total height is 297 mm; DGX overhead clearance is 20 mm. Added forty front blind holes: 3 mm throat, 15 mm depth and 15 mm pitch, twenty per side.

- 2026-11-21: Removed the end holes to leave eighteen per side, with 19 mm from rounded mouths to the outside top/bottom. Replaced separate inner rails with a solid 20.8 mm-wide, 10 mm-high shared divider on each device shelf.
