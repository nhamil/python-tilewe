import tilewe 
import tilewe.engine 

tournament = tilewe.engine.Tournament([
    tilewe.engine.RandomEngine("Random 1"), 
    tilewe.engine.RandomEngine("Random 2"), 
    tilewe.engine.RandomEngine("Random 3"), 
    tilewe.engine.RandomEngine("Random 4")
])

tournament.play(100)
