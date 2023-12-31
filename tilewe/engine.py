from typing import Callable
import random
import time
import math

import tilewe 

class Engine: 
    """
    Developers should extend this class to build their own engine.
    Currently requires overriding the `on_search` function which must
    return one legal move within the given time control.

    An Engine's self-estimated Elo should be relative to a 0-point scale,
    not a 1500-point scale. For example, if you think your engine would
    have a 50% win rate against an "average" opponent, you should leave it
    at None/0.0. If you think your engine would have a 75% win rate against
    an "average" opponent, you should set it to 200.0.

    For extension examples, see the Sample Engines below.
    For construction examples, see the tilewe.tournament.Tournament class.
    """
    
    def __init__(self, name: str, estimated_elo: float=None): 
        self.name = name  
        self.estimated_elo = estimated_elo
        self.seconds = 0 
        self.end_at = time.time() 

    def out_of_time(self) -> bool: 
        return time.time() >= self.end_at 

    def search(self, board: tilewe.Board, seconds: float=1.0) -> tilewe.Move: 
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
    Min OpenCorners/MoveDiff/PieceSize, very very weak
    RandomEngine, very weak
    TileWeightEngine with Turtle, very weak
    TileWeightEngine with WallCrawl, weak
    MostOpenCornersEngine, weak
    LargestPieceEngine, moderate
    MaximizeMoveDifferenceEngine, surprisingly strong
    SimpleSearchEngine, strong given a good eval function
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

    def __init__(self, name: str="Random", estimated_elo: float=None): 
        super().__init__(name, -100.0 if estimated_elo is None else estimated_elo)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move: 
        return random.choice(board.generate_legal_moves()) 

class OpenCornersEngine(Engine): 
    """
    Plays the move that results in the player having the most
    playable corners possible afterwards, i.e. maximizing the
    possible moves on the next turn.
    Fairly weak but does result in decent board coverage behavior.
    """

    def __init__(self, name: str=None, style: str="max", estimated_elo: float=None):
        if style not in ["max", "min"]:
            raise ValueError("Invalid style, must be 'max' or 'min'")

        name = name or ("MostOpenCorners" if style == "max" else "LeastOpenCorners")
        estimated_elo = (15.0 if style == "max" else -250.0) if estimated_elo is None else estimated_elo
        self.func = min if style == "min" else max
        
        super().__init__(name, estimated_elo)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move:
        moves = board.generate_legal_moves() 
        random.shuffle(moves) 
        
        player = board.current_player

        def corners_after_move(m: tilewe.Move) -> int: 
            with MoveExecutor(board, m):
                corners = board.n_player_corners(player) 
                return corners

        return self.func(moves, key=corners_after_move)

class PieceSizeEngine(Engine): 
    """
    Plays the best legal move prioritizing the following, in order:
        Piece with the most squares (i.e. most points)
        Piece that introduces the most corners
        Piece that has the most contacts
    Moderately strong from a greedy point hungry perspective. Since
    ties are common and result in a random move choice across the
    ties, it's effectively a greedy form of RandomEngine.
    """

    def __init__(self, name: str=None, style: str="max", estimated_elo: float=None):
        if style not in ["max", "min"]:
            raise ValueError("Invalid style, must be 'max' or 'min'")

        name = name or ("LargestPiece" if style == "max" else "SmallestPiece")
        estimated_elo = (30.0 if style == "max" else -150.0) if estimated_elo is None else estimated_elo
        self.func = min if style == "min" else max
        
        super().__init__(name, estimated_elo)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move:
        moves = board.generate_legal_moves() 
        random.shuffle(moves) 

        def score(m: tilewe.Move): 
            pc = m.piece
            return (tilewe.N_PIECE_TILES[pc] * 100 + 
                tilewe.N_PIECE_CORNERS[pc] * 10 + 
                tilewe.N_PIECE_CONTACTS[pc])

        best = self.func(moves, key=score)
        
        return best

class MoveDifferenceEngine(Engine): 
    """
    Plays the move that results in the player having the best difference 
    in subsequent legal move counts compared to all opponents. That is,
    how many legal moves the player has following this move minus how many
    legal moves all the opponents have following this move.
    Surprisingly strong due to implicitly incorporating various heuristics
    that result in behaviors seeking more open corners, blocking opponent corners, 
    getting access to an open area on the board, etc.
    """

    def __init__(self, name: str=None, style: str="max", estimated_elo: float=None):
        if style not in ["max", "min"]:
            raise ValueError("Invalid style, must be 'max' or 'min'")

        name = name or ("MaxMoveDiff" if style == "max" else "MinMoveDiff")
        estimated_elo = (50.0 if style == "max" else -200.0) if estimated_elo is None else estimated_elo
        self.func = min if style == "min" else max
        
        super().__init__(name, estimated_elo)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move:
        moves = board.generate_legal_moves() 
        random.shuffle(moves) 
        
        player = board.current_player
        N = board.n_players

        def eval_after_move(m: tilewe.Move) -> int: 
            with MoveExecutor(board, m):
                total = 0
                for color in range(N): 
                    n_moves = board.n_legal_moves(for_player=color)
                    total += n_moves * (1 if color == player else -1)
                return total

        return self.func(moves, key=eval_after_move)
    
class TileWeightEngine(Engine):
    """
    Evalutes tile ownership after each legal move and selects the move that maximizes
    ownership of tiles with the highest scores. Supports the built-in weight maps below
    and passing in your own custom set of tile weights, which must be a list of 400 values.
    Note that weights are ordered [A01, A02, ..., A20, B01, B02, ..., S20, T01, T02, ..., T20].

    Strength depends entirely on the strategy encapsulated by the given weights!
        'wall_crawl' seems moderate (better than random/open corners but weaker than others)
        'turtle' seems fairly weak (better than random but weaker than others)
    """

    WALL_CRAWL_WEIGHTS: list[int] = [
        100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,  # noqa: 241
        100, 90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  100,  # noqa: 241
        100, 90,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  30,  30,  30,  30,  30,  30,  30,  30,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  30,  25,  25,  25,  25,  25,  25,  30,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  30,  25,  10,  10,  10,  10,  25,  30,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  30,  25,  10,  0,   0,   10,  25,  30,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  30,  25,  10,  0,   0,   10,  25,  30,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  30,  25,  10,  10,  10,  10,  25,  30,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  30,  25,  25,  25,  25,  25,  25,  30,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  30,  30,  30,  30,  30,  30,  30,  30,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  40,  40,  40,  40,  40,  40,  40,  40,  40,  40,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  50,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  60,  75,  90,  100,  # noqa: 241
        100, 90,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  75,  90,  100,  # noqa: 241
        100, 90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  90,  100,  # noqa: 241
        100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,  # noqa: 241
    ]

    TURTLE_WEIGHTS: list[int] = [
        512, 256, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512,  # noqa: 241
        256, 256, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 256,  # noqa: 241
        128, 128, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 128, 128,  # noqa: 241
        64,  64,  64,  64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 64,  64,  64,   # noqa: 241
        32,  32,  32,  32, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 32, 32,  32,  32,   # noqa: 241
        16,  16,  16,  16, 16, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 16, 16, 16,  16,  16,   # noqa: 241
        8,   8,   8,   8,  8,  8,  8, 4, 2, 1, 1, 2, 4, 8, 8,  8,  8,  8,   8,   8,    # noqa: 241
        4,   4,   4,   4,  4,  4,  4, 4, 2, 1, 1, 2, 4, 4, 4,  4,  4,  4,   4,   4,    # noqa: 241
        2,   2,   2,   2,  2,  2,  2, 2, 2, 1, 1, 2, 2, 2, 2,  2,  2,  2,   2,   2,    # noqa: 241
        1,   1,   1,   1,  1,  1,  1, 1, 1, 1, 1, 1, 1, 1, 1,  1,  1,  1,   1,   1,    # noqa: 241
        1,   1,   1,   1,  1,  1,  1, 1, 1, 1, 1, 1, 1, 1, 1,  1,  1,  1,   1,   1,    # noqa: 241
        2,   2,   2,   2,  2,  2,  2, 2, 2, 1, 1, 2, 2, 2, 2,  2,  2,  2,   2,   2,    # noqa: 241
        4,   4,   4,   4,  4,  4,  4, 4, 2, 1, 1, 2, 4, 4, 4,  4,  4,  4,   4,   4,    # noqa: 241
        8,   8,   8,   8,  8,  8,  8, 4, 2, 1, 1, 2, 4, 8, 8,  8,  8,  8,   8,   8,    # noqa: 241
        16,  16,  16,  16, 16, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 16, 16, 16,  16,  16,   # noqa: 241
        32,  32,  32,  32, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 32, 32,  32,  32,   # noqa: 241
        64,  64,  64,  64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 64,  64,  64,   # noqa: 241
        128, 128, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 128, 128,  # noqa: 241
        256, 256, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 256,  # noqa: 241
        512, 256, 128, 64, 32, 16, 8, 4, 2, 1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512,  # noqa: 241
    ]

    weight_maps = {
        'wall_crawl': WALL_CRAWL_WEIGHTS,
        'turtle': TURTLE_WEIGHTS
    }

    weight_elos = {
        'wall_crawl': -10.0,
        'turtle': -40.0
    }

    names = {
        'wall_crawl': 'WallCrawler',
        'turtle': 'Turtle'
    }

    def __init__(self, 
                 name: str=None, 
                 style: str='wall_crawl', 
                 custom_weights: list[int | float]=None, 
                 estimated_elo: float=None): 
        """
        Current `style` built-in options are 'wall_crawl' and 'turtle'
        Can optionally provide a custom set of weights instead
        """

        if custom_weights is not None:
            if len(custom_weights) != 20 * 20:
                raise Exception("TileWeightEngine custom_weights must be a list of exactly 400 values")
            self.weights = custom_weights
            name = name or "CustomTileWeights"
            est_elo: float = 0.0 if estimated_elo is None else estimated_elo
        
        else:
            if style not in self.weight_maps:
                raise Exception("TileWeightEngine given invalid style choice")
            self.weights = self.weight_maps[style]
            name = name or self.names[style]
            est_elo: float = self.weight_elos[style] if estimated_elo is None else estimated_elo

        super().__init__(name, estimated_elo=est_elo)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move: 

        cur_player = board.current_player

        def evaluate_move_weight(move: tilewe.Move) -> float: 
            total: float = 0

            offset = move.to_tile - move.contact 
            for tile in tilewe.piece_tiles(move.piece, move.rotation): 
                total += self.weights[tile + offset]

            return total

        moves = board.generate_legal_moves()
        random.shuffle(moves)

        if board.ply < board.n_players:
            #  prune to one corner to reduce moves to evaluate
            corner = board.player_corners(cur_player)[0]
            moves = [i for i in moves if i.to_tile == corner]

        return max(moves, key=evaluate_move_weight)

class SimpleSearchEngine(Engine): 
    """
    Plays the move that gives the best result given the board evaluation function.
    Only searches a single ply deep and the eval function takes a board
    and which player to evaluate positively for.
    Strength depends entirely on the quality of the evaluation function!
    """

    def __init__(
        self,
        name: str=None,
        eval_board: Callable[[tilewe.Board, tilewe.Color], float]=None,
        estimated_elo: float=None,
    ):
        name = name or "SimpleSearch"

        if eval_board is None:
            estimated_elo = 75.0 if estimated_elo is None else estimated_elo
            self.eval_function = self.default_eval
        else:
            estimated_elo = 0.0 if estimated_elo is None else estimated_elo
            self.eval_function = eval_board
        
        super().__init__(name, estimated_elo)

    def default_eval(self, board: tilewe.Board, player: tilewe.Color) -> float:
        score = 0.0

        # iterate the players to evaluate the state of the board
        for color in range(0, board.n_players):
            if color == player:
                # bonus for score
                score += board.scores[color] * 0.5

                # bonus for playable corners
                score += board.n_player_corners(color) * 0.2

                # bonus for winning
                if board.finished and color in board.winners:
                    score += 1000

                # penalty for losing early
                if not board.finished and not board.can_play(for_player=color):
                    score -= 1000
            else:
                # penalty for other players' scores
                score -= board.scores[color] * 0.1
                
                # penalty for other players' playable corners
                score -= board.n_player_corners(color) * 0.04

                # bonus for other players losing early
                if not board.finished and not board.can_play(for_player=color):
                    score += 3

        return score

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move:
        moves: list[tilewe.Move] = board.generate_legal_moves()
        player: tilewe.Color = board.current_player
        moves_evaluated: int = 0

        best: float = -math.inf
        best_move: tilewe.Move = random.choice(moves)

        # check each legal move
        for move in moves:
            moves_evaluated += 1

            # respect the time control
            if moves_evaluated % 100 == 0 and self.out_of_time():
                break

            # evaluate the board state after the move
            with MoveExecutor(board, move):
                result: float = self.eval_function(board, player)

                if result > best:
                    best = result
                    best_move = move

        return best_move
