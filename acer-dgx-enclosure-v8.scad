// Parametric source: build_acer_v8.py. Removable front fan plate.
lcd_open_angle=5;
fan_plate_forward_offset=0;
color("SlateGray") import("concept-v8/shell.stl");
color("SeaGreen") translate([0,-fan_plate_forward_offset,0]) import("concept-v8/fan-plate.stl");
color("Orange") translate([0,11,145.5323505194681]) rotate([5-lcd_open_angle,0,0]) translate([0,-11,-145.5323505194681]) import("concept-v8/lcd.stl");
