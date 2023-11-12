from collections import defaultdict

import numpy as np 

print_color = True 

Tile = tuple[int, int] 

Piece = int 

Rotation = int 

Color = int

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
    Tile((y, x)) for y in range(20) for x in range(20)
]

TILE_NAMES = [
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1", "j1", "k1", "l1", "m1", "n1", "o1", "p1", "q1", "r1", "s1", "t1", 
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2", "j2", "k2", "l2", "m2", "n2", "o2", "p2", "q2", "r2", "s2", "t2", 
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3", "j3", "k3", "l3", "m3", "n3", "o3", "p3", "q3", "r3", "s3", "t3", 
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4", "j4", "k4", "l4", "m4", "n4", "o4", "p4", "q4", "r4", "s4", "t4", 
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5", "j5", "k5", "l5", "m5", "n5", "o5", "p5", "q5", "r5", "s5", "t5", 
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "i6", "j6", "k6", "l6", "m6", "n6", "o6", "p6", "q6", "r6", "s6", "t6", 
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "i7", "j7", "k7", "l7", "m7", "n7", "o7", "p7", "q7", "r7", "s7", "t7", 
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "i8", "j8", "k8", "l8", "m8", "n8", "o8", "p8", "q8", "r8", "s8", "t8", 
    "a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9", "j9", "k9", "l9", "m9", "n9", "o9", "p9", "q9", "r9", "s9", "t9", 
    "a10", "b10", "c10", "d10", "e10", "f10", "g10", "h10", "i10", "j10", "k10", "l10", "m10", "n10", "o10", "p10", "q10", "r10", "s10", "t10", 
    "a11", "b11", "c11", "d11", "e11", "f11", "g11", "h11", "i11", "j11", "k11", "l11", "m11", "n11", "o11", "p11", "q11", "r11", "s11", "t11", 
    "a12", "b12", "c12", "d12", "e12", "f12", "g12", "h12", "i12", "j12", "k12", "l12", "m12", "n12", "o12", "p12", "q12", "r12", "s12", "t12", 
    "a13", "b13", "c13", "d13", "e13", "f13", "g13", "h13", "i13", "j13", "k13", "l13", "m13", "n13", "o13", "p13", "q13", "r13", "s13", "t13", 
    "a14", "b14", "c14", "d14", "e14", "f14", "g14", "h14", "i14", "j14", "k14", "l14", "m14", "n14", "o14", "p14", "q14", "r14", "s14", "t14", 
    "a15", "b15", "c15", "d15", "e15", "f15", "g15", "h15", "i15", "j15", "k15", "l15", "m15", "n15", "o15", "p15", "q15", "r15", "s15", "t15", 
    "a16", "b16", "c16", "d16", "e16", "f16", "g16", "h16", "i16", "j16", "k16", "l16", "m16", "n16", "o16", "p16", "q16", "r16", "s16", "t16", 
    "a17", "b17", "c17", "d17", "e17", "f17", "g17", "h17", "i17", "j17", "k17", "l17", "m17", "n17", "o17", "p17", "q17", "r17", "s17", "t17", 
    "a18", "b18", "c18", "d18", "e18", "f18", "g18", "h18", "i18", "j18", "k18", "l18", "m18", "n18", "o18", "p18", "q18", "r18", "s18", "t18", 
    "a19", "b19", "c19", "d19", "e19", "f19", "g19", "h19", "i19", "j19", "k19", "l19", "m19", "n19", "o19", "p19", "q19", "r19", "s19", "t19", 
    "a20", "b20", "c20", "d20", "e20", "f20", "g20", "h20", "i20", "j20", "k20", "l20", "m20", "n20", "o20", "p20", "q20", "r20", "s20", "t20"
]

ROTATIONS = [
    NORTH, EAST, SOUTH, WEST, NORTH_F, EAST_F, SOUTH_F, WEST_F
] = [Rotation(x) for x in range(8)]

ROTATION_NAMES = [
    'n', 'e', 's', 'w', 'nf', 'ef', 'sf', 'wf'
]

COLORS = [
    BLUE, YELLOW, RED, GREEN
] = [Color(x) for x in range(4)]

NO_COLOR = -1 # type: Color 

COLOR_NAMES = [
    'blue', 'yellow', 'red', 'green'
]

# internally int, so copies value not reference 
_PrpSet = int

PIECE_COUNT = 0
_PIECES = [] # type: list[_Piece]
_PIECE_ROTATIONS = [] # type: list[_PieceRotation]
_PIECE_ROTATION_POINTS = [] # type: list[_PieceRotationPoint]
_PRP_SET_ALL = 0 # type: _PrpSet

class _Piece: 

    def __init__(self, name: str, id: int): 
        self.name = name 
        self.id = id 
        self.rotations = [] # type: list[_PieceRotation]
        self.unique = [] # type: list[bool]
        self.true_rot = [] # type: list[Rotation]
        self.true_rot_for = [] # type: list[list[Rotation]]

class _PieceRotation: 

    def __init__(self, name: str, pc: _Piece, rot: Rotation, shape: np.ndarray): 
        self.id = len(_PIECE_ROTATIONS)
        self.piece = pc
        self.rotation = rot 
        _PIECE_ROTATIONS.append(self) 

        self.name = name 
        self.shape = np.array(shape, dtype=np.uint8) 

        self.tiles = [] # type: list[Tile]
        self.contacts = [] # type: list[Tile]
        self.prps = {} # type: dict[Tile, _PieceRotationPoint]
        self.n_corners = 0

        self.contact_shape = np.zeros_like(shape, dtype=np.uint8)
        H,W = shape.shape
        for y in range(H): 
            for x in range(W): 
                # check each tile in piece 
                if shape[y,x] != 0: 
                    self.tiles.append((y, x))
                    v_neighbors = 0
                    h_neighbors = 0

                    if y > 0   and shape[y-1,x] != 0: v_neighbors += 1
                    if y < H-1 and shape[y+1,x] != 0: v_neighbors += 1
                    if x > 0   and shape[y,x-1] != 0: h_neighbors += 1
                    if x < W-1 and shape[y,x+1] != 0: h_neighbors += 1

                    n_neighbors = v_neighbors + h_neighbors

                    if (n_neighbors <= 1) or (v_neighbors == 1 and h_neighbors == 1): 
                        self.contacts.append((y, x))
                        self.contact_shape[y, x] = 1

        for coord in self.contacts: 
            self.prps[coord] = _PieceRotationPoint(name, self, coord) 
        
        self.n_corners = len(list(self.prps.values())[0].corners)

class _PieceRotationPoint: 

    def __init__(self, name: str, rot: _PieceRotation, pt: Tile): 
        self.id = len(_PIECE_ROTATION_POINTS)
        self.as_set = 1 << self.id 
        global _PRP_SET_ALL
        _PRP_SET_ALL |= self.as_set
        self.piece = rot.piece 
        self.rotation = rot 
        self.piece_id = self.piece.id 
        self.name = name 
        self.contact = pt 
        _PIECE_ROTATION_POINTS.append(self) 

        dy, dx = pt 
        
        self.tiles = [] # type: list[Tile]
        self.adjacent = set() # type: list[Tile]
        self.corners = set() # type: list[Tile]

        for y, x in rot.tiles: 
            self.tiles.append((y - dy, x - dx))

        for y, x in self.tiles: 
            for cy, cx in [(-1, 0), (1, 0), (0, -1), (0, 1)]: 
                rel = (y + cy, x + cx)
                if rel not in self.tiles: 
                    self.adjacent.add(rel) 

        for y, x in self.tiles: 
            for cy, cx in [(-1, -1), (1, -1), (-1, 1), (1, 1)]: 
                rel = (y + cy, x + cx)
                if rel not in self.tiles and rel not in self.adjacent: 
                    self.corners.add(rel) 
            
        self.adjacent = sorted(list(self.adjacent))
        self.corners = sorted(list(self.corners))

def _create_piece(name: str, shape: list[list[int]]) -> Piece: 
    global PIECE_COUNT 
    id = PIECE_COUNT 
    PIECE_COUNT += 1 
    pc = _Piece(name, id) 
    _PIECES.append(pc) 

    f_names = []
    def add(suffix: str, arr: np.ndarray): 
        rot = None 
        unique = True 
        true_rot = len(pc.rotations) # assume rotation is unique 

        for x in pc.rotations: 
            if x.shape.shape == arr.shape and np.all(x.shape == arr): 
                rot = x 
                unique = False 
                true_rot = x.rotation
                break 

        if rot is None: 
            rot = _PieceRotation(name + suffix, pc, len(pc.rotations), arr)

        f_names.append(suffix + "f")
        pc.rotations.append(rot) 
        pc.unique.append(unique) 
        pc.true_rot.append(true_rot) 
        pc.true_rot_for.append([]) 
        pc.true_rot_for[true_rot].append(rot.rotation)

    # original shape, north
    cur = np.array(shape, dtype=np.uint8)[::-1] 
    add("n", cur) 

    # east
    cur = np.rot90(cur, 1) 
    add("e", cur)

    # south
    cur = np.rot90(cur, 1) 
    add("s", cur)

    # west
    cur = np.rot90(cur, 1) 
    add("w", cur)

    # flipped 
    n_unflipped = len(pc.rotations) 
    for i in range(n_unflipped): 
        add(f_names[i], np.fliplr(pc.rotations[i].shape)) 
        
    return id 

O1 = _create_piece("O1", [
    [1]
]) 

I2 = _create_piece("I2", [
    [1], 
    [1]
])

I3 = _create_piece("I3", [
    [1],
    [1],
    [1]
])
L3 = _create_piece("L3", [
    [1, 0], 
    [1, 1]
])

I4 = _create_piece("I4", [
    [1], 
    [1], 
    [1], 
    [1]
])
L4 = _create_piece("L4", [
    [1, 0], 
    [1, 0], 
    [1, 1]
])
Z4 = _create_piece("Z4", [
    [1, 1, 0], 
    [0, 1, 1]
])
O4 = _create_piece("O4", [
    [1, 1], 
    [1, 1]
])
T4 = _create_piece("T4", [
    [1, 1, 1], 
    [0, 1, 0]
])

F5 = _create_piece("F5", [
    [0, 1, 1], 
    [1, 1, 0], 
    [0, 1, 0]
])
I5 = _create_piece("I5", [
    [1], 
    [1], 
    [1], 
    [1], 
    [1]
])
L5 = _create_piece("L5", [
    [1, 0], 
    [1, 0], 
    [1, 0], 
    [1, 1]
])
N5 = _create_piece("N5", [
    [0, 1], 
    [1, 1], 
    [1, 0], 
    [1, 0]
])
P5 = _create_piece("P5", [
    [1, 1], 
    [1, 1], 
    [1, 0]
])
T5 = _create_piece("T5", [
    [1, 1, 1], 
    [0, 1, 0], 
    [0, 1, 0]
])
U5 = _create_piece("U5", [
    [1, 0, 1], 
    [1, 1, 1]
])
V5 = _create_piece("V5", [
    [0, 0, 1], 
    [0, 0, 1], 
    [1, 1, 1]
])
W5 = _create_piece("W5", [
    [0, 0, 1], 
    [0, 1, 1], 
    [1, 1, 0]
])
X5 = _create_piece("X5", [
    [0, 1, 0], 
    [1, 1, 1], 
    [0, 1, 0]
])
Y5 = _create_piece("Y5", [
    [0, 1], 
    [1, 1], 
    [0, 1], 
    [0, 1]
])
Z5 = _create_piece("Z5", [
    [1, 1, 0], 
    [0, 1, 0], 
    [0, 1, 1]
])

_PRP_WITH_REL_COORD = defaultdict(_PrpSet) # type: dict[Tile, _PrpSet]
for _pt in _PIECE_ROTATION_POINTS: 
    for _tile in _pt.tiles: 
        _PRP_WITH_REL_COORD[_tile] |= _pt.as_set

_PRP_WITH_ADJ_REL_COORD = defaultdict(_PrpSet) # type: dict[Tile, _PrpSet]
for _pt in _PIECE_ROTATION_POINTS: 
    for _tile in _pt.adjacent: 
        _PRP_WITH_ADJ_REL_COORD[_tile] |= _pt.as_set

_PRP_REL_COORDS = set() # type: list[Tile]
for _pt in _PRP_WITH_REL_COORD:
    _PRP_REL_COORDS.add(_pt)
for _pt in _PRP_WITH_ADJ_REL_COORD:
    _PRP_REL_COORDS.add(_pt)
_PRP_REL_COORDS = list(_PRP_REL_COORDS)

_PRP_WITH_PC_ID = defaultdict(_PrpSet) # type: dict[int, _PrpSet]
for _pt in _PIECE_ROTATION_POINTS: 
    _PRP_WITH_PC_ID[_pt.piece_id] |= _pt.as_set

def out_of_bounds(tile: Tile) -> bool: 
    if tile[0] < 0 or tile[0] >= 20: 
        return True 
    if tile[1] < 0 or tile[1] >= 20: 
        return True 
    return False

class _PlayerState: 

    def __init__(self, prps: _PrpSet, corners: dict[Tile, _PrpSet], has_played: bool, score: int): 
        self.prps = prps 
        self.corners = corners 
        self.has_played = has_played 
        self.score = score

    def copy(self) -> '_PlayerState': 
        out = _PlayerState.__new__(_PlayerState) 
        out.prps = self.prps 
        out.corners = dict(self.corners)
        out.has_played = self.has_played 
        out.score = self.score 

        return out 

class _Player: 

    def __init__(self, name: str, id: Color, board: 'Board'): 
        self.name = name 
        self.id = id
        self._prps = _PRP_SET_ALL
        self.board = board 
        self.corners = {} # type: dict[Tile, _PrpSet]
        self.has_played = False 
        self.score = 0
        self._state = [] # type: list[_PlayerState]

        self.add_corner(A01) 
        self.add_corner(A20) 
        self.add_corner(T01) 
        self.add_corner(T20) 

    def copy_current_state(self, board: 'Board') -> '_Player': 
        out = _Player.__new__(_Player) 
        out.name = self.name 
        out.id = self.id 
        out._prps = self._prps 
        out.board = board 
        out.corners = dict(self.corners)
        out.has_played = self.has_played 
        out.score = self.score
        out._state = [] 

        return out 

    @property 
    def can_play(self) -> bool: 
        return len(self.corners) > 0 

    def push_state(self) -> None: 
        prps = self._prps 
        corners = dict(self.corners) 

        self._state.append(_PlayerState(prps, corners, self.has_played, self.score))

    def pop_state(self) -> bool: 
        state = self._state.pop() 

        self._prps = state.prps 
        self.corners = state.corners 
        self.has_played = state.has_played
        self.score = state.score 

    def remove_piece(self, piece_id: int) -> None: 
        # remove piece permutations from availability list 
        prps = _PRP_WITH_PC_ID[piece_id]
        self._prps &= ~prps

        remove = [] 

        # remove piece permutations from all open corners 
        for key, corner in self.corners.items(): 
            corner &= ~prps 
            if corner == 0: 
                remove.append(key)
            else: 
                # corner is value, not reference 
                self.corners[key] = corner 

        for r in remove: 
            del self.corners[r]

    def on_tiles_filled(self, tiles: list[Tile]) -> None: 
        # if an open corner was filled, no player can use it anymore
        for tile in tiles: 
            self.corners.pop(tile, None) 

        remove = []

        # for each open corner, 
        #     find all piece permutations that need one of the filled tiles
        #     and remove them from possible moves 
        for corner, prps in self.corners.items(): 
            invalid = 0 # type: _PrpSet
            for tile in tiles: 
                rel = (tile[0] - corner[0], tile[1] - corner[1]) 
                invalid |= _PRP_WITH_REL_COORD[rel]
            prps &= ~invalid 
            if prps == 0: 
                remove.append(corner) 
            else: 
                self.corners[corner] = prps

        for r in remove: 
            del self.corners[r]

    def add_corner(self, tile: Tile) -> None:
        if tile in self.corners or out_of_bounds(tile):
            return

        bad = 0 # type: _PrpSet

        for rel in _PRP_REL_COORDS: 
            pt = (rel[0] + tile[0], rel[1] + tile[1])
            if out_of_bounds(pt) or self.board._tiles[pt] != 0:
                bad |= _PRP_WITH_REL_COORD[rel]
            if not out_of_bounds(pt) and self.board._tiles[pt] == self.id + 1:
                bad |= _PRP_WITH_ADJ_REL_COORD[rel]

        prps = self._prps & ~bad
        if prps > 0:
            self.corners[tile] = prps

def n_piece_contacts(piece: Piece) -> int: 
    return len(_PIECES[piece].rotations[0].contacts)

def n_piece_tiles(piece: Piece) -> int: 
    return len(_PIECES[piece].rotations[0].tiles)

def n_piece_corners(piece: Piece) -> int: 
    return _PIECES[piece].rotations[0].n_corners

def piece_tiles(piece: Piece, rotation: Rotation, contact: Tile=None) -> list[Tile]: 
    if contact is None: 
        return list(_PIECES[piece].rotations[rotation].tiles)
    else: 
        return list(_PIECES[piece].rotations[rotation].prps[contact].tiles)

class Move: 

    def __init__(self, piece: Piece, rotation: Rotation, contact: Tile, to_square: Tile): 
        self.piece = piece 
        self.rotation = rotation 
        self.contact = contact 
        self.to_square = to_square 

    def __str__(self): 
        return _PIECES[self.piece].name + \
               ROTATION_NAMES[self.rotation] + \
               "-" + \
               TILE_NAMES[TILES.index(self.contact)] + \
               TILE_NAMES[TILES.index(self.to_square)]
    
    def is_equal(self, value: 'Move') -> bool: 
        return \
            self.piece == value.piece and \
            self.rotation == value.rotation and \
            self.contact == value.contact and \
            self.to_square == value.to_square 

    def __eq__(self, value: object) -> bool:
        if type(value) == Move: 
            return self.is_equal(value) 
        else: 
            return False 

class _BoardState: 

    def __init__(self, cur_player: int, tiles: list[Tile]): 
        self.cur_player = cur_player
        self.tiles = tiles 

class Board: 

    def __init__(self, n_players: int): 
        if n_players < 1 or n_players > 4: 
            raise Exception("Number of players must be between 1 and 4") 

        self._state = [] # type: list[_BoardState]
        self._tiles = np.zeros((20, 20), dtype=np.uint8) 
        self._n_players = n_players 
        self._players = [] # type: list[_Player]

        chars = [
            'B', 
            'Y', 
            'R', 
            'G'
        ]
        for i in range(n_players): 
            self._players.append(_Player(chars[i], i, self))

        self.current_player = BLUE # type: Color 
        self.finished = False 
        self.ply = 0 
        self.moves = [] # type: list[Move]

    def copy_current_state(self) -> 'Board': 
        out = Board.__new__(Board) 
        out._state = [] 
        out._tiles = np.copy(self._tiles)
        out._n_players = self._n_players 
        out._players = [p.copy_current_state(out) for p in self._players]
        out.current_player = self.current_player
        out.finished = self.finished 
        out.ply = self.ply 
        out.moves = [] 

        return out 

    @property
    def n_players(self) -> int: 
        return self._n_players 

    @property 
    def scores(self) -> list[int]: 
        return [p.score for p in self._players] 

    @property
    def winners(self) -> list[int]: 
        if not self.finished: 
            return None 
        
        best = [0]
        for i in range(1, len(self._players)): 
            if self._players[i].score == self._players[best[0]].score: 
                best.append(i)
            elif self._players[i].score > self._players[best[0]].score: 
                best = [i]
        return best 

    def player_corners(self, player: Color) -> list[Tile]: 
        return list(self._players[player].corners.keys())

    def n_player_corners(self, player: Color) -> int: 
        return len(self._players[player].corners)

    def player_score(self, player: Color) -> int: 
        return self._players[player].score 

    def can_play(self, player: Color) -> bool: 
        return self._players[player].can_play 
    
    def _remaining_piece_set(self, player: Color) -> set[Piece]: 
        pieces = set() 
        prps = self._players[player]._prps 

        while prps != 0: 
            # get least significant bit
            prp = (prps & -prps).bit_length() - 1
            # remove it so the next LSB is another PRP
            prps ^= 1 << prp

            pieces.add(_PIECE_ROTATION_POINTS[prp].piece_id)

        return pieces

    def remaining_pieces(self, player: Color) -> list[Piece]: 
        return list(self._remaining_piece_set(player))
    
    def n_remaining_pieces(self, player: Color) -> int: 
        return len(self._remaining_piece_set(player))
    
    def color_at(self, tile: Tile) -> Color: 
        return Color(self._tiles[tile] - 1)

    def _is_legal(self, prp_id: int, tile: Tile, player: Color=None) -> bool: 
        if player is None: 
            player = self.current_player 

        player = self._players[player] # type: _Player

        prps = player.corners.get(tile, 0) # type: _PrpSet
        return (prps & (1 << prp_id)) != 0

    def is_legal(self, move: Move, for_player: Color=None) -> bool: 
        player = self._players[self.current_player if for_player is None else for_player]

        # target tile must be empty 
        if move.to_square is None or self.color_at(move.to_square) != NO_COLOR: 
            return False 
        
        # piece must be real
        if move.piece is None or move.piece >= len(_PIECES) or move.piece < 0: 
            return False 
        pc = _PIECES[move.piece]

        # rotation must be real 
        if move.rotation is None or move.rotation >= len(ROTATIONS) or move.rotation < 0: 
            return False 
        pc_rot = pc.rotations[move.rotation] 

        # piece rotation must have the contact
        prp = pc_rot.prps.get(move.contact, None)
        if prp is None: 
            return False 

        # available permutations at the requested tile
        prps = player.corners.get(move.to_square, None)
        if prps is None: 
            return False 

        # permutation must fit at the corner square
        return (prps & prp.as_set) != 0

    def n_legal_moves(self, unique: bool=False, for_player: Color=None): 
        if not unique: 
            raise Exception("Non-unique rotations not supported yet") 
        
        player = self._players[self.current_player if for_player is None else for_player]
        total = 0 

        for prps in player.corners.values(): 
            total += prps.bit_count() 

        return total 

    def generate_legal_moves(self, unique: bool=False, for_player: Color=None): 
        if not unique: 
            raise Exception("Non-unique rotations not supported yet") 
        
        moves = [] # type: list[Move] 

        player = self._players[self.current_player if for_player is None else for_player]

        for to_sq, prps in player.corners.items(): 
            while prps != 0: 
                # get least significant bit
                prp_id = (prps & -prps).bit_length() - 1
                # remove it so the next LSB is another PRP
                prps ^= 1 << prp_id

                prp = _PIECE_ROTATION_POINTS[prp_id]

                moves.append(Move(
                    prp.piece.id, 
                    prp.rotation.rotation, 
                    prp.contact, 
                    to_sq
                ))
                
        return moves 

    def push(self, move: Move) -> None: 
        """
        Legality is assumed to be true. 
        """
        prp = _PIECES[move.piece].rotations[move.rotation].prps[move.contact]
        self._push_prp(move, prp, move.to_square) 

    def pop(self) -> None: 
        state = self._state.pop() 
        self.moves.pop() 

        # take back piece 
        for tile in state.tiles: 
            self._tiles[tile] = 0 

        self.current_player = state.cur_player 
        self.finished = False 
        self.ply -= 1 

        # player state is stored per player 
        for player in self._players: 
            player.pop_state() 

    def _push_prp(self, move: Move, prp: _PieceRotationPoint, tile: Tile) -> None: 
        self.moves.append(move) 

        player = self._players[self.current_player]

        for p in self._players: 
            p.push_state() 

        # absolute position of tiles 
        tiles = [(t[0] + tile[0], t[1] + tile[1]) for t in prp.tiles]
        corners = [(t[0] + tile[0], t[1] + tile[1]) for t in prp.corners]
        adj = [(t[0] + tile[0], t[1] + tile[1]) for t in prp.adjacent]

        for abs_tile in corners: 
            player.add_corner(abs_tile) 

        for abs_tile in tiles: 
            self._tiles[abs_tile] = self.current_player + 1

        for p in self._players: 
            p.on_tiles_filled(tiles) 

        # player can't place tiles adjacent to their own color 
        player.on_tiles_filled(adj) 
        player.remove_piece(prp.piece_id)

        if not player.has_played: 
            player.corners.pop(A01, None)
            player.corners.pop(A20, None)
            player.corners.pop(T01, None)
            player.corners.pop(T20, None)

        player.has_played = True 
        player.score += len(prp.tiles)

        # inc turn and make sure player can move 
        self.ply += 1
        cur_turn = self.current_player
        while True: 
            self.current_player += 1
            if self.current_player >= len(self._players): 
                self.current_player = 0 
            if self._players[self.current_player].can_play: 
                break 

            # looped all the way back to same player 
            # no player can play, game is done
            if cur_turn == self.current_player: 
                self.finished = True 
                break 

        self._state.append(_BoardState(cur_turn, tiles))

    def __str__(self): 
        out = "" 
        
        board = self._tiles[::-1]

        chars = None
        if print_color: 
            chars = [
                '.', 
                '\033[94mB\033[0m', 
                '\033[93mY\033[0m', 
                '\033[91mR\033[0m', 
                '\033[92mG\033[0m'
            ]
        else: 
            chars = [
                '.', 
                'B', 
                'Y', 
                'R', 
                'G'
            ]

        for y in range(20): 
            for x in range(20): 
                out += f"{chars[board[y,x]]} "
            out += "\n"

        for player in self._players: 
            out += f"{player.name}: {int(player.score)} "

            pcs = [_PIECES[pc] for pc in self._remaining_piece_set(player.id)]

            if len(pcs) > 0: 
                pcs = sorted(pcs, key=lambda x: x.id) 

                out += "( "
                for pc in pcs: 
                    out += pc.name + " " 
                out += ")\n"

        out += f"Finished: {self.finished}"
        if self.finished: 
            out += f"\nWinner: "
            for p in self.winners: 
                out += f"{self._players[p].name} "
        else: 
            out += f"\nTurn: {self._players[self.current_player].name}"

        return out 
