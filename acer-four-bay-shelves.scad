/**
 * Four Acer GN100 bays with left PSU pockets and open rear fan mounts.
 * Assembly coordinates: X = width, Y = height, Z = rearward depth.
 * Origin: front-bottom-left corner. Print transform maps [X,Y,Z] to
 * [Y,X,depth-Z]: rear face is Z=0 on the bed; shelf edges are vertical.
 * Component index (assembly coordinates, dimensions in mm):
 * shelves: [0, i*pitch, 0], [width, 5, depth], i=0..4
 * walls: [0/width-5, 0, 0], [5, height, depth]
 * retainers: device x edges, shelf top, front through device rear + ramp
 * fan mounts: three x centres per bay, bay centre Y, rear 5 mm of Z
 * cable holes: two x centres, through each shelf, in last 50.8 mm of Z
 */
wall_thickness_mm = 5;
shelf_thickness_mm = 5;
rack_height_mm = 315;
bay_count = 4;
dgx_width_mm = 150;
dgx_depth_mm = 150;
dgx_height_mm = 50.5;
// Delta ADP-240KB BA manufacturer dimensions; Acer OEM label pending.
psu_width_mm = 72;
psu_depth_mm = 162;
psu_height_mm = 23;
side_air_gap_mm = 22;
rear_extension_mm = 76.2;
cable_region_depth_mm = 50.8;
guide_height_mm = 10;
guide_thickness_mm = 3;
fit_clearance_mm = 0.6;
corner_return_mm = 5;
guide_ramp_length_mm = 10;
fan_frame_mm = 40;
fan_mount_width_mm = 44;
fan_hole_diameter_mm = 35;
fan_screw_pitch_mm = 32;
fan_screw_diameter_mm = 3.4;
fan_mount_depth_mm = 5;
fan_post_width_mm = 3;
fan_pair_pitch_mm = 48;
cable_dgx_width_mm = 40;
cable_psu_width_mm = 30;
cable_hole_depth_mm = 40;
printer_x_mm = 325;
printer_y_mm = 320;
printer_z_mm = 325;
cut_epsilon_mm = 0.1;
debug_axis_length_mm = 30;
debug_axis_thickness_mm = 1;
$fn = 48;
view = "print"; // print, assembly, colored, xray, shelf
psu_x_mm = wall_thickness_mm + side_air_gap_mm;
dgx_x_mm = psu_x_mm + psu_width_mm + side_air_gap_mm;
outer_width_mm = dgx_x_mm + dgx_width_mm + side_air_gap_mm + wall_thickness_mm;
front_device_mm = guide_thickness_mm + fit_clearance_mm;
outer_depth_mm = front_device_mm + dgx_depth_mm + rear_extension_mm;
bay_pitch_mm = (rack_height_mm-shelf_thickness_mm)/bay_count;
bay_clear_height_mm = bay_pitch_mm-shelf_thickness_mm;
top_air_gap_mm = bay_clear_height_mm-dgx_height_mm;
fan_y_offset_mm = bay_clear_height_mm/2;
cable_z_mm = outer_depth_mm-cable_region_depth_mm/2;
fan_centres_mm = [psu_x_mm+psu_width_mm/2,
 dgx_x_mm+dgx_width_mm/2-fan_pair_pitch_mm/2,
 dgx_x_mm+dgx_width_mm/2+fan_pair_pitch_mm/2];
assert(rack_height_mm<=printer_x_mm && outer_width_mm<=printer_y_mm && outer_depth_mm<=printer_z_mm,"Printer bounds exceeded");
assert(top_air_gap_mm==22,"Expected 22 mm over DGX");
assert(psu_height_mm<bay_clear_height_mm,"PSU too tall");
assert(cable_hole_depth_mm<=cable_region_depth_mm && cable_hole_depth_mm>=cable_dgx_width_mm,"Cable closing slopes must be <=45 degrees");
assert(guide_ramp_length_mm>=guide_height_mm,"Retainer ramps must be <=45 degrees");
assert(front_device_mm+psu_depth_mm+fit_clearance_mm+guide_thickness_mm+guide_ramp_length_mm<cable_z_mm-cable_hole_depth_mm/2,"PSU guides overlap cable region");
assert(fan_screw_pitch_mm/2*sqrt(2)-fan_screw_diameter_mm/2>fan_hole_diameter_mm/2,"Fan screws intersect flow hole");
assert(guide_height_mm<top_air_gap_mm,"Devices cannot lift over retainers");
echo(["dimensions",outer_width_mm,rack_height_mm,outer_depth_mm,bay_pitch_mm,top_air_gap_mm]);
echo(["devices",psu_width_mm,psu_depth_mm,psu_height_mm,dgx_width_mm,dgx_depth_mm,dgx_height_mm,psu_x_mm,dgx_x_mm,front_device_mm]);
echo(["features",guide_height_mm,guide_thickness_mm,fit_clearance_mm,corner_return_mm,cable_z_mm,cable_dgx_width_mm,cable_psu_width_mm,cable_hole_depth_mm]);
echo(["fans",fan_centres_mm,fan_y_offset_mm,fan_hole_diameter_mm,fan_screw_pitch_mm,fan_screw_diameter_mm,fan_mount_width_mm]);

/** Diamond passage through shelf. cx: X centre; width: maximum clear width.
 * Bounds: [cx-width/2,-epsilon,cable_z-depth/2] to opposite corner.
 * Front/rear pointed ends close progressively during rear-down printing.
 */
module cable_passage(cx,width) {
 translate([cx, shelf_thickness_mm+cut_epsilon_mm, cable_z_mm])
 rotate([90,0,0]) linear_extrude(shelf_thickness_mm+2*cut_epsilon_mm)
 polygon([[0,-cable_hole_depth_mm/2],[width/2,0],[0,cable_hole_depth_mm/2],[-width/2,0]]);
}
/** One shelf at Y=0. Bounds [0,0,0] to [outer_width,5,outer_depth].
 * Cable passages align vertically across all five shelves.
 */
module shelf() {
 difference() {
 cube([outer_width_mm,shelf_thickness_mm,outer_depth_mm]);
 cable_passage(psu_x_mm+psu_width_mm/2,cable_psu_width_mm);
 cable_passage(dgx_x_mm+dgx_width_mm/2,cable_dgx_width_mm);
 }
}
/** Retainer rail prism, on Y=0 shelf surface. x,width,z0,z1 define plan bounds.
 * Height 10 mm through z1, tapering to zero at z1+10. Rear ramp joins shelf.
 */
module guide_prism(x,width,z0,z1) {
 translate([x,0,0]) rotate([0,90,0]) linear_extrude(width)
 polygon([[-z0,0],[-z0,guide_height_mm],[-z1,guide_height_mm],[-z1-guide_ramp_length_mm,0]]);
}
/** Pocket for a device at X=x,Z=front_device. w,d are nominal body dimensions.
 * Bounds X=x-clearance-thickness through x+w+clearance+thickness;
 * Y=0..10; Z=0..front_device+d+clearance+thickness+10.
 * Full left/right guides, 5 mm returns at each front/rear corner. Centre ports stay open.
 */
module device_retainer(x,w,d) {
 back=front_device_mm+d+fit_clearance_mm;
 left=x-fit_clearance_mm-guide_thickness_mm;
 right=x+w+fit_clearance_mm;
 for (rail_x=[left,right]) guide_prism(rail_x,guide_thickness_mm,0,back+guide_thickness_mm);
 for (end_x=[x-fit_clearance_mm,x+w-corner_return_mm]) {
 translate([end_x,0,0]) cube([corner_return_mm+fit_clearance_mm,guide_height_mm,guide_thickness_mm]);
 guide_prism(end_x,corner_return_mm+fit_clearance_mm,back,back+guide_thickness_mm);
 }
}
/** Three rear fan mounts for one bay. y: shelf surface Y coordinate.
 * Bounds each: X=cx+-22, Y=y..y+bay_clear_height, Z=depth-5..depth.
 * Two narrow posts tie each 44 mm square mount to lower/upper shelf.
 * Only rings/posts remain at rear: all other rear areas are cable openings.
 */
module rear_fans(y) {
 for (cx=fan_centres_mm) translate([cx,y,outer_depth_mm-fan_mount_depth_mm])
 difference() {
 union() {
 translate([-fan_mount_width_mm/2,fan_y_offset_mm-fan_mount_width_mm/2,0]) cube([fan_mount_width_mm,fan_mount_width_mm,fan_mount_depth_mm]);
 for (px=[-fan_mount_width_mm/2,fan_mount_width_mm/2-fan_post_width_mm])
 translate([px,0,0]) cube([fan_post_width_mm,bay_clear_height_mm,fan_mount_depth_mm]);
 }
 translate([0,fan_y_offset_mm,-cut_epsilon_mm]) cylinder(h=fan_mount_depth_mm+2*cut_epsilon_mm,d=fan_hole_diameter_mm);
 for (dx=[-fan_screw_pitch_mm/2,fan_screw_pitch_mm/2],dy=[-fan_screw_pitch_mm/2,fan_screw_pitch_mm/2])
 translate([dx,fan_y_offset_mm+dy,-cut_epsilon_mm]) cylinder(h=fan_mount_depth_mm+2*cut_epsilon_mm,d=fan_screw_diameter_mm);
 }
}
/** Outer sidewalls. Bounds X=0..5 and width-5..width, Y=0..315,Z=0..depth.
 * Both walls connect every shelf. Vertical in rear-down print orientation.
 */
module sidewalls() {
 for (x=[0,outer_width_mm-wall_thickness_mm]) translate([x,0,0]) cube([wall_thickness_mm,rack_height_mm,outer_depth_mm]);
}
/** Complete one-piece rack, bounds [0,0,0]..[width,height,depth]. */
module rack() {
 sidewalls();
 for (i=[0:bay_count]) translate([0,i*bay_pitch_mm,0]) shelf();
 for (i=[0:bay_count-1]) {
 y=i*bay_pitch_mm+shelf_thickness_mm;
 translate([0,y,0]) {
 device_retainer(dgx_x_mm,dgx_width_mm,dgx_depth_mm);
 device_retainer(psu_x_mm,psu_width_mm,psu_depth_mm);
 }
 rear_fans(y);
 }
}
/** Axis visualization: origin, 30 mm +X/+Y/+Z rays, 1 mm section. */
module debug_axes() {
 color("red") cube([debug_axis_length_mm,debug_axis_thickness_mm,debug_axis_thickness_mm]);
 color("green") cube([debug_axis_thickness_mm,debug_axis_length_mm,debug_axis_thickness_mm]);
 color("blue") cube([debug_axis_thickness_mm,debug_axis_thickness_mm,debug_axis_length_mm]);
}
/** Nominal devices. Bounds inside retaining pockets, resting on shelf top. */
module devices() {
 for (i=[0:bay_count-1]) {
 y=i*bay_pitch_mm+shelf_thickness_mm;
 color("silver") translate([dgx_x_mm,y,front_device_mm]) cube([dgx_width_mm,dgx_height_mm,dgx_depth_mm]);
 color("orange") translate([psu_x_mm,y,front_device_mm]) cube([psu_width_mm,psu_height_mm,psu_depth_mm]);
 }
}
/** Colored assembly in use coordinates. Same rack bounds; devices add no extent. */
module assembly_colored() { color("SlateGray") rack(); devices(); }
/** Transparent inspection in use coordinates; geometry is unchanged. */
module assembly_xray() { color([0.4,0.6,0.7,0.2]) rack(); devices(); }
/** Rear-down print placement. Bounds [0,0,0]..[height,width,depth]. */
module print_pose() { translate([0,0,outer_depth_mm]) rotate(a=180,v=[1,1,0]) children(); }
if(view=="assembly") rack();
else if(view=="colored") assembly_colored();
else if(view=="xray") assembly_xray();
else if(view=="shelf") { shelf(); translate([0,shelf_thickness_mm,0]) {device_retainer(dgx_x_mm,dgx_width_mm,dgx_depth_mm);device_retainer(psu_x_mm,psu_width_mm,psu_depth_mm);} rear_fans(shelf_thickness_mm); }
else print_pose() rack();
