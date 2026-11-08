// Concept assembly, not a print layout. X right, Y rearward, Z up. Millimetres.
// Brick is an UNVERIFIED 70 x 160 x 36 placeholder. Retain original device cases.
// part: 0 empty assembly; 1 shell; 2 LCD; 3 device references; 4 fans; 5 rear retainer.
// Set show_devices=true for occupied preview. Hardware references are not printable.
show_devices=false;
part=0;
$fn=32;
brick_w=70; brick_d=160; brick_h=36;
acer_w=150; acer_d=150; acer_h=50.5;
front_extension=50.8; rear_extension=50.8;
W=280; D=front_extension+acer_d+rear_extension; H=200;
deck=55; acer_x=112; brick_x=20;
lcd_w=254; lcd_h=133.35; lcd_angle=15;
// LCD front face spans Y=0.49..35.0. Top-only attachments leave sides/bottom open.
module lcd_pose(){translate([(W-lcd_w)/2,35,H-6]) rotate([75,0,0]) translate([0,-lcd_h,0]) children();}
module rail(a,b,r=3){hull(){translate(a)sphere(r=r);translate(b)sphere(r=r);}}
// V2: vented shell, rear-loading supported bays, nesting perimeter foot.
module frame(){
 difference(){
  union(){
   // Continuous structural outer shell: floor, side walls, roof and rear wall.
   cube([W,D,6]);
   for(x=[0,W-4])translate([x,0,0])cube([4,D,H]);
   translate([0,0,H-10])cube([W,D,4]);
   translate([0,D-4,0])cube([W,4,H]);
   // Top recess: raised perimeter rim, 6mm above roof.
   difference(){translate([0,0,H-6])cube([W,D,6]);
    translate([8,8,H-6.1])cube([W-16,D-16,7]);}
   // Inset bottom perimeter foot seats into the next enclosure's recess.
   difference(){translate([8.5,8.5,-5])cube([W-17,D-17,6]);
    translate([13.5,13.5,-6])cube([W-27,D-27,8]);}
   // Full-width perforated load-bearing shelf, connected to both sides/rear.
   translate([0,48,deck-5])cube([W,D-48,5]);
   // Central support web divides brick and Acer; supports shelf and roof.
   translate([99,48,6])cube([4,D-48,H-16]);
   // Rear-loading guide lips with 1mm side clearance to each device.
   for(x=[17,91,109,263])translate([x,48,deck])cube([2,D-48,5]);
   // Front stops stop equipment short of fans; insertion is from rear.
   for(v=[[19,72],[111,152]])translate([v[0],47.8,deck])cube([v[1],3,6]);
   // Front fan bulkhead with clear apertures and mounting holes.
   translate([4,26,deck-5])cube([W-8,4,96]);
   // Rear retainer screw lands, outside insertion paths.
   for(x=[9,98,271])translate([x-4,D-12,deck+8])cube([8,12,12]);
  }
  // Two completely unobstructed loading openings, above the shelf.
  translate([15,D-13,deck])cube([80,15,90]);
  translate([107,D-13,deck])cube([160,15,90]);
  // Rear cable access below shelf.
  for(x=[15,112])translate([x,D-5,12])cube([x==15?78:153,6,30]);
  // Side ventilation slots; long ligaments retain a solid enclosure outline.
  for(x=[-1,W-5])for(y=[55:18:D-25])for(z=[15,72,112,152])
   translate([x,y,z])cube([6,9,25]);
  // Roof ventilation (kept inside stacking rim).
  for(x=[24:20:W-25])for(y=[56:26:D-25])
   translate([x,y,H-11])cube([10,16,6]);
  // Shelf holes, leaving continuous bearing strips below device edges.
  for(x=[34,54,128,148,168,188,208,228])for(y=[68:24:194])
   translate([x,y,deck-6])cube([10,13,7]);
  // Large rear exhaust slots above loading openings.
  for(x=[20:20:W-20])translate([x,D-5,154])cube([10,6,25]);
  // Fan apertures: lower half feeds device face; upper half blows over top.
  for(v=[[brick_x+brick_w/2,deck+brick_h],[acer_x+38,deck+acer_h],[acer_x+112,deck+acer_h]]){
   translate([v[0],25,v[1]])rotate([-90,0,0])cylinder(h=6,d=37);
   for(dx=[-16,16])for(dz=[-16,16])
    translate([v[0]+dx,25,v[1]+dz])rotate([-90,0,0])cylinder(h=6,d=3.3);
  }
  // Cable pass-throughs from each device bay to the lower cable compartment.
  for(x=[40,166])translate([x,218,deck-6])cube([40,20,7]);
  for(x=[9,98,271])translate([x,D-13,deck+14])rotate([-90,0,0])cylinder(h=15,d=3.3);
 }
}
// Removable rear retaining strip, fixed outside the loading openings.
// Remove it to slide devices in from the back. Its top stays below I/O zone.
module rear_retainer(){difference(){
 translate([5,D,deck+3])cube([W-10,3,15]);
 for(x=[9,98,271])translate([x,D-1,deck+14])rotate([-90,0,0])cylinder(h=5,d=3.3);
}}
module lcd_mount(){lcd_pose()difference(){union(){
 cube([lcd_w,lcd_h,5]);
 for(x=[(lcd_w-156.9)/2,(lcd_w+156.9)/2])for(y=[(lcd_h-114.96)/2,(lcd_h+114.96)/2])
 translate([x,y,-6.7])cylinder(h=6.8,d=8);
 }
 // Existing Waveshare panel window and 156.9 x 114.96 M3 hole pattern.
 translate([(lcd_w-156)/2+1,(lcd_h-89)/2+4,-8])cube([156,89,15]);
 for(x=[(lcd_w-156.9)/2,(lcd_w+156.9)/2])for(y=[(lcd_h-114.96)/2,(lcd_h+114.96)/2])
 translate([x,y,-8])cylinder(h=15,d=3.25);
 }}
module devices(){
 translate([acer_x,front_extension,deck])cube([acer_w,acer_d,acer_h]);
 translate([brick_x,front_extension,deck])cube([brick_w,brick_d,brick_h]);
}
module fan(cx,cz){translate([cx-20,30,cz-20])difference(){cube([40,20,40]);
 translate([20,-1,20])rotate([-90,0,0])cylinder(h=22,d=36);
 for(x=[4,36])for(z=[4,36])translate([x,-1,z])rotate([-90,0,0])cylinder(h=22,d=3.3);
 }
 // Hub and schematic blades, visualization only.
 translate([cx,40,cz])rotate([90,0,0]){cylinder(h=3,d=12,center=true);for(a=[0:60:300])rotate([0,0,a])translate([4,-2,-1])cube([12,5,2]);}
}
module fans(){fan(brick_x+brick_w/2,deck+brick_h);fan(acer_x+38,deck+acer_h);fan(acer_x+112,deck+acer_h);}
if(part==0||part==1)color("SlateGray")frame();
if(part==0||part==2)color("Orange")lcd_mount();
if((part==0 && show_devices)||part==3)color("Silver")devices();
if(part==0||part==4)color("DarkSlateGray")fans();

if(part==0||part==5)color("Orange")rear_retainer();
