#!/bin/bash

# Install some useful programs on the container
apt-get install vim gdb

# Symlink the qcows to the host so we only download them once
ln -sf /mount/.panda /root/.panda

# Move into the repo
cd /mount
