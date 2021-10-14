/*******************************************************************************
18650 Battery Holder
--
Copyright (C) 2021 Adam Oellermann
adam@oellermann.com
--
MIT License:
Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
--
Release History
  0.1: 2021-10-06
    Initial release
*******************************************************************************/

$fa = 1;
$fs = 0.4;

/************************************************************************************
DIMENSIONS
*************************************************************************************/
battery_diameter = 14.5; // 18 for 18650, 14.5 for AA
battery_wiggle_room = 0.6; // added to diameter so batteries don't get stuck - 1 for 18650, .6 for AA
separator_thickness = 0.5; // thickness of the division between cells
base_thickness = 1.5; // thickness of the base
wall_thickness = 1.5; // thickness of the outer wall
height = 12; // total height
rows = 2; // number of rows
cols = 2; // number of columns

module located_cylinder(diam, height, x, y, z) {
  // just places a cylinder in a location
  translate([x,y,z])
    cylinder(d=diam, h=height);
}

module solid() {
  // the solid piece - each cell will be cut out of this
  
  x1 = 0;
  x2 = (cols-1) * (battery_diameter + battery_wiggle_room + separator_thickness);
  y1 = 0;
  y2 = (rows-1) * (battery_diameter + battery_wiggle_room + separator_thickness);
  
  diam = battery_diameter + battery_wiggle_room + (wall_thickness*2);
  
  hull() {
    located_cylinder(diam, height, x1,y1,0);
    located_cylinder(diam, height, x2,y1,0);
    located_cylinder(diam, height, x1,y2,0);
    located_cylinder(diam, height, x2,y2,0);
  }
}

module holes() {
  hole_diam = battery_diameter + battery_wiggle_room;
  for (i=[0:rows-1]) {
    for (j=[0:cols-1]) {
      hole_x = j * (hole_diam + separator_thickness);
      hole_y = i * (hole_diam + separator_thickness);;
      located_cylinder(hole_diam, height, hole_x,hole_y,base_thickness);
    }
  }
  
}
module holder() {
  // removes the cell holders
  difference() {
    solid();
    holes();
  }
}

holder();