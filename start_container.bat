REM Stop and kill the existing container
docker stop pandare 2> NUL
docker rm pandare 2> NUL

REM Start a new instance of the container and mount this repo to /mount
docker run --rm -dit --name pandare -v "%~dp0:/mount" pandare/pandadev

REM Setup the container
docker exec -it pandare /mount/setup.sh

REM Attach a terminal to the container and exit
call attach_to_container.bat
exit /b 0
