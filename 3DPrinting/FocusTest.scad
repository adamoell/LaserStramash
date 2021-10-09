$fa = 1;
$fs = 0.4;

lens_diameter = 22;
led_diameter = 5;
led_clearance = 0.5; // was 0.3
led_carrier_thickness = 2;
led_carrier_clearance = 0.5;
led_carrier_plate = 2; // was 1, thickened to get the LED straighter
led_carrier_length = 150;

barrel_length = 150;
focussed_barrel_length = 22.0; // was 19.4, measure at 22.4
barrel_thickness = 2;

lens_holder_thickness = 2;
lens_holder_clearance = 0.3;
lens_holder_length = 10;
lens_holder_lip = 1;
flash_suppressor_length = 20;

// lens is held against end of barrel by lens holder
// led_carrier slides inside barrel to adjust focus

module barrel() {
  difference() {
    cylinder(d=lens_diameter, h=barrel_length);
    translate([0,0,-0.01])
    cylinder(d=lens_diameter-(2*barrel_thickness), h=barrel_length+0.02);
  }
}

module focussed_barrel() {
  rotate([0,180,0]) {
    difference() {
      cylinder(d=lens_diameter, h=focussed_barrel_length);
      translate([0,0,-0.01])
      cylinder(d=lens_diameter-(2*barrel_thickness), h=barrel_length+0.02);
    }
    
    // led mount
    led_carrier_od = lens_diameter-0.01;
    led_carrier_id = led_carrier_od - (2*led_carrier_thickness);
    translate([0,0,focussed_barrel_length-led_carrier_plate])
      difference() {
        cylinder(d=led_carrier_od, h=led_carrier_plate);
        translate([0,0,-0.01])
        cylinder(d=led_diameter + led_clearance, h=led_carrier_plate+0.02);
      }
  }
}

module lens_holder() {
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

module led_carrier() {
  led_carrier_od = lens_diameter-(2*barrel_thickness)-led_carrier_clearance;
  led_carrier_id = led_carrier_od - (2*led_carrier_thickness);
  // tube
  difference() {
    cylinder(d=led_carrier_od, h=led_carrier_length);
    translate([0,0,-0.01])
      cylinder(d=led_carrier_id, h=barrel_length+0.02);
    // cut out half the barrel to make it easier to run the wire
    translate([0,-led_carrier_od/2,led_carrier_plate+(led_carrier_thickness*4)])
      cube([led_carrier_od, led_carrier_od, led_carrier_length]);
  }
  
  // led mount
  difference() {
    cylinder(d=led_carrier_od, h=led_carrier_plate);
    translate([0,0,-0.01])
    cylinder(d=led_diameter + led_clearance, h=led_carrier_plate+0.02);
  }
}

//barrel();
//lens_holder();
//led_carrier();
focussed_barrel();