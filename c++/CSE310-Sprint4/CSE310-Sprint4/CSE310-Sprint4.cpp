#include <array>
#include <cctype>
#include <iostream>
#include <string>

using namespace std;

class Game
{
   public:

      Game() : board{' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}, roundNumber(0) {}

      void displayGameBoard() const
      {
         cout << '\n' << ' ' << board[0] << " | " << board[1] << " | " << board[2] << '\n'
              << "---+---+---\n" << ' ' << board[3] << " | " << board[4] << " | " << board[5] << '\n'
              << "---+---+---\n" << ' ' << board[6] << " | " << board[7] << " | " << board[8] << "\n\n";
      }

      char currentPiece() const { return roundNumber % 2 == 0 ? 'X' : 'O'; }
      int getRoundNumber() const { return roundNumber; }

      bool makeMove(int position)
      {
         if (position < 1 || position > 9 || board[position - 1] != ' ') return false;
         board[position - 1] = currentPiece();
         ++roundNumber;
         return true;
      }

      bool checkWinCondition() const
      {
         static const int winningLines[8][3] = {
            {0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
            {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}
         };
         for (const auto& line : winningLines)
            if (board[line[0]] != ' ' && board[line[0]] == board[line[1]] && board[line[0]] == board[line[2]]) return true;
         return false;
      }

      bool boardFull() const
      {
         for (char space : board) if (space == ' ') return false;
         return true;
      }

   private:

      array<char, 9> board;
      int roundNumber;
};

int main()
{
   Game game;

   cout << "Enter 'q' to quit the game. Otherwise, enter a number from 1 to 9"
        << " where the following numbers correspond to the locations on the grid:\n"
        << " 1 | 2 | 3\n---+---+---\n 4 | 5 | 6\n---+---+---\n 7 | 8 | 9\n\n"
        << "The current game board is:\n";

   while (true)
   {
      game.displayGameBoard();
      cout << game.currentPiece() << "> ";
      string input;
      if (!getline(cin, input)) return 0;
      if (input == "q" || input == "Q")
      {
         cout << "Game ended.\n";
         return 0;
      }
      if (input.size() != 1 || !isdigit(static_cast<unsigned char>(input[0])) || input[0] < '1' || input[0] > '9')
      {
         cout << "Please enter a valid number (1-9)\n";
         continue;
      }
      const char movingPiece = game.currentPiece();
      if (!game.makeMove(input[0] - '0'))
      {
         cout << "Please choose a space that hasn't been taken.\n\n";
         continue;
      }
      if (game.checkWinCondition())
      {
         game.displayGameBoard();
         cout << movingPiece << " is the Winner!\n";
         return 0;
      }
      if (game.boardFull())
      {
         game.displayGameBoard();
         cout << "The game is a draw!\n";
         return 0;
      }
   }
}
