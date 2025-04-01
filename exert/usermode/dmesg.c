#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hypercall.h"

int main(int argc, char** argv) {
    FILE *dmesgD = popen("dmesg", "r");
    char * line = NULL;
    size_t len = 0;
    size_t read;

    if (dmesgD == NULL)
        exit(EXIT_FAILURE);

    while (read = getline(&line, &len, dmesgD) != -1) {
        if (strstr(line, ".data")) {
            igloo_hypercall2(204, (unsigned long) line, (unsigned long) len);
            return 0;
        }
    }
}