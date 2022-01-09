#pragma once

#include <iostream>
#include <utility>
#include "IO.hpp"

enum Game {TIE = 1, NOUGHT = 'O', CROSS = 'X'};

#define SIZE 3
static int GRID[SIZE][SIZE];

int check_winner();

int play();
