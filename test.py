import unittest 

import tilewe 

class TestTilewe(unittest.TestCase): 
    
    def test_unique_legal_move(self): 
        board = tilewe.Board(4) 

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.NORTH, 
            contact=tilewe.A03, 
            to_square=tilewe.A20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.EAST, 
            contact=tilewe.A01, 
            to_square=tilewe.A01
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.NORTH, 
            contact=tilewe.A02, 
            to_square=tilewe.A20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.EAST, 
            contact=tilewe.B03, 
            to_square=tilewe.T20
        )))

    def test_nonunique_legal_move(self): 
        board = tilewe.Board(4) 

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.SOUTH, 
            contact=tilewe.A03, 
            to_square=tilewe.A20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.WEST, 
            contact=tilewe.A01, 
            to_square=tilewe.A01
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.NORTH_F, 
            contact=tilewe.A02, 
            to_square=tilewe.A20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.WEST_F, 
            contact=tilewe.B03, 
            to_square=tilewe.T20
        )))

        self.assertTrue(board.is_legal(tilewe.Move(
            piece=tilewe.O4, 
            rotation=tilewe.WEST_F, 
            contact=tilewe.B01, 
            to_square=tilewe.T01
        )))

    def test_unique_illegal_move(self): 
        board = tilewe.Board(4) 

        # contact is valid, but tiles would be placed off the board 
        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.NORTH, 
            contact=tilewe.A03, 
            to_square=tilewe.A01
        )))

        # contact is not valid 
        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.NORTH, 
            contact=tilewe.A01, 
            to_square=tilewe.A01
        )))

        # contact is invalid, and tiles would be placed off the board
        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.SOUTH, 
            contact=tilewe.C02, 
            to_square=tilewe.A20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=None, 
            rotation=tilewe.EAST, 
            contact=tilewe.B03, 
            to_square=tilewe.T20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=None, 
            contact=tilewe.B03, 
            to_square=tilewe.T20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.EAST, 
            contact=None, 
            to_square=tilewe.T20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.EAST, 
            contact=tilewe.B03, 
            to_square=None
        )))

    def test_nonunique_illegal_move(self): 
        board = tilewe.Board(4) 

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.Z5, 
            rotation=tilewe.SOUTH, 
            contact=tilewe.A03, 
            to_square=tilewe.A01
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.O4, 
            rotation=tilewe.WEST_F, 
            contact=tilewe.B01, 
            to_square=tilewe.T20
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.NORTH_F, 
            contact=tilewe.A02, 
            to_square=tilewe.A19
        )))

        self.assertFalse(board.is_legal(tilewe.Move(
            piece=tilewe.T4, 
            rotation=tilewe.WEST_F, 
            contact=tilewe.B02, 
            to_square=tilewe.T20
        )))

if __name__ == '__main__': 
    unittest.main() 
