// Assembled v3 viewer. Edit build_acer_v3.py for dimensions and regenerate STEP/STL.
// LCD rests inside the case at 5 degrees and swings forward for access.
// No fans are modeled: front and rear parts contain real mounting patterns.
show_lid=true;
lcd_open_angle=5; // 5 seated; larger angles swing forward
color("SlateGray") import("concept-v3/shell.stl");
if(show_lid) color("LightSlateGray") import("concept-v3/lid.stl");
color("Orange") translate([0,19,182]) rotate([5-lcd_open_angle,0,0]) translate([0,-19,-182]) import("concept-v3/lcd.stl");
color("Silver") import("concept-v3/rear-fan-carrier.stl");
