all: setup file_reader-x86_64 file_reader-armv5l file_reader-i386

CC_i386 = /opt/cross/i686-linux-musl-cross/bin/i686-linux-musl-cc

CC_X86_64 = /opt/cross/x86_64-linux-musl-cross/bin/x86_64-linux-musl-cc

CC_ARM = /opt/cross/arm-linux-musleabi-cross/bin/arm-linux-musleabi-cc

CFLAGS += -ggdb -static-libgcc -static

.PHONY: setup clean all

file_reader-i386: file_reader-i386.c
	${CC_i386} ${CFLAGS} -o build/$@ $^

file_reader-x86_64: file_reader-x86_64.c
	${CC_X86_64} ${CFLAGS} -o build/$@ $^

file_reader-armv5l: file_reader-armv5l.c
	${CC_ARM} ${CFLAGS} -o build/$@ $^

setup:
	if [ ! -d build ]; then mkdir build; \
	fi

clean:
	rm -rf build
