// Parametric source: build_acer_v7.py. Enlarged cable passages and forward LCD pivot.
lcd_open_angle=5;
color("SlateGray") import("concept-v7/shell.stl");
color("Orange") translate([0,11,145.5323505194681]) rotate([5-lcd_open_angle,0,0]) translate([0,-11,-145.5323505194681]) import("concept-v7/lcd.stl");
