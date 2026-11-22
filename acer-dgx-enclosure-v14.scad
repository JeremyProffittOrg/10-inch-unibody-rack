/**
 * Fan-first curved enclosure. Build with python build_acer_v14.py.
 * Print coordinates: X width, Y inverted use height, Z rearward depth.
 * Origin: front plate bounding-box corner on the bed.
 * Component index:
 * shell: 248 x 168 x 281.85 mm; fixed shelf and seven-fan plate.
 * lcd: 248 x 168 x 57.7 mm; separate screw-on full-outline front cap.
 * Assembly imports use X right, Y rearward, Z upward.
 */
part="assembly";
width_mm=248;
height_mm=168;
depth_mm=281.85;
cap_depth_mm=57.7;
axis_length_mm=30;
axis_thickness_mm=1;
assert(width_mm<=325 && height_mm<=320 && depth_mm<=325);

// Main single solid, fan plate on Z=0; bounds 0..width/height/depth.
module shell_print() { import("output/acer-v14/shell.stl"); }
// Separate face-down cap; same X/Y bounds, depth cap_depth_mm.
module lcd_print() { import("output/acer-v14/lcd.stl"); }
// Assembled use orientation; the cap rear meets the fan plate at Y=0.
module assembly_colored() {
    color("SlateGray") import("output/acer-v14/shell-assembly.stl");
    color("Orange") import("output/acer-v14/lcd-assembly.stl");
}
// Transparent shell exposes the fixed shelf and under-DGX channels.
module assembly_xray() {
    color([.3,.5,.6,.35]) import("output/acer-v14/shell-assembly.stl");
    color([1,.6,.2,.35]) import("output/acer-v14/lcd-assembly.stl");
}
// Three positive axes from origin; each axis_length_mm long.
module debug_axes() {
    color("red") cube([axis_length_mm,axis_thickness_mm,axis_thickness_mm]);
    color("green") cube([axis_thickness_mm,axis_length_mm,axis_thickness_mm]);
    color("blue") cube([axis_thickness_mm,axis_thickness_mm,axis_length_mm]);
}
if(part=="shell") shell_print();
else if(part=="lcd") lcd_print();
else assembly_colored();
