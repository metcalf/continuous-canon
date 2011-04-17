#include <piped_writer.h>

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

pipes_struct get_write_pipes(){
    pipes_struct pipes;
    
    pipes.writer = open(INPUT_PIPE_NAME, INPUT_PIPE_MODE);
    pipes.reader = open(OUTPUT_PIPE_NAME, OUTPUT_PIPE_MODE);
    
    return pipes;
}

int piped_transform(pipes_struct pipes, char* readptr, char* writeptr, int nbytes){
    int wbytes, rbytes;
    
    wbytes = write(pipes.writer, readptr, nbytes);
    if(wbytes < nbytes){
        return -1;
    }
    
    rbytes = read(pipes.reader, writeptr, wbytes);
    if(rbytes < 0){
            perror("ERROR: Unable to read");
            return -1;
        }
    return rbytes;
}
