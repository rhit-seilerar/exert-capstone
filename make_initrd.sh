#!/bin/bash

cachedir=/mount/cache
builddir=/mount/exert/usermode/build
echo $cachedir

cp $cachedir/busybox/busybox-$1 $cachedir/rootfs
mv $cachedir/rootfs/busybox-$1 $cachedir/rootfs/busybox

ln -s -f /busybox $cachedir/rootfs/bin/sh
ln -s -f /proc/self/fd $cachedir/rootfs/dev
ln -s -f /proc/self/fd/2 $cachedir/rootfs/dev/stderr
ln -s -f /proc/self/fd/0 $cachedir/rootfs/dev/stdin
ln -s -f /proc/self/fd/1 $cachedir/rootfs/dev/stdout

if [ $# -eq 2 ];
    then
        cp $builddir/$2 $cachedir/rootfs/;
        mv $cachedir/rootfs/$2 $cachedir/rootfs/user_prog;
fi

cd $cachedir/rootfs/
find . | cpio -H newc -o > ../customfs.cpio