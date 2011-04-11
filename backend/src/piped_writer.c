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

int looping_write(int write_pipe, char* bufptr, int nbytes){
    int wbytes;

    while (nbytes > 0) {
        if ((wbytes = write(write_pipe, bufptr, nbytes)) < 0)
            if (errno == ENOTTY)			/* retry. 				*/
                wbytes = write(write_pipe, bufptr, nbytes);

        if (wbytes < 0) {					/* write error			*/
            perror("ERROR: Unable to send file in looping write");
            return -1;
        }
        nbytes -= wbytes;
        bufptr += wbytes;

        if( g_signal != 0 )		/* signal(SIGTERM) writing end. */
            return -1;
	}
    
    return 0;
}

int write_piped(pipes_struct pipes, int pipe_fds, char* bufptr, int nbytes){
    if(looping_write(pipes.writer, bufptr, nbytes) < 0){
        perror("ERROR: Couldn't write to pipes");
    }
    
    
    int rbytes;
    int tbytes = nbytes;
    char buffer[nbytes];
    while(tbytes > 0){
        rbytes = read(pipes.reader, buffer, nbytes);
        if(rbytes < 0){
            perror("ERROR: Unable to read");
            return -1;
        } else if (rbytes > 0){
            if(looping_write(pipe_fds, buffer, rbytes) < 0){
                perror("ERROR: Couldn't write to printer");
                return -1;
            }
            tbytes -= rbytes;
        }
    }
    
    return nbytes;
}
