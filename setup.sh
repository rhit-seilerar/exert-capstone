# Install some useful programs on the container
apt-get install -y cpio xz-utils make

# Install busybox
mkdir cache
cd cache
mkdir busybox
cd busybox
wget https://www.busybox.net/downloads/binaries/1.21.1/busybox-binaries.tar.bz2
tar -xf busybox-binaries.tar.bz2
cp busybox-i486 busybox-i386
rm busybox-binaries.tar.bz2

mkdir temp
cd temp
wget http://mirror.archlinuxarm.org/aarch64/extra/busybox-1.36.1-2-aarch64.pkg.tar.xz
unxz busybox-1.36.1-2-aarch64.pkg.tar.xz
tar -xf busybox-1.36.1-2-aarch64.pkg.tar
cp ./usr/bin/busybox ../busybox-aarch64
cd ..
rm -r temp
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
