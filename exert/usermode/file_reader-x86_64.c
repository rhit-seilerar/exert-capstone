#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <cpuid.h>
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

        __asm ( "mov %1, %%eax; "
            "cpuid;"
            "mov %%eax, %0;"
            :"=r"(output)
            :"r"(input)
            :"%eax","%ebx","%ecx","%edx"
        );
    }
  
    return file_thing;

}