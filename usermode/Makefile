all: setup helloworld

# CC = ./cross/${ARCH}-linux-${LIBC}-cross/bin/${ARCH}-linux-${LIBC}-gcc

CFLAGS += -ggdb -static-libgcc -static

.PHONY: setup clean all

%: %.c
	${CC} ${CFLAGS} -o build/$@ $^

setup:
	mkdir build

clean:
	rm -rf helloworld
