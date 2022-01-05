CC = gcc
BIN = hangman_c
FLAGS = -Wall

SRC = hangman.c IO.c main.c
OBJS = hangman.o IO.o main.o

.PHONY: clean install

compile: $(OBJS)
	$(CC) $(FLAGS) $< -o $(BIN)

install: compile
	mv $(BIN) ../../bin

%.o: %.c
	$(CC) $(FLAGS) $< -o $@

clean:
	rm *.o