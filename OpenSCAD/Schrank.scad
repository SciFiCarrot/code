// parameters
thickness = 19;
height = 500;
width = 500;
depth = 500;

module board(length, width) {
	cube([length, width, thickness]);
}
board(500,500);


cube([500,19,500]);
translate([0,500-19,0]) {
	cube([500,19,500]);
}

translate([0,19,0]) {
	cube([500,500-2*19,19]);
}
translate([0,19,500-19]) {
	cube([500,500-2*19,19]);
}

translate([0,19,19]) {
	cube([19,500-2*19,500-2*19]);
}

translate([19,19,314+