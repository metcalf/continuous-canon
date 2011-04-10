#define INPUT_PIPE_NAME "/dev/pcin"
#define OUTPUT_PIPE_NAME "/dev/pcout"
#define INPUT_PIPE_MODE O_WRONLY
#define OUTPUT_PIPE_MODE O_RDONLY

typedef struct {
    int reader;
    int writer;
} pipes_struct;