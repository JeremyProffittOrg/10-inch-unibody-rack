// Parametric source: build_acer_v6.py. Filled ventilated bottom, integral roof.
lcd_open_angle=5;
color("SlateGray") import("concept-v6/shell.stl");
color("Orange") translate([0,19,145.5323505194681]) rotate([5-lcd_open_angle,0,0]) translate([0,-19,-145.5323505194681]) import("concept-v6/lcd.stl");
