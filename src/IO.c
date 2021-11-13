#include "IO.h"

int get_word(char *filename)
{
    FILE *fp = fopen(filename, 'r');
}

void clear_screen()
{
    system(CLEAN_CMD);
}