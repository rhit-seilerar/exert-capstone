#!/bin/bash

# Ramdisk Constants
RDSIZE=4000
BLKSIZE=1024

# Referesh
rm -rf /mnt/initrd
mkdir /mnt/initrd

# Create an empty ramdisk image
dd if=/dev/zero of=/tmp/ramdisk.img bs=$BLKSIZE count=$RDSIZE

# Make it an ext2 mountable file system
/sbin/mke2fs -F -m 0 -b $BLKSIZE /tmp/ramdisk.img $RDSIZE

# Mount it so that we can populate
mount /tmp/ramdisk.img /mnt/initrd -t ext2 -o loop

# Populate the filesystem (subdirectories)
mkdir /mnt/initrd/bin
mkdir /mnt/initrd/sys
mkdir /mnt/initrd/dev
mkdir /mnt/initrd/proc

# Grab busybox and create the symbolic links
pushd /mnt/initrd/bin
cp /mount/cache/busybox/busybox-$1 .
ln -s busybox-armv4l ash
ln -s busybox-armv4l mount
ln -s busybox-armv4l echo
ln -s busybox-armv4l ls
ln -s busybox-armv4l cat
ln -s busybox-armv4l ps
ln -s busybox-armv4l dmesg
ln -s busybox-armv4l sysctl
popd

# Grab the necessary dev files
cp -a /dev/console /mnt/initrd/dev
cp -a /dev/null /mnt/initrd/dev
if [[ -e /dev/tty ]]; then cp -a /dev/tty /mnt/initrd/dev; fi
if [[ -e /dev/tty1 ]]; then cp -a /dev/tty1 /mnt/initrd/dev; fi
if [[ -e /dev/tty2 ]]; then cp -a /dev/tty2 /mnt/initrd/dev; fi

# Equate sbin with bin
pushd /mnt/initrd
ln -s bin sbin
popd

# Create the init file
cat >> /mnt/initrd/linuxrc << EOF
#!/bin/ash
echo
echo "Simple initrd is active"
echo
mount -t proc /proc /proc
mount -t sysfs none /sys
uname -r
/bin/ash
EOF

# cp $1 /$1

chmod +x /mnt/initrd/linuxrc

# Finish up...
umount /mnt/initrd
gzip -f -9 /tmp/ramdisk.img
cp /tmp/ramdisk.img.gz ./ramdisk.img.gz