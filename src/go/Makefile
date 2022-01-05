GOC = go build
BIN = hangman_go
FLAGS = 

# subject to change in future
SRC = hangman.c IO.c main.c
OBJS = hangman.o IO.o main.o

.PHONY: clean install

compile: $(OBJS)
	$(GOC) $(FLAGS) $< -o $(BIN)

install: compile
	mv $(BIN) ../../bin

%.o: %.go
	$(GOC) $(FLAGS) $< -o $@

clean:
	rm *.o