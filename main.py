import random

import tilewe 

if __name__ == '__main__': 
    board = tilewe.Board(4) 
    print(board) 

    while not board.state.finished: 
        moves = board.get_legal_moves(unique=True) 
        move = random.choice(moves) 

        board.push_move(move) 
        print() 
        print(board) 
