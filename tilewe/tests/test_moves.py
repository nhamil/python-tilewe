import unittest 

import tilewe

class TestMoves(unittest.TestCase): 
    
    def test_unique_legal_move(self): 
        board = tilewe.Board(4) 

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.NORTH, 
            contact=tilewe.A03, 
            to_tile=tilewe.A20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.EAST, 
            contact=tilewe.A01, 
            to_tile=tilewe.A01
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.NORTH, 
            contact=tilewe.A02, 
            to_tile=tilewe.A20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.EAST, 
            contact=tilewe.B03, 
            to_tile=tilewe.T20
        )))

    def test_unique_illegal_move(self): 
        board = tilewe.Board(4) 

        # contact is valid, but tiles would be placed off the board 
        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.NORTH, 
            contact=tilewe.A03, 
            to_tile=tilewe.A01
        )))

        # contact is not valid 
        self.assertRaises(AttributeError, lambda: tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.NORTH, 
            contact=tilewe.A01, 
            to_tile=tilewe.A01
        ))

        # contact is invalid, and tiles would be placed off the board
        self.assertRaises(AttributeError, lambda: tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.SOUTH, 
            contact=tilewe.C02, 
            to_tile=tilewe.A20
        ))

        self.assertRaises(AttributeError, lambda: tilewe.Move(
            piece=None, 
            rotation=tilewe.EAST, 
            contact=tilewe.B03, 
            to_tile=tilewe.T20
        ))

        self.assertRaises(AttributeError, lambda: tilewe.Move(
            piece=tilewe.T4, 
            rotation=None, 
            contact=tilewe.B03, 
            to_tile=tilewe.T20
        ))

        self.assertRaises(AttributeError, lambda: tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.EAST, 
            contact=None, 
            to_tile=tilewe.T20
        ))

        self.assertRaises(AttributeError, lambda: tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.EAST, 
            contact=tilewe.B03, 
            to_tile=None
        ))

    def test_n_legal_moves(self): 
        board = tilewe.Board(4) 
        
        self.assertTrue(board.n_legal_moves() == len(board.generate_legal_moves()))

    # def test_null_move_1_player(self): 
    #     board = tilewe.Board(1) 

    #     self.assertEqual(board.current_player, tilewe.BLUE)
    #     board.push_null()
    #     self.assertEqual(board.current_player, tilewe.BLUE)
    #     board.pop_null() 
    #     self.assertEqual(board.current_player, tilewe.BLUE)

    # def test_null_move_2_player(self): 
    #     board = tilewe.Board(2) 

    #     self.assertEqual(board.current_player, tilewe.BLUE)
    #     board.push_null()
    #     self.assertEqual(board.current_player, tilewe.YELLOW)
    #     board.pop_null() 
    #     self.assertEqual(board.current_player, tilewe.BLUE)

    # def test_null_move_3_player(self): 
    #     board = tilewe.Board(3) 

    #     self.assertEqual(board.current_player, tilewe.BLUE)
    #     board.push_null()
    #     self.assertEqual(board.current_player, tilewe.YELLOW)
    #     board.push_null()
    #     self.assertEqual(board.current_player, tilewe.RED)
    #     board.push_null()
    #     self.assertEqual(board.current_player, tilewe.BLUE)
    #     board.pop_null() 
    #     board.pop_null() 
    #     self.assertEqual(board.current_player, tilewe.YELLOW)
    #     board.pop_null() 
    #     self.assertEqual(board.current_player, tilewe.BLUE)

    def test_legal_move_gen_full_game(self):
        board = tilewe.Board(4) 

        while not board.finished: 
            # assert that all generated unique moves are legal for every ply
            unique_moves = board.generate_legal_moves(unique=True)
            for mv in unique_moves:
                self.assertTrue(board.is_legal(mv))

            # assert that all generated non-unique moves are legal for every ply
            non_unique_moves = board.generate_legal_moves(unique=False)
            for mv in non_unique_moves:
                self.assertTrue(board.is_legal(mv))

            board.push(unique_moves[0])

if __name__ == '__main__': 
    unittest.main() 
