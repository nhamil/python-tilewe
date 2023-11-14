import multiprocessing

import tilewe 
import tilewe.engine
import tilewe.tournament

tournament = tilewe.tournament.Tournament([
    tilewe.engine.LargestPieceEngine(), 
    tilewe.engine.MostOpenCornersEngine(), 
    tilewe.engine.MaximizeMoveDifferenceEngine(), 
    tilewe.engine.WallCrawlerEngine(),
    tilewe.engine.RandomEngine()
])

results = tournament.play(10, n_threads=multiprocessing.cpu_count(), move_seconds=15)

# print the result of game 1
print(results.match_data[0].board)

# print the total real time the tournament took and the average duration of each match, in seconds
print(f"Tournament ran for {round(results.real_time, 4)}s with avg match duration {round(results.get_average_match_duration(), 4)}s")

