# 10-Inch Unibody Server Rack

A parametric, unibody 10-inch server rack designed to 3D print in a single piece on the **Bambu Labs H2D**. Prints front-face-down with **zero supports required**.

## Features

- **6U capacity** with standard EIA-310 mounting hole pattern
- **Prints in one piece** - no assembly required
- **No supports needed** - all geometry is self-supporting when printed face-down
- **Rounded exterior edges** for clean aesthetics and handling comfort
- **M6 nut traps** with diamond bevels for captive hardware
- **Grip bars** and filleted handle cutouts for comfortable carrying
- **Open back** for ventilation and cable management
- **Parametric design** - easily adjust rack units, depth, wall thickness
- **LCD + Raspberry Pi cases** in single/dual landscape and portrait layouts
- **Parametric viewing angle** with enclosure depth derived from the chosen angle

## Designs

### Stackable Acer GN100 enclosure (v8)

The latest Acer design is [v8](acer-dgx-enclosure-v8.md), with an integral
ventilated roof and bottom, a left power-brick bay, a hinged LCD mount, and a
removable four-fan plate with M3 attachment bosses. The enclosure, LCD mount,
and fan plate are packaged on three separate H2D plates. Earlier concepts and
their design notes are retained for reference.

Build with CadQuery using `python build_acer_v8.py`, then run
`node concept-v8/package_plates.cjs`. Open the resulting
`concept-v8/acer-dgx-enclosure-v8-separate-plates.3mf` in Bambu Studio.
The SCAD assembly viewer imports those generated meshes, so run the CAD build
before opening it. Generated meshes, STEP files and slicer projects stay local.
This enclosure has not been verified for support-free printing; tune supports
and material settings before printing. The brick dimensions remain provisional.

### Just a Rack (6U)

| Front View | Rear View |
|------------|-----------|
| ![Front](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/just-a-rack_front.png) | ![Rear](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/just-a-rack_rear.png) |

Unibody 6U 10-inch server rack with M6 nut traps, 18mm grip bars, filleted handle cutouts, and 30mm deep mounting rails. Prints support-free on the Bambu Labs H2D.

**Download STL**: [just-a-rack.stl](https://github.com/JeremyProffitt/10-inch-unibody-rack/releases/latest/download/just-a-rack.stl)

### Just a Rack with Pocket (6U)

| Front View | Rear View |
|------------|-----------|
| ![Front](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/just-a-rack-with-pocket_front.png) | ![Rear](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/just-a-rack-with-pocket_rear.png) |

Same rack with a USW Flex Mini pocket on the right interior wall. Includes a 45-degree support ramp and triangular cable routing cutout for support-free printing.

**Download STL**: [just-a-rack-with-pocket.stl](https://github.com/JeremyProffitt/10-inch-unibody-rack/releases/latest/download/just-a-rack-with-pocket.stl)

### Rack with Cubbies (6U)

| Front View | Rear View |
|------------|-----------|
| ![Front](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/rack-with-cubbies_front.png) | ![Rear](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/rack-with-cubbies_rear.png) |

Same rack with a 55mm cubby extension on the right side featuring horizontal shelves every 4 inches for accessory storage.

**Download STL**: [rack-with-cubbies.stl](https://github.com/JeremyProffitt/10-inch-unibody-rack/releases/latest/download/rack-with-cubbies.stl)

### Rack with Cubbies and Pocket (6U)

| Front View | Rear View |
|------------|-----------|
| ![Front](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/rack-with-cubbies-with-pocket_front.png) | ![Rear](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/rack-with-cubbies-with-pocket_rear.png) |

Cubby rack with a USW Flex Mini pocket on the divider wall between the rack interior and cubbies. Combines storage cubbies with the built-in switch pocket.

**Download STL**: [rack-with-cubbies-with-pocket.stl](https://github.com/JeremyProffitt/10-inch-unibody-rack/releases/latest/download/rack-with-cubbies-with-pocket.stl)

### Just a Rack Short (6U)

| Front View | Rear View |
|------------|-----------|
| ![Front](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/just-a-rack-short_front.png) | ![Rear](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/just-a-rack-short_rear.png) |

Shorter-depth variant of the standard unibody rack. Same M6 nut traps, grip bars, and handle cutouts as the full rack, but with a reduced front-to-back depth for locations with less clearance.

**Download STL**: [just-a-rack-short.stl](https://github.com/JeremyProffitt/10-inch-unibody-rack/releases/latest/download/just-a-rack-short.stl)

### Just a Rack with Pocket Short (6U)

| Front View | Rear View |
|------------|-----------|
| ![Front](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/just-a-rack-with-pocket-short_front.png) | ![Rear](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/just-a-rack-with-pocket-short_rear.png) |

Short-depth rack body with the built-in USW Flex Mini pocket on the right interior wall. Combines the compact depth of the short variant with the integrated switch storage of the pocket variant.

**Download STL**: [just-a-rack-with-pocket-short.stl](https://github.com/JeremyProffitt/10-inch-unibody-rack/releases/latest/download/just-a-rack-with-pocket-short.stl)

### Waveshare 7-Inch LCD Panel

| Front View | Rear View |
|------------|-----------|
| ![Front](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/waveshare-7inch-lcd-panel_front.png) | ![Rear](https://raw.githubusercontent.com/JeremyProffitt/10-inch-unibody-rack/master/assets/waveshare-7inch-lcd-panel_rear.png) |

Panel mount for the [Waveshare 7-inch LCD Display (Model B)](waveshare-7inch-lcd-display-b.md). Fits into a standard 10-inch rack panel slot, turning the LCD into a rack-mounted display.

**Documentation**: [waveshare-7inch-lcd-display-b.md](waveshare-7inch-lcd-display-b.md)

**Download STL**: [waveshare-7inch-lcd-panel.stl](https://github.com/JeremyProffitt/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-panel.stl)

### Waveshare LCD + Pi Case - Landscape

| Front View | Rear View |
|------------|-----------|
| ![Front](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-landscape_front.png) | ![Rear](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-landscape_rear.png) |

Closed landscape enclosure with a solid-bottom Pi tray, removable LCD lid, 25.4 mm internal connector service region, five localized 10 mm cable passages, and a parametric 35-degree display plane.

**Documentation**: [waveshare-7inch-lcd-case-landscape.md](waveshare-7inch-lcd-case-landscape.md)

**Download Base STL**: [waveshare-7inch-lcd-case-landscape-base.stl](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-landscape-base.stl)

**Download Lid STL**: [waveshare-7inch-lcd-case-landscape-lid.stl](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-landscape-lid.stl)

### Waveshare LCD + Pi Case - Portrait

| Front View | Rear View |
|------------|-----------|
| ![Front](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-portrait_front.png) | ![Rear](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-portrait_rear.png) |

Closed portrait enclosure with the LCD in a removable cap, the Pi on a solid floor behind it, top/right internal service regions, and only small 10 mm cable passages through the walls.

**Documentation**: [waveshare-7inch-lcd-case-portrait.md](waveshare-7inch-lcd-case-portrait.md)

**Download Base STL**: [waveshare-7inch-lcd-case-portrait-base.stl](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-portrait-base.stl)

**Download Lid STL**: [waveshare-7inch-lcd-case-portrait-lid.stl](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-portrait-lid.stl)

### Waveshare LCD + Pi Case - Dual Portrait Side-by-Side

| Front View | Rear View |
|------------|-----------|
| ![Front](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-dual-portrait-side-by-side_front.png) | ![Rear](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-dual-portrait-side-by-side_rear.png) |

Two portrait LCDs in one removable lid above a solid-bottom Pi enclosure, with a shared internal cable region, continuous walls, localized 10 mm cord passages, and a 35-degree default angle.

**Documentation**: [waveshare-7inch-lcd-case-dual-portrait-side-by-side.md](waveshare-7inch-lcd-case-dual-portrait-side-by-side.md)

**Download Base STL**: [waveshare-7inch-lcd-case-dual-portrait-side-by-side-base.stl](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-dual-portrait-side-by-side-base.stl)

**Download Lid STL**: [waveshare-7inch-lcd-case-dual-portrait-side-by-side-lid.stl](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-dual-portrait-side-by-side-lid.stl)

### Waveshare LCD + Pi Case - Dual Landscape Stacked

| Front View | Rear View |
|------------|-----------|
| ![Front](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-dual-landscape-stacked_front.png) | ![Rear](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-dual-landscape-stacked_rear.png) |

Two stacked landscape LCDs in a removable lid above a closed solid-bottom Pi tray, with continuous walls, five small cable passages, right-side internal connector clearance, and angle-derived enclosure depth.

**Documentation**: [waveshare-7inch-lcd-case-dual-landscape-stacked.md](waveshare-7inch-lcd-case-dual-landscape-stacked.md)

**Download Base STL**: [waveshare-7inch-lcd-case-dual-landscape-stacked-base.stl](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-dual-landscape-stacked-base.stl)

**Download Lid STL**: [waveshare-7inch-lcd-case-dual-landscape-stacked-lid.stl](https://github.com/JeremyProffittOrg/10-inch-unibody-rack/releases/latest/download/waveshare-7inch-lcd-case-dual-landscape-stacked-lid.stl)

## Print Instructions

1. **Orientation**: Place the front face (Z=0) down on the build plate
2. **Supports**: None needed
3. **Material**: PLA, PETG, or ASA
4. **Infill**: 20-30%
5. **Layer Height**: 0.2mm
6. **Bed Adhesion**: Brim recommended (large footprint)

## Building Locally

### Linux/macOS

```bash
./build.sh
```

### Windows

```batch
generate.bat
```

Output files (STL and PNG) are generated in the `output/` directory.

## References

- [10-inch rack dimensions (Jeff Geerling - Project MINI RACK)](https://mini-rack.jeffgeerling.com/)
- [EIA-310 rack standard (Wikipedia)](https://en.wikipedia.org/wiki/19-inch_rack)
- [Bambu Labs H2D specifications](https://bambulab.com/en-us/h2d/tech-specs)

## License

Open source hardware. See individual files for details.
