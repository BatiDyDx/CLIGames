#include "tictactoe.hpp"


int check_winner() {
    int row_sum, col_sum;
    for (int i = 0; i < SIZE; i++, row_sum = col_sum = 0) {
        for (int j = 0; j < SIZE; j++) {
            row_sum += GRID[i][j];
            col_sum += GRID[j][i];
        }
        if (row_sum == NOUGHT * 3 || col_sum == NOUGHT * 3) {
            return NOUGHT;
        } else if (row_sum == CROSS * 3 || col_sum == CROSS * 3) {
            return CROSS;
        }
    }
    return 0;
}


int play() {
    int result;
    std::pair<int, int> pos;
    do
    {
        clean_screen();
        render_screen(0);
        pos = take_input();
        GRID[pos.second][pos.first] = 1;
    } while (!(result = check_winner()));
    return result;
}
