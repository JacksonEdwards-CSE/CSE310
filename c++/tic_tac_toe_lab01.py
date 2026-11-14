# 1. Name:
#      Jackson Edwards
# 2. Assignment Name:
#      Lab 01: Tic-Tac-Toe
# 3. Assignment Description:
#      Write a program that can run a game of Tic-Tac-Toe, save and load a game file, 
#      and display a winner when a condition is met.
# 4. What was the hardest part? Be as specific as possible.
#      The hardest part for me was getting the win conditions to work properly. I finally
#      created a For loop containing a switch case that would run through each space on the 
#      board that a win condition could originate from and that solved my problem.
# 5. How long did it take for you to complete the assignment?
#      2.5 hours

import json

def save_game_to_json(game_board, round_number):

    data = {"board" : game_board, "round" : round_number}
    with open("game_data.json", 'wt') as filehandle:
        json_data = json.dumps(data)
        filehandle.write(json_data)

def load_game_from_json():
    try:
        with open("game_data.json", 'rt') as filehandle:
            json_data = filehandle.read()

            game_data = json.loads(json_data)

            return game_data["board"], game_data["round"]

    except (FileExistsError, FileNotFoundError):
        return [' ',' ',' ',
                ' ',' ',' ',
                ' ',' ',' ',], 0

def display_gameboard(game_board):
    print(f'''
 {game_board[0]} | {game_board[1]} | {game_board[2]}
---+---+---
 {game_board[3]} | {game_board[4]} | {game_board[5]}
---+---+---
 {game_board[6]} | {game_board[7]} | {game_board[8]}''')
    print()

def get_user_input(game_board, round_number):
    accepted = False
    while not accepted:

        if round_number % 2 == 0:
            user_choice = input("X> ")
            player = 'X'
        else:
            user_choice = input("O> ")
            player = 'O'

        
        if user_choice == 'q':

            accepted = True

        elif 0 >= int(user_choice) or int(user_choice) > 9:

            print("Please enter a valid number (1-9)")

        elif game_board[int(user_choice) - 1] == 'X' or game_board[int(user_choice) - 1] == 'O':

            print("Please choose a space that hasn't been taken.\n")

        else:

            accepted = True
    
    return user_choice, player

def update_game_board(game_board, user_choice, player):
    game_board[int(user_choice) - 1] = player

def check_win_condition(game_board):
    for space in range(7):
        match space:

            case 0:
                #Check Horizontal
                if game_board[space] != ' ' and game_board[space] == game_board[space + 1] and game_board[space] == game_board[space + 2]:
                    return False
                #Check Vertical
                elif game_board[space] != ' ' and game_board[space] == game_board[space + 3] and game_board[space] == game_board[space + 6]:
                    return False
                #Check Diagonal
                elif game_board[space] != ' ' and game_board[space] == game_board[space + 4] and game_board[space] == game_board[space + 8]:
                    return False
            case 1:
                #Check Vertical
                if game_board[space] != ' ' and game_board[space] == game_board[space + 3] and game_board[space] == game_board[space + 6]:
                    return False
            case 2:
                #Check Vertical
                if game_board[space] != ' ' and game_board[space] == game_board[space + 3] and game_board[space] == game_board[space + 6]:
                    return False
                #Check Diagonal
                elif game_board[space] != ' ' and game_board[space] == game_board[space + 2] and game_board[space] == game_board[space + 4]:
                    return False
            case 3:
                #Check Horizontal
                if game_board[space] != ' ' and game_board[space] == game_board[space + 1] and game_board[space] == game_board[space + 2]:
                    return False
            case 6:
                #Check Horizontal
                if game_board[space] != ' ' and game_board[space] == game_board[space + 1] and game_board[space] == game_board[space + 2]:
                    return False
            case _:
                return True

def main():

    blank = ' '

    print('''Enter 'q' to suspend your game. Otherwise, enter a number from 1 to 9
where the following numbers correspond to the locations on the grid:
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
 
 The current game board is:
 ''')
    
    game_board, round_number = load_game_from_json()
    
    playing = True

    while playing:
        
        display_gameboard(game_board)

        user_choice, player = get_user_input(game_board, round_number)

        if user_choice == 'q':
            save_game_to_json(game_board, round_number)
            playing = False
            
        else:
            update_game_board(game_board, user_choice, player)

            playing = check_win_condition(game_board)

            if playing == False:
                if round_number % 2 == 0:
                    print("X is the Winner!")
                else:
                    print("O is the Winner!")

                display_gameboard(game_board)
            
            round_number += 1
            save_game_to_json([' ',' ',' ',
                               ' ',' ',' ',
                               ' ',' ',' ',], 0)

if __name__ == "__main__":
    main()