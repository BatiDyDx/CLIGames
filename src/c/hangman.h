#ifndef HANGMAN_H
    #define HANGMAN_H

    #include "IO.h"
    #include <ctype.h>

    #define LIVES 6

    /*
    Initialize word to a string of underscores '_' of size len,
    and initializes all elements of attempts to '\0'
    */
    void init(char *word, int len, char attempts[LIVES-1]);

    /*
    Asks user for an input character, making sure
    it is an alphabetic number or 1.
    Returns it uppercased
    */
    char make_guess(void);

    /*
    Copies c to _to in all positions where c
    is present in _from. Returns pointer to _to.
    Example, replace_char('c', "coconut", "banana")
    would modify "banana" to "cacana"
    Returns c
    */
    char replace_char(char c, const char* _from, char* _to);

    /*
    Returns 1 if char c is in attempts. Else returns 0,
    adding c to the first position in attempts where
    the element is '\0'
    */
    int tried_attempt(char c, char attempts[LIVES-1]);

    /*
    Prints to terminal the interface of the game
    */
    void render_screen(int current_lives, const char* player_word, char attempts[LIVES-1]);

    /*
    Runs the logic of the hangman given a secret word,
    asking for user to guess the word.
    Returns an int indicating the status in which the
    game finished. 1 if is a win, 0 if is a loss, and -1
    if game was quitted
    */
    int play(const char *secret_word);

#endif