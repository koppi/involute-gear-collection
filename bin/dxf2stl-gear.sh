#!/usr/bin/env bash
#
# convert gear.dxf to gear.stl using OpenSCAD
#

I=$1
O=$2

TMP="$(mktemp --suffix=.dxf)"
TMP_OUT="$(mktemp --suffix=.stl)"
TMP_SCAD="$(mktemp --suffix=.scad)"

function finish {
  rm -f $TMP $TMP_OUT $TMP_SCAD
}

trap finish EXIT

cp -f $I $TMP

cat <<EOF > $TMP_SCAD
\$fn=40;

file="";
height=10;

difference() {
    linear_extrude(height = height, center = true, convexity = 10)
    import (file = file, layer = "0");
    linear_extrude(height = height, center = true, convexity = 10)
    import (file = file, layer = "depth-10.0");
};
EOF

printf -v file -- '-Dfile="%s"' $TMP

openscad -o $TMP_OUT -D 'quality="production"' $file -D'height=10' $TMP_SCAD

cp -f $TMP_OUT $O
