CC = g++
BIN = tictactoe
FLAGS = -Wall

SRC = tictactoe.cpp main.cpp IO.cpp

.PHONY: clean install

$(BIN): $(SRC)
	$(CC) $(SRC) $(FLAGS) -o $(BIN)

install: $(BIN)
	cp $(BIN) ../../bin

clean:
	rm *.o