from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize(
    'tilewe/__init__.pyx',
    'tilewe/elo.pyx',
    'tilewe/engine.pyx',
    'tilewe/tournament.pyx',
    'example_tournament.pyx',
    'example_game.pyx',
))