/*
Copyright (C) 2021 Adam Oellermann
adam@oellermann.com
--
  This file is part of Laser Stramash. 
  
  Laser Stramash is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  Laser Stramash is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>
--
This file contains the design for the prototype Laser Stramash gun. A 
gun comprises a number of components, each generated by a module:
- The barrel - main body of the gun - module barrel()
- The lens holder - fits over end of barrel to hold 22mm lens
  module lens_holder()
- The side panel - two needed, one either side of the barrel - 
  module sidepanel()
- The infrared receiver holder - slots into the top of the barrel
  module ir_recv_holder()
- The grip - slots into the barrel, and has a void for an 18650 cell -
  module grip()
- The battery cover panel - covers the battery slot in the grip -
  module batt_panel_cover()
- The RGB diffuser - print in clear/natural PLA to diffuse RGB LEDs
  module rgb_diffuser()

These modules are invoked at the end of the file - just uncomment the one you want.
--
Release History
  0.1: 2021-10-03
    First draft of gun barrel and side panels.
  0.2: 2021-10-04
    Corrected hole size for IR LED, increased side panel thickness, first draft of grip
  0.3: 2021-10-06
    Redid the grip - better parameterisation, longer grip, shallower angle
    Cutout grip for battery, battery mount details
    half-moon cutout on batt_cover_panel to make it easier to remove
  0.4: 2021-10-07
    move grip hole forward
    move reload btn to top of utility void
    clearance for laser over lens assembly
    IR receiver assembly
    fixing details for diffuser
    diffuser
*/

$fa = 1;
$fs = 0.4;

/************************************************************************************
DIMENSIONS
*************************************************************************************/
// main barrel
barrel_length = 220;
barrel_height = 45;
barrel_thickness = 30;
barrel_skin = 4;
front_skin = 10;
pcb_void_height = 35;
pcb_void_length = 120;
barrel_skin_thickness = (barrel_height - pcb_void_height) / 2;

utility_void_length = 80;
utility_void_height = 25;
utility_void_separator = 5;

utility_hole_diameter = 15;

button_hole_diameter = 13; // reload button

side_panel_thickness_min = 0.75;
side_panel_thickness_max = 6;

// lens holder
lens_diameter = 22;
lens_holder_thickness = 2;
lens_holder_clearance = 0.3;
lens_holder_length = 10;
lens_holder_lip = 1;
flash_suppressor_length = 20;

// RGB diffuser 
rgb_internal_width = 15; // thin: 17 thick:15
rgb_wall = 2; // thin:1 thick:2
rgb_external_width = rgb_internal_width + rgb_wall * 2;
rgb_recess_depth = 2.4;
rgb_internal_length = 100; // thin:102 thick:100
ir_receiver_length = 20; // additional length to allow for IR receiver
rgb_external_length = rgb_internal_length + rgb_wall * 2 + ir_receiver_length;
rgb_diffuser_clearance = 0.3; // increased from 0.2
ir_recv_width = 6.8; // 6.8 for VS1838B, 6.1 for TSOP4438 
ir_recv_height = 8.0; // excl legs 8.0 for VS1838B, 6.8 for TSO4438
ir_recv_depth = 3.5; // excl bump 3.5 for VS1838B, 4.0 for TSOP4438
ir_recv_bumpdepth = 1.7; // 1.7 for VS1838B, 1.6 for TSOP4438  
ir_recv_bumpwidth = 4.2; // 4.2 for VS1838B, 4.2 for TSOP 4438 
ir_recv_rgb_clearance = 0.2;

// grip
grip_thickness=21;
grip_joint_length=35;
grip_joint_height=20;
grip_joint_xwall=8; // thickness of front (pierced by btn) and back wall
grip_joint_void_length = grip_joint_length-grip_joint_xwall;
grip_joint_void_thickness = 18;
grip_back_offset=20;
grip_socket_clearance = 0.4;
grip_angle = 18; // grip angle in degrees
grip_width = 32; // was 36.5
grip_height = 120;
grip_base_thickness = 4;
battery_diameter = 18; // 18650
battery_length = 65; // 18650
battery_clearance_x = 1; // wiggle room
battery_void_width = battery_diameter + 5; // wiggle room
battery_void_length = 80;
butt_length = adj_given_hyp(h=grip_height,angle=grip_angle); // length of the angled portion
batt_cover_thickness=1;
batt_cover_xlip = 3; // width of the 'lip' for the battery cover
batt_cover_ylip = 2; // height of the 'lip' for the battery cover
batt_wiring_width = 15; //wiring channel through into barrel
batt_wiring_thickness = 10;
batt_clearance = 0.4;
batt_panel_width = battery_void_width + (2*batt_cover_xlip) - batt_clearance;
batt_panel_height = battery_void_length + (2*batt_cover_ylip) - batt_clearance;
batt_socket_length = 70;
batt_spring_channel_width = 4;
batt_spring_width = 17; // official dim 16.5
batt_spring_height = 16.5; // official dim 16
batt_spring_thickness = 0.5;
batt_spring_retainer = 0.5;
batt_spring_plate_thickness = .2+(battery_void_length - batt_clearance - batt_socket_length)/2;
batt_cover_panel_clearance = 0.2;
batt_cover_panel_shrink = 0.2; // take this off from every edge
bc_width = battery_void_width + (2 * batt_cover_xlip) - (batt_cover_panel_shrink * 2);
bc_height = battery_void_length + (2 * batt_cover_ylip) - (batt_cover_panel_shrink * 2);

fire_plate = grip_joint_xwall;
fire_hole_diameter = 13;
fire_void_length = 30;
fire_void_width = 18;
fire_button_zoffset = 12;

// optics
optic_diameter = lens_diameter; // exactly matches lens diameter
optic_length = 22.0; // was 19.4, measure at 22.4
lensholder_diameter = 2;
optic_thickness = 2;
led_diameter = 5;
led_clearance = 0.5; // was 0.3
laserbeam_diam = 5;
laserbody_diam = 6.8; // measures 6, this works for friction fit
laser_lipdepth = 1;

ir_recv_socket_diam = 10;

/************************************************************************************
BARREL
*************************************************************************************/
module laser_hole() {
  // Holder for a 6mm laser dot - intended for friction fit plus glue
  // beam hole
  x_offset = 5;
  translate([-0.05,optic_diameter/2+optic_thickness+0.6+x_offset,0])
    optic_hole(laserbeam_diam, front_skin+0.1);
  // body hole
  translate([0.05,optic_diameter/2+optic_thickness+0.6+x_offset,0])
    optic_hole(laserbody_diam, front_skin-laser_lipdepth);
  
}

module optic_hole(diameter, length) {
  // hollow out the optic assembly
  translate([10,optic_diameter/2+lensholder_diameter,barrel_thickness/2])
  rotate([0,-90,0])
    cylinder(d=diameter, h=length);
}
module optic() {
  // cylindrical projection which holds the lens at the right focal distance
  // from the IR LED
  translate([10,optic_diameter/2+lensholder_diameter,barrel_thickness/2])
  rotate([0,-90,0])
    cylinder(d=optic_diameter, h=optic_length);
  
}

module pcb_void() {
  // Void for the PCB
  translate([front_skin,(barrel_height-pcb_void_height)/2,-0.05])
    cube([pcb_void_length, pcb_void_height, barrel_thickness+0.1]);
}

module utility_void() {
  // a 'utility' void - provides a channel between the PCB void and the components
  // in the grip. This will also house the voltage booster board.
  x_offset = front_skin+pcb_void_length + utility_void_separator;
  translate([x_offset,(pcb_void_height-utility_void_height)+((barrel_height-pcb_void_height)/2),-0.05])
    cube([utility_void_length, utility_void_height, barrel_thickness+0.1]);
}
module barrel_solid() {
  // the solid barrel - complete shape without voids
  union() {
    // main barrel
    cube([barrel_length, barrel_height, barrel_thickness]);
    // 'kickback' end
    kickback_width = sqrt((barrel_height*barrel_height)/2);
    translate([barrel_length,0,0])
      rotate([0,0,45])
        cube([kickback_width, kickback_width, barrel_thickness]);
    // lens projection
    optic();
  }
 }
 
 module utility_hole() {
   // hole from the utility void into the pcb void
   uh_y = (pcb_void_height-utility_void_height)+((barrel_height-pcb_void_height)/2) + (utility_void_height/2);
   translate([front_skin + pcb_void_length-0.01,uh_y,barrel_thickness/2])
    rotate([0,90,0])
      cylinder(d=utility_hole_diameter,h=utility_void_separator+0.02);
 }
 
 module rgb_hole() {
   // hole from the PCB void into the RGB on top of the gun
   // sized to pass a 4-pin KF2510 plug
   
   rgb_hole_height = 13; // measured 11
   rgb_hole_width = 8; // measured 6
   
   skin = (barrel_height - pcb_void_height)/2;
   rgb_x = pcb_void_length;
   rgb_y = barrel_height-skin-0.05;
   rgb_z = (barrel_thickness-rgb_hole_height)/2;
   
   translate([rgb_x, rgb_y, rgb_z])
    cube([rgb_hole_width, skin+0.1, rgb_hole_height]);
 }
 
module reload_hole() {
  // hole at the bottom of the barrel for the reload button
  skin = (barrel_height - pcb_void_height)/2;
  
  // 3/4 way along utility = well clear of grip
  xoff = front_skin + pcb_void_length + utility_void_separator + (utility_void_length*.75); 
  //translate([front_skin+(2*button_hole_diameter),-0.05,barrel_thickness/2])
  translate([xoff,barrel_height-(skin+0.1)-0.05,barrel_thickness/2])
    rotate([-90,0,0])
      cylinder(d=button_hole_diameter,h=skin+0.2);
 }
 
 module screwhole(x,y) {
   // intended for M2 self-tapping
   screwhole_diam = 1.7;
   translate([x,y,-10])
    rotate([0,0,0])
      cylinder(d=screwhole_diam, h=50);
 }
 
module screwholes() {
  // screwholes to fit the side panels onto the barrel
   skin = (barrel_height - pcb_void_height)/2;
   x1 = front_skin / 2;
   x2 = front_skin + pcb_void_length + (utility_void_separator/2);
   x3a = front_skin + pcb_void_length + utility_void_separator + utility_void_length;
   x3 = ((barrel_length - x3a) / 2) + x3a;
   x4 = x3 + barrel_height/2 - 2;
   y1 = skin/2;
   y2 = barrel_height/2;
   y3 = barrel_height - (skin/2);
   screwhole(x1, y1);
   screwhole(x1, y2);
   screwhole(x1, y3);
   screwhole(x2, y1);
   screwhole(x2, y3);
   screwhole(x3, y1);
   screwhole(x3, y3);
   screwhole(x4, y2);
}
 
module grip_socket() {
  // Cutout for the grip - intended for friction fit + glue
  grip_z = (barrel_thickness-grip_thickness)/2;
  clearance = grip_socket_clearance/2;
  grip_x = pcb_void_length + front_skin + utility_void_separator*1.5; // barrel_length-grip_joint_length-grip_back_offset-clearance;
  translate([grip_x,-0.01,grip_z-clearance]) 
    cube([grip_joint_length+grip_socket_clearance,grip_joint_height,grip_thickness+grip_socket_clearance]);
}
 
module ir_recv_hole() {
  //xoff = front_skin; // + ir_recv_socket_diam
  xoff = (ir_receiver_length*0.35) + pcb_void_length - rgb_external_length + front_skin * 1.5 + (ir_recv_socket_diam/2);
  translate([xoff,barrel_height+0.05,barrel_thickness/2])
    rotate([90,0,0])
      cylinder(d=ir_recv_socket_diam,h=barrel_skin_thickness+0.1);
}

// module ir_recv_holder() {
//   ir_recv_slot_width = 8;
//   ir_recv_slot_depth = 2;
//   ir_recv_clearance = 0.3; // friction fit...

//   difference() {
//     cylinder(d=ir_recv_socket_diam-ir_recv_clearance,h=barrel_skin_thickness+0.1);
//     translate([-ir_recv_slot_depth/2,-ir_recv_slot_width/2,-0.01])
//       cube([ir_recv_slot_depth, ir_recv_slot_width, barrel_skin_thickness+0.2]);
//   }
// }

module barrel() {
  difference() {
    barrel_solid();
     
    // cutout for PCB
    pcb_void(); 
     
    // cutout for boost module etc
    utility_void();
     
    // coutout for IR optics
    translate([-optic_thickness, 0, 0])
      optic_hole(optic_diameter-(2*optic_thickness), optic_length);
    translate([0.05, 0, 0])
      optic_hole(led_diameter+led_clearance, optic_length+0.1);
     
    // cutout for laser
    laser_hole();
     
    // cutout for IR receiver
    //translate([0.05, optic_diameter, 0])
    // optic_hole(ir_recv_socket_diam, front_skin + 0.1);
     
    // cutout for grip
    grip_socket();
      
    // cutout hole between pcb void and utility void
    utility_hole();
     
    // cutout hole for connection to RGB
    rgb_hole();
     
    // cutout for reload button
    reload_hole();
    
    // screw holes for side panels
    screwholes();

    // hole fot the IR receiver
    ir_recv_hole();

    // slot for receiving RGB diffuser
    xoff = pcb_void_length - rgb_external_length + front_skin * 1.5;
    translate([xoff,barrel_height-rgb_recess_depth+0.02,barrel_thickness/2])
    rotate([90,0,0])
      rgb_diffuser_recess();
  }
  
}
 

/************************************************************************************
LENS HOLDER
*************************************************************************************/
module lens_holder() {
  // fits over the optics 'muzzle' to hold the lens in place
  lens_holder_diameter = lens_diameter + (lens_holder_thickness * 2) + lens_holder_clearance;
 
  // sleeve
  difference() {
    cylinder(d=lens_holder_diameter, h=lens_holder_length);
    translate([0,0,-0.01])
    cylinder(d=lens_diameter + lens_holder_clearance, h=lens_holder_length+0.02);
  }
  
  // lip
  difference() {
    cylinder(d=lens_holder_diameter, h=lens_holder_thickness);
    translate([0,0,-0.01])
    cylinder(d=lens_diameter - (lens_holder_lip*2), h=lens_holder_length+0.02);
  }
  
  // flash suppressor
  flash_suppressor_id = lens_diameter + lens_holder_clearance;
  translate([0,0,-flash_suppressor_length + 0.01])
  difference() {
    cylinder(d=lens_holder_diameter, h=flash_suppressor_length);
    translate([0,0,-0.01])
      cylinder(d1=flash_suppressor_id, d2=(flash_suppressor_id-lens_holder_lip*2), h=flash_suppressor_length+0.02);
  }
}
 

/************************************************************************************
SIDE PANELS
*************************************************************************************/
module panel_polyhedron() {
  // this generates the 'cool' 3d shape
  x1 = 0;
  x2 = barrel_length * 0.8;
  x3 = barrel_length;
  x4 = barrel_length + (barrel_height/2);
  y1 = 0;
  y2 = barrel_height/2;
  y3 = barrel_height;
  z1 = 0;
  z2 = side_panel_thickness_max - side_panel_thickness_min;
  
  PolyPoints = [
    [x1,y1,z1], // 0
    [x1,y3,z1], // 1
    [x3,y3,z1], // 2
    [x4,y2,z1], // 3
    [x3,y1,z1], // 4
    [x2,y2,z2] // 5 
  ];
  
  PolyFaces = [
    [0,1,2,3,4],
    [1,0,5],
    [5,0,4],
    [5,4,3],
    [5,3,2],
    [5,2,1]
  ];
  polyhedron(PolyPoints, PolyFaces);
}

module panel() {
  // the full side panel (no screwholes yet)
  x1 = 0;
  x2 = barrel_length * 0.8;
  x3 = barrel_length;
  x4 = barrel_length + (barrel_height/2);
  y1 = 0;
  y2 = barrel_height/2;
  y3 = barrel_height;
  
  // the outline of the panel - linear_extruded for the minimum thickness
  pp = [
    [x1,y1],
    [x1,y3],
    [x3,y3],
    [x4,y2],
    [x3,y1]
  ];
  
  linear_extrude(height=side_panel_thickness_min)
    polygon(pp);
  translate([0,0,side_panel_thickness_min-0.01])
    panel_polyhedron();
}

module sidepanel() {
  // the full side panel with screwholes
  difference() {
    panel();
    screwholes();
  }
}

/************************************************************************************
GRIP
*************************************************************************************/
module butt_solid() {
  // the base of the grip - ie the part you hold
  
  left_x = -grip_width;
  
  hull() {
    translate([0,0,-butt_length])
      cylinder(d=grip_thickness,h=butt_length);
    translate([left_x,0,-butt_length])
      cylinder(d=grip_thickness,h=butt_length);
  }
}

module batt_compartment() {
  // The battery compartment - the open space above the curved battery channel
  // Slightly wider than the battery width to allow room for wiring
  x_off = -(grip_width/2) - (battery_void_width/2);
  z_off = -butt_length + grip_base_thickness;
  translate([x_off,-(grip_thickness/2),z_off])
    cube([battery_void_width, grip_thickness/2, battery_void_length]);
}

module batt_cover_recess() {
  // creates the small depression for the cover to sit in
  bc_width = battery_void_width + (2 * batt_cover_xlip);
  bc_height = battery_void_length + (2 * batt_cover_ylip);
  x_off = -(grip_width/2) - (bc_width/2);
  z_off = -butt_length + grip_base_thickness - batt_cover_ylip;
  translate([x_off,-(grip_thickness/2),z_off])
    cube([bc_width, batt_cover_thickness, bc_height]);
}

module batt_wiring() {
  // the channel for wiring out the top of the grip
  wiring_length = butt_length - battery_void_length - grip_base_thickness;
  x_off = -(grip_width/2) - (batt_wiring_width/2);
  
  translate([x_off,-batt_wiring_thickness/2,-wiring_length-0.1])
    cube([batt_wiring_width,batt_wiring_thickness,wiring_length+0.2]);
}

 module batt_screwhole(x,y) {
   // intended for M2 self-tapping screws
   screwhole_diam = 1.7;
   screwhole_len = 10; 
   translate([x,0,y])
    rotate([90,0,0])
      cylinder(d=screwhole_diam, h=screwhole_len);
 }
 
module batt_screwholes() {
  // screwholes to fasten on cover
  x1 = -(grip_width/2) - (battery_void_width/2) - (batt_cover_xlip/2);
  y1 = -(butt_length - battery_void_length - grip_base_thickness);
  x2 = x1 + batt_cover_xlip + battery_void_width;
  y2 = y1 - battery_void_length;
  
  batt_screwhole(x1,y1);
  batt_screwhole(x2,y1);
  batt_screwhole(x1,y2);
  batt_screwhole(x2,y2);
}
 
module batt_cutout() {
  // 18650 cutout for the battery to nestle in
  bc_zoff = -butt_length + ((battery_void_length-batt_socket_length)/2) + grip_base_thickness;
  translate([-grip_width/2,0,bc_zoff])
    cylinder(d=battery_diameter+battery_clearance_x,h=batt_socket_length);
}

module batt_spring_socket_neg() {
  // holder for the negative-terminal spring
  bss_z = -butt_length + ((battery_void_length-batt_socket_length)/2) + grip_base_thickness-batt_spring_plate_thickness+0.001;
  translate([-grip_width/2,0,bss_z])
  union() {
    translate([-batt_spring_channel_width/2,-batt_spring_height/2,0])
      cube([batt_spring_channel_width,batt_spring_height,batt_spring_plate_thickness]);
    translate([-batt_spring_width/2,-batt_spring_height/2,batt_spring_plate_thickness-batt_spring_retainer-batt_spring_thickness])
        cube([batt_spring_width,batt_spring_height,batt_spring_thickness]);
  }
}

module batt_spring_socket_pos() {
  // holder for the positive-terminal spring
  bss_z = -butt_length + ((battery_void_length-batt_socket_length)/2) + grip_base_thickness-batt_spring_plate_thickness + batt_socket_length + batt_spring_plate_thickness -0.001;
  translate([-grip_width/2,0,bss_z])
  union() {
    translate([-batt_spring_channel_width/2,-batt_spring_height/2,0])
      cube([batt_spring_channel_width,batt_spring_height,batt_spring_plate_thickness]);
    translate([-batt_spring_width/2,-batt_spring_height/2,batt_spring_retainer])
        cube([batt_spring_width,batt_spring_height,batt_spring_thickness]);
  }
}

module butt() {
  // the angled portion of the grip, which you hold
  // includes void for battery
  
  // cut out the internal voids
  difference() {
    butt_solid();
    batt_compartment();
    
    // battery
    batt_cover_recess(); // top
    batt_cutout();
    
    // battery spring holders
    batt_spring_socket_neg();
    batt_spring_socket_pos();
    
    // screwholes
    batt_screwholes();
    
    // wiring route
    batt_wiring();
    
    
  }
}

module joint_body() {
  // the part that goes into the barrel/body
  triangle_height = opp_given_adj(a=grip_joint_length,angle=grip_angle);
  
  x1 = -grip_joint_length;
  x2 = 0;
  y1 = -(grip_joint_height + triangle_height);
  y2 = -grip_joint_height;
  y3 = 0;
  
  rotate([90,0,0])
  translate([0,grip_joint_height,-(grip_thickness/2)])
  linear_extrude(height=grip_thickness)
    polygon(points = [
      [x1,y1],
      [x1,y3],
      [x2,y3],
      [x2,y2]
    ]);
}

module joint_wiring() {
  // provides a channel for wires from switch & battery to be routed through into the barrel
  triangle_height = opp_given_adj(a=grip_joint_length,angle=grip_angle);
  wiring_height = triangle_height +grip_joint_height;
  x_off = -grip_joint_void_length - ((grip_joint_length-grip_joint_void_length)/2);
  translate([x_off,-(grip_joint_void_thickness/2),-triangle_height])
    cube([grip_joint_void_length,grip_joint_void_thickness,wiring_height+0.1]);
}

module joint() {
  // the portion of the grip that goes into the barrel socket
  difference() {
    joint_body();
    // remove the wiring channel
    joint_wiring();
  }
}


module grip_no_fire() {
  // the assembled grip, but no hole for fire button
  union() {
    xoff = 3;
    yoff = opp_given_adj(a=3,angle=grip_angle);
    translate([-xoff,0,0])
    rotate([0,-grip_angle,0])
      butt();
    translate([0.01,0,-0.01]) // make sure it comes out solid
      joint();
  }
}

module fire_button() {  
  // used to make hole/void for the fire button
  
  translate([-grip_joint_length-0.01,0,-(fire_void_width/2)-fire_button_zoffset])
  rotate([0,90,0])
  union() {
    // hole
    cylinder(d=fire_hole_diameter,h=fire_plate);
    // void
    translate([-(fire_void_width/2), -(fire_void_width/2),fire_plate-0.01])
    cube([fire_void_width, fire_void_width, fire_void_length]);  
    //translate([0, 0,fire_plate-0.01])
    //cylinder(d=fire_void_width,h=fire_void_length);
  }
}

module grip_shoulder() {
  // shoulder cuts out top part of butt to leave flush with barrel
  translate([0,-100,0])
  cube([200,200,200]);
}

module grip_front() {
  // cuts out front part of butt to leave flush
  
  translate([-200-grip_joint_length,-100,-200])
  cube([200,200,200]);
}

module grip() {
  // The complete assembled grip
  
  // rotate to lie flat on build plate
  rotate([-90,0,0])
  difference() {
    grip_no_fire();
    
    // space for the wiring through the joint
    joint_wiring();
    // fire button
    fire_button();
    // front face
    grip_front();
    // shoulder
    grip_shoulder();
  }
}

/************************************************************************************
BATTERY COVER PANEL
*************************************************************************************/
//module batt_cover_panel() {
//  // The battery cover panel
//  
//  difference() {
//    cube([batt_panel_width-batt_cover_panel_clearance,batt_panel_height-batt_cover_panel_clearance,batt_cover_thickness]);
//    cover_screwholes(); // remove screws!
//  }
//}

 module cover_screwhole(x,y) {
   // intended for M2 self-tapping
   screwhole_diam = 1.7;
   screwhole_len = 50; // plenty to go all the way through
   translate([x,y,-screwhole_len/2])
      cylinder(d=screwhole_diam, h=screwhole_len);
 }
 
module cover_screwholes() {
  // lays out the screwholes for the cover
  x1 = batt_cover_xlip/2 + batt_cover_panel_clearance*2;
  y1 = batt_cover_ylip/2 + batt_cover_panel_clearance*2;
  x2 = x1 + batt_cover_xlip/2 + battery_void_width;
  y2 = y1 + battery_void_length;
  
  cover_screwhole(x1,y1);
  cover_screwhole(x2,y1);
  cover_screwhole(x1,y2);
  cover_screwhole(x2,y2);
}

module batt_cover_stiffener() {
  batt_cover_stiffener_depth = 4;
  batt_cover_stiffener_wall = 1.5;
  batt_cover_stiffener_clearance = 0.5; // good friction fit
  
  
  // battery_void_width, battery_void_length
  width = battery_void_width - batt_cover_stiffener_clearance;
  height = battery_void_length - batt_cover_stiffener_clearance;
  
  translate([(bc_width-width)/2,0,(bc_height-height)/2])
  difference() {
    cube([width,batt_cover_stiffener_depth + batt_cover_thickness,height]);
    translate([batt_cover_stiffener_wall,0.1,batt_cover_stiffener_wall])
      cube([width-(2*batt_cover_stiffener_wall), batt_cover_stiffener_depth + batt_cover_thickness, height - (2*batt_cover_stiffener_wall)]);
  }
}

module batt_cover_finger_cutout() {
  // half-moon cutout to allow easier removal of the panel

  finger_cutout_diam = 8;
  finger_cutout_height = 10;
  
  z_off = -butt_length + grip_base_thickness - batt_cover_ylip + batt_cover_panel_shrink;

  translate([-grip_width/2,-(grip_thickness/2)-0.001,z_off]) 
    rotate([-90,0,0])
      cylinder(d=finger_cutout_diam, h=finger_cutout_height);
}

module batt_cover_panel() {
  // panel that sits in batt_cover_recess()


  
  x_off = -(grip_width/2) - (bc_width/2);
  z_off = -butt_length + grip_base_thickness - batt_cover_ylip + batt_cover_panel_shrink;
  
  // rotate to sit nicely on the build plate
  rotate([90,0,0]) {
    
    difference() {
      translate([x_off,-(grip_thickness/2),z_off]) {
        cube([bc_width, batt_cover_thickness, bc_height]);
        batt_cover_stiffener();
      }
      
      translate([0,-1,0])
        batt_screwholes();

      batt_cover_finger_cutout();
    }
    
  }
}

/************************************************************************************
RGB Diffuser
*************************************************************************************/
module diffuser(length, width, recess_depth) {
  difference() {
    hull() { // the main body
      translate([width/2,0,0])
        sphere(d=width);
      translate([length-width/2, 0, 0])
        sphere(d=width);
    }

    // cut off the bottom half
    translate([-0.05, -(width+0.1)/2,-width])
      cube([length+0.1, width+0.1, width]);
  }

  // and now the recess
  translate([0,0,-recess_depth+0.01])
    hull() {
      translate([width/2,0,0])
        cylinder(d=width, h=recess_depth);
      translate([length-width/2, 0, 0])
        cylinder(d=width, h=recess_depth);
    }
}

module ir_receiver_cutout() {
  // cutout to fit the IR received
  width = ir_recv_width + ir_recv_rgb_clearance;
  depth = ir_recv_depth + ir_recv_rgb_clearance;
  height = ir_recv_height + ir_recv_rgb_clearance;
  bump_d = ir_recv_bumpwidth + ir_recv_rgb_clearance;

  translate([ir_receiver_length/2,-width/2,0])
  union() {
    cube([depth, width, height]);
    translate([0,width/2,0])
      cylinder(d=bump_d, h=height);
    
  }

  w = rgb_internal_width-rgb_diffuser_clearance;
  translate([rgb_wall,0,-rgb_recess_depth+0.0])
    hull() {
      
      translate([w/2,0,0])
        cylinder(d=w, h=rgb_recess_depth+0.1);
      translate([rgb_internal_length-(rgb_diffuser_clearance*2)-w/2 + ir_receiver_length, 0, 0])
        cylinder(d=w, h=rgb_recess_depth+0.1);
    }
}

module rgb_diffuser() {
  // the complete part
  xclear = rgb_diffuser_clearance * 2;
  
  difference() {
    translate([rgb_diffuser_clearance, 0, 0])
      diffuser(rgb_external_length-(rgb_diffuser_clearance*2), rgb_external_width-rgb_diffuser_clearance, rgb_recess_depth);
    translate([rgb_wall+rgb_diffuser_clearance+ir_receiver_length,0,-0.01])
      diffuser(rgb_internal_length-(rgb_diffuser_clearance*2), rgb_internal_width-rgb_diffuser_clearance, rgb_recess_depth);
    ir_receiver_cutout();
  }
}

module rgb_diffuser_recess() {
  // and now the recess
  translate([0,0,-rgb_recess_depth+0.01])
    hull() {
      translate([rgb_external_width/2,0,0])
        cylinder(d=rgb_external_width, h=rgb_recess_depth);
      translate([rgb_external_length-rgb_external_width/2, 0, 0])
        cylinder(d=rgb_external_width, h=rgb_recess_depth);
    }
}

/************************************************************************************
Trig Utils
*************************************************************************************/
function opp_given_adj(a,angle) = a * tan(angle);
function hyp_given_adj(a,angle) = a / cos(angle);
function adj_given_hyp(h,angle) = h * cos(angle);

module mounted_diffuser() {
  xoff = pcb_void_length - rgb_external_length + front_skin * 1.5;
  translate([xoff,barrel_height,barrel_thickness/2])
    rotate([-90,0,0])
      rgb_diffuser();
}

/************************************************************************************
MAIN
Just uncomment the component you want
*************************************************************************************/
//sidepanel();
barrel();
//ir_recv_holder();
//grip();
//batt_cover_panel();
//rgb_diffuser();
  //mounted_diffuser(); // just a version of the rgb_diffuser positioned on the barrel
//lens_holder();