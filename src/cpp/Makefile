CPP = g++
BIN = hangman_cpp
FLAGS = -Wall

SRC = hangman.cpp IO.cpp main.cpp
OBJS = hangman.o IO.o main.o

.PHONY: clean install

compile: $(OBJS)
	$(CPP) $(FLAGS) $< -o $(BIN)

install: compile
	mv $(BIN) ../../bin

%.o: %.cpp
	$(CPP) $(FLAGS) $< -o $@

clean:
	rm *.o