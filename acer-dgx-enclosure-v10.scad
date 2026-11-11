// Vertically stacked Acer enclosure. Run build_acer_v10.py before opening.
// X across, Y rearward, Z upward; units mm. Render-only assembly viewer.
show_equipment=false;
show_lcd=true;
color("SlateGray") import("concept-v10/shell.stl");
color("SeaGreen") import("concept-v10/fan-plate.stl");
if(show_lcd) color("Orange") import("concept-v10/lcd.stl");
if(show_equipment) {
    color([.2,.2,.2,.6]) translate([67,60,6]) cube([70,160,36]);
    color([.7,.7,.7,.6]) translate([27,58,61.7]) cube([150,150,50.5]);
}
