import copy 
import unittest 

import tilewe 

class TestTilewe(unittest.TestCase): 
    
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

    def test_nonunique_legal_move(self): 
        board = tilewe.Board(4) 

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.SOUTH, 
            contact=tilewe.A03, 
            to_tile=tilewe.A20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.WEST, 
            contact=tilewe.A01, 
            to_tile=tilewe.A01
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.NORTH_F, 
            contact=tilewe.A02, 
            to_tile=tilewe.A20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.WEST_F, 
            contact=tilewe.B03, 
            to_tile=tilewe.T20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.O4, 
            rotation=tilewe.WEST_F, 
            contact=tilewe.B01, 
            to_tile=tilewe.T01
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
        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.NORTH, 
            contact=tilewe.A01, 
            to_tile=tilewe.A01
        )))

        # contact is invalid, and tiles would be placed off the board
        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.SOUTH, 
            contact=tilewe.C02, 
            to_tile=tilewe.A20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=None, 
            rotation=tilewe.EAST, 
            contact=tilewe.B03, 
            to_tile=tilewe.T20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=None, 
            contact=tilewe.B03, 
            to_tile=tilewe.T20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.EAST, 
            contact=None, 
            to_tile=tilewe.T20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.EAST, 
            contact=tilewe.B03, 
            to_tile=None
        )))

    def test_nonunique_illegal_move(self): 
        board = tilewe.Board(4) 

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.SOUTH, 
            contact=tilewe.A03, 
            to_tile=tilewe.A01
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.O4, 
            rotation=tilewe.WEST_F, 
            contact=tilewe.B01, 
            to_tile=tilewe.T20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.NORTH_F, 
            contact=tilewe.A02, 
            to_tile=tilewe.A19
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.WEST_F, 
            contact=tilewe.B02, 
            to_tile=tilewe.T20
        )))

    def test_nonunique_move_gen_legal(self): 
        board = tilewe.Board(4) 

        moves = board.generate_legal_moves(unique=False) 

        for move in moves: 
            self.assertTrue(board.is_legal(move))

    def test_nonunique_move_gen_has_unique_move(self): 
        board = tilewe.Board(4) 

        unique = board.generate_legal_moves(unique=True) 
        moves = board.generate_legal_moves(unique=False) 

        for move in moves: 
            self.assertTrue(move.to_unique() in unique)

    def test_n_legal_moves(self): 
        board = tilewe.Board(4) 
        
        self.assertTrue(board.n_legal_moves(unique=True) == len(board.generate_legal_moves(unique=True)))
        self.assertTrue(board.n_legal_moves(unique=False) == len(board.generate_legal_moves(unique=False)))

    def test_null_move_1_player(self): 
        board = tilewe.Board(1) 

        self.assertEqual(board.current_player, tilewe.BLUE)
        board.push_null()
        self.assertEqual(board.current_player, tilewe.BLUE)
        board.pop_null() 
        self.assertEqual(board.current_player, tilewe.BLUE)

    def test_null_move_2_player(self): 
        board = tilewe.Board(2) 

        self.assertEqual(board.current_player, tilewe.BLUE)
        board.push_null()
        self.assertEqual(board.current_player, tilewe.YELLOW)
        board.pop_null() 
        self.assertEqual(board.current_player, tilewe.BLUE)

    def test_null_move_3_player(self): 
        board = tilewe.Board(3) 

        self.assertEqual(board.current_player, tilewe.BLUE)
        board.push_null()
        self.assertEqual(board.current_player, tilewe.YELLOW)
        board.push_null()
        self.assertEqual(board.current_player, tilewe.RED)
        board.push_null()
        self.assertEqual(board.current_player, tilewe.BLUE)
        board.pop_null() 
        board.pop_null() 
        self.assertEqual(board.current_player, tilewe.YELLOW)
        board.pop_null() 
        self.assertEqual(board.current_player, tilewe.BLUE)

if __name__ == '__main__': 
    unittest.main() 
