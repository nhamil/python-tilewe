import random
import time 

import tilewe 

class Engine: 
    '''
        Developers should extend this class to build their own engine.
        Currently requires overriding the `search` function which must
        return one legal move within the given time control.
    '''
    def __init__(self, name: str): 
        self.name = name  
        self.seconds = 0 
        self.end_at = time.time() 

    def out_of_time(self) -> bool: 
        return time.time() >= self.end_at 

    def search(self, board: tilewe.Board, seconds: float) -> tilewe.Move: 
        self.end_at = time.time() + seconds 
        self.seconds = seconds 
        return self.on_search(board, seconds) 

    def on_search(self, board: tilewe.Board, seconds: float) -> tilewe.Move: 
        raise NotImplementedError() 

'''
    Sample Engines
    The following engines implement fairly simple strategies and can
    be used for testing your Engine against in tournaments.
    Approximate strength ordering:
        RandomEngine, very weak
        MostOpenCornersEngine, weak
        LargestPieceEngine, moderate
        MaximizeMoveDifferenceEngine, surprisingly strong
'''

class RandomEngine(Engine): 
    '''
        Literally just selects a random move from all legal moves.
        Pretty bad, but makes moves really fast.
    '''

    def __init__(self, name: str="Random"): 
        super().__init__(name)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move: 
        return random.choice(board.generate_legal_moves(unique=True)) 

class MostOpenCornersEngine(Engine): 
    '''
        Plays the move that results in the player having the most
        playable corners possible afterwards, i.e. maximizing the
        possible moves on the next turn.
        Fairly weak but does result in decent board coverage behavior.
    '''

    def __init__(self, name: str="MostOpenCorners"):
        super().__init__(name)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move:
        moves = board.generate_legal_moves(unique=True) 
        random.shuffle(moves) 
        
        player = board.current_player

        def corners_after_move(m: tilewe.Move) -> int: 
            board.push(m) 
            corners = board.n_player_corners(player) 
            board.pop() 
            return corners

        return max(moves, key=corners_after_move)

class LargestPieceEngine(Engine): 
    '''
        Plays the best legal move prioritizing the following, in order:
            Piece with the most squares (i.e. most points)
            Piece that introduces the most corners
            Piece that has the most contacts
        Moderately strong from a greedy point hungry perspective.
    '''

    def __init__(self, name: str="LargestPiece"):
        super().__init__(name)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move:
        moves = board.generate_legal_moves(unique=True) 
        random.shuffle(moves) 

        best = max(moves, key=lambda m: \
                        tilewe.n_piece_tiles(m.piece) * 100 + \
                        tilewe.n_piece_corners(m.piece) * 10 + \
                        tilewe.n_piece_contacts(m.piece))
        
        return best

class MaximizeMoveDifferenceEngine(Engine): 
    '''
        Plays the move that results in the player having the best difference 
        in subsequent legal move counts compared to all opponents. That is,
        how many legal moves the player has following this move minus how many
        legal moves all the opponents have following this move.
        Surprisingly strong due to implicitly incorporating various heuristics
        that result in behaviors seeking more open corners, blocking opponent corners, 
        getting access to an open area on the board, etc.
    '''

    def __init__(self, name: str="MaximizeMoveDifference"):
        super().__init__(name)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move:
        moves = board.generate_legal_moves(unique=True) 
        random.shuffle(moves) 
        
        player = board.current_player

        def eval_after_move(m: tilewe.Move) -> int: 
            board.push(m) 
            total = 0
            for color in range(board.n_players): 
                n_moves = board.n_legal_moves(unique=True, for_player=color)
                total += n_moves * (1 if color == player else -1)
            board.pop() 
            return total

        return max(moves, key=eval_after_move)