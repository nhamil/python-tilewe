# Tilewe for Python

Tilewe (pronounced "tile we") is a multiplayer tile-placing game. Players take turns placing pieces onto empty tiles on the board such that the following are true: 

* No piece may be directly adjacent to another piece of the same color 
* Every piece must be placed diagonally from another piece of the same color

The player(s) with the most tiles of their color placed on the board at the end of the game win. The game ends when no players are able to make another move.

## Terminology

### Board 

The board is a 20x20 grid on which tiles can be placed. Coordinates are defined such that a1 (`tilewe.A01`) is in the bottom-left, t1 (`tilewe.T01`) is in the bottom-right, a20 (`tilewe.A20`) is in the top-left, and t20 (`tilewe.T20`) is in the top-right. 

**Note:** To prevent name collisions with piece names, tile coordinate constants always use two digits, even for rows 1-9. 

### Piece 

A piece is one of 21 objects made up of tiles that can be placed on the board. Each piece can be rotated and flipped before being placed. The default orientation of piece is shown below: 

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

You can get the number of tiles in a piece with: 

```
>>> tilewe.n_piece_tiles(tilewe.O1)
1
>>> tilewe.n_piece_tiles(tilewe.X5)
5
>>> board = tilewe.Board(n_players=4)
>>> move = board.generate_legal_moves()[0]
>>> tilewe.n_piece_tiles(move.piece)
(varies)
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

You can get the coordinates for the tiles in a piece rotation with: 

```
>>> tilewe.piece_tile_coords(tilewe.O1, tilewe.NORTH)
[(0, 0)]
>>> tilewe.piece_tile_coords(tilewe.X5, tilewe.WEST_F)
[(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
>>> board = tilewe.Board(n_players=4)
>>> move = board.generate_legal_moves()[0]
>>> tilewe.piece_tile_coords(move.piece)
(varies)
```

### Open Corner 

Open corners are unclaimed tiles on the board that diagonally touch a tile owned by a player. One of a player's tiles must be placed on an available corner. Open corners are specified by their board coordinate. For example, if W5 is placed in the bottom-left corner of the board with its default rotation (north): 

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

The corners d1, a3, b4, and d4 become available to the player who played the piece. 

You can get the number of corners for a piece with: 

```
>>> tilewe.n_piece_corners(tilewe.O1)
4
>>> tilewe.n_piece_corners(tilewe.X5)
8
>>> board = tilewe.Board(n_players=4)
>>> move = board.generate_legal_moves()[0]
>>> tilewe.n_piece_corners(move.piece)
(varies)
```

### Contact Tile

Contact tiles are a subset of tiles within a piece. A contact tile is a tile that either has less than 2 neighbors, or 2 neighbors that connect at a right angle (contact tiles are denoted as `C` and non-contact tiles as `X`): 

```
O1    I2     I3     I4     V5
C  |  C   |  C   |  C   |  . . C 
   |  C   |  X   |  X   |  . . X  
   |      |  C   |  X   |  C X C 
   |      |      |  C   |  
```

When a piece is placed, one of that piece's contact tiles must be located at an open corner (d1, a3, b4, and d4 in the example above). Contact tiles are specified relative to the piece's current rotation. For example, the contact tile at the bottom left of W5 (when there is a tile there) is always considered the a1 contact tile (denoted as `C`): 

```
W5n     W5ef    W5s 
. . X   . . X   . X X 
. X X   . X X   X X .   . . .
C X .   C X .   C . .
```

For another example, consider the V5 tile's contact tiles (all denoted as `C`): 

```
V5n     V5e     V5s     V5w     
. . C   C . .   C X C   C X C   
. . X   X . .   X . .   . . X   
C X C   C X C   C . .   . . C   
```

Regardless of where the V5 piece is placed on the board, its contact tiles for each rotation are: 

* North: a1, c1, c3
* East: a1, a3, c1
* South: a1, a3, a3
* West: a3, c1, c3

You can get the number of contact tiles for a piece with: 

```
>>> tilewe.n_piece_contacts(tilewe.O1)
1
>>> tilewe.n_piece_contacts(tilewe.X5)
4
>>> board = tilewe.Board(4)
>>> move = board.generate_legal_moves()[0]
>>> tilewe.n_piece_contacts(move.piece)
(varies)
```

### Move

Moves consist of a piece, a rotation, a contact tile, and an open corner. When a move is played, the move's piece will be placed on the board in the given rotation such that the contact tile is on the open corner. 

The notation for a move is as follows: `[Piece][Rotation]-[Contact Tile][Open Corner]`

The move `F5e-a2d4` would be played as follows: 

```
               Before                                     After              
                                                                             
  +---+---+---+---+---+---+---+---+         +---+---+---+---+---+---+---+---+
8 |   |   |   |   |   |   |   |   |       8 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+         +---+---+---+---+---+---+---+---+
7 |   |   |   |   |   |   |   |   |       7 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+         +---+---+---+---+---+---+---+---+
6 |   |   |   |   |   |   |   |   |       6 |   |   |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+         +---+---+---+---+---+---+---+---+
5 |   |   |   |   |   |   |   |   |       5 |   |   |   |   | X |   |   |   |
  +---+---+---+---+---+---+---+---+  -->    +---+---+---+---+---+---+---+---+
4 |   |   |   |   |   |   |   |   |       4 |   |   |   | C | X | X |   |   |
  +---+---+---+---+---+---+---+---+         +---+---+---+---+---+---+---+---+
3 |   |   | X |   |   |   |   |   |       3 |   |   | X |   |   | X |   |   |
  +---+---+---+---+---+---+---+---+         +---+---+---+---+---+---+---+---+
2 |   | X | X |   |   |   |   |   |       2 |   | X | X |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+         +---+---+---+---+---+---+---+---+
1 | X | X |   |   |   |   |   |   |       1 | X | X |   |   |   |   |   |   |
  +---+---+---+---+---+---+---+---+         +---+---+---+---+---+---+---+---+
    a   b   c   d   e   f   g   h             a   b   c   d   e   f   g   h   
```

Where: 

* The newly-placed piece is F5
* The rotation is East (clockwise from default: see Rotation section)
* The contact tile is a2 (`C`: the middle left tile of the rotated F5 piece)
* The open corner is d4 (the board coordinate where the contact tile is placed)
    * This coordinate is open due to the W5 piece that was placed previously

You can get moves from a board: 

```
>>> import random
>>> board = tilewe.Board(n_players=4) 
>>> moves = board.generate_legal_moves()
>>> moves
(list of Moves for the current player)
>>> move = random.choice(moves) # select a random move 
>>> move.piece # piece constant
(varies) 
>>> move.rotation # rotation constant
(varies) 
>>> move.contact # tile constant (contact tile)
(varies) 
>>> move.to_tile # tile constant (open corner)
(varies)
>>> board.push(move) # make a move
>>> board.pop() # undo the last played move 
>>> board.generate_legal_moves(for_player=tilewe.GREEN)
(list of Moves that green could play as if it were their turn)
```

You can also construct your own moves: 

```
>>> board = tilewe.Board(n_players=4)
>>> move = tilewe.Move(
...     piece=tilewe.W5, 
...     rotation=tilewe.NORTH, 
...     contact=tilewe.A01, 
...     to_tile=tilewe.A01
... )
>>> if board.is_legal(move): 
...     board.push(move)
...     print(f"{move} is legal")
... else: 
...     print(f"{move} is illegal")
...
W5n-a1a1 is legal
```

## Other Rules 

When a player has no pieces on the board, they may play in any of the corners of the board (a1, a20, t1, t20) as long as the corner is unclaimed.

Players that can no longer make any moves are skipped. (`tilewe.Board.ply` is not incremented for skipped players)

## Other Properties and Methods

Get the ply (how many moves have been made): `board.ply`

Get the current player to move: `board.current_player`

Check if the game is done: `board.finished`

Get the winners of the game: `board.winners`

Get the number of remaining pieces a player has: `board.n_remaining_pieces(player)`

Get a list of remaining pieces a player has: `board.remaining_pieces(player)`

Get the number of open corners a player has: `board.n_player_corners(player)`

Get a list of open corners a player has: `board.player_corners(player)`

Whether or not a player can still play: `board.can_play(player)`

Get the color of a tile: `board.color_at(tile)`
