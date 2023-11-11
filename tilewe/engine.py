import random 
import time 

import tilewe 

class Engine: 

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

class RandomEngine(Engine): 

    def __init__(self, name: str="Random"): 
        super().__init__(name)

    def on_search(self, board: tilewe.Board, _seconds: float) -> tilewe.Move: 
        return random.choice(board.generate_legal_moves(unique=True)) 

class Tournament: 

    def __init__(self, engines: list[Engine]): 
        self.engines = list(engines) 

    def play(self, n_games: int): 
        games = 0
        wins = [0 for _ in range(len(self.engines))]
        totals = [0 for _ in range(len(self.engines))]

        for i in range(n_games): 
            winners, scores, _ = self._play_game(i) 

            if len(winners) > 0: # at least one player always wins, if none then game crashed 
                games += 1 
                for p in winners: 
                    wins[p] += 1 
                for p, s in enumerate(scores): 
                    totals[p] += s

            print(f"Game {i}: \twinners:", winners, "\tscores:", scores, "\ttotal wins:", wins, "\ttotal scores:", totals)

    def _play_game(self, i: int) -> tuple[list[int], list[int], tilewe.Board]: 
        board = tilewe.Board(n_players=len(self.engines))

        try: 
            while not board.finished: 
                move = self.engines[board.current_player].search(board.copy_current_state(), 60.0) 
                # TODO test legality 
                board.push(move) 

            return board.winners, board.scores, board
        
        except: 
            print(f"Exception occurred for game {i}")
            return [], [], board 
