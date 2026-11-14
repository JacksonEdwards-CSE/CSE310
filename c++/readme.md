# C++ Tic-Tac-Toe

A C++ console application that lets two players play a game of Tic-Tac-Toe. The project uses a `Game` class to manage the board, player turns, move validation, win conditions, and draw detection.

## Features

- Display a numbered 3-by-3 board for selecting moves.
- Alternate turns between player `X` and player `O`.
- Accept moves from 1 through 9 using standard console input.
- Reject invalid input and spaces that have already been taken.
- Check all rows, columns, and diagonals for a winning combination.
- Detect a full board and report a draw.
- Allow the user to quit by entering `q` or `Q`.

## Instructions for Build and Use

### Prerequisites

- Visual Studio with the Desktop development with C++ workload
- A compiler that supports C++20

### Build the application

Open `CSE310-Sprint4\CSE310-Sprint4.slnx` in Visual Studio. Select the `x64` platform and the `Debug` configuration, then choose **Build > Build Solution**.

### Run the game

Run the generated executable from Visual Studio or launch:

```text
CSE310-Sprint4\x64\Debug\CSE310-Sprint4.exe
```

At each turn, enter a number from 1 to 9 that corresponds to an open location on the board. Enter `q` to exit the game.

## Development Environment

The project was developed with:

- C++20
- Visual Studio and the MSVC compiler
- The C++ standard library, including `array`, `cctype`, `iostream`, and `string`
- A console application project targeting x64

## Project Structure

```text
c++/
├── CSE310-Sprint4/
│   ├── CSE310-Sprint4.slnx       # Visual Studio solution
│   └── CSE310-Sprint4/
│       ├── CSE310-Sprint4.cpp    # Game implementation and main loop
│       └── game_data.json        # Project data file
├── readme.md                     # Project documentation
└── sprint_time_log.md            # Development time log
```

## Program Design

The `Game` class stores the nine board spaces and the current round number. Its methods handle displaying the board, determining the current piece, placing valid moves, checking the eight possible winning lines, and detecting when the board is full. The `main` function manages the input loop and reports wins, draws, invalid moves, and quits.

## Useful Websites to Learn More

- [C++ reference](https://en.cppreference.com/w/)
- [Microsoft C++ documentation](https://learn.microsoft.com/en-us/cpp/)
- [Visual Studio C++ documentation](https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation?view=msvc-170)

## Future Work

- [ ] Add automated tests for move validation and win detection.
- [ ] Add save and load support for unfinished games.
- [ ] Add a replay option after a win or draw.
- [ ] Improve input handling for multi-character entries and whitespace.
- [ ] Add a single-player mode with a computer opponent.
