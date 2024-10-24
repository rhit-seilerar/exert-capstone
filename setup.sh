# Install some useful programs on the container
apt-get install -y cpio

# Install some pip dependencies
pip install --upgrade ipython pytest pytest-cov

# Symlink the qcows to the host so we only download them once
if [[ ! -d /mount/.panda ]]; then mkdir /mount/exert/usermode/.panda; fi
if [[ -L /root/.panda ]]; then rm /root/.panda; fi
ln -sf /mount/exert/usermode/.panda /root/.panda
