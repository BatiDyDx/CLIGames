#include "hangman.h"

void init(char *word, int len, char attempts[LIVES-1]) {
    for (int i = 0; i < len; word[i] = '_', i++);
    word[len] = '\0';
    for (int i = 0; i < LIVES-1; i++)
        attempts[i] = '\0';
}

char make_guess() {
    char c;
    printf("Input an alphabetic character (or 1 to quit): ");
    do {
        scanf("%c", &c);
    } while (!isalpha(c) && c != '1');
    return toupper(c);
}

char replace_char(char c, const char* _from, char* _to) {
    
    for (; *_from && *_to; _from++, _to++) {
        if (*_from == c)
            *_to = c;
    }
    return c;
}

int tried_attempt(char c, char attempts[LIVES-1]) {
    int i;
    for (i = 0; attempts[i] != '\0'; i++) {
        if (attempts[i] == c)
            return 1;
    }
    attempts[i] = c;
    return 0;
}

void render_screen(int current_lives, const char* player_word, char attempts[LIVES-1]) {
    printf("Lives remaining: %d\n", current_lives);
    printf("The word is: %s\n", player_word);
    printf("Your wrong guesses are:");
    while (*attempts != '\0') {
        printf(" %c", *attempts);
        attempts++;
    }
    printf("\n");
}

int play(const char *secret_word)
{
    int current_lives = LIVES;
    const int len = strlen(secret_word);
    char previous_attempts[LIVES - 1];
    char *player_word = malloc(sizeof(char) * (len + 1));
    init(player_word, len, previous_attempts);
    char guess;

    while (strcmp(player_word, secret_word) != 0 && current_lives > 0) {
        clear_screen();
        render_screen(current_lives, player_word, previous_attempts);
        guess = make_guess();
        if (guess == '1') {
            break;
        } else if (strchr(secret_word, guess) != NULL) {
            replace_char(guess, secret_word, player_word);
        } else {
            if (tried_attempt(guess, previous_attempts))
                continue;
            current_lives--;
        }
    }
    clear_screen();
    free(player_word);

    if (guess == '1') {
        return -1;
    }
    return current_lives;
}