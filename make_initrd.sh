#!/bin/bash

cachedir=/mount/cache
builddir=/mount/exert/usermode/build
echo $cachedir

cp $cachedir/busybox/busybox-$1 $cachedir/rootfs
mv $cachedir/rootfs/busybox-$1 $cachedir/rootfs/busybox

if [ $# -eq 2 ];
    then
        cp $builddir/$2 $cachedir/rootfs/;
        mv $cachedir/rootfs/$2 $cachedir/rootfs/user_prog;
fi

cd $cachedir/rootfs/
find . | cpio -H newc -o > ../customfs.cpio