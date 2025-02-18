#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
//open a file
//give the file descriptor to plugin
//make a new filereader for arm??
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

        int input = file_thing;
        int output;

        asm __volatile__
        ("push {%%r0-%%r4} \t\n\
        mov %%r0, %0 \t\n\
        mov %%r1, %1 \t\n\
        mov %%r2, %2 \t\n\
        mov %%r3, %3 \t\n\
        mcr p7, 0, r0, c0, c0, 0 \t\n\
        pop {%%r0-%%r4} \t\n"
      
      : /* no output registers */
      : "r" (input), "r" (input), "r" (input), "r" (input), "r" (input) /* input operands */
      : "r0","r1","r2","r3","r4" /* clobbered registers */
      );
    }
    return file_thing;

}