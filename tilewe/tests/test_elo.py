import unittest 

import tilewe
import tilewe.elo

class TestTilewe(unittest.TestCase): 
    
    def test_elo_win_rate(self): 
        # 50.00% win rate on matching elo
        self.assertEqual(tilewe.elo.elo_win_probability(1500, 1500), 0.5)

        # 64.01% win rate against 100 weaker enemy
        self.assertAlmostEqual(tilewe.elo.elo_win_probability(1500, 1400), 0.6401, 4)

        # 35.99% win rate against 100 stronger enemy
        self.assertAlmostEqual(tilewe.elo.elo_win_probability(1400, 1500), 0.3599, 4)
        
        # 94.68% win rate against 500 weaker enemy
        self.assertAlmostEqual(tilewe.elo.elo_win_probability(2000, 1500), 0.9468, 4)

        #  5.32% win rate against 500 stronger enemy
        self.assertAlmostEqual(tilewe.elo.elo_win_probability(1500, 2000), 0.0532, 4)

    def test_elo_rank_change(self):
        K = 32

        # loss against equally matched opponent gives -K/2 Elo
        self.assertEqual(tilewe.elo.compute_elo_adjustment_2(1500, 1500, 0, K), -16.0)
        
        # win against equally matched opponent gives +K/2 Elo
        self.assertEqual(tilewe.elo.compute_elo_adjustment_2(1500, 1500, 1, K), 16.0)

        # draw against equally matched opponent gives +/-0 Elo
        self.assertEqual(tilewe.elo.compute_elo_adjustment_2(1500, 1500, 0.5, K), 0.0)
        
        # loss against 100 stronger opponent gives -11.5179 Elo with K = 32
        self.assertAlmostEqual(tilewe.elo.compute_elo_adjustment_2(1500, 1600, 0, 32), -11.5179, 4)
        
        # win against 100 stronger opponent gives +20.4821 Elo with K = 32
        self.assertAlmostEqual(tilewe.elo.compute_elo_adjustment_2(1500, 1600, 1, 32), 20.4821, 4)

        # draw against 100 stronger opponent gives +4.4821 Elo with K = 32
        self.assertAlmostEqual(tilewe.elo.compute_elo_adjustment_2(1500, 1600, 0.5, 32), 4.4821, 4)
