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

    if (out == 1) {
        printf("Congratulations! You won :)\n");
    } else if (out == -1) {
        printf("You finished the game\n");
    } else {
        printf("You lost, but keep trying :(\n");
    }
    printf("The word was: << %s >>\n", secret_word);
    free(secret_word);
    return 0;
}