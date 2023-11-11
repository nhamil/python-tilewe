import multiprocessing

import tilewe 
import tilewe.engine

tournament = tilewe.engine.Tournament([
    tilewe.engine.RandomEngine("Random 1"), 
    tilewe.engine.RandomEngine("Random 2"), 
    tilewe.engine.RandomEngine("Random 3"), 
    tilewe.engine.RandomEngine("Random 4")
])

tournament.play(1000, n_threads=multiprocessing.cpu_count(), move_seconds=15)
