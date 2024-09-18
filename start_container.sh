#!/bin/bash

# Stop and kill the existing container
docker stop pandare 2> /dev/null
docker rm pandare 2> /dev/null

# Start a new instance of the container and mount this repo to /mount
docker run --rm -dit --name pandare -v "$(realpath $(dirname $0)):/mount" pandare/panda

# Setup the container
docker exec -it pandare /mount/setup.sh

# Attach this terminal to the container
./attach_to_container.sh
