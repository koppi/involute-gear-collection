#!/usr/bin/env bash

PATH=`pwd`/bin:$PATH

# cleanup
rm -rf angle-*

bin/create-involute-gear-collection.sh

# update the README.md's
for dir in $(ls -d1 angle-*/); do echo $dir; echo "# $dir" > $dir/README.md; for gear in $(ls -1rt $dir/*.dxf); do echo $gear; (echo ""; cat "$dir/$(basename $gear .dxf).md"; echo ""; echo -n '!'; echo "[$(basename $gear .dxf).png]($(basename $gear .dxf).png) [DXF]($(basename $gear)) [STL]($(basename $gear .dxf).stl)";) >> $dir/README.md; done; done

rm -f angle-*/teeth-*.md
