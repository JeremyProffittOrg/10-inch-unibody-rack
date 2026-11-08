// Parametric source: build_acer_v5.py. Integral roof and raised Acer platform.
// Thick LCD side sections extend from the pivots to the bottom of the panel.
lcd_open_angle=5;
color("SlateGray") import("concept-v5/shell.stl");
color("Orange") translate([0,19,158.2323505194681]) rotate([5-lcd_open_angle,0,0]) translate([0,-19,-158.2323505194681]) import("concept-v5/lcd.stl");
