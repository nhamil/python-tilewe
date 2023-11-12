import multiprocessing
import traceback
import random
import signal

import tilewe 
from tilewe.engine import Engine

class Tournament: 
    """
    Provides an easy construct for testing large amounts of games
    between 1 to 4 Engines. Utilizes multi-processing to play many
    games at once. Handles randomizing turn order and reports on 
    win/score results after each game completes. Currently does
    not enforce time controls, but Engines should follow them anyways.
    """

    def __init__(self, engines: list[Engine], move_seconds: int=60): 
        self.engines = list(engines)
        self._seconds = move_seconds
        self.move_seconds = self._seconds

    def play(self, n_games: int, n_threads: int=1, move_seconds: int=None):
        # initialize trackers and game controls
        games = 0
        wins = [0 for _ in range(len(self.engines))]
        totals = [0 for _ in range(len(self.engines))]
        self.move_seconds = move_seconds if move_seconds is not None else self._seconds

        N = len(self.engines)

        # prepare turn orders for the various games
        args = [] 
        for _ in range(n_games): 
            order = list(range(N))
            random.shuffle(order) 
            args.append(order) 

        # play games with the given level of concurrency
        with multiprocessing.Pool(n_threads, initializer=signal.signal, initargs=(signal.SIGINT, signal.SIG_IGN)) as pool: 
            try:
                for winners, scores, _ in pool.imap_unordered(self._play_game, args): 
                    if len(winners) > 0: # at least one player always wins, if none then game crashed 
                        games += 1 
                        for p in winners: 
                            wins[p] += 1 
                        for p, s in enumerate(scores): 
                            totals[p] += s

                        print(f"Game {games}: \twinners:", winners, "\tscores:", scores, "\ttotal wins:", wins, "\ttotal scores:", totals)
                    else: 
                        print("Game failed to terminate")
            except KeyboardInterrupt:
                print("Caught KeyboardInterrupt, terminating workers")
                pool.terminate()
                return

    def _play_game(self, player_to_engine: list[int]) -> tuple[list[int], list[int], tilewe.Board]: 
        board = tilewe.Board(n_players=len(self.engines))

        try: 
            engine_to_player = { value: key for key, value in enumerate(player_to_engine) }
            while not board.finished: 
                engine = self.engines[player_to_engine[board.current_player]]
                move = engine.search(board.copy_current_state(), self.move_seconds) 
                # TODO test legality 
                board.push(move) 

            # put scores back in original engine order 
            winners = [ player_to_engine[x] for x in board.winners ]
            board_scores = board.scores
            scores = [ board_scores[engine_to_player[i]] for i in range(len(self.engines)) ]

            return winners, scores, board
        
        except: 
            traceback.print_exc()
            return [], [], board 