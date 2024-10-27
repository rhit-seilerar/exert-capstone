# Install some useful programs on the container
apt-get install -y gcc cpio liblzo2-dev

# Install some pip dependencies
python3 -m pip install --upgrade pip
pip install --upgrade ipython pytest pytest-cov lz4 zstandard 
pip install --upgrade git+https://github.com/clubby789/python-lzo@b4e39df git+https://github.com/zestrada/vmlinux-to-elf

pandaLoc=/mount/exert/usermode/.panda

# Symlink the qcows to the host so we only download them once
if [[ ! -d $pandaLoc ]]; then mkdir $pandaLoc; fi
if [[ -L /root/.panda ]]; then rm /root/.panda; fi
ln -sf $pandaLoc /root/.panda
