#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


#define SECRET_WORD "PATATA"
#define INIT_LIVES 5

char make_guess(void)
{
    char c;
    char tmp[2];
    printf("Input a character: ");
    scanf("%s", tmp);

    c = tmp[0];
    // if the guess is an uppercase char, convert it to lowercase
    if (islower(c))
    {
        c = toupper(c);
    }

    return c;
}

int is_guess_correct(char c)
{
    if (strchr(SECRET_WORD, c) == NULL) return 0;

    return 1;
}


void print_correct_guesses(char *s)
{
    int len = strlen(SECRET_WORD);
    char *str = malloc(sizeof(char) * (len + 1));
    
    for (int i = 0; i < len; i++)
    {
        if (strchr(s, SECRET_WORD[i]) != NULL)
        {
            str[i] = SECRET_WORD[i];
        }
        else
        {
            str[i] = '_';
        }
    }
    str[len] = '\0';
    printf("The word is: %s\n", str);
    free(str);
}


void print_wrong_guesses(char *s)
{
    char c;
    int i = 0;
    
    printf("Wrong guesses:");
    while ((c = s[i++]) != '\0')
    {
        printf(" %c", c);
    }
    printf("\n");
}


int main()
{
    int len_secret_word = strlen(SECRET_WORD);
    int lives = INIT_LIVES;
    int endgame = 0;

    char *correct_guesses = malloc(sizeof(char) * (len_secret_word + 1));
    char *incorrect_guesses = malloc(sizeof(char) * (INIT_LIVES + 1));

    char guess;
    while ((lives > 0) || !(endgame))
    {
        guess = make_guess();
        // Check the guess hasnt been already made
        if (strchr(correct_guesses, guess) != NULL || strchr(incorrect_guesses, guess) != NULL)
        {
            continue;
        }
        
        if (is_guess_correct(guess))
        {
            // Add guess to correct_guesses
            
            // check if game has ended
        } 
        else
        {
            incorrect_guesses[INIT_LIVES - lives] = guess;
            lives--;
        }
        // Render game
        // Write number of lives left
        printf("Lives: %d\n", lives);

        // Write blank spaces with guessed chars
        print_correct_guesses(correct_guesses);

        // Write down wrong guesses
        print_wrong_guesses(incorrect_guesses);
    }
    if (lives == 0)
    {
        printf("You lost, the word was %s: \n", SECRET_WORD);
    }
    
    free(correct_guesses);
    free(incorrect_guesses);

    return 0;

}