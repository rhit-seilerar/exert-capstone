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
