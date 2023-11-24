import multiprocessing

import tilewe 
import tilewe.engine
import tilewe.tournament

def run_tournament():
    tournament = tilewe.tournament.Tournament([
        tilewe.engine.MoveDifferenceEngine("MaxMoveDiff", "max"), 
        tilewe.engine.MoveDifferenceEngine("MinMoveDiff", "min"), 
        tilewe.engine.PieceSizeEngine("LargestPiece", "max"), 
        tilewe.engine.PieceSizeEngine("SmallestPiece", "min"), 
        tilewe.engine.TileWeightEngine("WallCrawler", 'wall_crawl'),
        tilewe.engine.TileWeightEngine("Turtle", 'turtle'),
        tilewe.engine.OpenCornersEngine("MostOpenCorners", "max"), 
        tilewe.engine.OpenCornersEngine("LeastOpenCorners", "min"), 
        tilewe.engine.RandomEngine(),
    ])

    results = tournament.play(5000, n_threads=multiprocessing.cpu_count(), move_seconds=15)

    # print the result of game 1
    print(results.match_data[0].board)

    # print the total real time the tournament took and the average duration of each match, in seconds
    print(f"Tournament ran for {round(results.real_time, 4)}s with avg " + 
          f"match duration {round(results.average_match_duration, 4)}s\n")

    # print the engine rankings sorted by win_counts desc and then by elo_error_margin desc
    print(results.get_engine_rankings_display('win_counts', 'desc'))
    print(results.get_engine_rankings_display('elo_error_margin', 'desc'))

if __name__ == '__main__':
    run_tournament()
