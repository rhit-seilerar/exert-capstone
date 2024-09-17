docker stop pandare 2> /dev/null
docker rm pandare 2> /dev/null
docker run --rm -dit --name pandare -v "$(realpath $(dirname $0)):/mount" pandare/panda
docker exec -it pandare /mount/setup.sh
