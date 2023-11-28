import multiprocessing

import tilewe 
import tilewe.engine
import tilewe.tournament

def run_tournament():
    tournament = tilewe.tournament.Tournament([
        tilewe.engine.MoveDifferenceEngine(style="max"), 
        tilewe.engine.MoveDifferenceEngine(style="min"), 
        tilewe.engine.PieceSizeEngine(style="max"), 
        tilewe.engine.PieceSizeEngine(style="min"), 
        tilewe.engine.TileWeightEngine("WallCrawler", 'wall_crawl'),
        tilewe.engine.TileWeightEngine("Turtle", 'turtle'),
        tilewe.engine.OpenCornersEngine(style="max"), 
        tilewe.engine.OpenCornersEngine(style="min"), 
        tilewe.engine.RandomEngine("Random 1"),
        tilewe.engine.RandomEngine("Random 2"),
        tilewe.engine.RandomEngine("Random 3"),
    ])
    
    results = tournament.play(100, n_threads=multiprocessing.cpu_count(), move_seconds=1, elo_mode="estimated")

    # print the result of game 1
    # print(results.match_data[0].board)

    # print the total real time the tournament took and the average duration of each match, in seconds
    print(f"Tournament ran for {round(results.real_time, 4)}s with avg " + 
          f"match duration {round(results.average_match_duration, 4)}s\n")

    # print the engine rankings sorted by win_counts desc and then by elo_error_margin asc
    # print(results.get_engine_rankings_display('win_counts', 'desc'))
    # print(results.get_engine_rankings_display('elo_error_margin', 'asc'))

if __name__ == '__main__':
    run_tournament()
