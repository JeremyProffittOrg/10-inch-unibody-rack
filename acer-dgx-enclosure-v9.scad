// Vertically stacked Acer enclosure. Run build_acer_v9.py before opening.
// X across, Y rearward, Z upward; units mm. Render-only assembly viewer.
show_equipment=false;
show_lcd=true;
color("SlateGray") import("concept-v9/shell.stl");
color("SeaGreen") import("concept-v9/fan-plate.stl");
if(show_lcd) color("Orange") import("concept-v9/lcd.stl");
if(show_equipment) {
    color([.2,.2,.2,.6]) translate([67,58,9]) cube([70,160,36]);
    color([.7,.7,.7,.6]) translate([27,58,62.7]) cube([150,150,50.5]);
}
