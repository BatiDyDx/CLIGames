#ifndef IO_H
    #define IO_H

    #include <time.h>
    #include <stdlib.h>
    #include <stdio.h>
    #include <assert.h>
    #include <string.h>


    #ifdef _WIN32
        #define CLEAN_CMD "cls"
    #else
        #define CLEAN_CMD "clear"
    #endif

    typedef struct {
            int num_lines;
            char** lines;
    } FILE_CONTENT;

    /*
    Opens a file using fopen, exiting with an error code
    if not able to open the file, else returning the FILE
    corresponding structure pointer
    */
    FILE* open_or_exit(const char* filename, char* mode);

    /*
    Given the name of a file containing possible words for
    the game, it returns a random one
    */ 
    char* get_word(const char *filename);

    /*
    Returns a random integer between min and max,
    only low endpoint included
    */
    static int random_num(int min, int max);

    /*
    Returns a FILE_CONTENT with the number of
    lines and an array of pointers pointing to
    the lines of the file
    */
    FILE_CONTENT readlines(FILE* fp);

    /*
    Takes a pointer to a FILE_CONTENT and
    frees each element of the array of lines
    and the array itself
    */
    void free_FILE_CONTENT(FILE_CONTENT* fc);

    /*
    Clears command line
    */
    void clear_screen(void);

#endif