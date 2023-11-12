import multiprocessing
import traceback
import random
import signal

import tilewe 
from tilewe.engine import Engine
from tilewe.elo import compute_elo_adjustment_n

class Tournament: 
    """
    Provides an easy construct for testing large amounts of games
    for any amount of engines greater than 1. Utilizes multiprocessing to play many
    games at once. Handles randomizing turn order and reports on 
    win/score results after each game completes. Currently does
    not enforce time controls, but Engines should follow them anyways.

    Example
    -------
    >>> tournament = tilewe.tournament.Tournament([
        tilewe.engine.LargestPieceEngine(), 
        tilewe.engine.MostOpenCornersEngine(), 
        tilewe.engine.MaximizeMoveDifferenceEngine(), 
        tilewe.engine.RandomEngine()
    ], move_seconds=30)
    >>> tournament.play(1000, n_threads=multiprocessing.cpu_count(), move_seconds=15)
    """

    def __init__(self, engines: list[Engine], move_seconds: int=60):
        """
        Parameters
        ----------
        n_games : int
            The number of games to play
        engines : list[Engine]
            The list of engines to play in the games (at least 1)
        move_seconds : int=60
            The default time control if `play` doesn't override it
        """
        
        if (len(engines) < 1):
            raise Exception("Number of engines must be greater than 0")
        
        self.engines = list(engines)
        self._seconds = move_seconds
        self.move_seconds = self._seconds

    def play(self, n_games: int, n_threads: int=1, move_seconds: int=None, verbose_board: bool=False):
        """
        Used to launch a series of games in an initialized Tournament.

        Parameters
        ----------
        n_games : int
            The number of games to play
        n_threads : int=1
            The number of simultaneous games to multiprocess
        move_seconds : int=60
            Optional override for the time control for these games
        verbose_board : bool=False
            Whether or not to print the final board state of each match
        """
        
        # initialize trackers and game controls
        total_games = 0
        wins = [0 for _ in range(len(self.engines))]
        games = [0 for _ in range(len(self.engines))]
        elos = [0 for _ in range(len(self.engines))]
        totals = [0 for _ in range(len(self.engines))]
        self.move_seconds = move_seconds if move_seconds is not None else self._seconds

        N = len(self.engines)

        # prepare turn orders for the various games
        args = [] 
        for _ in range(n_games): 
            order = list(range(N))
            random.shuffle(order) 
            args.append(order[:4]) 

        # play games with the given level of concurrency
        with multiprocessing.Pool(n_threads, initializer=signal.signal, initargs=(signal.SIGINT, signal.SIG_IGN)) as pool: 
            try:
                for winners, scores, board, player_to_engine in pool.imap_unordered(self._play_game, args): 
                    if len(winners) > 0: # at least one player always wins, if none then game crashed 
                        total_games += 1 
                        for p in winners: 
                            wins[p] += 1 
                        for p, s in enumerate(scores): 
                            totals[p] += s
                            if s > 0:
                                games[p] += 1

                        # get the names and scores for involved players
                        game_players = [player_to_engine[i] for i in range(board.n_players)]
                        player_names = [self.engines[i].name for i in game_players]
                        player_scores = [scores[i] for i in game_players]
                        winner_names = [self.engines[i].name for i in winners]
                        
                        # if there are enough players, compute elo changes
                        if board.n_players > 1:
                            player_elos = [elos[i] for i in game_players]
                            delta_elos = compute_elo_adjustment_n(player_elos, player_scores)
                            for player, index in zip(game_players, range(len(game_players))):
                                elos[player] += delta_elos[index]
                            # new_elos = [elos[i] for i in game_players]

                        # output match results
                        out_names = ' '.join([f"{i:14.14}" for i in player_names])
                        print(f"Game {total_games:>{len(str(n_games))}}: {out_names:{board.n_players * 15}}  Scores: {player_scores}  Winner(s): {', '.join(winner_names)}")
                        if verbose_board:
                            print(board)
                            print("")

                        # every match chunk (or minimum 5 matches) output rankings
                        if total_games % max(5, n_threads) == 0:
                            print(f"\n{'Rank':4} {'Name':24} {'Elo':>5} {'Games':>6} {'Score':>10} {'Wins':>6} {'Win Rate':>9}")
                            ranked_engines = sorted(range(len(self.engines)), key=lambda x: -elos[x])
                            for engine, rank in zip(ranked_engines, range(len(self.engines))):
                                print(f"{rank:>4d} {self.engines[engine].name:24.24} {elos[engine]:>5.0f} {games[engine]:>6d} {totals[engine]:>10d} {wins[engine]:>6d} {(wins[engine]/games[engine]*100):>8.2f}%")
                            print("")
                    else: 
                        print("Game failed to terminate")
            except KeyboardInterrupt:
                print("Caught KeyboardInterrupt, terminating workers")
                pool.terminate()
                return

    def _play_game(self, player_to_engine: list[int]) -> tuple[list[int], list[int], tilewe.Board, dict[int, int]]:
        """
        An individual game launched by the `play` wrapper.
        Plays one game given the list of engines and returns results.

        Parameters
        ----------
        player_to_engine : list[int]
            List of engine indices indicating the players and their turn order

        Returns
        -------
        winners : list[int]
            A list of the engine indices that won the match
        scores : list[int]
            A list of the scores earned for each engine (even those not in this match, as 0)
        board : tilewe.Board
            A reference to the game board in it's finished state
        player_to_engine : dict[int, int]
            A mapping of player position (i.e. turn order) to engine index for this match
        """

        board = tilewe.Board(n_players=len(player_to_engine))
        try: 
            engine_to_player = { value: key for key, value in enumerate(player_to_engine) }
            while not board.finished: 
                engine = self.engines[player_to_engine[board.current_player]]
                move = engine.search(board.copy_current_state(), self.move_seconds) 
                # TODO test legality 
                board.push(move) 

            # put scores back in original engine order 
            winners = [ player_to_engine[x] for x in board.winners ]
            scores = [ board.scores[engine_to_player[i]] if i in engine_to_player else 0 for i in range(len(self.engines)) ]

            return winners, scores, board, player_to_engine
        
        except: 
            traceback.print_exc()
            return [], [], board 