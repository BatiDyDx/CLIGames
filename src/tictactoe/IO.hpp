#pragma once

#include <stdlib.h>

#ifdef _WIN32
    #define CLEAN_CMD "cls"
#else
    #define CLEAN_CMD "clear"
#endif

#define clean_screen() system(CLEAN_CMD);

std::pair<int, int> take_input();

void render_row(int row);

void render_screen(int turn);
