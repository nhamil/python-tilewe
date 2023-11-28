from setuptools import setup, find_packages, Extension

ext_modules = [
    Extension(
        name="ctilewe", 
        sources=[
            "tilewe/src/ctilewemodule.c", 
            "tilewe/src/tilewe/Source/Tilewe/Piece.c", 
            "tilewe/src/tilewe/Source/Tilewe/Tables.c"
        ], 
        include_dirs=[
            "tilewe/src/tilewe/Source", 
            "tilewe/src/tilewe/Source/Tilewe"
        ], 
        extra_compile_args=["-O3", "-funroll-loops"]
    )   
]

setup(
    name='tilewe', 
    version='0.0.3', 
    packages=find_packages(), 
    ext_modules=ext_modules
)
