import tilewe 

Tile = int
Piece = int 
Rotation = int 
Color = int
Move = int

TILES: list[Tile] 
PIECES: list[Piece] 
ROTATIONS: list[Rotation] 
COLOR: list[Color] 

NO_PIECES: Piece 
NO_COLOR: Color 

TILE_NAMES: list[str] 
PIECE_NAMES: list[str] 
ROTATION_NAMES: list[str] 
COLOR_NAMES: list[str] 

class Board: 

    def __init__(self, n_players: int=4): 
        ...

    def __str__(self) -> str: 
        ...

    @property 
    def ply(self) -> int: 
        ...

    @property 
    def current_player(self) -> Color: 
        """Color of the current player"""
        ...

    @property 
    def cur_player(self) -> Color: 
        """Color of the current player"""
        ...

    @property
    def n_players(self) -> int: 
        """Number of players"""
        ...

    @property 
    def scores(self) -> list[int]: 
        ...

    @property
    def winners(self) -> list[int]: 
        ...

    @property 
    def finished(self) -> bool: 
        """Whether the game is done"""
        ...

    def generate_legal_moves(self, for_player: tilewe.Color=None) -> list[tilewe.Move]: 
        """Generates moves"""
        ... 

    def push(self, move: tilewe.Move) -> None: 
        """Play a move"""
        ...

    def pop(self) -> None: 
        """Undo a move"""
        ...

    def n_legal_moves(self, for_player: Color=None) -> int: 
        """Gets total number of legal moves for a player"""
        ...

    def n_remaining_pieces(self, for_player: Color=None) -> int: 
        """Gets total number of pieces remaining for a player"""
        ...

    def remaining_pieces(self, for_player: Color=None) -> list[tilewe.Piece]: 
        """Gets a list of pieces remaining for a player"""
        ...

    def n_player_corners(self, for_player: Color=None) -> int: 
        """Gets total number of open corners for a player"""
        ...

    def player_corners(self, for_player: Color=None) -> list[tilewe.Tile]: 
        """Gets a list of the open corners for a player"""
        ...

    def player_score(self, for_player: Color=None) -> int: 
        """Gets the score of a player"""
        ...
        
    def can_play(self, for_player: Color=None) -> bool: 
        """Whether a player has remaining moves"""
        ...

    def is_legal(self, move: tilewe.Move, for_player: Color=None) -> bool: 
        """Whether a move is legal for a player"""
        ...
