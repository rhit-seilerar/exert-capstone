all: helloworld

CFLAGS += -ggdb

.PHONY: clean all

%: %.c
	${CC} ${CFLAGS} -o $@ $^

clean:
	rm -rf helloworld
