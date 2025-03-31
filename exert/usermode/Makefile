all: setup file_reader-x86_64 file_reader-armv5l file_reader-i386 file_reader-aarch64 dmesg-i386 dmesg-x86_64 dmesg-armv5l dmesg-aarch64

CC_i386 = /opt/cross/i686-linux-musl-cross/bin/i686-linux-musl-cc

CC_X86_64 = /opt/cross/x86_64-linux-musl-cross/bin/x86_64-linux-musl-cc

CC_ARM = /opt/cross/arm-linux-musleabi-cross/bin/arm-linux-musleabi-cc

CC_AARCH64 = /opt/cross/aarch64-linux-musl-cross/bin/aarch64-linux-musl-cc

CFLAGS += -ggdb -static-libgcc -static

.PHONY: setup clean all

file_reader-i386: file_reader.c
	${CC_i386} ${CFLAGS} -o build/$@ $^

file_reader-x86_64: file_reader.c
	${CC_X86_64} ${CFLAGS} -o build/$@ $^

file_reader-armv5l: file_reader.c
	${CC_ARM} ${CFLAGS} -o build/$@ $^

file_reader-aarch64: file_reader.c
	${CC_AARCH64} ${CFLAGS} -o build/$@ $^

dmesg-i386: dmesg.c
	${CC_i386} ${CFLAGS} -o build/$@ $^

dmesg-x86_64: dmesg.c
	${CC_X86_64} ${CFLAGS} -o build/$@ $^

dmesg-armv5l: dmesg.c
	${CC_ARM} ${CFLAGS} -o build/$@ $^

dmesg-aarch64: dmesg.c
	${CC_AARCH64} ${CFLAGS} -o build/$@ $^

setup:
	@if [ ! -d build ]; then mkdir build; fi

clean:
	rm -rf build
