import random

board = []
BOARD_SIZE = 5

def reset_board(size=5):
    global board, BOARD_SIZE
    BOARD_SIZE = size
    board = [['' for _ in range(size)] for _ in range(size)]

def valid_move(r, c):
    return board[r][c] == ''

def place_piece(r, c, symbol):
    board[r][c] = symbol

def check_winner(symbol):

    for i in range(BOARD_SIZE):
        if all(board[i][j] == symbol for j in range(BOARD_SIZE)):
            return True
        if all(board[j][i] == symbol for j in range(BOARD_SIZE)):
            return True

    if all(board[i][i] == symbol for i in range(BOARD_SIZE)): return True
    if all(board[i][BOARD_SIZE - i - 1] == symbol for i in range(BOARD_SIZE)): return True
    return False

def smart_ai_move():
    empty = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == '']
    if not empty:
        return None

    for symbol in ['O', 'X']:
        for (r, c) in empty:
            board[r][c] = symbol
            if check_winner(symbol):
                board[r][c] = ''
                return (r, c) if symbol == 'O' else (r, c)
            board[r][c] = ''
    return random.choice(empty)
