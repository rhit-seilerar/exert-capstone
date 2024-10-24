# Install some useful programs on the container
apt-get install -y cpio

# Install some pip dependencies
pip install ipython pytest pytest-cov lz4 zstandard git+https://github.com/clubby789/python-lzo@b4e39df git+https://github.com/marin-m/vmlinux-to-elf

# Symlink the qcows to the host so we only download them once
if [[ ! -d /mount/.panda ]]; then mkdir /mount/.panda; fi
if [[ -L /root/.panda ]]; then rm /root/.panda; fi
ln -sf /mount/.panda /root/.panda
