# Install some useful programs on the container
apt-get install -y cpio

# Install busybox
mkdir cache
cd cache
mkdir busybox
cd busybox
wget https://www.busybox.net/downloads/binaries/1.21.1/busybox-binaries.tar.bz2
tar -xf busybox-binaries.tar.bz2
cp busybox-i486 busybox-i386
rm busybox-binaries.tar.bz2
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

# Pull the rootfs folder and copy it into the cache
rm -r /tmp/panda
cd /tmp/
git clone https://github.com/panda-re/panda.git
cd panda
git switch kernelinfo_user
cd panda/plugins/osi_linux/utils/kernelinfo_user
cp -r rootfs $rootfsLoc