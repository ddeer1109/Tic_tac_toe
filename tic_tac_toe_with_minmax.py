from os import system, name
from time import sleep
import sys
import random
import copy
import math
import time

# dict with translation of moves input given by human to board indexes
rows = {"A": 0, "B": 1, "C": 2}
columns = {"1": 0, "2": 1, "3": 2}

def clear(): 
    """Clears console"""
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

def init_board():
    """Returns an empty 3-by-3 board (with .)."""
    board = []
    for i in range(0,3):
        board.append([".",".","."])
    
    return board

def get_possible_moves(board):
    possible_moves = []
    for x, y in enumerate(board):
        for z in range(len(y)):
            if board[x][z] == ".":
                possible_moves.append((x,z))
    return possible_moves
    


def is_place_free(board, row, col):
    """Checks if place with given coordinates is empty"""
    if board[row][col] == ".": return True
    else: return False

def get_move(board, player):
    """Returns the coordinates of a valid move for player on board."""
    
    print(f"Player {player} turn.")
    correct_input = validate_input()
    
    usr_row, usr_col = correct_input[0], correct_input[1]
    row, col = rows[usr_row], columns[usr_col]
    
    if is_place_free(board, row, col):
        return row, col
    
    print(f"Place {correct_input[0]}{correct_input[1]} is taken")
    return get_move(board, player)
    

def validate_input():
    """Returns str with user input with not translated indexes of move if it is correct"""
    player_select = str.upper(input("Input: "))
    try:
        row_input_not_correct = player_select[0] not in rows.keys()
        column_input_not_correct = player_select[1] not in columns.keys()
        length_input_not_correct = len(player_select) > 2
        
        if player_select == "QUIT":
            sys.exit("Terminated by user. Thank you for your time.")
        
        elif row_input_not_correct or column_input_not_correct or length_input_not_correct:
            print("Please provide empty row and column index without spaces.")
            player_select = validate_input()
    except:
            print("Please provide empty row and column index without spaces.")
            player_select = validate_input()

    return player_select


#player "O" is max ai
def maximum(board, alpha, beta):
    

    # Possible values for maxv are:
    # -1 - loss
    # 0  - a tie
    # 1  - win

    # We're initially setting it to -2 as worse than the worst case:
    maxv = -2

    px = None
    py = None


    # If the game came to an end, the function needs to return
    # the evaluation function of the end. That can be:
    # -1 - loss
    # 0  - a tie
    # 1  - win
    x_wins = has_won(board, "X")
    o_wins = has_won(board, "O")
    board_is_full = is_full(board)
    if x_wins:
        return (-1, 0, 0)
    elif o_wins:
        return (1, 0, 0)
    elif board_is_full and not x_wins and not o_wins:
        return (0, 0, 0)

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == '.':
                # On the empty field player 'O' makes a move and calls Min
                # That's one branch of the game tree.
                board[i][j] = 'O'
                (m, min_i, min_j) = minimum(board, -2, 2)
                # Fixing the maxv value if needed
                if m > maxv:
                    maxv = m
                    px = i
                    py = j
                # Setting back the field to empty
                board[i][j] = '.'

                if maxv >= beta:
                        return (maxv, px, py)

                if maxv > alpha:
                    alpha = maxv
    return (maxv, px, py)

def minimum(board, alpha, beta):

    # Possible values for minv are:
    # -1 - win
    # 0  - a tie
    # 1  - loss

    # We're initially setting it to 2 as worse than the worst case:
    minv = 2

    qx = None
    qy = None
    x_wins = has_won(board, "X")
    o_wins = has_won(board, "O")
    board_is_full = is_full(board)
    if x_wins:
        return (-1, 0, 0)
    elif o_wins:
        return (1, 0, 0)
    elif board_is_full and not x_wins and not o_wins:
        return (0, 0, 0)

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == '.':
                board[i][j] = 'X'
                (m, max_i, max_j) = maximum(board, -2, 2)
                if m < minv:
                    minv = m
                    qx = i
                    qy = j
                board[i][j] = '.'
                if minv <= alpha:
                    return (minv, qx, qy)

                if minv < beta:
                    beta = minv
    return (minv, qx, qy)

    
def mark(board, player, row, col):
    """Marks the element at row & col on the board for player."""
    board[row][col] = player
    # return board

def has_won(board, player):
    """Returns True if player has won the game."""
    diagonal1 = (board[0][0], board[1][1], board[2][2])
    diagonal2 = (board[0][2], board[1][1], board[2][0])
    horizontals = [
        (board[0][0], board[0][1], board[0][2]),
        (board[1][0], board[1][1], board[1][2]),
        (board[2][0], board[2][1], board[2][2])
        ]
    verticals = [
        (board[0][0], board[1][0], board[2][0]),
        (board[0][1], board[1][1], board[2][1]),
        (board[0][2], board[1][2], board[2][2])
        ]
    if diagonal1.count(player) == 3 or diagonal2.count(player) == 3: 
        return True
        
    if (player, player, player) in horizontals or (player,player,player) in verticals: return True


def is_full(board):
    """Returns True if board is full."""
    empty_slot_on_board = lambda row: "." in board[row]
    for count in range(0,3):
        if empty_slot_on_board(count):
            return False
    return True

def print_board(board):
    """Prints a 3-by-3 board on the screen with borders."""
    printable = f"""
        1   2   3
    A   {board[0][0]} | {board[0][1]} | {board[0][2]}
       ---+---+---
    B   {board[1][0]} | {board[1][1]} | {board[1][2]}
       ---+---+---
    C   {board[2][0]} | {board[2][1]} | {board[2][2]}
    """
    print(printable)

def print_result(winner):
    """Congratulates winner or proclaims tie (if winner equals zero)."""
    greet = f"{winner} has won!"
    if winner == None:
        print("It's a tie")
    print(f"""
    {len(greet)*"="}
    {greet}
    {len(greet)*"="}""")



def tictactoe_game(mode='HUMAN-HUMAN'):
    """Runs right game mode based on given argument"""
    board = init_board()
    clear()
    if mode == "HUMAN-HUMAN":        
        human_vs_human(board)
    elif mode == "HUMAN-AI":
        human_vs_ai(board)
    elif mode == "AI-AI":
        ai_vs_ai(board)


def human_vs_human(board):
    """Processes human vs human game mode"""
    board_not_full = not is_full(board)
    while board_not_full:
        
        process_turn_of_player(board, "X")
        if is_full(board) == True:
            break
        process_turn_of_player(board, "0")
        

    handle_win(None, board)

def human_vs_ai(board, current_turn = "X"):
    while True:
        print_board(board)
        x_wins, o_wins = has_won(board, "X"), has_won(board, "O")

        # Printing the appropriate message if the game has ended:
        if x_wins:
            handle_win("X", board)
            break
        elif o_wins:
            handle_win("O", board)
            break
        elif is_full(board) and not x_wins and not o_wins:
            handle_win(None, board)
            break


        # If it's player's turn
        if current_turn == 'X':

            while True:

                start = time.time()
                (m, qx, qy) = minimum(board, -2, 2)
                end = time.time()
                print('Evaluation time: {}s'.format(round(end - start, 7)))
                print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                px, py = get_move(board, "X")

                (qx, qy) = (px, py)

    
                mark(board, "X", px, py)
                current_turn = 'O'
                break
            

        # If it's AI's turn
        else:
            (m, px, py) = maximum(board, -2, 2)
            mark(board, "O", px, py)
            current_turn = 'X'
        clear()

def ai_vs_ai(board, current_turn = "X"):
    """Processes AI vs AI game mode"""
    while True:
        print_board(board)
        x_wins, o_wins = has_won(board, "X"), has_won(board, "O")

        
        if x_wins:
            handle_win("X", board)
            break
        elif o_wins:
            handle_win("O", board)
            break
        elif is_full(board) and not x_wins and not o_wins:
            handle_win(None, board)
            break


        if current_turn == 'X':

            (m, px, py) = minimum(board, -2, 2)
            mark(board, "X", px, py)
            current_turn = 'O'
            

        else:
            (m, px, py) = maximum(board, -2, 2)
            mark(board, "O", px, py)
            current_turn = 'X'
        sleep(1)
        clear()
    

def process_turn_of_player(board, player):
    """Processes turn of player or AI and handles win"""
    print_board(board)
    
    r, c = get_move(board,player)
    
    
    mark(board, player, r, c)
    

    if has_won(board, player) == True: 
        handle_win(player, board)
    clear()

def handle_win(player, board):
    clear()
    print_result(player), print_board(board)
    print("Thanks for the game. Want to try again y/n?")
    decision = input(":")
    if str.lower(decision) == "y":
        main_menu()
    else:
        sys.exit("Thanks for your time")

def main_menu():
    print("""Choose mode of the game:
    1. human vs human
    2. human vs computer
    3. spectate computer vs computer""")
    user_choice = input(":")
    if user_choice == "1":
        tictactoe_game('HUMAN-HUMAN')
    elif user_choice == "2":
        tictactoe_game('HUMAN-AI')
    elif user_choice == "3":
        tictactoe_game('AI-AI')
    else:
        print("incorrect input")
        sleep(2)
        clear()
        main_menu()

if __name__ == '__main__':
    main_menu()
