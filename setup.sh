# Install some useful programs on the container
apt-get install -y cpio xz-utils make

# Install busybox

if [ ! -d cache ]
then
    mkdir cache
fi
cd cache

if [ ! -d busybox ]
then
    mkdir busybox
fi
cd busybox

if [ ! -e busybox-binaries.tar.bz2 ]
then
    wget https://www.busybox.net/downloads/binaries/1.21.1/busybox-binaries.tar.bz2
fi
tar -xf busybox-binaries.tar.bz2
cp busybox-i486 busybox-i386

if [ ! -d temp ]
then
    mkdir temp
fi
cd temp

if [ ! -e busybox-1.36.1-2-aarch64.pkg.tar.xz ]
then
    wget http://mirror.archlinuxarm.org/aarch64/extra/busybox-1.36.1-2-aarch64.pkg.tar.xz
fi
unxz busybox-1.36.1-2-aarch64.pkg.tar.xz
tar -xf busybox-1.36.1-2-aarch64.pkg.tar
cp ./usr/bin/busybox ../busybox-aarch64
cd ..
cd ..

# Install some pip dependencies
python3 -m pip install --upgrade pip
pip install --upgrade ipython pytest pytest-cov

chmod +x /mount/make_initrd.sh

pandaLoc=/mount/cache/.panda
rootfsLoc=/mount/cache/rootfs

# Symlink the qcows to the host so we only download them once
if [[ ! -d $pandaLoc ]]; then mkdir $pandaLoc; fi
if [[ -L /root/.panda ]]; then rm /root/.panda; fi
ln -sf $pandaLoc /root/.panda
