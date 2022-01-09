#include "main.hpp"

int main() {
    
    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
            GRID[i][j] = 0;
    }
    

    int winner = play();
    switch (winner)
    {
    case NOUGHT:
        std::cout << "Player with noughts wins" << std::endl;
        break;
    
    case CROSS:
        std::cout << "Player with crosses wins" << std::endl;
    
    case TIE:
        std::cout << "It's a tie" << std::endl;
        break;
    }
    return 0;
}