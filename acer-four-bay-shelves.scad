/**
 * Rounded four-bay Acer shelf viewer. Geometry is built by acer_four_bay_geometry.py.
 * Assembly: X width, Y height, Z rearward; origin front-bottom-left.
 * Print: [X,Y,Z] -> [Y,X,depth-Z], rear face on Z=0.
 * Component index: five 3 mm shelves at Y=73.5*i; 25 mm outer walls X=0/273;
 * four continuous 10 mm-high shared dividers; eight retaining pockets; twelve rear fan rings; ten rounded cable windows; thirty-six 3 mm blind front holes at 15 mm pitch/depth.
 */
outer_width_mm=298;
rack_height_mm=297;
outer_depth_mm=255.2;
shelf_pitch_mm=73.5;
shelf_thickness_mm=3;
psu_x_mm=27;
psu_width_mm=72;
psu_depth_mm=162;
psu_height_mm=23;
dgx_x_mm=121;
dgx_width_mm=150;
dgx_depth_mm=150;
dgx_height_mm=50.5;
front_device_mm=29;
printer_x_mm=325;
printer_y_mm=320;
printer_z_mm=325;
debug_axis_length_mm=30;
debug_axis_thickness_mm=1;
bay_count=4;
view="print";
assert(rack_height_mm<=printer_x_mm && outer_width_mm<=printer_y_mm && outer_depth_mm<=printer_z_mm,"Printer bounds exceeded");
/** Complete rounded native-CAD solid. Bounds [0,0,0]..[298,297,255.2].
 * Run the generator first. This viewer has no alternative geometry path.
 */
module rack() {import("output/acer-four-bay/acer-four-bay-shelves-assembly.stl");}
/** Rear-down print placement; bounds [0,0,0]..[297,298,255.2]. */
module print_pose() {multmatrix([[0,1,0,0],[1,0,0,0],[0,0,-1,outer_depth_mm],[0,0,0,1]]) children();}
/** Nominal body envelopes at each shelf surface, inside the retaining pockets. */
module devices() {
 for(i=[0:bay_count-1]) {
 y=shelf_thickness_mm+i*shelf_pitch_mm;
 color("silver") translate([dgx_x_mm,y,front_device_mm]) cube([dgx_width_mm,dgx_height_mm,dgx_depth_mm]);
 color("orange") translate([psu_x_mm,y,front_device_mm]) cube([psu_width_mm,psu_height_mm,psu_depth_mm]);
 }
}
/** Coordinate axes at origin; length 30 mm, section 1 mm. */
module debug_axes() {
 color("red") cube([debug_axis_length_mm,debug_axis_thickness_mm,debug_axis_thickness_mm]);
 color("green") cube([debug_axis_thickness_mm,debug_axis_length_mm,debug_axis_thickness_mm]);
 color("blue") cube([debug_axis_thickness_mm,debug_axis_thickness_mm,debug_axis_length_mm]);
}
/** Colored geometry and device envelopes; same bounding box as rack(). */
module assembly_colored() {color("SlateGray") rack();devices();}
/** Transparent inspection; same bounding box as rack(). */
module assembly_xray() {color([0.4,0.6,0.7,0.2]) rack();devices();}
if(view=="assembly") rack();
else if(view=="colored") assembly_colored();
else if(view=="xray") assembly_xray();
else if(view=="shelf") intersection(){rack();cube([outer_width_mm,shelf_pitch_mm+shelf_thickness_mm,outer_depth_mm]);}
else print_pose() rack();
