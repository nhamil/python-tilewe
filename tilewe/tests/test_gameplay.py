import unittest 
import logging
import random
import sys

import tilewe
from tilewe.engine import RandomEngine

class TestGameplay(unittest.TestCase): 

    log = logging.getLogger( "Test_Debug" )
    
    def test_no_moves_is_finished(self):
        random.seed(0)
        board = tilewe.Board(4) 
        while (moves := board.generate_legal_moves(unique=True)):
            mv: tilewe.Move = random.choice(moves)
            board.push(mv)
        
        self.log.debug("test_no_moves_is_finished\n" + str(board))

        # assert that when no more moves can be played, the game is finished
        self.assertTrue(board.finished)

        # assert that when no more moves can be played, all players have can_play() == False
        for i in range(board.n_players):
            self.assertFalse(board.can_play(player=i))

    def test_finished_game_state(self):
        random.seed(0)
        board = tilewe.Board(4) 
        engine = RandomEngine()
        while not board.finished:
            mv: tilewe.Move = engine.search(board)
            board.push(mv)
        
        self.log.debug("test_finished_game_state\n" + str(board))

        for i in range(board.n_players):
            # assert that when the game is marked finished, no moves can be played
            self.assertEqual(board.n_legal_moves(unique=True, for_player=i), 0)
            self.assertEqual(board.generate_legal_moves(unique=True, for_player=i), [])

            self.assertEqual(board.n_legal_moves(unique=False, for_player=i), 0)
            self.assertEqual(board.generate_legal_moves(unique=False, for_player=i), [])

            self.assertFalse(board.can_play(player=i))

            # assert that when there are no moves, players have 0 open corners
            self.assertEqual(len(board.player_corners(i)), 0)
            self.assertEqual(board.n_player_corners(i), 0)

        expected_game = [
            'T5e-c3t20', 'P5sf-a3a20', 'P5sf-b1t1', 'Z5e-a1a1', 'Z4n-c1q18', 'I4n-a4c17', 'N5nf-b1r4', 'L5e-a1d4',
            'L4wf-c1n18', 'L4s-b1d18', 'I2n-a1s7', 'F5w-c2c6', 'F5wf-c3k17', 'Y5nf-a4d13', 'L5ef-d2p5', 'I3e-a1d7',
            'Y5w-d2k20', 'Z5n-c1c9', 'V5n-c1p8', 'U5n-a2e3', 'W5w-a3k14', 'T4w-a1e14', 'F5ef-c2l4', 'I2e-a1b8',
            'O1n-a1n20', 'U5n-a2e9', 'U5n-a2i2', 'Y5n-a3h6', 'T4n-a2n14', 'V5w-a3f13', 'O1n-a1o11', 'N5e-a2j8',
            'P5w-c1h18', 'I2e-a1i14', 'Y5sf-a2q11', 'L3e-b2i9', 'V5n-c3k12', 'O1n-a1h15', 'L3s-b1q14', 'V5n-c1g10',
            'L3e-a2r17', 'L5n-b1b13', 'L4nf-b3q3', 'O1n-a1k6', 'I3n-a3s15', 'L3e-a1g16', 'T4w-b2o2', 'W5e-b1m9',
            'I2e-b1e17', 'F5s-a1k15', 'Z4nf-b1o16', 'T4w-a1n11', 'I4n-a4t12', 'Z4nf-a1i18', 'I3n-a3t6', 'Z4nf-a1n6',
            'T5e-c1h3', 'T5w-a1q8', 'I4e-d1g6', 'L4e-a1m14', 'Z5e-c3c5']
        all_moves = [str(move) for move in board.moves]

        # assert that the expected game was played
        unexpected_game_msg = "Expected game not played, was generate_legal_moves() changed intentionally?"
        self.assertEqual(all_moves, expected_game, unexpected_game_msg)
        self.assertEqual(board.winners, [2], unexpected_game_msg)

    def test_open_corners_first_moves(self):
        engine = RandomEngine()
        
        # test for games of all valid player counts
        for n in [1, 2, 3, 4]:
            random.seed(0)
            board = tilewe.Board(n) 
            while board.ply < board.n_players:
                current_player = board.current_player

                # assert that player N has 4-N of the opening corners to choose from
                self.assertEqual(board.n_player_corners(current_player), 4 - board.ply)
                mv: tilewe.Move = engine.search(board)
                board.push(mv)

                # assert that the next player is (N + 1) % num players (when all players remain in the game)
                self.assertEqual(board.current_player, (current_player + 1) % board.n_players)

            # assert that a starting corner has been taken by each player's first move
            start_corners = [tilewe.A01, tilewe.A20, tilewe.T01, tilewe.T20]
            taken_start_corners = sum([1 for c in start_corners if board.color_at(c) != tilewe.NO_COLOR])
            self.assertEqual(taken_start_corners, board.n_players)

if __name__ == "__main__":
    # enables logging if file run directly instead of through pytest
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test_Debug").setLevel(logging.DEBUG)
    unittest.main()
