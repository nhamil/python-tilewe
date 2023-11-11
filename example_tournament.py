import multiprocessing

import tilewe 
import tilewe.engine

tournament = tilewe.engine.Tournament([
    tilewe.engine.LargestPieceEngine(), 
    tilewe.engine.MostOpenCornersEngine(), 
    tilewe.engine.MaximizeMoveDifferenceEngine(), 
    tilewe.engine.RandomEngine()
])

tournament.play(1000, n_threads=multiprocessing.cpu_count(), move_seconds=15)
