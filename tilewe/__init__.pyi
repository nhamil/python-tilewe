import tilewe 

Tile = int
Piece = int 
Rotation = int 
Color = int
Move = int

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
