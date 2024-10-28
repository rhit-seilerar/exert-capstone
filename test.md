# Manual Testing Procedures

## Black-Box

### Init
1. Run `python exert.py init`
2. Validate that `pandare/panda:latest` and `ghcr.io/panda-re/embedded-toolchains:latest` are pulled
3. Validate that `EXERT successfully initialized!` is printed

### Dev

#### Reset
1. Run `python exert.py dev attach`
2. Run `python exert.py dev reset`
3. Run `docker ps`
4. Verify that no `pandare` container is running

#### Attach
1. Run `python exert.py dev attach`
2. Validate that `setup.sh` is run
3. Validate that you are dropped into `/mount`
4. Run `docker ps` and take note of the running container
5. Open another shell and run `python exert.py dev attach`
6. Run `docker ps` and validate that terminal attached to the previous container

#### Test
1. Run `python exert.py dev test`
2. Validate that `setup.sh` is run
3. Validate that all tests are run

### Ramdisk Generator
1. Uncomment the lines in plugin.py that run the file
2. Comment out the generic Panda line and the line for running the uname serial command
3. Run `from exert.usermode import plugin` and `plugin.run()` in Python in the Docker container.
4. Snapshots will error, but otherwise the emulator will start and end as expected.

### Dev-compile
1. Run `python exert.py dev compile arm musleabi`
2. Check if `exert/usermode/build/helloworld` was created
3. Run `python exert.py dev attach`
4. Run `/mount/exert/usermode/build/helloworld`
5. Verify "hello world" is printed to the terminal
