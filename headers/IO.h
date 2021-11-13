#ifndef IO_H
#define IO_H

#include <ranlib.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

#ifdef _WIN32
    #define CLEAN_CMD "cls"
#else
    #define CLEAN_CMD "clear"
#endif

/*
Given the name of a file containing possible words for
the game, it returns a random one
*/ 
int get_word(char *filename);

/*
Clears command line
*/
void clear_screen(void);

#endif