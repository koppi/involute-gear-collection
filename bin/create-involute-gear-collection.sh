#!/usr/bin/env bash

function gen {
  T=$1
  A=$2

  P=angle-$A

  mkdir -p $P

  O=$P/teeth-$T

  N=$(expr $T + 0)

  # make number of spokes depend on number of teeth
  if [ $(($N % 2)) -eq 0 ];
  then
      S=4;
  else
      S=3;
  fi
  
  if [ $N -lt 10 ]; then
      S=0
  fi
  

  echo "involute-gear-generator $O.dxf"
  involute-gear-generator \
      -o $O.dxf \
      --showOption 1 \
      --wheel1ToothCount $N \
      --pressureAngle $A \
      --wheel1CenterHoleDiamater 3 &> $O.md
  
  dxf2svg.py $O.dxf &&
  convert -density 300 -fill white -opaque none $O.svg $O.png &&
  convert -flatten $O.png $O.png &&
  rm -f $O.svg &&
  dxf2stl-gear.sh $O.dxf $O.stl
  dxfmerge.py -i $O.dxf -u 220 -w 240 -o $O-multiple.dxf -a 5 -b 0 -z 1 &>> $O.md
}

for a in 14.5 20; do
    for i in $(seq -w 5 60); do
        gen $i $a
    done
    montage angle-$a/*.png angle-$a.png
done
