import pyximport
pyximport.install(setup_args={"script_args" : ["--verbose"]})

import example_tournament
import os
import sys

sys.path.insert(0, os.path.abspath("."))

example_tournament.start()