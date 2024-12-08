#!/bin/bash

cachedir=$(pwd)/cache
echo $cachedir

# Refresh
pushd /tmp/
rm -rf initramfs
mkdir initramfs

# Populate the filesystem (subdirectories)
mkdir initramfs/bin
mkdir initramfs/sys
mkdir initramfs/dev
mkdir initramfs/proc

# Grab busybox and create the symbolic links
pushd initramfs/bin
cp "$cachedir/busybox-$1" ./busybox
ln -s busybox ash
ln -s busybox mount
ln -s busybox echo
ln -s busybox ls
ln -s busybox cat
ln -s busybox ps
ln -s busybox dmesg
ln -s busybox sysctl
popd

# Grab the necessary dev files
cp -a /dev/console /tmp/initramfs/dev/console
cp -a /dev/ram0 /tmp/initramfs/dev/ram0
cp -a /dev/null /tmp/initramfs/dev/null
if [[ -e /dev/ttyS0 ]]; then cp -a /dev/ttyS0 /tmp/initramfs/dev/ttyS0; fi
if [[ -e /dev/tty ]]; then cp -a /dev/tty /tmp/initramfs/dev/tty; fi
if [[ -e /dev/tty1 ]]; then cp -a /dev/tty1 /tmp/initramfs/dev/tty1; fi
if [[ -e /dev/tty2 ]]; then cp -a /dev/tty2 /tmp/initramfs/dev/tty2; fi

# Equate sbin with bin
pushd /tmp/initramfs
ln -s bin sbin
popd

# Create the init file
cat >> /tmp/initramfs/linuxrc << EOF
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

chmod +x /tmp/initramfs/linuxrc

cd /tmp/initramfs
find . -print0 | cpio --null -ov --format=newc | gzip > ../initramfs.cpio.gz
cd ..

popd
cp /tmp/initramfs.cpio.gz .