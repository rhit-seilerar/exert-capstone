# Install some useful programs on the container
apt-get install -y cpio

# Install some pip dependencies
pip install --upgrade ipython pytest pytest-cov

pandaLoc=/mount/exert/usermode/.panda

# Symlink the qcows to the host so we only download them once
if [[ ! -d $pandaLoc ]]; then mkdir $pandaLoc; fi
if [[ -L /root/.panda ]]; then rm /root/.panda; fi
ln -sf $pandaLoc /root/.panda
