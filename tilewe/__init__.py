import sys 

if sys.version_info[0] != 3 or sys.version_info[1] < 10:
    raise Exception("Requires Python 3.10+")

Tile = int
Piece = int 
Rotation = int 
Color = int

# game details related constant declarations
TILES = [
    A01, B01, C01, D01, E01, F01, G01, H01, I01, J01, K01, L01, M01, N01, O01, P01, Q01, R01, S01, T01, 
    A02, B02, C02, D02, E02, F02, G02, H02, I02, J02, K02, L02, M02, N02, O02, P02, Q02, R02, S02, T02, 
    A03, B03, C03, D03, E03, F03, G03, H03, I03, J03, K03, L03, M03, N03, O03, P03, Q03, R03, S03, T03, 
    A04, B04, C04, D04, E04, F04, G04, H04, I04, J04, K04, L04, M04, N04, O04, P04, Q04, R04, S04, T04, 
    A05, B05, C05, D05, E05, F05, G05, H05, I05, J05, K05, L05, M05, N05, O05, P05, Q05, R05, S05, T05, 
    A06, B06, C06, D06, E06, F06, G06, H06, I06, J06, K06, L06, M06, N06, O06, P06, Q06, R06, S06, T06, 
    A07, B07, C07, D07, E07, F07, G07, H07, I07, J07, K07, L07, M07, N07, O07, P07, Q07, R07, S07, T07, 
    A08, B08, C08, D08, E08, F08, G08, H08, I08, J08, K08, L08, M08, N08, O08, P08, Q08, R08, S08, T08, 
    A09, B09, C09, D09, E09, F09, G09, H09, I09, J09, K09, L09, M09, N09, O09, P09, Q09, R09, S09, T09, 
    A10, B10, C10, D10, E10, F10, G10, H10, I10, J10, K10, L10, M10, N10, O10, P10, Q10, R10, S10, T10, 
    A11, B11, C11, D11, E11, F11, G11, H11, I11, J11, K11, L11, M11, N11, O11, P11, Q11, R11, S11, T11, 
    A12, B12, C12, D12, E12, F12, G12, H12, I12, J12, K12, L12, M12, N12, O12, P12, Q12, R12, S12, T12, 
    A13, B13, C13, D13, E13, F13, G13, H13, I13, J13, K13, L13, M13, N13, O13, P13, Q13, R13, S13, T13, 
    A14, B14, C14, D14, E14, F14, G14, H14, I14, J14, K14, L14, M14, N14, O14, P14, Q14, R14, S14, T14, 
    A15, B15, C15, D15, E15, F15, G15, H15, I15, J15, K15, L15, M15, N15, O15, P15, Q15, R15, S15, T15, 
    A16, B16, C16, D16, E16, F16, G16, H16, I16, J16, K16, L16, M16, N16, O16, P16, Q16, R16, S16, T16, 
    A17, B17, C17, D17, E17, F17, G17, H17, I17, J17, K17, L17, M17, N17, O17, P17, Q17, R17, S17, T17, 
    A18, B18, C18, D18, E18, F18, G18, H18, I18, J18, K18, L18, M18, N18, O18, P18, Q18, R18, S18, T18, 
    A19, B19, C19, D19, E19, F19, G19, H19, I19, J19, K19, L19, M19, N19, O19, P19, Q19, R19, S19, T19, 
    A20, B20, C20, D20, E20, F20, G20, H20, I20, J20, K20, L20, M20, N20, O20, P20, Q20, R20, S20, T20
] = [
    Tile(i) for i in range(20 * 20)
]

TILE_COORDS = [
    (x, y) for y in range(20) for x in range(20)
]

TILE_NAMES = [
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1", "j1", "k1", "l1", "m1", "n1", "o1", "p1", "q1", "r1", "s1", "t1",                      # noqa: 501
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2", "j2", "k2", "l2", "m2", "n2", "o2", "p2", "q2", "r2", "s2", "t2",                      # noqa: 501
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3", "j3", "k3", "l3", "m3", "n3", "o3", "p3", "q3", "r3", "s3", "t3",                      # noqa: 501
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4", "j4", "k4", "l4", "m4", "n4", "o4", "p4", "q4", "r4", "s4", "t4",                      # noqa: 501
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5", "j5", "k5", "l5", "m5", "n5", "o5", "p5", "q5", "r5", "s5", "t5",                      # noqa: 501
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "i6", "j6", "k6", "l6", "m6", "n6", "o6", "p6", "q6", "r6", "s6", "t6",                      # noqa: 501
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "i7", "j7", "k7", "l7", "m7", "n7", "o7", "p7", "q7", "r7", "s7", "t7",                      # noqa: 501
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "i8", "j8", "k8", "l8", "m8", "n8", "o8", "p8", "q8", "r8", "s8", "t8",                      # noqa: 501
    "a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9", "j9", "k9", "l9", "m9", "n9", "o9", "p9", "q9", "r9", "s9", "t9",                      # noqa: 501
    "a10", "b10", "c10", "d10", "e10", "f10", "g10", "h10", "i10", "j10", "k10", "l10", "m10", "n10", "o10", "p10", "q10", "r10", "s10", "t10",  # noqa: 501
    "a11", "b11", "c11", "d11", "e11", "f11", "g11", "h11", "i11", "j11", "k11", "l11", "m11", "n11", "o11", "p11", "q11", "r11", "s11", "t11",  # noqa: 501
    "a12", "b12", "c12", "d12", "e12", "f12", "g12", "h12", "i12", "j12", "k12", "l12", "m12", "n12", "o12", "p12", "q12", "r12", "s12", "t12",  # noqa: 501
    "a13", "b13", "c13", "d13", "e13", "f13", "g13", "h13", "i13", "j13", "k13", "l13", "m13", "n13", "o13", "p13", "q13", "r13", "s13", "t13",  # noqa: 501
    "a14", "b14", "c14", "d14", "e14", "f14", "g14", "h14", "i14", "j14", "k14", "l14", "m14", "n14", "o14", "p14", "q14", "r14", "s14", "t14",  # noqa: 501
    "a15", "b15", "c15", "d15", "e15", "f15", "g15", "h15", "i15", "j15", "k15", "l15", "m15", "n15", "o15", "p15", "q15", "r15", "s15", "t15",  # noqa: 501
    "a16", "b16", "c16", "d16", "e16", "f16", "g16", "h16", "i16", "j16", "k16", "l16", "m16", "n16", "o16", "p16", "q16", "r16", "s16", "t16",  # noqa: 501
    "a17", "b17", "c17", "d17", "e17", "f17", "g17", "h17", "i17", "j17", "k17", "l17", "m17", "n17", "o17", "p17", "q17", "r17", "s17", "t17",  # noqa: 501
    "a18", "b18", "c18", "d18", "e18", "f18", "g18", "h18", "i18", "j18", "k18", "l18", "m18", "n18", "o18", "p18", "q18", "r18", "s18", "t18",  # noqa: 501
    "a19", "b19", "c19", "d19", "e19", "f19", "g19", "h19", "i19", "j19", "k19", "l19", "m19", "n19", "o19", "p19", "q19", "r19", "s19", "t19",  # noqa: 501
    "a20", "b20", "c20", "d20", "e20", "f20", "g20", "h20", "i20", "j20", "k20", "l20", "m20", "n20", "o20", "p20", "q20", "r20", "s20", "t20"   # noqa: 501
]

ROTATIONS = [
    NORTH, EAST, SOUTH, WEST, NORTH_F, EAST_F, SOUTH_F, WEST_F
] = [Rotation(x) for x in range(8)]

ROTATION_COUNT: int = len(ROTATIONS)

ROTATION_NAMES = [
    'n', 'e', 's', 'w', 'nf', 'ef', 'sf', 'wf'
]

COLORS = [
    BLUE, YELLOW, RED, GREEN
] = [Color(x) for x in range(4)]

NO_COLOR: Color = Color(len(COLORS))

COLOR_COUNT: int = len(COLORS) 

COLOR_NAMES = [
    'blue', 'yellow', 'red', 'green'
]

PIECES = [
    O1, I2, I3, L3, O4, I4, L4, 
    Z4, T4, F5, I5, L5, N5, P5, 
    T5, U5, V5, W5, X5, Y5, Z5, 
] = [Piece(x) for x in range(21)]

NO_PIECE: Piece = Piece(len(PIECES))

PIECE_COUNT: int = len(PIECES)

PIECE_NAMES = [
    "O1", "I2", "I3", "L3", "O4", "I4", "L4", 
    "Z4", "T4", "F5", "I5", "L5", "N5", "P5", 
    "T5", "U5", "V5", "W5", "X5", "Y5", "Z5", 
]

def tile_to_coords(tile: Tile) -> tuple[int, int]: 
    """Converts a valid tile to xy coordinates"""
    ...

def tile_in_bounds(tile: Tile) -> bool: 
    """Checks if a tile value is valid"""
    ...

def coords_to_tile(coords: tuple[int, int]) -> Tile: 
    """Converts valid xy coordinates to a tile"""
    ...

def coords_in_bounds(coords: tuple[int, int]) -> bool: 
    """Checks if xy coordinates are valid"""
    ...

def n_piece_tiles(piece: Piece) -> int: 
    """Returns number of tiles in a piece"""
    ...

def n_piece_contacts(piece: Piece) -> int: 
    """Returns number of contacts in a piece"""
    ...

def n_piece_corners(piece: Piece) -> int: 
    """Returns number of open corners a piece provides"""
    ...

def piece_tiles(piece: Piece, rotation: Rotation) -> list[Tile]: 
    """
    Returns piece tiles relative to a rotation, where A01 is the bottom-left
    coordinate of that rotations's bounding box
    """
    ...

def piece_contacts(piece: Piece, rotation: Rotation) -> list[Tile]: 
    """
    Returns piece contacts relative to a rotation, where A01 is the bottom-left
    coordinate of that rotations's bounding box
    """
    ...

class Move: 
    """Represents a board move"""

    def __init__(piece: Piece, rotation: Rotation, contact: Tile, to_tile: Tile): 
        """Creates a move"""
        ...

    @property 
    def piece(self) -> Piece: 
        """Piece used by the move"""
        ...

    @property
    def rotation(self) -> Rotation: 
        """Rotation used by the move"""
        ...

    @property
    def contact(self) -> Tile: 
        """Contact used by the move"""
        ...

    @property 
    def to_tile(self) -> Tile: 
        """Tile that the move's contact will be placed at"""
        ...

class Board: 
    """Represents a tilewe board"""

    def __init__(self, n_players: int=4): 
        """Creates a board"""
        ...

    @property 
    def ply(self) -> int: 
        """Current ply, where each move increments the ply"""
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
        """List of each player's score"""
        ...

    @property
    def winners(self) -> list[int]: 
        """List of current winners"""
        ...

    @property 
    def finished(self) -> bool: 
        """Whether the game is done"""
        ...

    def generate_legal_moves(self, for_player: Color=None) -> list[Move]: 
        """Generates moves"""
        ... 

    def push(self, move: Move) -> None: 
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

    def remaining_pieces(self, for_player: Color=None) -> list[Piece]: 
        """Gets a list of pieces remaining for a player"""
        ...

    def n_player_corners(self, for_player: Color=None) -> int: 
        """Gets total number of open corners for a player"""
        ...

    def player_corners(self, for_player: Color=None) -> list[Tile]: 
        """Gets a list of the open corners for a player"""
        ...

    def player_score(self, for_player: Color=None) -> int: 
        """Gets the score of a player"""
        ...
        
    def can_play(self, for_player: Color=None) -> bool: 
        """Whether a player has remaining moves"""
        ...

    def is_legal(self, move: Move, for_player: Color=None) -> bool: 
        """Whether a move is legal for a player"""
        ...

from ctilewe import *  # noqa: E402, F401, F403

N_PIECE_TILES:    list[int] = [n_piece_tiles(piece)    for piece in range(PIECE_COUNT)]  # noqa: E241, E272
N_PIECE_CORNERS:  list[int] = [n_piece_corners(piece)  for piece in range(PIECE_COUNT)]  # noqa: E241, E272
N_PIECE_CONTACTS: list[int] = [n_piece_contacts(piece) for piece in range(PIECE_COUNT)]  # noqa: E241, E272
