all: setup file_reader

CC = /opt/cross/${ARCH}-linux-${LIBC}-cross/bin/${ARCH}-linux-${LIBC}-gcc

CFLAGS += -ggdb -static-libgcc -static

.PHONY: setup clean all

%: %.c
	${CC} ${CFLAGS} -o build/$@ $^

setup:
	if [ ! -d build ]; then mkdir build; \
	fi

clean:
	rm -rf build
