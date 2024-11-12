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

# Symlink the qcows to the host so we only download them once
if [[ ! -d $pandaLoc ]]; then mkdir $pandaLoc; fi
if [[ -L /root/.panda ]]; then rm /root/.panda; fi
ln -sf $pandaLoc /root/.panda
