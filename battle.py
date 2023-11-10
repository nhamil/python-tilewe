import random
import tilewe
import signal
from typing import Callable
from multiprocessing import Pool

#from community import random_bot, tile_size_bot
#from michael import Bot as michael_bot
#from mason import Bot as mason_bot
#from nik import Bot as nik_bot

tilewe.print_color = False

# Runs a single game with the specified bots in their given player order
# Author: Michael
def play_game(
    id: int, 
    B1: Callable[[tilewe.Board, tilewe.Color], tilewe.Move], 
    B2: Callable[[tilewe.Board, tilewe.Color], tilewe.Move], 
    B3: Callable[[tilewe.Board, tilewe.Color], tilewe.Move], 
    B4: Callable[[tilewe.Board, tilewe.Color], tilewe.Move]
) -> tilewe.Board:
    # Player count
    player_count = sum([1 for i in [B1, B2, B3, B4] if i is not None])

    # Init game
    board = tilewe.Board(player_count) 

    # Play game
    print(f"Starting Game #{id}")
    while not board.finished: 
        if (board.current_player == tilewe.COLORS[0]):
            move = B1(board, tilewe.COLORS[0])
        elif (board.current_player == tilewe.COLORS[1]):
            move = B2(board, tilewe.COLORS[1])
        elif (board.current_player == tilewe.COLORS[2]):
            move = B3(board, tilewe.COLORS[2])
        elif (board.current_player == tilewe.COLORS[3]):
            move = B4(board, tilewe.COLORS[3])
        board.push(move) 
    
    # Finish game
    print(f"Finished Game #{id}")
    print(board)
    return board

# Runs a series of game's in parallel using multiprocessing
# Shuffle's the play order across games and reports stats at the end
# Author: Michael
def multiprocessed_games(
    B1: Callable[[tilewe.Board, tilewe.Color], tilewe.Move], 
    B2: Callable[[tilewe.Board, tilewe.Color], tilewe.Move] | None, 
    B3: Callable[[tilewe.Board, tilewe.Color], tilewe.Move] | None, 
    B4: Callable[[tilewe.Board, tilewe.Color], tilewe.Move] | None,
    identifiers: list[str] = ['P1', 'P2', 'P3', 'P4'],
    game_count: int = 100,
    pool_size: int = 8
) -> None:
    # Play games simultaneously
    boards = []
    bots = [i for i in [B1, B2, B3, B4] if i is not None]
    player_count = len(bots)

    with Pool(pool_size, initializer=signal.signal, initargs=(signal.SIGINT, signal.SIG_IGN)) as p:
        try:
            args = []
            for i in range(0, game_count):
                random.shuffle(bots)
                args.append([i, *(bots + ([None] * (4 - len(bots))))])
            boards = p.starmap(play_game, args)
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            p.terminate()
            return
    
    # Record data
    pos_wins = [0, 0, 0, 0]
    pos_scores = [0, 0, 0, 0]
    player_wins = [0, 0, 0, 0]
    player_scores = [0, 0, 0, 0]
    for arg_list in args:
        board = boards[arg_list[0]]
        for player in range(0, player_count):
            bot = arg_list[player + 1]
            if bot == B1:
                botPos = 0
            elif bot == B2:
                botPos = 1
            elif bot == B3:
                botPos = 2
            elif bot == B4:
                botPos = 3

            if player in board.winners:
                pos_wins[player] += 1
                player_wins[botPos] += 1
            pos_scores[player] += board._players[player].score
            player_scores[botPos] += board._players[player].score

    # Output data
    for player in range(0, player_count):
        print(f"Position {player}: {pos_wins[player]}/{game_count} wins, {pos_scores[player]} total score, avg score {round(pos_scores[player]/game_count, 3)}")
    for player in range(0, player_count):
        print(f"Player {identifiers[player]}: {player_wins[player]}/{game_count} wins, {player_scores[player]} total score, avg score {round(player_scores[player]/game_count, 3)}")

def piece_size(piece: tilewe.Piece) -> int: len(tilewe._PIECES[piece].rotations[0].tiles)

# Author: Nik
def random_bot(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move:
    moves = board.generate_legal_moves(unique=True) 
    return random.choice(moves) 

# Author: Michael
def tile_size_bot(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move:
    moves = sorted(board.generate_legal_moves(unique=True), key=lambda x: -piece_size(x.piece))
    largestSize = len(tilewe._PIECES[max(moves, key=lambda x: piece_size(x.piece)).piece].rotations[0].tiles)
    largestCount = sum(1 for x in moves if piece_size(x.piece) == largestSize)
    return random.choice(moves[:largestCount])

# Define Bots here. If less players desired, replace with None in the multiprocessedGames call.
def player1(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move: return tile_size_bot(board, player)
def player2(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move: return random_bot(board, player)
def player3(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move: return tile_size_bot(board, player)
def player4(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move: return random_bot(board, player)

if __name__ == '__main__': 
    GAME_COUNT = 1000
    THREAD_COUNT = 8
    multiprocessed_games(
        player1,
        player2,
        player3,
        player4,
        ['TileSize1', 'Random1', 'TileSize2', 'Random2'],
        GAME_COUNT,
        THREAD_COUNT
    )