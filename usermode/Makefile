all: helloworld

CFLAGS += -ggdb -static-libgcc -static

.PHONY: clean all

%: %.c
	${CC} ${CFLAGS} -o $@ $^

clean:
	rm -rf helloworld
