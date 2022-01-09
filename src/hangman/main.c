#include "main.h"

int main(int argc, char const *argv[]) 
{
    int out;

    if (argc != 2)
    {
        printf("Usage: %s <file>\n", argv[0]);
        return 1;
    }
    
    char *secret_word = get_word(argv[1]);
    out = play(secret_word);

    switch (out) {
    case -1:
        printf("You finished the game\n");
        break;
    case 0:
        printf("You lost, but keep trying :(\n");
        break;
    default:
        printf("Congratulations! You won :)\n");
        break;
    }
    printf("The word was: << %s >>\n", secret_word);
    free(secret_word);
    return 0;
}