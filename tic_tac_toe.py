from os import system, name
from time import sleep
import sys
import random
import copy

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

def get_copy_of_board(board):
    """Return independent copy of given board for AI processing"""
    return copy.deepcopy(board)


def get_ai_move(board, player):
    """Processes board and returns value chosen by algorithm: 
    (search for winning move) > (search for move preventing opponents win) > 
    (take center) > (take random corner) > (take random from rest) """

    if player == "X":
        opponent = "0"
    elif player == "0":
        opponent = "X"
    
    #searching for winning move
    for row in range(3):
        for col in range(3):
            copy = get_copy_of_board(board)
            if is_place_free(copy, row, col):
                mark(copy, player, row, col)            
                if has_won(copy, player):
                    return row, col
    #searching for move preventing opponent win in next move 
    for row in range(3):
        for col in range(3):
            copy = get_copy_of_board(board)
            if is_place_free(copy, row, col):
                mark(copy, opponent, row, col)
                if has_won(copy, opponent):
                    return row, col
   

    #taking center if empty
    if is_place_free(board, 1, 1):
        return 1, 1

    #taking random corner if empty
    move_on_corner = choose_random_move_from_passed_list(board, [(0,0), (0,2), (2,0), (2,2)])

    if move_on_corner != None:
        return move_on_corner

    #taking random area from the rest
    return choose_random_move_from_passed_list(board, [(1,0), (1,2), (0,1), (2,1)])
    

    
def choose_random_move_from_passed_list(board, moves_list):
    """Returns random move from list with possible moves made inside of function
    Possible moves are based on current state of board and given moves_list list"""
    possible_moves = []
    
    for move in moves_list:
        if is_place_free(board, move[0], move[1]):
            possible_moves.append(move)

    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    else:
        return None

    
def mark(board, player, row, col):
    """Marks the element at row & col on the board for player."""
    board[row][col] = player
    # return board

def has_won(board, player):
    """Returns True if player has won the game."""
    horizontal = lambda row: (board[row][0], board[row][1], board[row][2])
    vertical =   lambda col: (board[0][col], board[1][col], board[2][col])
    diagonal1 = (board[0][0], board[1][1], board[2][2])
    diagonal2 = (board[0][2], board[1][1], board[2][0])
    
    if diagonal1.count(player) == 3 or diagonal2.count(player) == 3: 
        return True
    
    for index in range (0,3):
        if horizontal(index).count(player) == 3: return True
        elif vertical(index).count(player) == 3: return True

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
        clear()
        if is_full(board) == True:
            break
    
        process_turn_of_player(board, "0")
        clear()
    handle_win(None, board)

def human_vs_ai(board):
    """Processes human vs AI game mode"""
    board_not_full = not is_full(board)
    while board_not_full:
        
        process_turn_of_player(board, "X")
    
        if is_full(board) == True:
            break
    
        process_turn_of_player(board, "0", AI = True)
    
    handle_win(None, board)

def ai_vs_ai(board):
    """Processes AI vs AI game mode"""
    board_not_full = not is_full(board)
    while board_not_full:
        
        process_turn_of_player(board, "X", AI=True)
        sleep(2)
        clear()
        if is_full(board) == True:
            break

        process_turn_of_player(board, "0", AI=True)
        sleep(2)
        clear()
    handle_win(None, board)
    

def process_turn_of_player(board, player, AI=False):
    """Processes turn of player or AI and handles win"""
    print_board(board)
    
    if AI == True:
        r, c = get_ai_move(board, player)  
    else:
        r, c = get_move(board,player)
    
    
    mark(board, player, r, c)
    

    if has_won(board, player) == True: 
        handle_win(player, board)
    
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