import unittest 

import tilewe

class TestTilewe(unittest.TestCase): 
    
    def test_tile_tuple_conversion(self): 
        for tile in tilewe.TILES: 
            self.assertEqual(tile, tilewe.coords_to_tile(tilewe.tile_to_coords(tile))) 
