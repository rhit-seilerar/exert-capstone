

# Install some useful programs on the container
apt-get install vim gdb

#create a folder for panda output
# Symlink the qcows to the host so we only download them once
mkdir /mount/.panda
ln -sf /mount/.panda /root/.panda

# Move into the repo
cd /mount
