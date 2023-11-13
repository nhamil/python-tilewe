import multiprocessing

import tilewe 
import tilewe.engine
import tilewe.tournament

def start():
    tournament = tilewe.tournament.Tournament([
        tilewe.engine.LargestPieceEngine(), 
        tilewe.engine.MostOpenCornersEngine(), 
        tilewe.engine.MaximizeMoveDifferenceEngine(), 
        tilewe.engine.WallCrawlerEngine(),
        tilewe.engine.RandomEngine()
    ])

    tournament.play(1000, n_threads=multiprocessing.cpu_count(), move_seconds=15)
