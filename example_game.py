import random

import tilewe

tilewe.print_color = True 

def start():
    board = tilewe.Board(4) 
    while not board.finished: 
        mv = random.choice(board.generate_legal_moves(unique=True))
        board.push(mv) 
        print(board) 
