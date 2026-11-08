// Concept assembly, not a print layout. X right, Y rearward, Z up. Millimetres.
// Brick is an UNVERIFIED 70 x 160 x 36 placeholder. Retain original device cases.
// part: 0 assembled; 1 frame; 2 LCD mount; 3 device references; 4 fan references.
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
module frame(){
 difference(){union(){
  // Open floor perimeter and cable-management ribs.
  for(x=[0,W-10])translate([x,0,0])cube([10,D,7]);
  for(y=[0,D-10])translate([0,y,0])cube([W,10,7]);
  for(y=[55,115,175,225])translate([8,y,1])cube([W-16,5,5]);
  // Four continuous load paths; upper frame has no roof.
  for(x=[0,W-14])for(y=[0,D-14])translate([x,y,0])cube([14,14,H]);
  for(x=[0,W-10])translate([x,0,H-10])cube([10,D,10]);
  for(y=[0,D-10])translate([0,y,H-10])cube([W,10,10]);
  // Device support crossmembers, leaving 48mm clear cable space below.
  for(y=[front_extension+12,front_extension+acer_d-18])
   translate([0,y,deck-7])cube([W,7,7]);
  // Narrow longitudinal saddles and locating lips.
  for(x=[brick_x,brick_x+brick_w-7,acer_x,acer_x+acer_w-7]){
   translate([x,front_extension,deck-5])cube([7,160,5]);
   translate([x,front_extension+160,deck-5])cube([7,4,10]);
  }
  // Front fan carrier posts; each fan centre is exactly device-top height.
  for(v=[[brick_x+brick_w/2,deck+brick_h],[acer_x+38,deck+acer_h],[acer_x+112,deck+acer_h]])
   for(dx=[-23,20])translate([v[0]+dx,29,7])cube([3,21,v[1]+20-7]);
  // Top-only LCD support arms, from crossbeam to the panel's upper corners.
  for(x=[22,W-22])rail([x,7,H-5],[x,36,H-10],4);
  // Tapered stack locating pegs, above load-bearing post shoulders.
  for(x=[7,W-7])for(y=[7,D-7])translate([x,y,H])cylinder(h=5,d1=7,d2=5.5);
 }
 // Matching underside sockets, 0.4mm diametral clearance, 1mm depth margin.
 for(x=[7,W-7])for(y=[7,D-7])translate([x,y,-0.01])cylinder(h=6.01,d=7.4);
 // Cable tie slots through lower side rails.
 for(x=[-1,W-11])for(y=[65,125,185])translate([x,y,2])cube([12,10,3]);
 }
}
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
if(part==0||part==3)color("Silver")devices();
if(part==0||part==4)color("DarkSlateGray")fans();
