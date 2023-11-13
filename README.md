# Tilewe for Python

Tilewe (pronounced "tile we") is a multiplayer tile-placing game. Players take turns placing pieces onto empty tiles on the board such that the following are true: 

* No piece may be directly adjacent to another piece of the same color 
* Every piece must be placed diagonally from another piece of the same color

The player with the most tiles of their color at the end of the game wins. 

## Terminology

### Board 

The board is a 20x20 grid on which tiles can be placed. Coordinates are defined such that A1 (`tilewe.A01`) is in the bottom-left, T1 (`tilewe.T01`) is in the bottom-right, A20 (`tilewe.A20`) is in the top-left, and T20 (`tilewe.T20`) is in the top-right. 

**Note:** To prevent name collisions with piece names, tile coordinate constants always use two digits, even for rows 1-9. 

### Piece 

A piece is one of 23 objects made up of tiles that can be placed on the board. Each piece can be rotated and flipped before being placed. The default orientation of piece is shown below: 

```
O1   I2   I3   L3    O4    I4   L4    Z4      T4      I5   L5    N5    P5  
                                                                           
X    X    X    X .   X X   X    X .   X X .   X X X   X    X .   . X   X X 
     X    X    X X   X X   X    X .   . X X   . X .   X    X .   X X   X X 
          X                X    X X                   X    X .   X .   X . 
                           X                          X    X X   X .       
                                                      X                    
                                                                           
F5      Y5    T5      U5      V5      W5      X5      Z5                   
                                                                           
. X X   . X   X X X   X . X   . . X   . . X   . X .   X X .                
X X .   X X   . X .   X X X   . . X   . X X   X X X   . X .                
. X .   . X   . X .           X X X   X X .   . X .   . X X                
        . X                                                                
```

### Rotation

Pieces can be placed in any possible orientation. There are up to eight possible: 

* North (n): the default rotation 
* East (e): rotated clockwise 
* South (s): rotated 180 degrees 
* West (w): rotated counterclockwise
* North-flipped (nf): flipped horizontally 
* East-flipped (ef): rotated clockwise and then flipped horizontally 
* South-flipped (sf): rotated 180 degrees and then flipped horizontally  
* West-flipped (wf): rotated counterclockwise and then flipped horizontally 

Flipping vertically is also physically possible but is not explicitly supported in this library as it is equivalent to rotating 180 degrees and flipping horizontally.

For many pieces, there are some rotations that result in the same orientation. For example, W5 is equivalent from the north and east-flipped rotations: 

```
W5n     W5e     W5ef
. . X   X . .   . . X 
. X X   X X .   . X X
X X .   . X X   X X .
```

### Corner 

Corners are tiles on the board that diagonally touch a tile owned by a player. One of a player's tiles must be placed on an available corner. Corners are specified by their board coordinate. For example, if W5 is placed in the bottom-left corner of the board with its default rotation (north): 

```
  +---+---+---+---+
4 |   | o |   | o |
  +---+---+---+---+
3 | o |   | X |   |
  +---+---+---+---+
2 |   | X | X |   |
  +---+---+---+---+
1 | X | X |   | o |
  +---+---+---+---+
    a   b   c   d
```

The corners d1, b3, b4, and d4 become available to the player who played the piece. 

### Contact

A contact is a tile within a piece that has corners. When a piece is placed, one of that piece's contacts must be located at an open corner (d1, b3, b4, and d4 in the example) above. Contacts are specified relative to the piece's current rotation. For example, the contact at the bottom of: 

```

```

### Move

## Rules 



## Usage
