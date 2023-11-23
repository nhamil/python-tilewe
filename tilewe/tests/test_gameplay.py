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

        # play a game until no legal moves are generated
        tracked_ply = 0
        while (moves := board.generate_legal_moves(unique=True)):
            board.push(random.choice(moves))

            # assert that the game finishes before 84 moves (i.e. no infinite loop)
            tracked_ply += 1
            self.assertLessEqual(tracked_ply, 84)
        
        self.log.debug("test_no_moves_is_finished\n" + str(board))

        # assert that when no more moves can be played, the game is finished
        self.assertTrue(board.finished)

        # assert that when no more moves can be played, all players have can_play() == False
        for i in range(board.n_players):
            self.assertFalse(board.can_play(for_player=i))

    def test_finished_game_state(self):
        random.seed(0)
        board = tilewe.Board(4) 

        # play a game until the state is marked finished
        tracked_ply = 0
        while not board.finished:
            board.push(random.choice(sorted(board.generate_legal_moves(), key=lambda m: tilewe.move_str(m))))

            # assert that the game finishes before 84 moves (i.e. no infinite loop)
            tracked_ply += 1
            self.assertLessEqual(tracked_ply, 84)
        
        self.log.debug("test_finished_game_state\n" + str(board))

        for i in range(board.n_players):
            # assert that when the game is marked finished, no moves can be played
            self.assertEqual(board.n_legal_moves(for_player=i), 0)
            self.assertEqual(board.generate_legal_moves(for_player=i), [])

            self.assertFalse(board.can_play(for_player=i))

            # assert that when there are no moves, players have 0 open corners
            self.assertEqual(len(board.player_corners(i)), 0)
            self.assertEqual(board.n_player_corners(i), 0)

        expected_game = [
            'Z4e-a1a1', 'P5n-a3a20', 'W5n-c3t20', 'Z5ef-c1t1', 'T5e-c1c4', 'F5n-b3b17', 'L4w-c1q19', 'T4w-a1s4',  
            'Y5wf-a2d7', 'X5n-a2d16', 'Y5wf-d2n18', 'Y5nf-b3q4', 'O1n-a1h6', 'Z5ef-c1f18', 'O4n-a2n16', 'P5wf-c1r7', 
            'L5e-a2d3', 'V5n-c3c14', 'I3e-a1p14', 'L5sf-b4o8', 'I2e-a1i7', 'L3w-b2g15', 'T4s-b2m14', 'V5w-c1m9', 
            'L4e-a1h8', 'Y5w-b1h16', 'X5n-c2k14', 'I5e-e1m4', 'P5sf-b1g10', 'I3n-a3h13', 'Z4e-b2j19', 'F5sf-b3h3', 
            'N5wf-c2k6', 'T5s-a1i10', 'U5w-a3s15', 'I3n-a3n3', 'L3w-a1k8', 'W5e-a3d11', 'O1n-a1h15', 'O1n-a1j2', 
            'U5w-b1c8', 'L4ef-a2k16', 'N5w-a2o12', 'W5w-b2s9', 'W5w-c1e13', 'O1n-a1i15', 'I2n-a2i12', 'I2e-b1h5', 
            'T4w-b2b14', 'Z4nf-a1n17', 'F5e-b3o10', 'L3n-b1f1', 'U5n-a2q17', 'Z5ef-a3o7', 'T5s-c1f4', 'I2e-a1g20', 
            'T5e-c3m8', 'L4nf-b3c3', 'L5wf-d1n19', 'N5w-a2n14', 'T4n-a2r12'
        ]
        all_moves = [tilewe.move_str(move) for move in board.moves]

        # assert that the expected game was played
        unexpected_game_msg = "Expected game not played, was generate_legal_moves() changed intentionally?"
        self.assertEqual(all_moves, expected_game, unexpected_game_msg)
        self.assertEqual(board.winners, [1], unexpected_game_msg)

    def test_open_corners_first_moves(self):
        engine = RandomEngine()
        
        # test for games of all valid player counts
        for n in [1, 2, 3, 4]:
            random.seed(0)
            board = tilewe.Board(n) 
            while board.ply < board.n_players:
                current_player = board.current_player
                current_ply = board.ply

                # assert that player N has 4-N of the opening corners to choose from
                self.assertEqual(board.n_player_corners(current_player), 4 - board.ply)

                board.push(engine.search(board))

                # assert that the next player is (N + 1) % num players (when all players remain in the game)
                self.assertEqual(board.current_player, (current_player + 1) % board.n_players)

                # assert that ply increases with the move
                self.assertEqual(board.ply, current_ply + 1)

            # assert that a starting corner has been taken by each player's first move
            start_corners = [tilewe.A01, tilewe.A20, tilewe.T01, tilewe.T20]
            taken_start_corners = sum([1 for c in start_corners if board.color_at(c) != tilewe.NO_COLOR])
            self.assertEqual(taken_start_corners, board.n_players)

if __name__ == "__main__":
    # enables logging if file run directly instead of through pytest
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test_Debug").setLevel(logging.DEBUG)
    unittest.main()
