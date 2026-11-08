// Assembled viewer. Parametric source: build_acer_v4.py.
show_lid=true;
lcd_open_angle=5;
color("SlateGray") import("concept-v4/shell.stl");
if(show_lid) color("LightSlateGray") import("concept-v4/lid.stl");
color("Orange") translate([0,19.0,158.2323505194681]) rotate([5-lcd_open_angle,0,0]) translate([0,-19.0,-158.2323505194681]) import("concept-v4/lcd.stl");
