// Vertically stacked Acer enclosure. Run build_acer_v13.py before opening.
// X across, Y rearward, Z upward; units mm. Render-only assembly viewer.
show_equipment=false;
show_lcd=true;
color("SlateGray") import("concept-v13/shell.stl");
color("SeaGreen") import("concept-v13/fan-plate.stl");
if(show_lcd) color("Orange") import("concept-v13/lcd.stl");
if(show_equipment) {
    color([.2,.2,.2,.6]) translate([67,79.05,6]) cube([70,160,36]);
    color([.7,.7,.7,.6]) translate([27,77.05,61.7]) cube([150,150,50.5]);
}




color("Silver") import("concept-v13/dgx-shelf.stl");
