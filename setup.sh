# Install some useful programs on the container
apt-get update && apt-get install -y vim gdb

# Install some pip dependencies
pip install ipython

# Symlink the qcows to the host so we only download them once
if [[ ! -d /mount/.panda ]]; then mkdir /mount/.panda; fi
if [[ -L /root/.panda ]]; then rm /root/.panda; fi
ln -sf /mount/.panda /root/.panda

# Move into the repo
cd /mount
