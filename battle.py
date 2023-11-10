import random
import tilewe
import signal
from typing import Callable
from multiprocessing import Pool

#from community import randomBot, tileSizeBot
#from michael import Bot as MichaelBot
#from mason import Bot as MasonBot
#from nik import Bot as NikBot

tilewe.print_color = False

# Runs a single game with the specified bots in their given player order
# Author: Michael
def playGame(
    id: int, 
    B1: Callable[[tilewe.Board, tilewe.Color], tilewe.Move], 
    B2: Callable[[tilewe.Board, tilewe.Color], tilewe.Move], 
    B3: Callable[[tilewe.Board, tilewe.Color], tilewe.Move], 
    B4: Callable[[tilewe.Board, tilewe.Color], tilewe.Move]
) -> tilewe.Board:
    # Player count
    playerCount = sum([1 for i in [B1, B2, B3, B4] if i is not None])

    # Init game
    board = tilewe.Board(playerCount) 

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
def multiprocessedGames(
    B1: Callable[[tilewe.Board, tilewe.Color], tilewe.Move], 
    B2: Callable[[tilewe.Board, tilewe.Color], tilewe.Move] | None, 
    B3: Callable[[tilewe.Board, tilewe.Color], tilewe.Move] | None, 
    B4: Callable[[tilewe.Board, tilewe.Color], tilewe.Move] | None,
    identifiers: list[str] = ['P1', 'P2', 'P3', 'P4'],
    gameCount: int = 100,
    poolSize: int = 8
) -> None:
    # Play games simultaneously
    boards = []
    bots = [i for i in [B1, B2, B3, B4] if i is not None]
    playerCount = len(bots)

    with Pool(poolSize, initializer=signal.signal, initargs=(signal.SIGINT, signal.SIG_IGN)) as p:
        try:
            args = []
            for i in range(0, gameCount):
                random.shuffle(bots)
                args.append([i, *(bots + ([None] * (4 - len(bots))))])
            boards = p.starmap(playGame, args)
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            p.terminate()
            return
    
    # Record data
    posWins = [0, 0, 0, 0]
    posScores = [0, 0, 0, 0]
    playerWins = [0, 0, 0, 0]
    playerScores = [0, 0, 0, 0]
    for argList in args:
        board = boards[argList[0]]
        for player in range(0, playerCount):
            bot = argList[player + 1]
            if bot == B1:
                botPos = 0
            elif bot == B2:
                botPos = 1
            elif bot == B3:
                botPos = 2
            elif bot == B4:
                botPos = 3

            if player in board.winners:
                posWins[player] += 1
                playerWins[botPos] += 1
            posScores[player] += board._players[player].score
            playerScores[botPos] += board._players[player].score

    # Output data
    for player in range(0, playerCount):
        print(f"Position {player}: {posWins[player]}/{gameCount} wins, {posScores[player]} total score, avg score {round(posScores[player]/gameCount, 3)}")
    for player in range(0, playerCount):
        print(f"Player {identifiers[player]}: {playerWins[player]}/{gameCount} wins, {playerScores[player]} total score, avg score {round(playerScores[player]/gameCount, 3)}")

# Author: Nik
def randomBot(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move:
    moves = board.generate_legal_moves(unique=True) 
    return random.choice(moves) 

# Author: Michael
def tileSizeBot(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move:
    moves = sorted(board.generate_legal_moves(unique=True), key=lambda x: -len(tilewe._PIECES[x.piece].rotations[0].tiles))
    largestSize = len(tilewe._PIECES[max(moves, key=lambda x: len(tilewe._PIECES[x.piece].rotations[0].tiles)).piece].rotations[0].tiles)
    largestCount = sum(1 for i in moves if len(tilewe._PIECES[i.piece].rotations[0].tiles) == largestSize)
    return random.choice(moves[:largestCount])

# Define Bots here. If less players desired, replace with None in the multiprocessedGames call.
def player1(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move: return tileSizeBot(board, player)
def player2(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move: return randomBot(board, player)
def player3(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move: return tileSizeBot(board, player)
def player4(board: tilewe.Board, player: tilewe.Color) -> tilewe.Move: return randomBot(board, player)

if __name__ == '__main__': 
    GAME_COUNT = 1000
    THREAD_COUNT = 8
    multiprocessedGames(
        player1,
        player2,
        player3,
        player4,
        ['TileSize1', 'Random1', 'TileSize2', 'Random2'],
        GAME_COUNT,
        THREAD_COUNT
    )