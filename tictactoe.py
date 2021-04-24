"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = 0
    count_O = 0
    
    for row in board: #count boxes
        
        count_X += row.count("X")
        count_O += row.count("O")
        
    if count_X + count_O == 0: #player_X goes first
        return X
    else:
        if count_X <= count_O:
            return X
        if count_O < count_X:
            return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    actions = []
    
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == None:
                actions.append((row,col))
    
    return actions
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    count_X = 0
    count_O = 0
    
    for row in board: #count boxes
        
        count_X += row.count("X")
        count_O += row.count("O")
        
    if count_X + count_O == 0: #player_X goes first
        player_turn =  X
    else:
        if count_X <= count_O:
            player_turn = X
        if count_O < count_X:
            player_turn = O
            
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player_turn
    
    return new_board
            


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    

    
    for row in board: #find winner based on rows   
        count_X = row.count("X")
        count_O = row.count("O")
        
        if count_X == len(board[0]):
            print("x win by rows")
            return X
            
        if count_O == len(board):
            print("o win by rows")
            return O
        

    
    for col in range(len(board[0])): #find winner based on columns
        count_X = 0
        count_O = 0
        for row in range(len(board)):
            if board[row][col] == X:
                count_X += 1
            if board[row][col] == O:
                count_O += 1
            if count_X == len(board):
                print("x win by col")
                return X
            if count_O == len(board):
                print("o win by col")
                return O
    
    count_X = 0
    count_O = 0
    
    for col in range(len(board[0])): #find winner based diagonal top left down
        for row in range(len(board)):
            if row == col:
                if board[row][col] == X:
                    count_X += 1
                if board[row][col] == O:
                    count_O += 1
                if count_X == len(board):
                    print("x win by diagonal top left")
                    return X
                    
                if count_O == len(board):
                    print("o win by diagonal top left")
                    return O
    
    count_X = 0
    count_O = 0
    
    for col in range(len(board[0])): #find winner based diagonal top right down
        for row in range(len(board)):
            if (row + col) == (len(board)-1):
                if board[row][col] == X:
                    count_X += 1
                if board[row][col] == O:
                    count_O += 1
                if count_X == len(board):
                    print("x win by diagonal top right")
                    return X
                if count_O == len(board):
                    print("o win by diagonal top right")
                    return O
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True

#final check for draw
    count_X = 0
    count_O = 0
    for row in board: 
        count_X += row.count("X")
        count_O += row.count("O")
        
    if (count_X + count_O) == len(board)*len(board):
        return True
    
#if no winner and no draw, game continues
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    
    
    if current_player == X:
        max_value_list = []
        for action in actions(board):
            max_value_list.append(min_value(result(board, action)))
        print(max_value_list)
        print(actions(board))
        print(board)
        return(actions(board)[max_value_list.index(max(max_value_list))])

    if current_player == O:
        min_value_list = []
        for action in actions(board):
            min_value_list.append(max_value(result(board, action)))
        print(min_value_list)
        print(actions(board))
        print(board)
        return(actions(board)[min_value_list.index(min(min_value_list))])
    


def max_value(board):
    if terminal(board) == True:
        value = utility(board)
        return value
    value_list = []
    for action in actions(board):
        value = min_value(result(board, action))
        value_list.append(value)

        
    return(max(value_list))
        
        
def min_value(board):                    
    if terminal(board) == True:
        value = utility(board)
        return value
    value_list = []
    for action in actions(board):
        value = max_value(result(board, action))
        value_list.append(value)
    return(min(value_list))
