import random
import time 
import math

import tilewe 

class Engine: 
    """
    Developers should extend this class to build their own engine.
    Currently requires overriding the `on_search` function which must
    return one legal move within the given time control.

    For extension examples, see the Sample Engines below.
    For construction examples, see the tilewe.tournament.Tournament class.
    """
    
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

"""
Sample Engines

The following engines implement fairly simple strategies and can
be used for testing your Engine against in tournaments.
Approximate strength ordering:
    WallCrawlerEngine, very weak
    RandomEngine, very weak
    MostOpenCornersEngine, weak
    LargestPieceEngine, moderate
    MaximizeMoveDifferenceEngine, surprisingly strong
"""

class MoveExecutor(object):
    """
    Helper for testing board state after applying a move when
    you intend to pop that move afterwards. See example usage
    in the Sample Engines below.
    """
    
    def __init__(self, board: tilewe.Board, move: tilewe.Move):
        self.board = board
        self.move = move
    
    def __enter__(self):
        self.board.push(self.move)

    def __exit__(self, *args):
        self.board.pop()

class RandomEngine(Engine): 
    """
    Literally just selects a random move from all legal moves.
    Pretty bad, but makes moves really fast.
    """

    def __init__(self, name: str="Random"): 
        super().__init__(name)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move: 
        return random.choice(board.generate_legal_moves(unique=True)) 

class MostOpenCornersEngine(Engine): 
    """
    Plays the move that results in the player having the most
    playable corners possible afterwards, i.e. maximizing the
    possible moves on the next turn.
    Fairly weak but does result in decent board coverage behavior.
    """

    def __init__(self, name: str="MostOpenCorners"):
        super().__init__(name)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move:
        moves = board.generate_legal_moves(unique=True) 
        random.shuffle(moves) 
        
        player = board.current_player

        def corners_after_move(m: tilewe.Move) -> int: 
            with MoveExecutor(board, m):
                corners = board.n_player_corners(player) 
                return corners

        return max(moves, key=corners_after_move)

class LargestPieceEngine(Engine): 
    """
    Plays the best legal move prioritizing the following, in order:
        Piece with the most squares (i.e. most points)
        Piece that introduces the most corners
        Piece that has the most contacts
    Moderately strong from a greedy point hungry perspective. Since
    ties are common and result in a random move choice across the
    ties, it's effectively a greedy form of RandomEngine.
    """

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
    """
    Plays the move that results in the player having the best difference 
    in subsequent legal move counts compared to all opponents. That is,
    how many legal moves the player has following this move minus how many
    legal moves all the opponents have following this move.
    Surprisingly strong due to implicitly incorporating various heuristics
    that result in behaviors seeking more open corners, blocking opponent corners, 
    getting access to an open area on the board, etc.
    """

    def __init__(self, name: str="MaximizeMoveDifference"):
        super().__init__(name)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move:
        moves = board.generate_legal_moves(unique=True) 
        random.shuffle(moves) 
        
        player = board.current_player

        def eval_after_move(m: tilewe.Move) -> int: 
            with MoveExecutor(board, m):
                total = 0
                for color in range(board.n_players): 
                    n_moves = board.n_legal_moves(unique=True, for_player=color)
                    total += n_moves * (1 if color == player else -1)
                return total

        return max(moves, key=eval_after_move)
    
class TileWeightEngine(Engine):
    """
    Evalutes tile ownership after each legal move and selects the move that maximizes
    ownership of tiles with the highest scores. Supports the built-in weight maps below
    and passing in your own custom set of tile weights, which must be a list of 400 floats.
    Note that weights are ordered [A01, A02, ..., A20, B01, B02, ..., S20, T01, T02, ..., T20].

    Strength depends entirely on the strategy encapsulated by the given weights!
        'wall_crawl' seems moderate (better than random/open corners but weaker than others)
        'turtle' seems fairly weak (better than random but weaker than others)
    """

    WALL_CRAWL_WEIGHTS: list[float] = [
        1, 1,   1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,   1,  
        1, 0.9, 0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9, 1,  
        1, 0.9, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6 , 0.6,  0.6,  0.6,  0.6,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.3,  0.3,  0.3,  0.3,  0.3,  0.3,  0.3,  0.3,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.3,  0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.3,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.3,  0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.3,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.3,  0.25, 0.1,  0.1,  0.1,  0.1,  0.25, 0.3,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.3,  0.25, 0.1,  0,    0,    0.1,  0.25, 0.3,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.3,  0.25, 0.1,  0.1,  0.1,  0.1,  0.25, 0.3,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.3,  0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.3,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.3,  0.3,  0.3,  0.3,  0.3,  0.3,  0.3,  0.3,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.75, 0.9, 1,  
        1, 0.9, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.9, 1,  
        1, 0.9, 0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9,  0.9, 1,  
        1, 1,   1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,   1
    ]

    TURTLE_WEIGHTS: list[float] = [
        512, 256, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 
        256, 256, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 256, 
        128, 128, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 128, 128, 
        64,  64,  64,  64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 64,  64,  64, 
        32,  32,  32,  32, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 32, 32,  32,  32, 
        16,  16,  16,  16, 16, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 16, 16, 16,  16,  16, 
        8,   8,   8,   8,  8,  8,  8, 4, 2, 1, 1, 2, 4, 8, 8,  8,  8,  8,   8,   8, 
        4,   4,   4,   4,  4,  4,  4, 4, 2, 1, 1, 2, 4, 4, 4,  4,  4,  4,   4,   4, 
        2,   2,   2,   2,  2,  2,  2, 2, 2, 1, 1, 2, 2, 2, 2,  2,  2,  2,   2,   2, 
        1,   1,   1,   1,  1,  1,  1, 1, 1, 1, 1, 1, 1, 1, 1,  1,  1,  1,   1,   1, 
        1,   1,   1,   1,  1,  1,  1, 1, 1, 1, 1, 1, 1, 1, 1,  1,  1,  1,   1,   1, 
        2,   2,   2,   2,  2,  2,  2, 2, 2, 1, 1, 2, 2, 2, 2,  2,  2,  2,   2,   2, 
        4,   4,   4,   4,  4,  4,  4, 4, 2, 1, 1, 2, 4, 4, 4,  4,  4,  4,   4,   4, 
        8,   8,   8,   8,  8,  8,  8, 4, 2, 1, 1, 2, 4, 8, 8,  8,  8,  8,   8,   8, 
        16,  16,  16,  16, 16, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 16, 16, 16,  16,  16, 
        32,  32,  32,  32, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 32, 32,  32,  32, 
        64,  64,  64,  64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 64,  64,  64, 
        128, 128, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 128, 128, 
        256, 256, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 256, 
        512, 256, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 
    ]

    weight_maps = {
        'wall_crawl': WALL_CRAWL_WEIGHTS,
        'turtle': TURTLE_WEIGHTS
    }

    def __init__(self, name: str="TileWeight", weight_map: str='wall_crawl', custom_weights: list[float]=None): 
        """
        Current `weight_map` built-in options are 'wall_crawl' and 'turtle'
        Can optionally provide a custom set of weights instead
        """

        super().__init__(name)

        if custom_weights is not None:
            if len(custom_weights) != 20 * 20:
                raise Exception("TileWeightEngine custom_weights must be a list of exactly 400 floats")
            self.weights = custom_weights
        
        else:
            if weight_map not in self.weight_maps:
                raise Exception("TileWeightEngine given invalid weight_map choice")
            self.weights = self.weight_maps[weight_map]

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move: 

        cur_player = board.current_player

        def get_owned_tiles_list(board: tilewe.Board, player: tilewe.Color):
            ownership = []
            for tile in tilewe.TILES:
                ownership.append(1 if board.color_at(tile) == player else 0)
            return ownership   

        def tile_score_after_move(move: tilewe.Move) -> int: 
            with MoveExecutor(board, move):
                owned_tiles = get_owned_tiles_list(board, cur_player)
                return sum([t[0] * t[1] for t in zip(owned_tiles, self.weights)])

        moves = board.generate_legal_moves(unique=True)
        if board.ply < board.n_players:
            #  prune to one corner to reduce moves to evaluate
            corner = board.player_corners(cur_player)[0]
            moves = [i for i in moves if i.to_tile == corner]

        return max(moves, key=tile_score_after_move)
