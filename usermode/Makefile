all: helloworld

CC = ./cross/${ARCH}-linux-${LIBC}-cross/bin/${ARCH}-linux-${LIBC}-gcc

CFLAGS += -ggdb -static-libgcc -static

.PHONY: clean all

%: %.c
	${CC} ${CFLAGS} -o build/$@ $^

clean:
	rm -rf helloworld
