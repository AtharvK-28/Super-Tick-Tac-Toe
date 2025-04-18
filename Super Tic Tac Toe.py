from tkinter import *
from tkinter import messagebox   #Allows us to show pop-up messages to the user
from tkinter import simpledialog    #For asking for player names

root = Tk()     #New Window
root.title('Super Tic Tac Toe Game')    #Window title

#Variables
clicked = True  #Determines who's turn True=Player 1(X) and False=Player 2(O)
count = 0   #Number of moves
player1_name = ""   #Stores players' name
player2_name = ""
next_board = None   #Which board to play next (None means player can choose any board)
winner = False  #Is there a winner yet?

#Track the state of each small board 
#Values can be " " (empty), "X", "O", or "T" (tie)
main_board = [[" " for _ in range(3)] for _ in range(3)] #Main 3X3 Board where the winner will be determined from
main_winner = " "  #Winner of the entire game

#Frames
game_frame = Frame(root)
game_frame.pack(padx=10, pady=10)

status_frame = Frame(root)
status_frame.pack(pady=5)

main_viz_frame = Frame(root)
main_viz_frame.pack(pady=10)

#Status labels
status_label = Label(status_frame, text="", font=("Helvetica", 12))
status_label.pack()

instructions_label = Label(status_frame, text="", font=("Helvetica", 10), wraplength=400)
instructions_label.pack(pady=5)

#Store all the buttons for the 9 tic-tac-toe boards
#boards[row][col][button_row][button_col]
boards = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]

#Store frames for each small board
board_frames = [[None for _ in range(3)] for _ in range(3)]

#Store labels for the main board visualization
main_labels = [[None for _ in range(3)] for _ in range(3)]

def disableSmallBoard(board_r, board_c):
    """Disable all buttons in a small board"""
    for r in range(3):
        for c in range(3):
            boards[board_r][board_c][r][c].config(state=DISABLED)

def updateStatus():
    """Update the status display to show current player and instructions"""
    player_name = player1_name if clicked else player2_name
    current_player = "X" if clicked else "O"
    
    if winner:
        if main_winner == "T":
            status_label.config(text="Game Over - It's a Tie!")
        else:
            winner_name = player1_name if main_winner == "X" else player2_name
            status_label.config(text=f"Game Over - {winner_name} wins!")
        instructions_label.config(text="Click 'New Game' to play again.")
        return
        
    status_label.config(text=f"Current Turn: {player_name} ({current_player})")
    
    if next_board is None:
        instructions_label.config(text="You can play on any available board.")
    else:
        r, c = next_board
        instructions_label.config(text=f"You must play on the board at position ({r+1},{c+1}).")

def updateMetaVisualization():
    """Update the visual representation of the main-board"""
    for r in range(3):
        for c in range(3):
            text = main_board[r][c]
            bg_color = "#f0f0f0"  #Default background
            
            if text == "X":
                bg_color = "#ffaaaa"  #Light red for X
            elif text == "O":
                bg_color = "#aaaaff"  #Light blue for O
            elif text == "T":
                bg_color = "#cccccc"  #Gray for ties
                text = "="
                
            main_labels[r][c].config(text=text, bg=bg_color)

def highlightActiveBoard():
    """Highlight the board that's currently playable"""
    for r in range(3):
        for c in range(3):
            #Skip boards that are already won
            if main_board[r][c] != " ":
                continue
                
            if next_board is None or (r, c) == next_board:
                board_frames[r][c].config(bg="#80ffaa")  #Light green for active
            else:
                board_frames[r][c].config(bg="#f0f0f0")  #Default for inactive

def checkSmallBoardWinner(board_r, board_c):
    """Check if a specific small board has a winner"""
    #Get the text values from all buttons in this small board
    board_values = [[boards[board_r][board_c][r][c]["text"] for c in range(3)] for r in range(3)]
    
    #Check rows
    for r in range(3):
        if board_values[r][0] != " " and board_values[r][0] == board_values[r][1] == board_values[r][2]:
            return board_values[r][0]
    
    #Check columns
    for c in range(3):
        if board_values[0][c] != " " and board_values[0][c] == board_values[1][c] == board_values[2][c]:
            return board_values[0][c]
    
    #Check diagonals
    if board_values[0][0] != " " and board_values[0][0] == board_values[1][1] == board_values[2][2]:
        return board_values[0][0]
    if board_values[0][2] != " " and board_values[0][2] == board_values[1][1] == board_values[2][0]:
        return board_values[0][2]
    
    #Check if board is full (tie)
    is_full = all(board_values[r][c] != " " for r in range(3) for c in range(3))
    if is_full:
        return "T"  #Tie
        
    return " "  #No winner yet

def markSmallBoardWinner(board_r, board_c, player):
    """Mark a small board as won by a player or tied"""
    global main_board
    
    main_board[board_r][board_c] = player
    
    #Color the background of all buttons in this board
    bg_color = "#ffaaaa" if player == "X" else "#aaaaff" if player == "O" else "#cccccc"
    
    for r in range(3):
        for c in range(3):
            boards[board_r][board_c][r][c].config(state=DISABLED, bg=bg_color)
    
    #Update the main visualization
    updateMetaVisualization()

def checkMetaWinner():
    """Check if there's a winner on the main board"""
    global main_winner, winner
    
    #Check rows
    for r in range(3):
        if main_board[r][0] in ["X", "O"] and main_board[r][0] == main_board[r][1] == main_board[r][2]:
            main_winner = main_board[r][0]
            winner = True
            return True
    
    #Check columns
    for c in range(3):
        if main_board[0][c] in ["X", "O"] and main_board[0][c] == main_board[1][c] == main_board[2][c]:
            main_winner = main_board[0][c]
            winner = True
            return True
    
    #Check diagonals
    if main_board[0][0] in ["X", "O"] and main_board[0][0] == main_board[1][1] == main_board[2][2]:
        main_winner = main_board[0][0]
        winner = True
        return True
    if main_board[0][2] in ["X", "O"] and main_board[0][2] == main_board[1][1] == main_board[2][0]:
        main_winner = main_board[0][2]
        winner = True
        return True
    
    #Check if main board is full (tie)
    is_full = all(main_board[r][c] != " " for r in range(3) for c in range(3))
    if is_full:
        main_winner = "T"  #Tie
        winner = True
        return True
        
    return False  #No winner yet

def buttonClicked(board_r, board_c, r, c):
    """Handle button clicks on the small boards"""
    global clicked, count, next_board, winner
    
    #If game is over, do nothing
    if winner:
        return
        
    #Check if this is a valid move
    if next_board is not None and next_board != (board_r, board_c):
        messagebox.showerror("Invalid Move", "You must play in the highlighted board.")
        return
        
    #Check if the button is already filled
    if boards[board_r][board_c][r][c]["text"] != " ":
        messagebox.showerror("Invalid Move", "This cell is already taken.")
        return
        
    #Make the move
    if clicked:  #Player 1's turn (X)
        boards[board_r][board_c][r][c]["text"] = "X"
    else:  #Player 2's turn (O)
        boards[board_r][board_c][r][c]["text"] = "O"
    
    count = count + 1
    
    #Check if this move resulted in a win on this small board
    boardWinner = checkSmallBoardWinner(board_r, board_c)
    if boardWinner != " ":
        markSmallBoardWinner(board_r, board_c, boardWinner)
        
        #Check if this resulted in a win on the main board
        if checkMetaWinner():
            updateStatus()
            highlightActiveBoard()
            
            if main_winner == "T":
                messagebox.showinfo("Game Over", "The game is a tie!")
            else:
                winner_name = player1_name if main_winner == "X" else player2_name
                messagebox.showinfo("Game Over", f"{winner_name} wins the game!")
                
            return
    
    #Determine the next board to play on
    if main_board[r][c] == " ":
        next_board = (r, c)
    else:
        #If the corresponding board is already won/tied, player can choose any board
        next_board = None
    
    #Switch turns
    clicked = not clicked
    
    #Update the UI
    updateStatus()
    highlightActiveBoard()

def start():
    """Start a new game"""
    global player1_name, player2_name, clicked, count, next_board, winner, main_board, main_winner, boards, board_frames, main_labels
    
    #Ask for player names if they're not set yet
    if player1_name == "" or player2_name == "":
        player1_name = simpledialog.askstring("Player 1", "Enter name for Player 1 (X):")
        if player1_name is None: 
            player1_name = "Player 1"
            
        player2_name = simpledialog.askstring("Player 2", "Enter name for Player 2 (O):")
        if player2_name is None:
            player2_name = "Player 2"
    
    #Reset game state
    clicked = True  #X goes first
    count = 0
    next_board = None
    winner = False
    main_winner = " "
    
    #Reset the main board
    main_board = [[" " for _ in range(3)] for _ in range(3)]
    
    #Create the main 3x3 grid to hold the 9 small boards
    for board_r in range(3):
        for board_c in range(3):
            #Create a frame with a border for each small board
            board_frame = Frame(game_frame, borderwidth=2, relief="solid", padx=3, pady=3)
            board_frame.grid(row=board_r, column=board_c, padx=5, pady=5)
            board_frames[board_r][board_c] = board_frame
            
            #Create the 3x3 grid of buttons for this small board
            for r in range(3):
                for c in range(3):
                    #Lambda needs defaults to capture the current values
                    button = Button(
                        board_frame, 
                        text=" ", 
                        font=("Helvetica", 12), 
                        height=2, 
                        width=4, 
                        bg="#f0f0f0",
                        command=lambda br=board_r, bc=board_c, br2=r, bc2=c: buttonClicked(br, bc, br2, bc2)
                    )
                    button.grid(row=r, column=c, padx=1, pady=1)
                    boards[board_r][board_c][r][c] = button
    
    # Create a visual representation of the main board
    main_label = Label(main_viz_frame, text="Main Board Status:", font=("Helvetica", 12))
    main_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))
    
    main_frame = Frame(main_viz_frame, borderwidth=2, relief="solid")
    main_frame.grid(row=1, column=0, columnspan=3)
    
    for r in range(3):
        for c in range(3):
            label = Label(
                main_frame, 
                text=" ", 
                font=("Helvetica", 14), 
                width=3, 
                height=1,
                borderwidth=1, 
                relief="solid"
            )
            label.grid(row=r, column=c, padx=3, pady=3)
            main_labels[r][c] = label
    
    # Update the UI
    updateMetaVisualization()
    updateStatus()
    highlightActiveBoard()

# Start the game
start()

# Start the main event loop
root.mainloop()
