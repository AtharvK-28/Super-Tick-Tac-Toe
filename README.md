**Super Tic Tac Toe - Python Tkinter Edition**
This is an advanced Super Tic Tac Toe game implemented in Python using the Tkinter GUI library. Instead of the classic 3x3 board, this version contains 9 Tic Tac Toe boards (3x3 grid of 3x3 boards), and you must win on the main board by winning individual small boards.


**How to Play**
The game is for two players: Player 1 (X) and Player 2 (O).

Players are prompted to enter their names at the start.

Each move you make determines which small board your opponent must play in next.

E.g., If you play in position (2, 1) of a small board, your opponent must play on the small board at (2, 1) on the main grid.

If the required board is already won or tied, the opponent may play anywhere.

The goal is to win 3 small boards in a row (horizontal, vertical, or diagonal) on the main 3x3 board.


**Features**
Interactive GUI with clearly separated small boards

Highlights the current active board for user guidance

Real-time main board visualization

Handles wins, ties, and invalid moves with message popups

Color-coded boards:

Red for X

Blue for O

Grey for ties

Displays game status and whose turn it is


**Game Flow**
Start: Run the script, enter player names when prompted.

Play: Click on valid cells to make a move.

Win/Tie Detection: After each move, the game checks:

If a small board is won/tied.

If the overall main board has a winner.

End: Game ends when a player wins the main board or all small boards are tied.
