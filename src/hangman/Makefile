CC = gcc
BIN = hangman
FLAGS = -Wall

SRC = hangman.c IO.c main.c
OBJS = hangman.o IO.o main.o

.PHONY: clean install

$(BIN):
	$(CC) $(FLAGS) $(SRC) -o $(BIN)

install: compile
	cp $(BIN) ../../bin

%.o: %.c
	$(CC) $(FLAGS) $< -o $@

clean:
	rm *.o