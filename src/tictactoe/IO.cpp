#include "tictactoe.hpp"
#include "IO.hpp"

std::pair<int, int> take_input() {
    int input, x, y;
    std::cout << "Input row and column as matrix notation: ";
    do {
        std::cin >> input;
        x = input % 10;
        y = input / 10;
    } while (x < SIZE && y < SIZE);

    std::pair<int, int> pos (x, y);
    return pos;
}


void render_row(int row) {
    for (int col = 0; col < SIZE; col++)
        std::cout << " " << GRID[col][row] << " ";
    std::cout << '\n';
}


void render_screen(int turn) {
    std::cout << "Tic Tac Toe\n\n";
    
    int row = 0;
    render_row(row++);
    std::cout << "----+----+-----\n";
    render_row(row++);
    std::cout << "----+----+-----\n";
    render_row(row);

    std::cout << "It's " << (turn == NOUGHT ? "crosses" : "noughts") << " turn\n";
}
