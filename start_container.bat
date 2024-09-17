docker stop pandare 2> nul
docker rm pandare 2> nul
docker run --rm -dit --name pandare -v "%~dp0:/mount" pandare/pandadev
#docker exec -it pandare /mount/setup.sh
exit /b 0