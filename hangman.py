import random
import sys
import os


if os.name == "posix":
    CLEAN_CMD = "clear"
elif os.name == "nt":
    CLEAN_CMD = "cls"
else:
    raise RuntimeWarning(
        """Clearing command line for operative systems others than Windows, OS X and Linux distributions is not supported"""
    )


def clean_screen() -> None:
    os.system(CLEAN_CMD)


def get_word(filename: str) -> str:
    with open(filename, 'r') as f:
        words = f.readlines()
    word = random.choice(words).strip().upper()
    return word


def make_guess() -> str:
    char = input("Insert an alphanumerical character (or 1 to quit): ").upper()
    while not (char.isalpha or char == '1'):
        return make_guess()
    return char


def replace_char(char: str, src: str, to: str) -> str:
    to_chars = list(to)
    for i in range(len(src)):
        if src[i] == char:
            to_chars[i] = char
    return "".join(to_chars)


def render_screen(lives: int, word: str, wrong_attempts) -> None:
        print(f"Lives remaining: {lives}")
        print(f"The word is: {word}")
        if wrong_attempts:
            print(f"Your wrong guesses are: ", end='')
            print(*wrong_attempts, sep=', ')


def play(sec_word: str) -> int:
    player_word: str = '_' * len(sec_word)
    wrong_guesses = set()
    lives: int = 5
    while lives > 0 and player_word != sec_word:
        clean_screen()
        render_screen(lives, player_word, wrong_guesses)
        guess = make_guess()
        if guess == '1': break
        elif guess in sec_word:
            player_word = replace_char(guess, sec_word, player_word)
        else:
            if not guess in wrong_guesses:
                lives -= 1
                wrong_guesses.add(guess)

    clean_screen()
    if guess == '1':
        out = -1
    elif lives == 0:
        out = 0
    else:
        out = 1

    return out


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 hangman.py <file>")
        return
    filename = sys.argv[1]
    secret_word = get_word(filename)
    game_status = play(secret_word)
    if game_status == 1:
        print(f"Congratulations! You won :)")
    elif game_status == -1:
        print(f"You finished the game")
    else:
        print(f"You lost, but keep trying")
    print(f"The word was: << {secret_word} >>")


if __name__ == '__main__':
    main()