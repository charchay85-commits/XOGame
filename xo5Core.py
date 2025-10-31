import random

board = []
BOARD_SIZE = 5

def reset_board(size=5):
    global board, BOARD_SIZE
    BOARD_SIZE = size
    board = [['' for _ in range(size)] for _ in range(size)]

def valid_move(r, c):
    return board[r][c] == ''

def place_piece(r, c, piece):
    board[r][c] = piece

def check_winner(player):
    # แนวนอน
    for r in range(BOARD_SIZE):
        if all(board[r][c] == player for c in range(BOARD_SIZE)):
            return True
    # แนวตั้ง
    for c in range(BOARD_SIZE):
        if all(board[r][c] == player for r in range(BOARD_SIZE)):
            return True
    # ทแยง ↘
    if all(board[i][i] == player for i in range(BOARD_SIZE)):
        return True
    # ทแยง ↙
    if all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
        return True
    return False

def get_empty_cells():
    return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == '']

def smart_ai_move():
    """AI: ถ้าเจอช่องที่ชนะได้ให้ลงทันที ถ้ามีช่องที่คนจะชนะให้บล็อก"""
    empty = get_empty_cells()
    if not empty:
        return None

    # ลองชนะเอง
    for r, c in empty:
        board[r][c] = 'O'
        if check_winner('O'):
            board[r][c] = ''
            return (r, c)
        board[r][c] = ''

    # บล็อกผู้เล่น
    for r, c in empty:
        board[r][c] = 'X'
        if check_winner('X'):
            board[r][c] = ''
            return (r, c)
        board[r][c] = ''

    # ถ้าไม่มีอะไรพิเศษ random
    return random.choice(empty)
