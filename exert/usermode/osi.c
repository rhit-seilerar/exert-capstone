#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hypercall.h"

int data_address() {
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

int task_struct_size() {
    FILE *slabInfo = fopen("/proc/slabinfo", "r");
    char * line = NULL;
    size_t len = 0;
    size_t read;

    if (slabInfo == NULL)
        exit(EXIT_FAILURE);

    while (read = getline(&line, &len, slabInfo) != -1) {
        if (strstr(line, "task_struct")) {
            igloo_hypercall2(204, (unsigned long) line, (unsigned long) len);
            return 0;
        }
    }
}

int main(int argc, char** argv) {

    if (strncmp(argv[1], "data_address", 13) == 0) {
        return data_address();
    }

    if (strncmp(argv[1], "task_struct_size", 17) == 0) {
        return task_struct_size();
    }

    return 0;
}