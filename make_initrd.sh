#!/bin/bash

cachedir=/mount/cache
builddir=/mount/exert/usermode/build

echo $cachedir
echo $#

cp $cachedir/busybox/busybox-$1 $cachedir/rootfs
mv $cachedir/rootfs/busybox-$1 $cachedir/rootfs/busybox

ln -s -f /busybox $cachedir/rootfs/bin/sh
ln -s -f /proc/self/fd $cachedir/rootfs/dev
ln -s -f /proc/self/fd/2 $cachedir/rootfs/dev/stderr
ln -s -f /proc/self/fd/0 $cachedir/rootfs/dev/stdin
ln -s -f /proc/self/fd/1 $cachedir/rootfs/dev/stdout

if [ $# -ge 2 ];
    then
        cp $builddir/$2 $cachedir/rootfs/;
        mv $cachedir/rootfs/$2 $cachedir/rootfs/user_prog;
fi

if [[ -e $cachedir/rootfs/init ]]; then rm $cachedir/rootfs/init; fi

command=""
if [ $# -eq 2 ];
    then
        command=/user_prog
fi
if [ $# -eq 3 ];
    then
        command=$3;
fi

cat > $cachedir/rootfs/init <<EOF
#!/bin/sh
 
/busybox mount -t proc none /proc
/busybox mount -t sysfs none /sys
/busybox mount -t debugfs none /sys/kernel/debug
/busybox mount /dev -t devtmpfs dev

/busybox echo -e "\nBoot took \$(/busybox cut -d' ' -f1 /proc/uptime) seconds\n"
 
$command

exec /busybox sh
EOF

chmod +x $cachedir/rootfs/init

cd $cachedir/rootfs/
find . | cpio -H newc -o > ../customfs.cpio