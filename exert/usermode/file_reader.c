#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include "hypercall.h"
//open a file
//give the file descriptor to plugin
int main(int argc, char** argv){
    if(argc <= 1){
        return -1;
    }
    int file_thing = open(argv[1], O_RDONLY);
    // printf("will this print?");
    // printf("eels %d \n", file_thing);
    // checking if the file is created
    if (close(file_thing) == -1) {
        printf("Not opened\n");
        exit(-1);
    }
    else {
        printf("The file is: %d\n", file_thing);
        igloo_hypercall(0, file_thing);
    }
    return file_thing;

}